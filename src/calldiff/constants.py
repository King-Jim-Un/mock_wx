"""Constants, enums, and types"""

from enum import Enum, auto
import logging
from pathlib import Path
import wx

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation

# Types:


# Enums:
class LineType(Enum):
    EQUAL = auto()
    INSERT = auto()
    DELETE = auto()
    REPLACE = auto()


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
            DIFF_TEXT_OFFSET = (5, 2)

    class PUBSUB:
        NEW_NODE = "NEW_NODE"
        UPDATE_NODE = "UPDATE_NODE"

    class PATHS:
        CALL_DIFF = Path(__file__).parent.resolve()
        ROOT = CALL_DIFF.parents[1].resolve()
        MOCK_WX = CALL_DIFF.parent / "mock_wx"
        TEST_RUNNER = MOCK_WX / "__main__.py"
