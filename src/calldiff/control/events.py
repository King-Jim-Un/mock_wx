"""Event handlers"""

from dataclasses import dataclass, field
import logging
from typing import Any
import wx

from calldiff import application
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
        app = application.get_app()
        self.frame = app.frame
        self.live_data = app.live_data

    def display_success(self, test: TestFunction) -> None:
        ...

    def display_call_diff(self, test: TestFunction) -> None:
        self.live_data.display_test = test
        self.frame.diff_panel.show_error()
        self.frame.diff_panel.Show()
        self.frame.content.Layout()

    def display_other_error(self, test: TestFunction) -> None:
        ...

    def display_none(self, data) -> None:
        self.frame.diff_panel.Hide()
