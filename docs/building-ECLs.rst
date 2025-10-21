Building `call` Lists
=====================

"You said it was easy to build these ECLs. Okay, so how do we do it?"

Let's flesh out the rest of that example source code. Normally, all four of the `MainFrame`, `Command`, `MyApp`, and
main code would be in separate files, but I've lumped them together for expediency:

.. code-block:: python

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
            wx.GetApp().cmd_processor.Submit(Command(True))

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
        frame: MainFrame
        cmd_processor: wx.CommandProcessor

        def OnInit(self) -> bool:
            """Initialize the application"""
            self.frame = MainFrame(None, -1, "Name and Address", name="frame")
            self.frame.Show()
            self.cmd_processor = wx.CommandProcessor()
            return True


    if __name__ == "__main__":
        MyApp().MainLoop()

Please note how I've used the `name` attribute in this code. I've used `name` when the new object gets saved in a
`self.XXX` member and haven't when it wasn't. When I did, I always made the `name` match the member's name. This helps
mock_wx identify objects and will make it easier to copy ECLs into your code.

We want to test `MyFrame.on_close()`, but first, we'll need to copy the template and edit in the obvious bits:

.. code-block:: python

    """Test the MainFrame class"""

    from mock_wx.test_case import wxTestCase, note_func

    import logging
    from unittest.mock import call
    import wx

    from sample2 import MainFrame

    # Constants:
    LOG = logging.getLogger(__name__)


    class TestMainFrame(wxTestCase):
        def setUp(self):
            with self.create_dut():
                self.dut = MainFrame(None, name="dut")
            self.SETUP = [call()]

        def test_construct(self):
            """The setUp() function should instantiate the DUT"""
            self.check(self.SETUP)

        # @note_func("on_close")
        # def test_on_close(self) -> None:
        #     """Should display a confirmation dialog before losing any unsaved changes"""
        #     expect = self.SETUP
        #
        #     # No unsaved changes
        #     # Unsaved changes, the user clicks "No" on the dialog
        #     # Same but the user clicks "Yes"
        #
        #     self.check(expect)

I've commented out `test_on_close()` for now so we can focus on self.ecl. The ECL defaults to `call()` because we know
that's incorrect. Let's run the test as-is and look at the output:

.. code-block:: shell

    > python -m unittest test_sample2.py
    F
    ======================================================================
    FAIL: test_construct (test_sample2.TestMainFrame.test_construct)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\git\CallDiff\scratch\test_sample2.py", line 32, in test_construct
        self.check(self.ecl)
        ~~~~~~~~~~^^^^^^^^^^
      File "C:\git\CallDiff\src\mock_wx\_test_case.py", line 219, in check
        self.mock.assert_has_calls(expect)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^
      File "C:\Python313\Lib\unittest\mock.py", line 1014, in assert_has_calls
        raise AssertionError(
        ...<3 lines>...
        ) from cause
    AssertionError: Calls not found.
    Expected: [call()]
      Actual: [call.MainFrame(None, name='dut'),
     call.Point(10, 10),
     call.Button(self.dut, label='Submit', pos=self.Point.obj0, name='button1'),
     call.self.dut.button1.Bind({'EVT_BUTTON'}, <function MainFrame.on_submit at 0x000002130E412DE0>),
     call.Point(10, 50),
     call.Button(self.dut, label='Undo', pos=self.Point.obj1, name='button2'),
     call.self.dut.button2.Bind({'EVT_BUTTON'}, <function MainFrame.on_undo at 0x000002130E412E80>),
     call.Point(10, 90),
     call.Button(self.dut, label='Redo', pos=self.Point.obj2, name='button3'),
     call.self.dut.button3.Bind({'EVT_BUTTON'}, <function MainFrame.on_redo at 0x000002130E412F20>),
     call.self.dut.Bind({'EVT_CLOSE'}, <bound method MainFrame.on_close of self.dut>)]

    ----------------------------------------------------------------------
    Ran 1 test in 0.010s

    FAILED (failures=1)

And there it is, almost perfect, mock_wx is showing us the actual call list. There's only four bits that it couldn't
quite guess:
* `<function MainFrame.on_submit at 0x000002130E412DE0>` should have been `self.dut.on_submit`
* `<function MainFrame.on_undo at 0x000002130E412E80>` should have been `self.dut.on_undo`
* `<function MainFrame.on_redo at 0x000002130E412F20>` should have been `self.dut.on_redo`
* `<bound method MainFrame.on_close of self.dut>` should have been `self.dut.on_close`

Let's copy those actual calls into our ECL and fix the function names:

.. code-block:: python

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

Once again, note the I used the `name` attribute when creating the DUT. This won't always be possible, but we'll get the
best results when we can.

Now, the test should now pass.

.. code-block:: shell

    > python -m unittest test_sample2.py
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.010s

    OK

Let's fill in the fist part of our `test_on_close()` function as discussed earlier but without the "giving you the
answer" bit of me including the ECLs. Instead, we'll just use one `call()` like before:

.. code-block:: python

    @note_func("on_close")
    def test_on_close(self) -> None:
        """Should display a confirmation dialog before losing any unsaved changes"""
        ecl = self.ecl

        # No unsaved changes
        event = wx.CloseEvent(name="/event")
        ecl += [call()]
        event.CanVeto.return_value = True
        self.app.cmd_processor.IsDirty.return_value = False
        self.dut.on_close(event)
        ecl += [call()]

        # Unsaved changes, the user clicks "No" on the dialog
        # Same but the user clicks "Yes"

        self.check(ecl)

When we run the test this time, we'll see:

.. code-block:: shell

    > python -m unittest test_sample2.py
    .F
    ======================================================================
    FAIL: test_on_close (test_sample2.TestMainFrame.test_on_close)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\git\CallDiff\src\mock_wx\_test_case.py", line 261, in wrapper2
        return_value = func(*args2, **kwargs2)
      File "C:\git\CallDiff\scratch\test_sample2.py", line 109, in test_on_close
        self.check(ecl)
        ~~~~~~~~~~^^^^^
      File "C:\git\CallDiff\src\mock_wx\_test_case.py", line 219, in check
        self.mock.assert_has_calls(expect)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^
      File "C:\Python313\Lib\unittest\mock.py", line 1014, in assert_has_calls
        raise AssertionError(
        ...<3 lines>...
        ) from cause
    AssertionError: Calls not found.
    Expected: [call.MainFrame(None, name='dut'),
     call.Point(10, 10),
     call.Button(self.dut, label='Submit', pos=self.Point.obj0, name='button1'),
     call.self.dut.button1.Bind({'EVT_BUTTON'}, <function MainFrame.on_submit at 0x00000239D84DAFC0>),
     call.Point(10, 50),
     call.Button(self.dut, label='Undo', pos=self.Point.obj1, name='button2'),
     call.self.dut.button2.Bind({'EVT_BUTTON'}, <function MainFrame.on_undo at 0x00000239D84DB060>),
     call.Point(10, 90),
     call.Button(self.dut, label='Redo', pos=self.Point.obj2, name='button3'),
     call.self.dut.button3.Bind({'EVT_BUTTON'}, <function MainFrame.on_redo at 0x00000239D84DB100>),
     call.self.dut.Bind({'EVT_CLOSE'}, <bound method MainFrame.on_close of self.dut>),
     call(),
     call()]
      Actual: [call.MainFrame(None, name='dut'),
     call.Point(10, 10),
     call.Button(self.dut, label='Submit', pos=self.Point.obj0, name='button1'),
     call.self.dut.button1.Bind({'EVT_BUTTON'}, <function MainFrame.on_submit at 0x00000239D84DAFC0>),
     call.Point(10, 50),
     call.Button(self.dut, label='Undo', pos=self.Point.obj1, name='button2'),
     call.self.dut.button2.Bind({'EVT_BUTTON'}, <function MainFrame.on_undo at 0x00000239D84DB060>),
     call.Point(10, 90),
     call.Button(self.dut, label='Redo', pos=self.Point.obj2, name='button3'),
     call.self.dut.button3.Bind({'EVT_BUTTON'}, <function MainFrame.on_redo at 0x00000239D84DB100>),
     call.self.dut.Bind({'EVT_CLOSE'}, <bound method MainFrame.on_close of self.dut>),
     call.CloseEvent(name='/event'),
     call.self.on_close(event),
     call.event.CanVeto(),
     call.GetApp(),
     call.self.app.cmd_processor.IsDirty(),
     call.event.Skip()]

    ----------------------------------------------------------------------
    Ran 2 tests in 0.012s

    FAILED (failures=1)

The `test_constructor()` function is still passing, but the new `test_on_close()` doesn't. We can see the ECL had all
the calls from the constructor, and there's the two `call()` elements we added as placeholders. Below that is the actual
calls. This includes the constructor calls, a call to create the event, and calls that match what we'd expect when we
trace through the function by hand.

We don't even need to massage these calls. They already look exactly as we'd hope. So, let's paste them into their
appropriate slots:

.. code-block:: python

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
        # Same but the user clicks "Yes"

        self.check(ecl)

Once again, the tests pass:

.. code-block:: shell

    > python -m unittest test_sample2.py
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.010s

    OK

And that's 90% of mock_wx testing!
* Write the tests with `call()` placeholders in the ECLs.
* Run the test.
* Read and verify the actual calls to make sure the code is executing as you expect.
* Copy and edit the calls into your ECLs.
* Re-run the test to make sure it passes now.
* Proceed onto the next part of the test—lather, rinse, repeat.
