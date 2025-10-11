"""Application data not saved/restored between runs"""

from dataclasses import dataclass, field
import logging
import wx

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


@dataclass
class TestsRoot:
    node_id: wx.TreeItemId = field(default_factory=wx.TreeItemId)


@dataclass
class LiveData:
    """Application data not saved/restored between runs"""
    tree_root: TestsRoot = field(default_factory=TestsRoot)
