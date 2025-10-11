import sys
from pathlib import Path

wx_path = str(Path(__file__).resolve().parent)
if wx_path not in sys.path:
    sys.path.insert(0, wx_path)

from mock_wx._test_case import wxTestCase, patch, note_func

__all__ = ["wxTestCase", "patch", "note_func"]
