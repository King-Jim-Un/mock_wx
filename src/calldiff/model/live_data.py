"""Application data not saved/restored between runs"""

from dataclasses import dataclass, field
import logging
from typing import Optional
import wx

from calldiff.model.comparison import HashableComparison

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
    compare_exception: Optional[HashableComparison] = None
