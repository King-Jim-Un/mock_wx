"""Difference panel"""

import logging
import wx

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation

from calldiff import application
from calldiff.constants import CONSTANTS, LineType


class DiffPanel(wx.ScrolledCanvas):
    font: wx.Font

    def __init__(self, *args, **kwargs) -> None:
        """Constructor"""
        super().__init__(*args, **kwargs)
        app = application.get_app()
        self.font = wx.Font(app.settings.font_size, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.Bind(wx.EVT_PAINT, self.on_paint)

    def on_paint(self, _event: wx.PaintEvent) -> None:
        """Handle paint event"""
        app = application.get_app()
        contents = app.live_data.compare_exception
        settings = app.settings
        backgrounds = {
            LineType.EQUAL: settings.equal_background,
            LineType.INSERT: settings.insert_line_background,
            LineType.DELETE: settings.delete_line_background,
            LineType.REPLACE: settings.replace_background,
        }
        foregrounds = {
            LineType.EQUAL: settings.equal_text,
            LineType.INSERT: settings.insert_line_text,
            LineType.DELETE: settings.delete_line_text,
            LineType.REPLACE: settings.replace_text,
        }
        size = self.GetClientSize()
        dc = wx.PaintDC(self)
        try:
            self.DoPrepareDC(dc)

            dc.SetBackground(wx.Brush(settings.desktop_background))
            dc.Clear()
            if contents is None:
                return

            # Get line size
            dc.SetFont(self.font)
            text = str(contents.last_line_num())
            max_width, max_height = dc.GetTextExtent(text)
            col_width = int(max_width * CONSTANTS.WINDOWS.DIFF.LINE_NUM_SCALE[0])
            line_height = int(max_height * CONSTANTS.WINDOWS.DIFF.LINE_NUM_SCALE[1])

            # Draw number pane
            pen_width = CONSTANTS.WINDOWS.DIFF.DIVIDER_WIDTH
            panel_offset = col_width + pen_width
            panel_width = size.width - panel_offset
            dc.SetPen(wx.Pen(settings.rule, pen_width))
            dc.SetBrush(wx.Brush(settings.number_background))
            dc.DrawRectangle(-pen_width, -pen_width, col_width + (pen_width * 2), size.height + (pen_width * 2))
            diff_text_offset = CONSTANTS.WINDOWS.DIFF.DIFF_TEXT_OFFSET

            # Loop over lines
            for index, line in enumerate(contents.comparison_lines):
                color = backgrounds[line.line_type]
                dc.SetPen(wx.Pen(color))
                dc.SetBrush(wx.Brush(color))
                y = line_height * index
                dc.DrawRectangle(panel_offset, y, panel_width, line_height)
                if line.expect:
                    dc.SetTextForeground(settings.number_text)
                    line_number = str(line.expect.line_number)
                    text_width, text_height = dc.GetTextExtent(line_number)
                    offset = CONSTANTS.WINDOWS.DIFF.LINE_NUM_OFFSET
                    dc.DrawText(line_number, offset[0] + max_width - text_width, offset[1] + y)
                if line.line_type == LineType.REPLACE:
                    self.draw_replacement_line(dc, index, panel_offset, line_height)
                else:
                    dc.SetTextForeground(foregrounds[line.line_type])
                    text = str(line)
                    dc.DrawText(text, diff_text_offset[0] + panel_offset, diff_text_offset[1] + y)
        finally:
            dc.Destroy()

    def draw_replacement_line(self, dc: wx.DC, index: int, panel_offset: int, line_height: int) -> None:
        """Draw a line of text in replacement mode"""
        app = application.get_app()
        contents = app.live_data.compare_exception
        settings = app.settings
        line = contents.comparison_lines[index]
        backgrounds = {
            LineType.EQUAL: settings.replace_background,
            LineType.INSERT: settings.insert_line_background,
            LineType.DELETE: settings.delete_line_background,
            LineType.REPLACE: settings.replace_background,
        }
        foregrounds = {
            LineType.EQUAL: settings.replace_text,
            LineType.INSERT: settings.insert_line_text,
            LineType.DELETE: settings.delete_line_text,
            LineType.REPLACE: settings.replace_text,
        }
        x = panel_offset
        y = line_height * index
        text_indent = CONSTANTS.WINDOWS.DIFF.DIFF_TEXT_OFFSET[0]
        for chunk in line.line_analysis.chunks:
            color = backgrounds[chunk.chunk_type]
            dc.SetPen(wx.Pen(color))
            dc.SetBrush(wx.Brush(color))
            text_width, text_height = dc.GetTextExtent(chunk.text)
            dc.DrawRectangle(x, y, text_width, line_height)
            dc.SetTextForeground(foregrounds[chunk.chunk_type])
            dc.DrawText(chunk.text, x + text_indent, CONSTANTS.WINDOWS.DIFF.DIFF_TEXT_OFFSET[1] + y)
            x += text_width + text_indent
            text_indent = 0
