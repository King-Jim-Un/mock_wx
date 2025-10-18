"""Preference settings"""

from dataclasses import dataclass, field
import logging
import wx

from calldiff.model.app_settings import AppSettings

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


@dataclass
class Preferences(AppSettings):
    """Preference settings"""
    exposition_text: wx.Colour = field(default_factory=lambda: wx.Colour(54, 124, 54))
    bold_weight: int = wx.FONTWEIGHT_BOLD
    log_text: wx.Colour = field(default_factory=lambda: wx.Colour(54, 68, 124))
    stdout_text: wx.Colour = field(default_factory=lambda: wx.Colour(0, 0, 0))
    stderr_text: wx.Colour = field(default_factory=lambda: wx.Colour(106, 32, 32))
    show_fancy_diff: bool = True  # TODO
    show_passing_tests: bool = False  # TODO
    font_size: int = 11
    desktop_background: wx.Colour = field(default_factory=lambda: wx.Colour(51, 51, 51))
    number_background: wx.Colour = field(default_factory=lambda: wx.Colour(228, 228, 200))
    number_text: wx.Colour = field(default_factory=lambda: wx.Colour(0, 0, 0))
    rule: wx.Colour = field(default_factory=lambda: wx.Colour(255, 255, 0))
    equal_background: wx.Colour = field(default_factory=lambda: wx.Colour(255, 255, 255))
    equal_text: wx.Colour = field(default_factory=lambda: wx.Colour(0, 0, 0))
    delete_line_background: wx.Colour = field(default_factory=lambda: wx.Colour(106, 32, 32))
    delete_line_text: wx.Colour = field(default_factory=lambda: wx.Colour(255, 255, 255))
    insert_line_background: wx.Colour = field(default_factory=lambda: wx.Colour(54, 124, 54))
    insert_line_text: wx.Colour = field(default_factory=lambda: wx.Colour(255, 255, 255))
    replace_background: wx.Colour = field(default_factory=lambda: wx.Colour(198, 198, 198))
    replace_text: wx.Colour = field(default_factory=lambda: wx.Colour(0, 0, 0))
    replace_delete_background: wx.Colour = field(default_factory=lambda: wx.Colour(106, 32, 32))
    replace_delete_text: wx.Colour = field(default_factory=lambda: wx.Colour(255, 255, 255))
    replace_insert_background: wx.Colour = field(default_factory=lambda: wx.Colour(54, 124, 54))
    replace_insert_text: wx.Colour = field(default_factory=lambda: wx.Colour(255, 255, 255))
    hover_delete_line_background: wx.Colour = field(default_factory=lambda: wx.Colour(106, 32, 32))
    hover_delete_line_text: wx.Colour = field(default_factory=lambda: wx.Colour(0, 0, 0))
    hover_insert_line_background: wx.Colour = field(default_factory=lambda: wx.Colour(54, 124, 54))
    hover_insert_line_text: wx.Colour = field(default_factory=lambda: wx.Colour(0, 0, 0))
    hover_replace_background: wx.Colour = field(default_factory=lambda: wx.Colour(0, 0, 0))
    hover_replace_text: wx.Colour = field(default_factory=lambda: wx.Colour(255, 255, 255))
    hover_replace_delete_background: wx.Colour = field(default_factory=lambda: wx.Colour(255, 0, 0))
    hover_replace_delete_text: wx.Colour = field(default_factory=lambda: wx.Colour(0, 0, 0))
    hover_replace_insert_background: wx.Colour = field(default_factory=lambda: wx.Colour(0, 255, 0))
    hover_replace_insert_text: wx.Colour = field(default_factory=lambda: wx.Colour(0, 0, 0))
