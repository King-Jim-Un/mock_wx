"""Persistent application settings"""

from dataclasses import dataclass
import logging
from pathlib import Path
from typing import Optional
import wx

from calldiff.model.settings import Settings

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


@dataclass
class AppSettings(Settings):
    """Persistent application settings"""

    maximize: bool = False
    window_rect: tuple = ()
    logging_level: int = logging.WARNING
    log_file: Optional[Path] = None
