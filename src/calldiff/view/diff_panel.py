"""Difference panel"""

import logging
import wx

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation

from calldiff.app_header import get_app
from calldiff.constants import CONSTANTS
from calldiff.model.comparison import HashableComparison


class DiffPanel(wx.ScrolledCanvas):
    contents: HashableComparison
    font: wx.Font

    def __init__(self, *args, **kwargs) -> None:
        """Constructor"""
        super().__init__(*args, **kwargs)
        self.font = wx.Font(
            get_app().settings.font_size, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL
        )
        self.Bind(wx.EVT_PAINT, self.on_paint)

    def set_contents(self, contents: HashableComparison) -> None:
        self.contents = contents

    def on_paint(self, _event: wx.PaintEvent) -> None:
        """Handle paint event"""
        app = get_app()
        dc = wx.PaintDC(self)
        try:
            self.DoPrepareDC(dc)

            dc.SetBackground(wx.Brush(app.settings.desktop_background))
            dc.Clear()

            # Get line size
            text = str(len(self.contents))
            max_width, max_height = dc.GetTextExtent(text)
            col_width = int(max_width * CONSTANTS.WINDOWS.DIFF.LINE_NUM_SCALE[0])
            line_height = int(max_height * CONSTANTS.WINDOWS.DIFF.LINE_NUM_SCALE[1])

            # Draw line numbers
            pen_width = CONSTANTS.WINDOWS.DIFF.DIVIDER_WIDTH
            dc.SetPen(wx.Pen(app.settings.rule, pen_width))
            dc.SetBrush(wx.Brush(app.settings.number_background))
            dc.DrawRectangle(-pen_width, -pen_width, col_width, self.GetClientSize().height + (pen_width * 2))
            dc.SetPen(wx.Pen(app.settings.number_text))
            dc.SetFont(self.font)
            x, y = CONSTANTS.WINDOWS.DIFF.LINE_NUM_OFFSET
            for line_num in range(1, len(self.contents) + 1):
                text_width, text_height = dc.GetTextExtent(str(line_num))
                dc.DrawText(str(line_num), x + max_width - text_width, y)
                y += line_height
        finally:
            dc.Destroy()
