import wx

# Constants:
_ = wx.GetTranslation


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs) -> None:
        """Constructor"""
        super().__init__(*args, **kwargs)
        self.button1 = wx.Button(self, label=_("Submit"), pos=wx.Point(10, 10), name="button1")
        self.button1.Bind(wx.EVT_BUTTON, self.on_submit)
        self.button2 = wx.Button(self, label=_("Undo"), pos=wx.Point(10, 50), name="button2")
        self.button2.Bind(wx.EVT_BUTTON, self.on_undo)
        self.button3 = wx.Button(self, label=_("Redo"), pos=wx.Point(10, 90), name="button3")
        self.button3.Bind(wx.EVT_BUTTON, self.on_redo)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    @staticmethod
    def on_submit(_event: wx.CommandEvent) -> None:
        """Handle submit event"""
        wx.GetApp().cmd_processor.Submit(Command())

    @staticmethod
    def on_undo(_event: wx.CommandEvent) -> None:
        """Handle undo event"""
        wx.GetApp().cmd_processor.Undo()

    @staticmethod
    def on_redo(_event: wx.CommandEvent) -> None:
        """Handle redo event"""
        wx.GetApp().cmd_processor.Redo()

    def on_close(self, event: wx.CloseEvent) -> None:
        """Handler for close events"""
        if event.CanVeto() and wx.GetApp().cmd_processor.IsDirty():
            dialog = wx.MessageDialog(
                self,
                _("You'll lose your unsaved changes if you quit now. Quit anyway?"),
                _("Unsaved Changes"),
                wx.ICON_WARNING | wx.YES_NO | wx.NO_DEFAULT,
            )
            try:
                if dialog.ShowModal() == wx.ID_NO:
                    event.Veto()
                    return
            finally:
                dialog.Destroy()

        event.Skip()


class Command(wx.Command):
    """Do nothing"""
    def Do(self) -> bool:
        return True
    def Undo(self) -> bool:
        return True


class MyApp(wx.App):
    def OnInit(self) -> bool:
        self.frame = MainFrame(None, -1, "Name and Address", name="frame")
        self.frame.Show()
        self.cmd_processor = wx.CommandProcessor()
        return True


if __name__ == "__main__":
    MyApp().MainLoop()
