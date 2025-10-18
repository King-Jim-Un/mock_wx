"""Event handlers"""

from dataclasses import dataclass, field
from datetime import timedelta
import logging
from pubsub import pub
from typing import Any, Optional

import wx

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

    def display_success(self, test: TestFunction) -> None:
        """Display success panel"""
        self.live_data.status.add(StatusFlags.DISPLAY_SUCCESS)
        self.live_data.status.discard(StatusFlags.DISPLAY_NONE)
        self.live_data.status.discard(StatusFlags.DISPLAY_DIFF)
        self.live_data.status.discard(StatusFlags.DISPLAY_EXCEPTION)
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
        self.live_data.status.add(StatusFlags.DISPLAY_DIFF)
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
        self.live_data.status.add(StatusFlags.DISPLAY_EXCEPTION)
        self.live_data.status.discard(StatusFlags.DISPLAY_SUCCESS)
        self.live_data.status.discard(StatusFlags.DISPLAY_NONE)
        self.live_data.status.discard(StatusFlags.DISPLAY_DIFF)
        self.frame.diff_panel.Hide()
        ...  # TODO
        self.frame.rich_text.Show()
        self.frame.content.Layout()

    def display_none(self, data) -> None:
        """Hide all panels"""
        self.live_data.status.add(StatusFlags.DISPLAY_NONE)
        self.live_data.status.discard(StatusFlags.DISPLAY_DIFF)
        self.live_data.status.discard(StatusFlags.DISPLAY_EXCEPTION)
        self.live_data.status.discard(StatusFlags.DISPLAY_SUCCESS)
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

    def about(self, _event: Optional[wx.Event] = None) -> None:
        """About the application"""
        LOG.info("About")


# TODO: show incomplete test
# TODO: test completion event should update if selected test
