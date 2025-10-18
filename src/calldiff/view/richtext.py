"""Rich text display for log messages and errors"""

from dataclasses import dataclass
import logging
from typing import List

import wx
from wx import richtext

from mock_wx.test_runner import Actions

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


@dataclass
class TextChunk:
    text_type: Actions
    text: str


class RichText(richtext.RichTextCtrl):
    chunks: List[TextChunk]
    length: int = 0
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chunks = []

    def add_chunk(self, text_type: Actions, text: str):
        if text_type == Actions.EXPOSITION:
            style = wx.TextAttr(wx.RED)
        else:
            style = wx.TextAttr(wx.BLACK)
        self.chunks.append(TextChunk(text_type, text))
        self.AppendText(text)
        new_len = self.length + len(text)
        self.SetStyle(self.length, new_len, style)
        self.length = new_len

    def Clear(self):
        self.chunks = []
        self.length = 0
        super().Clear()