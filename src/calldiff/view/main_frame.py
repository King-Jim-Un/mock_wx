"""Main application frame"""

import logging
import wx

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation

from calldiff import application
from calldiff.view.diff_panel import DiffPanel


class MainFrame(wx.Frame):
    """Main application frame"""
    def __init__(self, *args, **kwargs) -> None:
        """Constructor"""
        super().__init__(*args, **kwargs)

        self.diff_panel = DiffPanel(self, name="diff_panel")
        self.set_data()

        self.Bind(wx.EVT_CLOSE, self.on_close)

    def set_data(self):  # TODO REMOVE THIS
        from unittest.mock import Mock, mock_open, call
        from calldiff.model.comparison import HashableComparison
        mock = Mock()
        mock_open(mock.open, "some read data")
        mock.one()
        mock.two.three().four()
        mock.five(6, 7, 8, 9, 10, eleven=12, thirteen=14).thirteen("fourteen")
        with mock.open("test", "rt") as file_obj:
            mock.write(file_obj.read())
        expect = [
            call.one(),
            call.two.three(),
            call.two.three().four(),
            call.five(6, 7, 8, 9, 10, thirteen=14, eleven=12),
            call.five().thirteen("fourteen"),
            call.open("tst", "rt"),
            call.open("tet", "rt"),
            call.open().__enter__(),
            call.open().read(),
            call.write("some read data"),
            call.open().__exit__(None, None, None),
            call.open().close(),
        ]
        comparison = HashableComparison(expect, mock)
        comparison.compare()
        self.diff_panel.set_contents(comparison)

    def on_close(self, event: wx.CloseEvent) -> None:
        """Save the frame size before closing"""
        event.Skip()
        settings = application.get_app().settings
        settings.maximize = self.IsMaximized()
        self.Freeze()
        self.Restore()
        settings.window_rect = self.GetRect()
