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

        self.settings = Preferences.load(self.args.reset)
        self.live_data = LiveData()

        # TODO
        self.frame = wx.Frame(None, title=_("CallDiff"), name="frame")
        # TODO apply settings
        from calldiff.view.diff_panel import DiffPanel

        self.diff_panel = DiffPanel(self.frame, name="diff_panel")
        self.diff_panel.set_contents([str(x) for x in range(100)])
        self.frame.Show()
        # TODO frame on_close update settings

        return True

    def OnExit(self) -> int:
        """Clean up"""
        self.settings.save()
        return super().OnExit()
