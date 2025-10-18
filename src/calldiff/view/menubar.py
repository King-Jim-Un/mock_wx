"""Menubar displayed at top of main frame"""

import logging
from typing import Callable
import wx

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation

from calldiff import application


class Menu(wx.Menu):
    """Custom menu that handles binding events to items"""

    def add(
        self, name: str, handler: Callable, help_str: str = "", item_id: int = wx.ID_ANY, kind: int = wx.ITEM_NORMAL
    ) -> wx.MenuItem:
        """Add a menu item and bind a handler to it"""
        item = self.Append(item_id, name, help_str, kind)
        self.Bind(wx.EVT_MENU, handler, id=item.GetId())
        return item


class MenuBar(wx.MenuBar):
    """Menubar displayed at top of main frame"""

    def __init__(self, *args, **kwargs) -> None:
        """Constructor"""
        super().__init__(*args, **kwargs)

        events = application.get_app().events

        file_menu = Menu()
        file_menu.add(_("&Quit"), events.quit, _("Close the application"), wx.ID_EXIT)
        self.Append(file_menu, _("&File"))

        view_menu = Menu()
        view_menu.add(_("&Preferences"), events.preferences, _("Configure application preferences"), wx.ID_PREFERENCES)
        self.fancy = view_menu.add(
            _("Show &Fancy Diff"), events.fancy, _("Show a fancy diff instead of unified diff"), kind=wx.ITEM_CHECK
        )
        self.Append(view_menu, _("&View"))

        help_menu = Menu()
        help_menu.add(_("&About"), events.about, _("About the application"), wx.ID_ABOUT)
        self.Append(help_menu, _("&Help"))
