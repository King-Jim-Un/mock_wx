import wx

FILENAME = "name_and_address.txt"


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        try:
            with open(FILENAME, "rt") as file_obj:
                first = file_obj.readline().strip()
                last = file_obj.readline().strip()
                address = file_obj.read().strip()
        except Exception:
            first = last = address = ""

        panel = wx.Panel(self)
        wx.StaticText(panel, -1, "Name:", wx.Point(10, 15))
        self.first = wx.TextCtrl(panel, -1, first, wx.Point(60, 10), name="first")
        self.first.Bind(wx.EVT_TEXT, self.on_edit)
        wx.StaticText(panel, -1, "Last:", wx.Point(10, 45))
        self.last = wx.TextCtrl(panel, -1, last, wx.Point(60, 40), name="last")
        self.last.Bind(wx.EVT_TEXT, self.on_edit)
        wx.StaticText(panel, -1, "Address:", wx.Point(10, 75))
        self.address = wx.TextCtrl(
            panel, -1, address, wx.Point(60, 70), wx.Size(250, 70), style=wx.TE_MULTILINE, name="address"
        )

        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_edit(self, event: wx.CommandEvent) -> None:
        event.Skip()
        first = self.first.GetValue()
        last = self.last.GetValue()
        self.SetTitle(f"{last}, {first}" if first and last else "Name and Address")

    def on_close(self, event: wx.CloseEvent):
        event.Skip()
        with open(FILENAME, "wt") as file_obj:
            file_obj.write(f"{self.first.GetValue()}\n{self.last.GetValue()}\n{self.address.GetValue()}")


class MyApp(wx.App):
    def OnInit(self) -> bool:
        self.frame = MainFrame(None, -1, "Name and Address", name="frame")
        self.frame.Show()
        return True


if __name__ == "__main__":
    MyApp().MainLoop()
