from mock_wx import wxTestCase, note_func, patch

from unittest.mock import mock_open, call
import wx

import sample1


class TestMainFrame(wxTestCase):
    def setUp(self):
        with self.create_dut("/sample1.open"):
            mock_open(self.mock.sample1.open, "first\nlast\naddress1\naddress2")
            self.dut = sample1.MainFrame(None, name="dut")
        self.SETUP = [
            call.dut(None, name="dut"),
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
            call.StaticText(self.objs.Panel[0], -1, "Name:", self.objs.Point[0]),
            call.Point(60, 10),
            call.dut.first(self.objs.Panel[0], -1, "first", self.objs.Point[1], name="first"),
            call.dut.first.Bind({"EVT_TEXT"}, self.dut.on_edit),
            call.Point(10, 45),
            call.StaticText(self.objs.Panel[0], -1, "Last:", self.objs.Point[2]),
            call.Point(60, 40),
            call.dut.last(self.objs.Panel[0], -1, "last", self.objs.Point[3], name="last"),
            call.dut.last.Bind({"EVT_TEXT"}, self.dut.on_edit),
            call.Point(10, 75),
            call.StaticText(self.objs.Panel[0], -1, "Address:", self.objs.Point[4]),
            call.Point(60, 70),
            call.Size(250, 70),
            call.dut.address(
                self.objs.Panel[0],
                -1,
                "address1\naddress2",
                self.objs.Point[5],
                self.objs.Size[0],
                style={"TE_MULTILINE"},
                name="address",
            ),
            call.dut.Bind({"EVT_CLOSE"}, self.dut.on_close),
        ]

    def test_construct_file_exists(self):
        """Should load the file if it exists"""
        self.check(self.SETUP)

    @patch("/sample1.open")
    def test_construct_file_not_exists(self):
        exception = FileNotFoundError()
        with self.create_dut("/sample1.open"):
            self.mock.sample1.open.side_effect = exception
            self.dut = sample1.MainFrame(None, name="dut")
        expect = [
            call.dut(None, name="dut"),
            call.sample1.open("name_and_address.txt", "rt"),
            call.sample1.open_raised(exception),
            call.Panel(self.dut),
            call.Point(10, 15),
            call.StaticText(self.objs.Panel[0], -1, "Name:", self.objs.Point[0]),
            call.Point(60, 10),
            call.dut.first(self.objs.Panel[0], -1, "", self.objs.Point[1], name="first"),
            call.dut.first.Bind({"EVT_TEXT"}, self.dut.on_edit),
            call.Point(10, 45),
            call.StaticText(self.objs.Panel[0], -1, "Last:", self.objs.Point[2]),
            call.Point(60, 40),
            call.dut.last(self.objs.Panel[0], -1, "", self.objs.Point[3], name="last"),
            call.dut.last.Bind({"EVT_TEXT"}, self.dut.on_edit),
            call.Point(10, 75),
            call.StaticText(self.objs.Panel[0], -1, "Address:", self.objs.Point[4]),
            call.Point(60, 70),
            call.Size(250, 70),
            call.dut.address(
                self.objs.Panel[0],
                -1,
                "",
                self.objs.Point[5],
                self.objs.Size[0],
                style={"TE_MULTILINE"},
                name="address",
            ),
            call.dut.Bind({"EVT_CLOSE"}, self.dut.on_close),
        ]
        self.check(expect)

    @note_func("on_edit")
    def test_on_edit(self):
        expect = self.SETUP

        event = wx.CommandEvent()
        expect += [call.CommandEvent()]

        self.mock.dut.first.GetValue.return_value = "first"
        self.mock.dut.last.GetValue.return_value = "last"
        self.dut.on_edit(event)
        expect += [
            call.on_edit(self.objs.CommandEvent[0]),
            call.CommandEvent.Skip(),
            call.dut.first.GetValue(),
            call.dut.last.GetValue(),
            call.dut.SetTitle("last, first"),
        ]

        self.check(expect)

    @note_func("on_close")
    @patch("/sample1.open")
    def test_on_close(self):
        expect = self.SETUP
        mock_open(self.mock.sample1.open)

        event = wx.CloseEvent()
        expect += [call.CloseEvent()]

        self.mock.dut.first.GetValue.return_value = "first"
        self.mock.dut.last.GetValue.return_value = "last"
        self.mock.dut.address.GetValue.return_value = "address1\naddress2"
        self.dut.on_close(event)
        expect += [
            call.on_close(self.objs.CloseEvent[0]),
            call.CloseEvent.Skip(),
            call.sample1.open("name_and_address.txt", "wt"),
            call.sample1.open_return_value(self.mock.sample1.open.return_value),
            call.sample1.open().__enter__(),
            call.dut.first.GetValue(),
            call.dut.last.GetValue(),
            call.dut.address.GetValue(),
            call.sample1.open().write("first\nlast\naddress1\naddress2"),
            call.sample1.open().__exit__(None, None, None),
            call.sample1.open().close(),
        ]
        self.check(expect)
