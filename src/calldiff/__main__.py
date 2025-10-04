"""Main entrypoint"""

from argparse import ArgumentParser
import logging
from pathlib import Path
import wx

from calldiff.app_body import CallDiffApp

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


def main() -> None:
    """Main entrypoint"""
    parser = ArgumentParser()
    parser.add_argument("-r", "--reset", action="store_true", help="Reset saved settings")
    parser.add_argument("-v", "--verbose", action="count", default=1, help="Increase verbosity")
    parser.add_argument("-q", "--quiet", action="store_const", const=0, dest="verbose", help="Decrease verbosity")
    parser.add_argument("-l", "--log-file", type=Path, help="Specify log file")
    CallDiffApp(parser.parse_args()).MainLoop()


if __name__ == "__main__":
    main()
