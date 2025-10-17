"""Application data not saved/restored between runs"""

from dataclasses import dataclass, field
import logging
from pathlib import Path
from typing import Optional, Dict
import wx

from calldiff.control.run_tests import TestFile, TestFunction

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


@dataclass
class TestsRoot:
    """The root node in the testing tree"""
    node_id: wx.TreeItemId = field(default_factory=wx.TreeItemId)


@dataclass
class LiveData:
    """Application data not saved/restored between runs"""
    tree_root: TestsRoot = field(default_factory=TestsRoot)
    test_files: Dict[Path, TestFile] = field(default_factory=dict)
    display_test: Optional[TestFunction] = None
