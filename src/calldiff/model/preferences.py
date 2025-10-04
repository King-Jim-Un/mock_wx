"""Preference settings"""

from dataclasses import dataclass, field
import logging
import wx

from calldiff.model.app_settings import AppSettings
from calldiff.constants import ColorTuple

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


@dataclass
class Preferences(AppSettings):
    """Preference settings"""
    font_size: int = 11
    desktop_background: ColorTuple = ColorTuple((51, 51, 51))
    number_background: ColorTuple = ColorTuple((228, 228, 200))
    number_text: ColorTuple = ColorTuple((0, 0, 0))
    rule: ColorTuple = ColorTuple((255, 255, 0))
    equal_background: ColorTuple = ColorTuple((255, 255, 255))
    equal_text: ColorTuple = ColorTuple((0, 0, 0))
    delete_line_background: ColorTuple = ColorTuple((106, 32, 32))
    delete_line_text: ColorTuple = ColorTuple((255, 255, 255))
    insert_line_background: ColorTuple = ColorTuple((54, 124, 54))
    insert_line_text: ColorTuple = ColorTuple((255, 255, 255))
    replace_background: ColorTuple = ColorTuple((159, 159, 159))
    replace_text: ColorTuple = ColorTuple((0, 0, 0))
    replace_delete_background: ColorTuple = ColorTuple((106, 32, 32))
    replace_delete_text: ColorTuple = ColorTuple((255, 255, 255))
    replace_insert_background: ColorTuple = ColorTuple((54, 124, 54))
    replace_insert_text: ColorTuple = ColorTuple((255, 255, 255))
    hover_delete_line_background: ColorTuple = ColorTuple((106, 32, 32))
    hover_delete_line_text: ColorTuple = ColorTuple((0, 0, 0))
    hover_insert_line_background: ColorTuple = ColorTuple((54, 124, 54))
    hover_insert_line_text: ColorTuple = ColorTuple((0, 0, 0))
    hover_replace_background: ColorTuple = ColorTuple((0, 0, 0))
    hover_replace_text: ColorTuple = ColorTuple((159, 159, 159))
    hover_replace_delete_background: ColorTuple = ColorTuple((106, 32, 32))
    hover_replace_delete_text: ColorTuple = ColorTuple((0, 0, 0))
    hover_replace_insert_background: ColorTuple = ColorTuple((54, 124, 54))
    hover_replace_insert_text: ColorTuple = ColorTuple((0, 0, 0))
