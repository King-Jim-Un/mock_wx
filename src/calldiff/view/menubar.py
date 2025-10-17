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
    def add(self, name: str, handler: Callable, help_str: str="", item_id: int=wx.ID_ANY) -> wx.MenuItem:
        """Add a menu item and bind a handler to it"""
        item = self.Append(item_id, name, help_str)
        self.Bind(wx.EVT_MENU, handler, id=item.GetId())
        return item


class MenuBar(wx.MenuBar):
    """Menubar displayed at top of main frame"""
    def __init__(self, *args, **kwargs) -> None:
        """Constructor"""
        super().__init__(*args, **kwargs)

        events = application.get_app().events

        file_menu  = Menu()
        file_menu.add(_("&Preferences"), events.preferences, _("Configure application preferences"), wx.ID_PREFERENCES)
        file_menu.AppendSeparator()
        file_menu.add(_("&Quit"), events.quit, _("Close the application"), wx.ID_EXIT)
        self.Append(file_menu, _("&File"))

        help_menu = Menu()
        help_menu.add(_("&About"), events.about, _("About the application"), wx.ID_ABOUT)
        self.Append(help_menu, _("&Help"))
