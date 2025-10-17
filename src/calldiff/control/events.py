"""Event handlers"""

from dataclasses import dataclass, field
import logging
from typing import Any, Optional
import wx

from calldiff import application
from calldiff.constants import StatusFlags
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

    def display_success(self, test: TestFunction) -> None:
        """Display success panel"""
        self.live_data.status.add(StatusFlags.DISPLAY_SUCCESS)
        self.live_data.status.discard(StatusFlags.DISPLAY_NONE)
        self.live_data.status.discard(StatusFlags.DISPLAY_DIFF)
        self.live_data.status.discard(StatusFlags.DISPLAY_EXCEPTION)
        self.frame.diff_panel.Hide()
        self.frame.rich_text.Show()
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

    def preferences(self, _event: Optional[wx.Event]=None)->None:
        """Configure application preferences"""
        LOG.info("Preferences")

    def quit(self, _event: Optional[wx.Event]=None)-> None:
        """Close the application"""
        application.get_app().frame.Close()

    def about(self, _event: Optional[wx.Event]=None)->None:
        """About the application"""
        LOG.info("About")
