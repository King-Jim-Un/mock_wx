"""Main entrypoint"""

# Ensure we import wx before mock_wx to foil mock_wx's path tweaks
import wx
import mock_wx

from argparse import ArgumentParser
from pathlib import Path
import logging

from calldiff.constants import CONSTANTS
from calldiff.application import CallDiffApp

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


def main():
    """Main entrypoint"""
    parser = ArgumentParser()
    parser.add_argument("-r", "--reset", action="store_true", help="Reset saved settings")
    parser.add_argument("-v", "--verbose", action="count", default=1, help="Increase verbosity")
    parser.add_argument("-q", "--quiet", action="store_const", const=0, dest="verbose", help="Decrease verbosity")
    parser.add_argument("-l", "--log-file", type=Path, help="Specify log file")
    args = parser.parse_args()

    if args.log_file:
        ...  # TODO
    else:
        level = CONSTANTS.COMMANDLINE.VERBOSITY.get(args.verbose, CONSTANTS.COMMANDLINE.MAX_VERBOSITY)
        logging.basicConfig(level=level)

    CallDiffApp(args.reset).MainLoop()


if __name__ == "__main__":
    main()
