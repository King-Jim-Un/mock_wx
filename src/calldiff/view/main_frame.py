"""Main application frame"""

import logging
import wx

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation

from calldiff.app_header import get_app
from calldiff.view.diff_panel import DiffPanel


class MainFrame(wx.Frame):
    """Main application frame"""
    def __init__(self, *args, **kwargs) -> None:
        """Constructor"""
        super().__init__(*args, **kwargs)

        self.diff_panel = DiffPanel(self, name="diff_panel")
        self.diff_panel.set_contents([str(x) for x in range(100)])

        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event: wx.CloseEvent) -> None:
        event.Skip()
        settings = get_app().settings
        settings.maximize = self.IsMaximized()
        self.Freeze()
        self.Restore()
        settings.window_rect = self.GetRect()
