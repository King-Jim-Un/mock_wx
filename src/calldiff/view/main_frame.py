"""Main application frame"""

import logging
from pubsub import pub
import wx

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation

from mock_wx._test_case import CallDifference

from calldiff import application
from calldiff.constants import CONSTANTS
from calldiff.control.run_tests import TestFunction
from calldiff.view.diff_panel import DiffPanel
from calldiff.view.menubar import MenuBar
from calldiff.view.statusbar import StatusBar


class MainFrame(wx.Frame):
    """Main application frame"""
    menubar: MenuBar
    statusbar: StatusBar
    def __init__(self, *args, **kwargs) -> None:
        """Constructor"""
        super().__init__(*args, **kwargs)
        app = application.get_app()

        # ┌─ menubar ──────────────────────────────────────────────────────────────┐
        # └────────────────────────────────────────────────────────────────────────┘
        #
        # ┌─ splitter ─────────────────────────────────────────────────────────────┐
        # │                                                                        │
        # │ ┌─ tree ──────┐ ┌─ content ──────────────────────────────────────────┐ │
        # │ │             │ │                                                    │ │
        # │ │             │ │ ┌─ sizer ────────────────────────────────────────┐ │ │
        # │ │             │ │ │                                                │ │ │
        # │ │             │ │ │ ┌─ diff_panel ───────────────────────────────┐ │ │ │
        # │ │             │ │ │ │                                            │ │ │ │
        # │ │             │ │ │ │                                            │ │ │ │
        # │ │             │ │ │ │                                            │ │ │ │
        # │ │             │ │ │ │                                            │ │ │ │
        # │ │             │ │ │ │                                            │ │ │ │
        # │ │             │ │ │ └────────────────────────────────────────────┘ │ │ │
        # │ │             │ │ │                                                │ │ │
        # │ │             │ │ │ ┌─ TBD ──────────────────────────────────────┐ │ │ │
        # │ │             │ │ │ │                                            │ │ │ │
        # │ │             │ │ │ │                                            │ │ │ │
        # │ │             │ │ │ │                                            │ │ │ │
        # │ │             │ │ │ │                                            │ │ │ │
        # │ │             │ │ │ │                                            │ │ │ │
        # │ │             │ │ │ └────────────────────────────────────────────┘ │ │ │
        # │ │             │ │ └────────────────────────────────────────────────┘ │ │
        # │ └─────────────┘ └────────────────────────────────────────────────────┘ │
        # └────────────────────────────────────────────────────────────────────────┘
        #
        # ┌─ statusbar ────────────────────────────────────────────────────────────┐
        # └────────────────────────────────────────────────────────────────────────┘
        self.menubar = MenuBar()
        self.SetMenuBar(self.menubar)

        self.splitter = wx.SplitterWindow(self, style=wx.SP_3D | wx.SP_LIVE_UPDATE, name="splitter")

        self.tree = wx.TreeCtrl(self.splitter, name="tree")
        app.live_data.tree_root.node_id = self.tree.AddRoot(_("Tests"), data=app.live_data.tree_root)

        self.content = wx.Panel(self.splitter, name="content")

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.content.SetSizer(sizer)

        self.diff_panel = DiffPanel(self.content, name="diff_panel")
        self.diff_panel.Hide()
        sizer.Add(self.diff_panel, 1, wx.EXPAND)

        self.splitter.SplitVertically(self.tree, self.content, app.settings.sash_position)

        self.statusbar = StatusBar(self, name="statusbar")
        self.SetStatusBar(self.statusbar)

    def complete_init(self) -> None:
        """Binding event handlers"""
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_tree)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        pub.subscribe(self.new_node, CONSTANTS.PUBSUB.NEW_NODE)
        pub.subscribe(self.update_node, CONSTANTS.PUBSUB.UPDATE_NODE)

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
        """Add a new node to the tree"""
        obj.node_id = self.tree.AppendItem(parent.node_id, str(obj), data=obj)
        self.tree.Expand(parent.node_id)

    def update_node(self, obj) -> None:
        """Update a node in the tree"""
        item_id = self.tree.GetSelection()
        if item_id.IsOk():
            if self.tree.GetItemData(item_id) == obj:
                self.on_select(obj)

    def on_tree(self, event: wx.TreeEvent) -> None:
        """Handle a node selection event"""
        self.on_select(self.tree.GetItemData(event.GetItem()))

    def on_select(self, data):
        """Handle a tree node selection event"""
        events = application.get_app().events
        if isinstance(data, TestFunction):
            if data.completed:
                if data.run_failure is None:
                    events.display_success(data)
                elif isinstance(data.run_failure, CallDifference):
                    events.display_call_diff(data)
                else:
                    events.display_other_error(data)
            else:
                events.display_none(data)
        else:
            events.display_none(data)
