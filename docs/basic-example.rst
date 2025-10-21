Example Test:
=============

.. note:: As you may have guessed from the name, mock_wx leverages ``Mock`` objects from ``unittest.mock``. The
   following example—and indeed all of this documentation—presumes you are fluent in their use. If not, this would be an
   excellent time for a refresher! https://docs.python.org/3/library/unittest.mock.html

Suppose you've bound a ``wx.EVT_CLOSE`` handler to your main frame that checks for any unsaved data before quitting. The
pertinent bits of code might look a bit like:

.. code-block:: python

    import wx

    # Constants:
    _ = wx.GetTranslation


    class MainFrame(wx.Frame):
        def __init__(self, *args, **kwargs) -> None:
            """Constructor"""
            super().__init__(*args, **kwargs)
            ...
            self.Bind(wx.EVT_CLOSE, self.on_close)

        def on_close(self, event: wx.CloseEvent) -> None:
            """Handler for close events"""
            app = wx.GetApp()
            if event.CanVeto() and app.cmd_processor.IsDirty():
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

I like to start writing my tests with a comment or log message for each execution path I see through the function. To
test the ``on_close()`` function, I would write something like this:

.. code-block:: python

    @note_func("on_close")
    def test_on_close(self):
        """Should display a confirmation dialog before losing any unsaved changes"""
        ecl = self.ecl

        # No unsaved changes
        # Unsaved changes, the user clicks "No" on the dialog
        # Same but the user clicks "Yes"

        self.check(ecl)

Yes, there's a little boilerplate code above and below the comments, but for the moment, let's ignore that and focus
only on the test.

To test how the function behaves, we will first need an event to pass into it:

.. code-block:: python

    # No unsaved changes
    event = wx.CloseEvent(name="/event")

.. note::
   Events don't accept ``name`` parameters, right? Well, the events we create here—all wx objects technically—are more
   mock objects than ordinary wx objects. Without complaint, these objects will accept any parameters or members we
   specify.

Next, we want this mock object to return ``True`` if anyone calls its ``CanVeto()`` method:

.. code-block:: python

    event.CanVeto.return_value = True

Additionally, we want the application's command processor to return ``False`` when someone calls its ``IsDirty()``
method:

.. code-block:: python

    self.app.cmd_processor.IsDirty.return_value = False

The ``on_close()`` method has no return value, so we can just call it directly:

.. code-block:: python

    self.dut.on_close(event)

At this point, you might be thinking, "You're skipping too many steps! What does that '/event' name mean? What's that
``self.dut`` refer to?" And yes, yes, I realize you don't have all the information just yet. I want to show you the
shape of an example first. The specifics will be explained later on.

Finally, this portion of the test will need to add to the ECL. Note that creating the ``wx.CloseEvent`` will get
journaled just like everything else wx-related, so it sets some expectations too:

.. code-block:: python

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

Note how each entry added to the expectations follows what we expect the code to do. We call the ``on_close()``
function, we check ``CanVeto()``, we call ``wx.GetApp()``, we check ``IsDirty()``, and then we fall through with an
``event.skip()``.

If you're getting nervous about how you'll have to write ECL entries, then take a deep breath and relax. You won't have
to. This call list will actually be computer-generated. You'll only have to copy them, read them over and verify that
they're what you'd expect, and to do a little tweaking when they're imperfect. I promise!

The other two parts of this test are similar except that we also have to specify what ``ShowModal()`` will return:

.. code-block:: python

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

And that's what ledger testing looks like. You create one test file to test each file of source code. In them, you
create one test suite to test each class defined in your source code. And then you create one or more test functions to
test each method in your classes. The tests work through each of the execution paths in the code and keep a ledger of
what calls they will make.

Sound intriguing? Read on, and we'll discuss all the bits in detail.
