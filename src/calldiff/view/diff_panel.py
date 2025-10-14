"""Difference panel"""

from dataclasses import dataclass
import logging
from pubsub import pub
from typing import List, Optional, Tuple, Dict
import wx

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation

from calldiff import application
from calldiff.constants import CONSTANTS, LineType


@dataclass
class Change:
    rect: wx.Rect
    lines: range
    text: str = ""


class DiffPanel(wx.ScrolledCanvas):
    font: wx.Font
    changes: List[Change]
    size: wx.Size
    max_width: int
    max_height: int
    col_width: int
    line_height: int
    pen_width: int
    diff_text_offset: Tuple[int, int]
    panel_offset: int
    panel_width: int
    mouse_over_change: Optional[int] = None
    click_change: Optional[int] = None
    backgrounds: Dict[LineType, wx.Colour]
    foregrounds: Dict[LineType, wx.Colour]
    select_bgs: Dict[LineType, wx.Colour]
    select_fgs: Dict[LineType, wx.Colour]
    replace_bgs: Dict[LineType, wx.Colour]
    replace_fgs: Dict[LineType, wx.Colour]
    sel_repl_bgs: Dict[LineType, wx.Colour]
    sel_repl_fgs: Dict[LineType, wx.Colour]

    def __init__(self, *args, **kwargs) -> None:
        """Constructor"""
        super().__init__(*args, **kwargs)
        self.changes = []
        settings = application.get_app().settings
        self.font = wx.Font(settings.font_size, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_MOTION, self.on_move)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_move)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_up)
        pub.subscribe(self.on_show_error, CONSTANTS.PUBSUB.SHOW_ERROR)
        self.backgrounds = {
            LineType.EQUAL: settings.equal_background,
            LineType.INSERT: settings.insert_line_background,
            LineType.DELETE: settings.delete_line_background,
            LineType.REPLACE: settings.replace_background,
        }
        self.foregrounds = {
            LineType.EQUAL: settings.equal_text,
            LineType.INSERT: settings.insert_line_text,
            LineType.DELETE: settings.delete_line_text,
            LineType.REPLACE: settings.replace_text,
        }
        self.select_bgs = {
            LineType.EQUAL: settings.equal_background,
            LineType.INSERT: settings.hover_insert_line_background,
            LineType.DELETE: settings.hover_delete_line_background,
            LineType.REPLACE: settings.hover_replace_background,
        }
        self.select_fgs = {
            LineType.EQUAL: settings.equal_text,
            LineType.INSERT: settings.hover_insert_line_text,
            LineType.DELETE: settings.hover_delete_line_text,
            LineType.REPLACE: settings.hover_replace_text,
        }
        self.replace_bgs = {
            LineType.EQUAL: settings.replace_background,
            LineType.INSERT: settings.insert_line_background,
            LineType.DELETE: settings.delete_line_background,
            LineType.REPLACE: settings.replace_background,
        }
        self.replace_fgs = {
            LineType.EQUAL: settings.replace_text,
            LineType.INSERT: settings.insert_line_text,
            LineType.DELETE: settings.delete_line_text,
            LineType.REPLACE: settings.replace_text,
        }
        self.sel_repl_bgs = {
            LineType.EQUAL: settings.hover_replace_background,
            LineType.INSERT: settings.hover_replace_insert_background,
            LineType.DELETE: settings.hover_replace_delete_background,
            LineType.REPLACE: settings.hover_replace_background,
        }
        self.sel_repl_fgs = {
            LineType.EQUAL: settings.hover_replace_text,
            LineType.INSERT: settings.hover_replace_insert_text,
            LineType.DELETE: settings.hover_replace_delete_text,
            LineType.REPLACE: settings.hover_replace_text,
        }
        self.pen_width = CONSTANTS.WINDOWS.DIFF.DIVIDER_WIDTH
        self.diff_text_offset = CONSTANTS.WINDOWS.DIFF.DIFF_TEXT_OFFSET

    def on_show_error(self):
        self.on_size()

    def on_size(self, event: Optional[wx.SizeEvent] = None) -> None:
        if event:
            event.Skip()
        self.changes = []
        latest_change: Optional[Change] = None
        contents = application.get_app().live_data.compare_exception
        if contents:
            self.size = self.GetClientSize()
            text = str(contents.last_line_num())
            dc = wx.ClientDC(self)
            try:
                self.max_width, self.max_height = dc.GetTextExtent(text)
            finally:
                dc.Destroy()
            self.col_width = int(self.max_width * CONSTANTS.WINDOWS.DIFF.LINE_NUM_SCALE[0])
            self.line_height = int(self.max_height * CONSTANTS.WINDOWS.DIFF.LINE_NUM_SCALE[1])
            self.panel_offset = self.col_width + self.pen_width
            self.panel_width = self.size.width - self.panel_offset
            for index, line in enumerate(contents.comparison_lines):
                y = self.line_height * index
                rect = wx.Rect(self.panel_offset, y, self.panel_width, self.line_height)
                if line.line_type == LineType.EQUAL:
                    latest_change = None
                else:
                    if latest_change is None:
                        latest_change = Change(rect, range(index, index + 1), line.to_copy())
                        self.changes.append(latest_change)
                    else:
                        latest_change.rect.height += self.line_height
                        latest_change.lines = range(latest_change.lines[0], index + 1)
                        latest_change.text += line.to_copy()

    def index_in(self, index: int) -> bool:
        if self.click_change is None:
            if self.mouse_over_change is None:
                return False
            else:
                return index in self.changes[self.mouse_over_change].lines
        else:
            return index in self.changes[self.click_change].lines

    def on_paint(self, _event: wx.PaintEvent) -> None:
        """Handle paint event"""
        app = application.get_app()
        contents = app.live_data.compare_exception
        settings = app.settings
        dc = wx.PaintDC(self)
        try:
            self.DoPrepareDC(dc)

            dc.SetBackground(wx.Brush(settings.desktop_background))
            dc.Clear()
            if contents is None:
                return
            dc.SetFont(self.font)

            # Draw number pane
            dc.SetPen(wx.Pen(settings.rule, self.pen_width))
            dc.SetBrush(wx.Brush(settings.number_background))
            dc.DrawRectangle(
                -self.pen_width,
                -self.pen_width,
                self.col_width + (self.pen_width * 2),
                self.size.height + (self.pen_width * 2),
            )

            # Loop over lines
            for index, line in enumerate(contents.comparison_lines):
                if self.index_in(index):
                    background = self.select_bgs[line.line_type]
                    foreground = self.select_fgs[line.line_type]
                else:
                    background = self.backgrounds[line.line_type]
                    foreground = self.foregrounds[line.line_type]
                dc.SetPen(wx.Pen(background))
                dc.SetBrush(wx.Brush(background))
                y = self.line_height * index
                rect = wx.Rect(self.panel_offset, y, self.panel_width, self.line_height)
                dc.DrawRectangle(rect)
                if line.expect:
                    dc.SetTextForeground(settings.number_text)
                    line_number = str(line.expect.line_number)
                    text_width, text_height = dc.GetTextExtent(line_number)
                    offset = CONSTANTS.WINDOWS.DIFF.LINE_NUM_OFFSET
                    dc.DrawText(line_number, offset[0] + self.max_width - text_width, offset[1] + y)
                if line.line_type == LineType.REPLACE:
                    self.draw_replacement_line(dc, index, self.panel_offset, self.line_height)
                else:
                    dc.SetTextForeground(foreground)
                    text = str(line)
                    dc.DrawText(text, self.diff_text_offset[0] + self.panel_offset, self.diff_text_offset[1] + y)
            if (self.mouse_over_change is not None) and (self.click_change in [None, self.mouse_over_change]):
                art = wx.ArtProvider.GetBitmap(wx.ART_COPY)
                rect = self.changes[self.mouse_over_change].rect
                point = wx.Point(rect.right - 50, rect.top + ((rect.height - art.Size.height) // 2))
                dc.DrawBitmap(art, point, True)
        finally:
            dc.Destroy()

    def draw_replacement_line(self, dc: wx.DC, index: int, panel_offset: int, line_height: int) -> None:
        """Draw a line of text in replacement mode"""
        app = application.get_app()
        contents = app.live_data.compare_exception
        line = contents.comparison_lines[index]
        x = panel_offset
        y = line_height * index
        text_indent = CONSTANTS.WINDOWS.DIFF.DIFF_TEXT_OFFSET[0]
        for chunk in line.line_analysis.chunks:
            if self.index_in(index):
                background = self.sel_repl_bgs[chunk.chunk_type]
                foreground = self.sel_repl_fgs[chunk.chunk_type]
            else:
                background = self.replace_bgs[chunk.chunk_type]
                foreground = self.replace_fgs[chunk.chunk_type]
            dc.SetPen(wx.Pen(background))
            dc.SetBrush(wx.Brush(background))
            text_width, text_height = dc.GetTextExtent(chunk.text)
            dc.DrawRectangle(x, y, text_width, line_height)
            dc.SetTextForeground(foreground)
            dc.DrawText(chunk.text, x + text_indent, CONSTANTS.WINDOWS.DIFF.DIFF_TEXT_OFFSET[1] + y)
            x += text_width + text_indent
            text_indent = 0

    def find_change(self, point: wx.Point) -> Optional[int]:
        for index, change in enumerate(self.changes):
            if change.rect.Contains(point):
                return index
        return None

    def on_move(self, event: wx.MouseEvent) -> None:
        event.Skip()
        mouse_over_change = self.find_change(event.GetPosition())
        if mouse_over_change != self.mouse_over_change:
            rect = self.changes[self.mouse_over_change if mouse_over_change is None else mouse_over_change].rect
            rect = wx.Rect(rect.x-5,rect.y-5,rect.width+5,rect.height+5)
            self.RefreshRect(rect)
            self.mouse_over_change = mouse_over_change

    def on_down(self, event: wx.MouseEvent) -> None:
        event.Skip()
        self.click_change = self.find_change(event.GetPosition())

    def on_up(self, event: wx.MouseEvent) -> None:
        event.Skip()
        click_change = self.find_change(event.GetPosition())
        if (click_change == self.click_change) and (click_change is not None):
            wx.TheClipboard.Open()
            try:
                wx.TheClipboard.SetData(wx.TextDataObject(self.changes[click_change].text))
                wx.TheClipboard.Flush()
            finally:
                wx.TheClipboard.Close()
        if self.click_change is not None:
            self.RefreshRect(self.changes[self.click_change].rect)
        self.click_change = None
