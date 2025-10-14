from base64 import b64decode
from dataclasses import dataclass, field
import logging
from pathlib import Path
import pickle
from pubsub import pub
from threading import Thread
from subprocess import Popen, PIPE
import sys
from typing import Any, Dict, Optional, List, Tuple
import wx

from mock_wx.test_runner import Actions, FileDetails, TestCaseDetails, TestDetails, TestResults

from calldiff import application
from calldiff.constants import CONSTANTS
from calldiff.model.comparison import HashableComparison

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


def safe_publish(topic: str, **kwargs):
    wx.CallAfter(pub.sendMessage, topic, **kwargs)


@dataclass
class TestFunction:
    test_class: "TestClass"
    func_name: str
    doc_string: Optional[str] = None
    run_failure: Optional[Exception] = None
    completed: bool = False
    stream: List[Tuple[Actions, str]] = field(default_factory=list)
    node_id: wx.TreeItemId = field(default_factory=wx.TreeItemId)

    def __str__(self) -> str:
        return f"{self.func_name} ({self.doc_string})" if self.doc_string else self.func_name


@dataclass
class TestClass:
    test_file: "TestFile"
    class_name: str
    inst_failure: Optional[Exception] = None
    doc_string: Optional[str] = None
    tests: List[TestFunction] = field(default_factory=list)
    node_id: wx.TreeItemId = field(default_factory=wx.TreeItemId)

    def __str__(self) -> str:
        return f"{self.class_name} ({self.doc_string})" if self.doc_string else self.class_name


@dataclass
class TestFile:
    path: Path
    import_failure: Optional[Exception] = None
    doc_string: Optional[str] = None
    test_classes: List[TestClass] = field(default_factory=list)
    node_id: wx.TreeItemId = field(default_factory=wx.TreeItemId)

    def __str__(self) -> str:
        return f"{self.path.name} ({self.doc_string})" if self.doc_string else self.path.name


class RunTestsThread(Thread):
    objects_by_id: Dict[int, Any]
    test_files: Dict[Path, TestFile]
    running_test: Optional[TestFunction] = None

    def __init__(self, base_dir: Path):
        super().__init__()
        self.process = Popen(
            [sys.executable, CONSTANTS.PATHS.TEST_RUNNER, "-l=DEBUG", base_dir], stdout=PIPE, text=True
        )
        self.objects_by_id = {}
        self.test_files = {}

    def recast_obj(self, obj: Any) -> Any:
        # THIS CODE RUNS IN A THREAD! DO NOT CALL OUT WITHOUT wx.CallAfter!
        test_file: TestFile
        test_class: TestClass
        test_function: TestFunction
        if isinstance(obj, Path):
            test_file = TestFile(obj)
            self.test_files[obj] = test_file
            live_data = application.get_app().live_data
            safe_publish(CONSTANTS.PUBSUB.NEW_NODE, obj=test_file, parent=live_data.tree_root)
            return test_file
        elif isinstance(obj, FileDetails):
            test_file = self.objects_by_id[obj.path_id]  # type: ignore
            test_file.import_failure = obj.import_failure
            test_file.doc_string = obj.doc_string
            safe_publish(CONSTANTS.PUBSUB.UPDATE_NODE, obj=test_file)
            return test_file
        elif isinstance(obj, TestCaseDetails):
            test_file = self.objects_by_id[obj.path_id]  # type: ignore
            test_class = TestClass(test_file, obj.class_name, obj.inst_failure, obj.doc_string)
            test_file.test_classes.append(test_class)
            safe_publish(CONSTANTS.PUBSUB.NEW_NODE, obj=test_class, parent=test_file)
            return test_class
        elif isinstance(obj, TestDetails):
            test_class = self.objects_by_id[obj.test_case_id]  # type: ignore
            test_function = TestFunction(test_class, obj.func_name, obj.doc_string)
            test_class.tests.append(test_function)
            safe_publish(CONSTANTS.PUBSUB.NEW_NODE, obj=test_function, parent=test_class)
            return test_function
        elif isinstance(obj, TestResults):
            test_function = self.objects_by_id[obj.test_id]  # type: ignore
            test_function.run_failure = obj.run_failure
            test_function.completed = True
            safe_publish(CONSTANTS.PUBSUB.UPDATE_NODE, obj=test_function)
            self.running_test = None
            return test_function
        else:
            assert False, f"unknown object: {obj}"

    def run(self) -> None:
        # THIS CODE RUNS IN A THREAD! DO NOT CALL OUT WITHOUT wx.CallAfter!
        while True:
            text = self.process.stdout.readline()
            if not text:
                break
            action, payload = pickle.loads(b64decode(text))
            if action == Actions.ASSIGN_ID:
                id_num, obj = payload
                self.objects_by_id[id_num] = self.recast_obj(obj)
            elif action in [Actions.STDOUT, Actions.STDERR, Actions.LOG]:
                if self.running_test:
                    self.running_test.stream.append((action, payload))
                else:
                    LOG.warning("Can't associate with a test: %s(%r)", action.name, payload)
            elif action == Actions.RUN_TEST:
                self.running_test = self.objects_by_id[payload]
            elif action == Actions.EXIT:
                LOG.debug("return-code: %r", payload)
        failure = self.test_files[list(self.test_files)[0]].test_classes[0].tests[1].run_failure  # TODO
        application.get_app().live_data.compare_exception = HashableComparison.from_exception(failure)  # TODO
        safe_publish(CONSTANTS.PUBSUB.TEST_COMPLETE)
        safe_publish(CONSTANTS.PUBSUB.SHOW_ERROR)
