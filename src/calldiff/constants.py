"""Constants, enums, and types"""

import logging
from typing import Tuple, NewType
import wx
from mypy.types import NewType

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation

# Types:
ColorTuple = NewType("ColorTuple", Tuple[int, int, int])


class CONSTANTS:
    """Constants"""
    class COMMANDLINE:
        VERBOSITY = {0: logging.ERROR, 1: logging.WARNING, 2: logging.INFO, 3: logging.DEBUG}
        MAX_VERBOSITY = logging.DEBUG

    class PERSIST:
        APP_NAME = "CallDiff"
        VENDOR_NAME = "CallDiff"
        PATH_NAME = "SETTINGS"

    class WINDOWS:
        class DIFF:
            LINE_NUM_SCALE = (1.7, 1.2)
            LINE_NUM_OFFSET = (5, 2)
            DIVIDER_WIDTH = 2
