from mock_wx import wxTestCase, note_func, patch, call

import logging
import wx

from sample2 import MainFrame

LOG = logging.getLogger(__name__)


class TestMainFrame(wxTestCase):
    def setUp(self):
        with self.create_dut():
            self.dut = MainFrame(None, name="dut")
        self.ecl = [
            call.MainFrame(None, name="dut"),
            call.Point(10, 10),
            call.Button(self.dut, label="Submit", pos=self.Point.obj0, name="button1"),
            call.self.dut.button1.Bind({"EVT_BUTTON"}, self.dut.on_submit),
            call.Point(10, 50),
            call.Button(self.dut, label="Undo", pos=self.Point.obj1, name="button2"),
            call.self.dut.button2.Bind({"EVT_BUTTON"}, self.dut.on_undo),
            call.Point(10, 90),
            call.Button(self.dut, label="Redo", pos=self.Point.obj2, name="button3"),
            call.self.dut.button3.Bind({"EVT_BUTTON"}, self.dut.on_redo),
            call.self.dut.Bind({"EVT_CLOSE"}, self.dut.on_close),
        ]

    def test_construct(self):
        self.check(self.ecl)

    @note_func("on_close")
    def test_on_close(self) -> None:
        """Should display a confirmation dialog before losing any unsaved changes"""
        ecl = self.ecl

        # No unsaved changes
        event = wx.CloseEvent(name="/event")
        ecl += [call.CloseEvent(name="/event")]
        event.CanVeto.return_value = True
        self.app.cmd_processor.IsDirty.return_value = False
        self.dut.on_close(event)
        ecl += [
            call.self.on_close(event),
            call.event.CanVeto(),
            call.GetApp(),
            call.self.app.cmd_processor.IsDirty(),
            call.event.Skip(),
        ]

        # Unsaved changes, the user clicks "No" on the dialog
        self.app.cmd_processor.IsDirty.return_value = True
        self.mock.MessageDialog.return_value.ShowModal.return_value = wx.ID_NO
        self.dut.on_close(event)
        ecl += [
            call.self.on_close(event),
            call.event.CanVeto(),
            call.GetApp(),
            call.self.app.cmd_processor.IsDirty(),
            call.MessageDialog(
                self.dut,
                "You'll lose your unsaved changes if you quit now. Quit anyway?",
                "Unsaved Changes",
                {"ICON_WARNING", "YES_NO", "NO_DEFAULT"},
            ),
            call.MessageDialog().ShowModal(),
            call.event.Veto(),
            call.MessageDialog().Destroy(),
        ]

        # Same but the user clicks "Yes"
        self.mock.MessageDialog.return_value.ShowModal.return_value = wx.ID_YES
        self.dut.on_close(event)
        ecl += [
            call.self.on_close(event),
            call.event.CanVeto(),
            call.GetApp(),
            call.self.app.cmd_processor.IsDirty(),
            call.MessageDialog(
                self.dut,
                "You'll lose your unsaved changes if you quit now. Quit anyway?",
                "Unsaved Changes",
                {"ICON_WARNING", "YES_NO", "NO_DEFAULT"},
            ),
            call.MessageDialog().ShowModal(),
            call.MessageDialog().Destroy(),
            call.event.Skip(),
        ]

        self.check(ecl)
