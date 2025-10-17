"""Rich text display for log messages and errors"""

from dataclasses import dataclass
import logging
from typing import List

import wx
from wx import richtext

from calldiff.constants import TextType

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


@dataclass
class TextChunk:
    text_type: TextType
    text: str


class RichText(richtext.RichTextCtrl):
    chunks: List[TextChunk]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chunks = []

    def add_chunk(self, text_type: TextType, text: str):
        self.chunks.append(TextChunk(text_type, text))
        self.AppendText(text)
