from argparse import Namespace
from importlib import import_module
import os
from typing import Tuple, Any, List
from unittest import TestCase
from unittest.mock import Mock, _Call

# Globals:
G_APP = None
G_MOCK = Mock()
G_OBJS = Namespace()

# Types:
CallParts = Tuple[str, List[str], List[Tuple[str, str]]]
CallList = List[CallParts]


def _find_patch_path(patch_str: str) -> Tuple[Any, Mock, str, Any]:
    """Find the patch path from a patch string"""
    # Note: A patch_str of "function" is for patching self.dut.function while a patch_string of "/os.chdir" will import
    # os and patch chdir in it.
    test_case = wxTestCase.test_case
    if patch_str.startswith("/"):
        parts = patch_str[1:].split(".")
        last_index = len(parts) - 1
        mock = test_case.mock
        prev_obj = None
        for index, part in enumerate(parts):
            try:
                obj = import_module(".".join(parts[: index + 1]))
            except ModuleNotFoundError:
                if hasattr(prev_obj, part):
                    obj = getattr(prev_obj, part)
                else:
                    obj = prev_obj.__builtins__[part]
            if index == last_index:
                break
            mock = getattr(mock, part)
            prev_obj = obj
    else:
        parts = patch_str.split(".")
        last_index = len(parts) - 1
        prev_obj = test_case.dut
        mock = test_case.mock
        obj = None
        for index, part in enumerate(parts):
            if index == last_index:
                break
            obj = getattr(prev_obj, part)
            mock = getattr(mock, part)
            if index == last_index:
                break
            prev_obj = obj
    return prev_obj, mock, part, obj


class BaseClass:
    def __init__(self, *args, **kwargs):
        if "name" in kwargs:
            name = kwargs["name"]
            if name in ["dut", "app"]:
                self._name = f"self.{name}"
                self._mock = getattr(G_MOCK, name)
            else:
                self._name = f"self.dut.{name}"
                self._mock = getattr(G_MOCK.dut, name)
        else:
            name = self.__class__.__name__
            self._mock = getattr(G_MOCK, name)
            if name not in G_OBJS:
                setattr(G_OBJS, name, [])
            value = getattr(G_OBJS, name)
            self._name = f"self.objs.{name}[{len(value)}]"
            value.append(self)
        self._mock(*args, **kwargs)

    def __str__(self):
        return self._name

    def __repr__(self):
        return self._name

    def __getattr__(self, name):
        return getattr(self._mock, name)


class CallDifference(Exception):
    def __init__(self, expect: CallList, actual: CallList):
        self.expect, self.actual = expect, actual

    def __str__(self):
        return "<CallDifference>"


class wxTestCase(TestCase):
    """Base class for user test suites"""
    test_case: "wxTestCase"

    def create_dut(self, *patches):
        """Context function for creating a DUT"""
        # Note: Use this pattern
        # def setUp(self):
        #     with self.create_dut():
        #         self.dut = ClassName(args)
        wxTestCase.test_case = self
        self.patch_list = []

        class CreateDut:
            """Internal object for context"""

            def __enter__(self):
                from mock_wx.wx import App

                global G_APP, G_OBJS

                G_APP = App(name="app")
                G_MOCK.reset_mock()
                G_OBJS = Namespace()
                for patch_str in patches:
                    obj, mock, part, value = _find_patch_path(patch_str)
                    wxTestCase.test_case.patch_list.append((obj, part, value))
                    def wrapper(*args, **kwargs):
                        try:
                            return_value = getattr(mock, part)(*args, **kwargs)
                            if return_value is not None:
                                getattr(mock, f"{part}_return_value")(return_value)
                            return return_value
                        except Exception as error:
                            getattr(mock, f"{part}_raised")(error)
                            raise
                    if isinstance(obj, dict):
                        obj[obj] = wrapper
                    else:
                        setattr(obj, part, wrapper)

            def __exit__(self, exc_type, exc_val, exc_tb):
                for obj, part, value in wxTestCase.test_case.patch_list:
                    if isinstance(obj, dict):
                        obj[part] = value
                    else:
                        setattr(obj, part, value)

        return CreateDut()

    def create_app(self, *patches):
        """Context function for creating a wx.App() as the DUT"""
        # Note: Use this pattern
        # def setUp(self):
        #     with self.create_app():
        #         self.dut = AppName(args)
        # Use EITHER create_dut() or create_app(), but not both.
        wxTestCase.test_case = self
        self.patch_list = []

        class CreateApp:
            """Internal object for context"""

            def __enter__(self):
                global G_OBJS

                G_MOCK.reset_mock()
                G_OBJS = Namespace()
                for patch_str in patches:
                    obj, mock, part = _find_patch_path(patch_str)
                    wxTestCase.test_case.patch_list.append((obj, part, getattr(obj, part)))

                    def wrapper(*args, **kwargs):
                        try:
                            return_value = getattr(mock, part)(*args, **kwargs)
                            if return_value is not None:
                                getattr(mock, f"{part}_return_value")(return_value)
                        except Exception as error:
                            getattr(mock, f"{part}_raised")(error)
                            raise

                    setattr(obj, part, wrapper)

            def __exit__(self, exc_type, exc_val, exc_tb):
                global G_APP

                G_APP = wxTestCase.test_case.dut
                for obj, part, old_func in wxTestCase.test_case.patch_list:
                    setattr(obj, part, old_func)

        return CreateApp()

    def check(self, expect: List[_Call]):
        """Check the expectations against mock calls"""
        if "CALL_DIFF_RUNNER" in os.environ:
            expected: CallList = []
            for item in expect:
                args = [repr(arg) for arg in item[1]]
                kwargs = [(key, repr(value)) for key, value in item[2].items()]
                expected.append((item[0], args, kwargs))
            actual: CallList = []
            for item in self.mock.mock_calls:
                args = [repr(arg) for arg in item[1]]
                kwargs = [(key, repr(value)) for key, value in item[2].items()]
                actual.append((item[0], args, kwargs))
            if expected != actual:
                raise CallDifference(expected, actual)
        else:
            self.mock.assert_has_calls(expect)

    @property
    def app(self):
        """Return the current app object"""
        return G_APP

    @property
    def objs(self):
        """Used to access ephemeral objects"""
        return G_OBJS

    @property
    def mock(self):
        """Return the mock object"""
        return G_MOCK


def note_func(func_name):
    def wrapper1(func):
        def wrapper2(*args2, **kwargs2):
            obj, mock, part, value = _find_patch_path(func_name)
            old_func = getattr(obj, part)

            def wrapper3(*args3, **kwargs3):
                getattr(mock, part)(*args3, **kwargs3)
                try:
                    return_value = old_func(*args3, **kwargs3)
                    if return_value is not None:
                        getattr(mock, f"{part}_return_value")(return_value)
                except Exception as error:
                    getattr(mock, f"{part}_raised")(error)
                    raise
                return return_value

            if isinstance(obj, dict):
                obj[part] = wrapper3
            else:
                setattr(obj, part, wrapper3)
            return_value = func(*args2, **kwargs2)
            if isinstance(obj, dict):
                obj[part] = old_func
            else:
                setattr(obj, part, old_func)
            return return_value

        return wrapper2

    return wrapper1


def patch(func_name):
    def wrapper1(func):
        def wrapper2(*args2, **kwargs2):
            obj, mock, part, old_func = _find_patch_path(func_name)

            def wrapper3(*args3, **kwargs3):
                try:
                    return_value = getattr(mock, part)(*args3, **kwargs3)
                    if return_value is not None:
                        getattr(mock, f"{part}_return_value")(return_value)
                except Exception as error:
                    getattr(mock, f"{part}_raised")(error)
                    raise
                return return_value

            if isinstance(obj, dict):
                obj[part] = wrapper3
            else:
                setattr(obj, part, wrapper3)
            return_value = func(*args2, **kwargs2)
            if isinstance(obj, dict):
                obj[part] = old_func
            else:
                setattr(obj, part, old_func)
            return return_value

        return wrapper2

    return wrapper1
