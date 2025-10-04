"""Executable portion of application object"""

from argparse import Namespace
import logging
import wx

from calldiff.constants import CONSTANTS

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


class CallDiffApp(wx.App):
    args: Namespace

    def __init__(self, args: Namespace) -> None:
        """Constructor"""
        self.args = args
        if args.log_file:
            ...  # TODO
        else:
            level = CONSTANTS.COMMANDLINE.VERBOSITY.get(args.verbose, CONSTANTS.COMMANDLINE.MAX_VERBOSITY)
            logging.basicConfig(level=level)
        super().__init__()

    def OnInit(self) -> bool:  # type: ignore
        """Initialization"""
        from calldiff.model.preferences import Preferences
        from calldiff.model.live_data import LiveData
        from calldiff.view.main_frame import MainFrame

        self.settings = Preferences.load(self.args.reset)
        self.live_data = LiveData()
        self.frame = MainFrame(None, title=_("CallDiff"), name="frame")
        if self.settings.window_rect:
            self.frame.SetRect(self.settings.window_rect)
        if self.settings.maximize:
            self.frame.Maximize()
        self.frame.Show()

        return True

    def OnExit(self) -> int:
        """Clean up"""
        self.settings.save()
        return super().OnExit()
