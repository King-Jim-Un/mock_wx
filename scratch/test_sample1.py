from mock_wx import wxTestCase, note_func, patch, call

import logging
from unittest.mock import mock_open
import wx

import sample1

LOG = logging.getLogger(__name__)


class TestMainFrame(wxTestCase):
    def setUp(self):
        with self.create_dut("/sample1.open"):
            mock_open(self.mock.sample1.open, "first\nlast\naddress1\naddress2")
            self.dut = sample1.MainFrame(None, name="dut")
        self.ecl = [
            call.MainFrame(None, name="dut"),
            call.sample1.open("name_and_address.txt", "rt"),
            call.sample1.open_return_value(self.mock.sample1.open.return_value),
            call.sample1.open().__enter__(),
            call.sample1.open().readline(),
            call.sample1.open().readline(),
            call.sample1.open().read(),
            call.sample1.open().__exit__(None, None, None),
            call.sample1.open().close(),
            call.Panel(self.dut),
            call.Point(10, 15),
            call.StaticText(self.Panel.obj0, -1, "Name:", self.Point.obj0),
            call.Point(60, 10),
            call.TextCtrl(self.Panel.obj0, -1, "first", self.Point.obj1, name="first"),
            call.self.dut.first.Bind({"EVT_TEXT"}, self.dut.on_edit),
            call.Point(10, 45),
            call.StaticText(self.Panel.obj0, -1, "Last:", self.Point.obj2),
            call.Point(60, 40),
            call.TextCtrl(self.Panel.obj0, -1, "last", self.Point.obj3, name="last"),
            call.self.dut.last.Bind({"EVT_TEXT"}, self.dut.on_edit),
            call.Point(10, 75),
            call.StaticText(self.Panel.obj0, -1, "Address:", self.Point.obj4),
            call.Point(60, 70),
            call.Size(250, 70),
            call.TextCtrl(
                self.Panel.obj0,
                -1,
                "address1\naddress2",
                self.Point.obj5,
                self.Size.obj0,
                style={"TE_MULTILINE"},
                name="address",
            ),
            call.self.dut.Bind({"EVT_CLOSE"}, self.dut.on_close),
        ]

    def test_construct_file_exists(self):
        """Should load the file if it exists"""
        self.check(self.ecl)

    @patch("/sample1.open")
    def test_construct_file_not_exists(self):
        exception = FileNotFoundError()
        with self.create_dut("/sample1.open"):
            self.mock.sample1.open.side_effect = exception
            self.dut = sample1.MainFrame(None, name="dut")
        ecl = [
            call.MainFrame(None, name="dut"),
            call.sample1.open("name_and_address.txt", "rt"),
            call.sample1.open_raised(FileNotFoundError()),
            call.Panel(self.dut),
            call.Point(10, 15),
            call.StaticText(self.Panel.obj0, -1, "Name:", self.Point.obj0),
            call.Point(60, 10),
            call.TextCtrl(self.Panel.obj0, -1, "", self.Point.obj1, name="first"),
            call.self.dut.first.Bind({"EVT_TEXT"}, self.dut.on_edit),
            call.Point(100000, 45),
            # call.Point(10, 45),
            call.StaticText(self.Panel.obj0, -1, "Last:", self.Point.obj2),
            call.Point(60, 40),
            call.TextCtrl(self.Panel.obj0, -1, "", self.Point.obj3, name="last"),
            call.self.dut.last.Bind({"EVT_TEXT"}, self.dut.on_edit),
            call.Point(10, 75),
            call.StaticText(self.Panel.obj0, -1, "Address:", self.Point.obj4),
            call.Point(60, 70),
            call.Size(250, 70),
            call.TextCtrl(
                self.Panel.obj0, -1, "", self.Point.obj5, self.Size.obj0, style={"TE_MULTILINE"}, name="address"
            ),
            call.self.dut.Bind({"EVT_CLOSE"}, self.dut.on_close),
        ]
        self.check(ecl)

    @note_func("on_edit")
    def test_on_edit(self):
        ecl = self.ecl

        event = wx.CommandEvent()
        ecl += [call.CommandEvent()]
        print("printed message")

        self.mock.dut.first.GetValue.return_value = "first"
        self.mock.dut.last.GetValue.return_value = "last"
        self.dut.on_edit(event)
        ecl += [
            call.self.on_edit(self.CommandEvent.obj0),
            call.CommandEvent().Skip(),
            call.self.dut.first.GetValue(),
            call.self.dut.last.GetValue(),
            call.self.dut.SetTitle("last, first"),
        ]

        self.check(ecl)

    @note_func("on_close")
    @patch("/sample1.open")
    def test_on_close(self):
        ecl = self.ecl
        mock_open(self.mock.sample1.open)

        event = wx.CloseEvent()
        ecl += [call.CloseEvent()]

        LOG.info("in-band log message")
        self.dut.first.GetValue.return_value = "first"
        self.dut.last.GetValue.return_value = "last"
        self.dut.address.GetValue.return_value = "address1\naddress2"
        self.dut.on_close(event)
        ecl += [
            call.self.on_close(self.CloseEvent.obj0),
            call.CloseEvent().Skip(),
            call.sample1.open("name_and_address.txt", "wt"),
            call.sample1.open_return_value(self.mock.sample1.open.return_value),
            call.sample1.open().__enter__(),
            call.self.dut.first.GetValue(),
            call.self.dut.last.GetValue(),
            call.self.dut.address.GetValue(),
            call.sample1.open().write("first\nlast\naddress1\naddress2"),
            call.sample1.open().__exit__(None, None, None),
            call.sample1.open().close(),
        ]
        self.check(ecl)


LOG.debug("out-of-band log message")
