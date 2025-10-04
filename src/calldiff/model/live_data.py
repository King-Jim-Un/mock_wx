"""Application data not saved/restored between runs"""

from dataclasses import dataclass, field
import logging
import wx

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


@dataclass
class LiveData:
    """Application data not saved/restored between runs"""
    ...
