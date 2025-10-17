from argparse import Namespace
from base64 import b64encode
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from importlib import import_module
from pathlib import Path
import pickle
import sys
from typing import Tuple, Any, NewType, List, Optional, TextIO, Callable, Dict

from mock_wx._test_case import wxTestCase


class Actions(Enum):
    START = auto()
    ASSIGN_ID = auto()  # Payload is List[Tuple[IdNum, Any]]
    STDOUT = auto()
    STDERR = auto()
    LOG = auto()
    RUN_TEST = auto()
    EXIT = auto()


Command = NewType("Command", Tuple[Actions, Any])
IdNum = NewType("IdNum", int)


@dataclass
class TestStart:
    test_id: IdNum
    timestamp: datetime = field(default_factory=lambda: datetime.now())


@dataclass
class TestsDone:
    return_code: int
    timestamp: datetime = field(default_factory=lambda: datetime.now())


@dataclass
class TestResults:
    test_id: IdNum
    run_failure: Optional[Exception] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now())


@dataclass
class TestDetails:
    test_case_id: IdNum
    func_name: str
    doc_string: Optional[str] = None


@dataclass
class TestCaseDetails:
    path_id: IdNum
    class_name: str
    inst_failure: Optional[Exception] = None
    doc_string: Optional[str] = None


@dataclass
class FileDetails:
    path_id: IdNum
    import_failure: Optional[Exception] = None
    doc_string: Optional[str] = None


@dataclass
class Writer:
    action: Actions
    writer: Callable

    def write(self, text: str):
        self.writer((self.action, text))

    def flush(self):
        pass


@dataclass
class Tester:
    args: Namespace
    stdout: TextIO = field(init=False)
    stderr: TextIO = field(init=False)
    log: Writer = field(init=False)

    def __post_init__(self):
        self.log = Writer(Actions.LOG, self.write)

    def patch_std(self) -> None:
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        sys.stdout = Writer(Actions.STDOUT, self.write)
        sys.stderr = Writer(Actions.STDERR, self.write)

    def write(self, obj: Tuple[Actions, Any]) -> None:
        text = b64encode(pickle.dumps(obj))
        self.stdout.write(text.decode("ascii") + "\n")

    def assign_id(self, obj: Any) -> IdNum:
        id_num = IdNum(id(obj))
        self.write((Actions.ASSIGN_ID, (id_num, obj)))
        return id_num

    def scan_files(self) -> Dict[Path, IdNum]:
        paths: Dict[Path, IdNum] = {}
        for path in self.args.base_dir.glob("**/test*.py"):
            path_id = self.assign_id(path)
            paths[path] = path_id
        return paths

    def path_to_dot_path(self, path: Path) -> str:
        path, name = path.parent, path.stem
        parts = [name]
        while path != self.args.base_dir:
            path, name = path.parent, path.name
            parts.insert(0, name)
        return ".".join(parts)

    def load_tests(self, test_case: wxTestCase, test_case_id: IdNum) -> None:
        tests: List[Tuple[str, Callable, IdNum]] = []
        for name in sorted(dir(test_case)):
            if name.startswith("test_"):
                func = getattr(test_case, name)
                if callable(func):
                    test_details = TestDetails(test_case_id, name, func.__doc__)
                    test_id = self.assign_id(test_details)
                    tests.append((name, func, test_id))
        for name, func, test_id in tests:
            self.write((Actions.RUN_TEST, TestStart(test_id)))
            try:
                if hasattr(test_case, "setUp"):
                    test_case.setUp()
                func()
                if hasattr(test_case, "tearDown"):
                    test_case.tearDown()
                result = TestResults(test_id)
            except Exception as error:
                result = TestResults(test_id, error)
            self.assign_id(result)

    def load_test_cases(self, module, path_id: IdNum) -> None:
        for name in sorted(dir(module)):
            if name.startswith("Test"):
                test_case_class = getattr(module, name)
                test_case_details = TestCaseDetails(path_id, name, test_case_class.__doc__)
                try:
                    test_case = test_case_class()
                    test_case_id = self.assign_id(test_case_details)
                    self.load_tests(test_case, test_case_id)
                except Exception as error:
                    test_case_details.inst_failure = error
                    self.assign_id(test_case_details)

    def load_module(self, path: Path, path_id: IdNum) -> None:
        file_details = FileDetails(path_id)
        try:
            module = import_module(self.path_to_dot_path(path))
            file_details.doc_string = module.__doc__
            self.assign_id(file_details)
            self.load_test_cases(module, path_id)
        except Exception as error:
            file_details.import_failure = error
            self.assign_id(file_details)

    def run(self) -> int:
        self.patch_std()
        self.write((Actions.START, datetime.now()))

        paths = self.scan_files()
        for path in sorted(paths):
            self.load_module(path, paths[path])

        return_code = 0
        self.write((Actions.EXIT, TestsDone(return_code)))
        return return_code
