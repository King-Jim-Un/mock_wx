"""Main application frame"""

import logging
from pubsub import pub
import wx

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation

from calldiff import application
from calldiff.constants import CONSTANTS
from calldiff.view.diff_panel import DiffPanel


class MainFrame(wx.Frame):
    """Main application frame"""
    def __init__(self, *args, **kwargs) -> None:
        """Constructor"""
        super().__init__(*args, **kwargs)
        app = application.get_app()

        self.splitter = wx.SplitterWindow(self, style=wx.SP_3D | wx.SP_LIVE_UPDATE, name="splitter")
        self.tree = wx.TreeCtrl(self.splitter, name="tree")
        app.live_data.tree_root.node_id = self.tree.AddRoot(_("Tests"), data=app.live_data.tree_root)
        self.diff_panel = DiffPanel(self.splitter, name="diff_panel")
        self.splitter.SplitVertically(self.tree, self.diff_panel, app.settings.sash_position)
        self.set_data()

        self.Bind(wx.EVT_CLOSE, self.on_close)
        pub.subscribe(self.new_node, CONSTANTS.PUBSUB.NEW_NODE)
        pub.subscribe(self.update_node, CONSTANTS.PUBSUB.UPDATE_NODE)

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
        settings.sash_position = self.splitter.GetSashPosition()

    def new_node(self, obj, parent) -> None:
        obj.node_id = self.tree.AppendItem(parent.node_id, str(obj), data=obj)
        self.tree.Expand(parent.node_id)

    def update_node(self, obj) -> None:
        self.tree.SetItemText(obj.node_id, str(obj))
