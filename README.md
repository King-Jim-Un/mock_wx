# What is mock_wx?

mock_wx is a framework for ledger testing that has been designed for wxPython applications.

# What is ledger testing?

Ledger testing is a new type of unit testing where each test assembles a list of steps that they expect the test
function to perform. Then, at the end of the test, the framework checks that ledger of the steps actually performed
against the provided list of expectations.

## A real-world analogy

Suppose you were the device under test (DUT) and one task you performed was going to the store to buy eggs. If we wanted
to write a test for this task and were using classical unit testing, we might write:

* Go to the store to buy eggs
* The test passes if there's eggs in the fridge

In ledger testing, we might write something like:

* Go to the store to buy eggs
* The test passes if you performed the following actions:
    * Drove to the store
    * Bought a dozen eggs
    * Drove home
    * Put the eggs in the fridge

Ledger testing worries less about return values and more about the steps taken to get there.

## Is that better than classical unit testing?

Maybe? Beats me, but I find this style of testing works particularly well with testing wxPython applications. Give it a
try, and let me know what you think!

## Will mock_wx test *only* wxPython applications?

No. You can use mock_wx to test other objects. You won't need to use a different framework to test compute-only portions
of your code, for example, objects that don't interact with the wxPython library.

# What is CallDiff?

CallDiff is a GUI tool for running tests and finding ledger errors. You don't have to use it as Python's built-in
unittest library will run mock_wx tests just fine, but it is handy when a larger ledger test fails, and it isn't obvious
why.

# Why do I need a specialized test package for testing wxPython applications?

That's a great question! Ideally, wxPython would have been written with testing in mind, but it wasn't, and it just
doesn't "play nicely" with unit tests. If we try writing classical unit tests on any code that interacts with the
wxPython library, we'll get an error that it isn't running, and if we try testing while it *is* running, well, that just
seems to make things worse.

Various frameworks have come out to try and tackle this problem. I've tried a few, and they just didn't work the way
that I wanted to test. That's why I made "yet another" wxPython testing framework. Hopefully, this will work better for
you as well.

# Example test:

Suppose you've bound a `wx.EVT_CLOSE` handler to your main frame that checks for any unsaved data before quitting. The
pertinent bits of code might look a bit like:

```python
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
```

To test the `on_close()` function, I like to start my with a comment for each execution path I see through the function:

```python
@note_func("on_close")
def test_on_close(self):
    """Should display a confirmation dialog before losing any unsaved changes"""
    expect = self.SETUP

    # No unsaved changes
    # Unsaved changes, the user clicks "No" on the dialog
    # Same but the user clicks "Yes"

    self.check(expect)
```

Yes, there's a little boilerplate code above and below the comments, but for the moment, let's ignore that and focus
only on the test.