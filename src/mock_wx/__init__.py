from importlib import import_module
from unittest import TestCase
from unittest.mock import Mock
from typing import Tuple, Any
import wx
from wx import base_class


def _find_patch_path(patch_str: str) -> Tuple[Any, Mock, str]:
    """Find the patch path from a patch string"""
    # Note: A patch_str of "function" is for patching self.dut.function while a patch_string of "/os.chdir" will import
    # os and patch chdir in it.
    test_case = wxTestCase.test_case
    if patch_str.startswith("/"):
        parts = patch_str[1:].split(".")
        last_index = len(parts) - 1
        mock = test_case.mock
        for index, part in enumerate(parts):
            obj = import_module(".".join(parts[:index + 1]))
            if index == last_index:
                break
            mock = getattr(mock, part)
    else:
        parts = patch_str.split(".")
        last_index = len(parts) - 1
        obj = test_case.dut
        mock = test_case.mock
        for index, part in enumerate(parts):
            if index == last_index:
                break
            obj = getattr(obj, part)
            mock = getattr(mock, part)
    return obj, mock, part


class wxTestCase(TestCase):
    """Base class for user test suites"""
    def create_dut(self, *patches):
        """Context function for creating a DUT"""
        # Note: Use this pattern
        # def setUp(self):
        #     with self.create_dut():
        #         self.dut = ClassName(args)
        wxTestCase.test_case = self
        self.patch_dict = {}
        class CreateDut:
            """Internal object for context"""
            def __enter__(self):
                base_class.G_APP = wx.App(name="app")
                base_class.G_MOCK.reset_mock()
                base_class.G_OBJS = {}
                for patch_str in patches:
                    wxTestCase.test_case._patch(patch_str)
            def __exit__(self, exc_type, exc_val, exc_tb):
                for patch_str in patches:
                    wxTestCase.test_case._unpatch(patch_str)
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
                base_class.G_MOCK.reset_mock()
                base_class.G_OBJS = {}
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
                    setattr(obj, part, wrapper)
            def __exit__(self, exc_type, exc_val, exc_tb):
                base_class.G_APP = wxTestCase.test_case.dut
                for obj, part, old_func in wxTestCase.test_case.patch_list:
                    setattr(obj, part, old_func)
        return CreateApp()
    def check(self, expect):
        """Check the expectations against mock calls"""
        self.mock.assert_has_calls(expect)
    @property
    def app(self):
        """Return the current app object"""
        return base_class.G_APP
    @property
    def objs(self):
        """Used to access ephemeral objects"""
        return base_class.G_OBJS
    @property
    def mock(self):
        """Return the mock object"""
        return base_class.G_MOCK
def note_func(func_name):
    def wrapper1(func):
        def wrapper2(*args2, **kwargs2):
            obj, mock, part = _find_patch_path(func_name)
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
            setattr(obj, part, wrapper3)
            return_value = func(*args2, **kwargs2)
            setattr(obj, part, old_func)
            return return_value
        return wrapper2
    return wrapper1
def patch(func_name):
    def wrapper1(func):
        def wrapper2(*args2, **kwargs2):
            obj, mock, part = _find_patch_path(func_name)
            old_func = getattr(obj, part)
            def wrapper3(*args3, **kwargs3):
                try:
                    return_value = getattr(mock, part)(*args3, **kwargs3)
                    if return_value is not None:
                        getattr(mock, f"{part}_return_value")(return_value)
                except Exception as error:
                    getattr(mock, f"{part}_raised")(error)
                    raise
                return return_value
            setattr(obj, part, wrapper3)
            return_value = func(*args2, **kwargs2)
            setattr(obj, part, old_func)
            return return_value
        return wrapper2
    return wrapper1
