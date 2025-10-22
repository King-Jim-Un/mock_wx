"""Event handlers"""

from dataclasses import dataclass, field
from datetime import timedelta
import logging
from pubsub import pub
from typing import Any, Optional
from unittest import SkipTest

import wx

from mock_wx.test_case import CallDifference
from mock_wx.test_runner import Actions

from calldiff import application
from calldiff.constants import StatusFlags, CONSTANTS
from calldiff.control.run_tests import TestFunction
from calldiff.model.live_data import LiveData
from calldiff.view.main_frame import MainFrame

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


@dataclass
class EventHandlers:
    """Event handler class"""

    displayed: Any = None
    frame: MainFrame = field(init=False)
    live_data: LiveData = field(init=False)

    def complete_init(self) -> None:
        """Constructor finalization"""
        app = application.get_app()
        self.frame = app.frame
        self.live_data = app.live_data
        pub.subscribe(self.test_complete, CONSTANTS.PUBSUB.TEST_COMPLETE)

    def test_complete(self) -> None:
        print(application.get_app().live_data)

    @staticmethod
    def delta_to_str(diff: timedelta) -> str:
        text = str(diff)
        if text.endswith("000"):
            text = text[:-3]
        if text.startswith("0:"):
            text = text[2:]
            if text.startswith("0"):
                text = text[1:]
                if text.startswith("0:"):
                    text = text[2:]
                    if text.startswith("0"):
                        text = text[1:]
                        if text.startswith("0."):
                            text = f"{text[2:5]}.{text[5:]}"
                            if text.startswith("0"):
                                text = text[1:]
                                if text.startswith("0"):
                                    text = text[1:]
                                    if text.startswith("0."):
                                        text = text[2:]
                                        if text.startswith("0"):
                                            text = text[1:]
                                            if text.startswith("0"):
                                                text = text[1:]
                                        return f"{text} microseconds"
                            return f"{text} milliseconds"
                    return f"{text} seconds"
            return f"{text} minutes"
        return f"{text} hours"

    def on_select(self, data):
        """Handle a tree node selection event"""
        if isinstance(data, TestFunction):
            if data.completed:
                if data.run_failure is None:
                    self.display_success(data)
                elif isinstance(data.run_failure, SkipTest):
                    self.display_skip(data)
                elif isinstance(data.run_failure, CallDifference):
                    self.display_call_diff(data)
                else:
                    self.display_other_error(data)
            else:
                self.display_none(data)
        elif data is application.get_app().live_data.tree_root:
            self.display_tree_root()
        else:
            self.display_none(data)

    def display(self, flag: StatusFlags) -> None:
        """Set only the given display flag"""
        self.live_data.status.discard(StatusFlags.DISPLAY_NONE)
        self.live_data.status.discard(StatusFlags.DISPLAY_DIFF)
        self.live_data.status.discard(StatusFlags.DISPLAY_EXCEPTION)
        self.live_data.status.discard(StatusFlags.DISPLAY_SUCCESS)
        self.live_data.status.discard(StatusFlags.DISPLAY_FILE_SUMMARY)
        self.live_data.status.add(flag)

    def display_tree_root(self) -> None:
        """Display status by paths"""
        self.display(StatusFlags.DISPLAY_FILE_SUMMARY)
        text = ""
        for test_file in application.get_app().live_data.test_files.values():
            tests_passed = tests_failed = tests_skipped = 0
            import_time = test_file.run_time
            for test_class in test_file.test_classes:
                for test in test_class.tests:
                    if test.completed:
                        if test.run_failure is None:
                            tests_passed += 1
                        elif isinstance(test.run_failure, SkipTest):
                            tests_skipped += 1
                        else:
                            tests_failed += 1
                    import_time -= test.run_time
            text += f"Path: {test_file.path}\n"
            if tests_failed:
                text += f"Tests passed: {tests_passed}\nTests failed: {tests_failed}\n"
                if tests_skipped:
                    text += f"Tests skipped: {tests_skipped}\n"
            elif tests_skipped or tests_passed:
                if tests_skipped:
                    text += f"OK ({tests_skipped} tests skipped)\n"
                else:
                    text += "OK\n"
            else:
                text += "No tests found\n"
            text += "Total run time: %s\nImport time: %s\n\n" % (self.delta_to_str(test_file.run_time), self.delta_to_str(import_time))
        self.frame.rich_text.Clear()
        self.frame.rich_text.add_chunk(Actions.EXPOSITION, text)

    def display_skip(self, test: TestFunction) -> None:
        """Display skipped panel"""
        self.display(StatusFlags.DISPLAY_SUCCESS)
        ...  # TODO
        self.frame.diff_panel.Hide()

    def display_success(self, test: TestFunction) -> None:
        """Display success panel"""
        self.display(StatusFlags.DISPLAY_SUCCESS)
        self.frame.diff_panel.Hide()
        self.live_data.display_test = test
        text_ctrl = self.frame.rich_text
        text_ctrl.Clear()
        text = _("\bTest file:\b %s\n\bTest suite:\b %s\n\bUnit test:\b %s\n\n") % (
            test.test_class.test_file.path,
            test.test_class,
            test,
        )
        text_ctrl.add_chunk(Actions.EXPOSITION, text)
        for text_type, text in test.stream:
            text_ctrl.add_chunk(text_type, text)
        text = _("\n\bSUCCESS\nRun time:\b %s") % self.delta_to_str(test.run_time)
        text_ctrl.add_chunk(Actions.EXPOSITION, text)
        text_ctrl.Show()
        self.frame.content.Layout()

    def display_call_diff(self, test: TestFunction) -> None:
        """Display call difference panel"""
        self.display(StatusFlags.DISPLAY_DIFF)
        self.live_data.status.discard(StatusFlags.DISPLAY_NONE)
        self.live_data.status.discard(StatusFlags.DISPLAY_EXCEPTION)
        self.live_data.status.discard(StatusFlags.DISPLAY_SUCCESS)
        self.live_data.display_test = test
        self.frame.diff_panel.show_error()
        self.frame.diff_panel.Show()
        self.frame.rich_text.Hide()
        self.frame.content.Layout()

    def display_other_error(self, test: TestFunction) -> None:
        """Display other exception panel"""
        self.display(StatusFlags.DISPLAY_EXCEPTION)
        self.frame.diff_panel.Hide()
        ...  # TODO
        self.frame.rich_text.Show()
        self.frame.content.Layout()

    def display_none(self, data) -> None:
        """Hide all panels"""
        self.display(StatusFlags.DISPLAY_NONE)
        self.frame.diff_panel.Hide()
        self.frame.rich_text.Hide()

    def preferences(self, _event: Optional[wx.Event] = None) -> None:
        """Configure application preferences"""
        LOG.info("Preferences")

    def quit(self, _event: Optional[wx.Event] = None) -> None:
        """Close the application"""
        application.get_app().frame.Close()

    def fancy(self, _event: Optional[wx.Event] = None) -> None:
        """Fancy preference toggled"""
        LOG.info("Fancy")

    def passing(self, _event: Optional[wx.Event] = None) -> None:
        """Show passing tests toggled"""
        LOG.info("Passing tests")

    def on_open(self, _event: Optional[wx.Event] = None) -> None:
        """Select tests/suites to run"""
        LOG.info("Open")

    def about(self, _event: Optional[wx.Event] = None) -> None:
        """About the application"""
        LOG.info("About")


# TODO: show incomplete test
# TODO: test completion event should update if selected test
