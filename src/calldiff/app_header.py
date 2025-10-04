"""Structure portion of application object"""

# See src/calldiff/README.md for details

from argparse import Namespace
import logging
import wx

from calldiff.model.preferences import Preferences
from calldiff.model.live_data import LiveData

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


class CallDiffApp(wx.App):
    args: Namespace
    settings: Preferences
    live_data: LiveData


def get_app() -> CallDiffApp:
    """Typed wrapper around wx.GetApp()"""
    return wx.GetApp()  # type: ignore
