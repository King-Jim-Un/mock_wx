"""Application object"""

import logging
import wx

from calldiff.constants import CONSTANTS
from control.events import EventHandlers
from calldiff.model.preferences import Preferences
from calldiff.model.live_data import LiveData
from calldiff.view.main_frame import MainFrame

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


class CallDiffApp(wx.App):
    """Application object"""
    settings: Preferences
    live_data: LiveData
    frame: MainFrame
    events: EventHandlers

    def __init__(self, reset: bool) -> None:
        """Constructor"""
        self.reset = reset
        super().__init__()

    def OnInit(self) -> bool:  # type: ignore
        """Initialization"""
        self.settings = Preferences.load(self.reset)
        self.live_data = LiveData()
        self.events = EventHandlers()
        self.frame = MainFrame(None, title=_("CallDiff"), name="frame")
        if self.settings.window_rect:
            self.frame.SetRect(self.settings.window_rect)
        if self.settings.maximize:
            self.frame.Maximize()
        self.frame.Show()
        self.events.complete_init()
        self.frame.complete_init()

        from calldiff.control.run_tests import RunTestsThread  # TODO
        RunTestsThread(CONSTANTS.PATHS.ROOT / "scratch").start()

        return True

    def OnExit(self) -> int:
        """Clean up"""
        self.settings.save()
        return super().OnExit()


def get_app() -> CallDiffApp:
    """Wrapper around wx.GetApp() for typing purposes"""
    # See src/README.md for more
    return wx.GetApp()  # type: ignore
