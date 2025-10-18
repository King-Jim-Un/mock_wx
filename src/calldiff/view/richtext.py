"""Rich text display for log messages and errors"""

import logging
import wx

from mock_wx.test_runner import Actions

from calldiff import application

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


class RichText(wx.TextCtrl):
    def add_chunk(self, text_type: Actions, text: str):
        settings = application.get_app().settings
        colors = {
            Actions.EXPOSITION: settings.exposition_text,
            Actions.LOG: settings.log_text,
            Actions.STDOUT: settings.stdout_text,
            Actions.STDERR: settings.stderr_text,
        }
        style = wx.TextAttr(colors[text_type])
        subchunks = text.split("\b") if text_type == Actions.EXPOSITION else [text]
        for index, subchunk in enumerate(subchunks):
            style.SetFontWeight(settings.bold_weight if index % 2 else wx.FONTWEIGHT_NORMAL)
            self.SetDefaultStyle(style)
            self.AppendText(subchunk)
