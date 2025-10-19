# What is mock_wx?

mock_wx is a framework for ledger testing that has been designed for wxPython applications.

# What is ledger testing?

Ledger testing is a new type of unit testing where each test assembles a list of steps that they expect the test
function to perform. Then, at the end of the test, the framework checks that ledger of the steps actually performed
against the provided list of expectations.

## A Real-world Analogy

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

# Example Test:

> ``📝`` Note: As you may have guessed from the name, mock_wx leverages `Mock` objects from `unittest.mock`. The
> following example—and indeed all of this documentation—presumes you are fluent in their use. If not, this would be an
> excellent time for a refresher! https://docs.python.org/3/library/unittest.mock.html

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

I like to start writing my tests with a comment or log message for each execution path I see through the function. To
test the `on_close()` function, I would write something like this:

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

To test how the function behaves, we will first need an event to pass into it:

```python
# No unsaved changes
event = wx.CloseEvent(name="/event")
```

> ``📝`` Note: Events don't accept `name` parameters, right? Well, the events we create here—all wx objects
> technically—are more mock objects than ordinary wx objects. Without complaint, these objects will accept any
> parameters or members we specify.

Next, we want this mock object to return `True` if anyone calls its `CanVeto()` method:

```python
event.CanVeto.return_value = True
```

Additionally, we want the application's command processor to return `False` when someone calls its `IsDirty()` method:

```python
self.app.cmd_processor.IsDirty.return_value = False
```

The `on_close()` method has no return value, so we can just call it directly:

```python
self.dut.on_close(event)
```

At this point, you might be thinking, "You're skipping too many steps! What does that '/event' name mean? What's that
`self.dut` refer to?" And yes, yes, I realize you don't have all the information just yet. I want to show you the shape
of an example first. The specifics will be explained later on.

Finally, this portion of the test will need to set some expectations. Note that creating the `wx.CloseEvent` will get
journaled just like everything else wx-related, so it sets some expectations too:

```python
# No unsaved changes
event = wx.CloseEvent(name="/event")
expect += [call.CloseEvent(name="/event")]
event.CanVeto.return_value = True
self.app.cmd_processor.IsDirty.return_value = False
self.dut.on_close(event)
expect += [
    call.self.on_close(event),
    call.event.CanVeto(),
    call.GetApp(),
    call.self.app.cmd_processor.IsDirty(),
    call.event.Skip(),
]
```

Note how each entry added to the expectations follows what we expect the code to do. We call the `on_close()` function,
we check `CanVeto()`, we call `wx.GetApp()`, we check `IsDirty()`, and then we fall through with an `event.skip()`.

If you're getting nervous about how you'll have to write all of these ledger entries, then take a deep breath and relax.
You won't have to. This call list will actually be computer-generated. You won't have to do it by hand. You'll only have
to copy them, read them over and verify that they're what you'd expect, and to do a little tweaking when they're not
perfect. I promise!

The other two parts of this test are similar except that we also have to specify what `ShowModal()` will return:

```python
# Unsaved changes, the user clicks "No" on the dialog
self.app.cmd_processor.IsDirty.return_value = True
self.mock.MessageDialog.return_value.ShowModal.return_value = wx.ID_NO
self.dut.on_close(event)
expect += [
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
expect += [
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
```

And that's what ledger testing looks like. You create one test file to test each file of source code. In them, you
create one test suite to test each class defined in your source code. And then you create one or more test functions to
test each method in your classes. The tests work through each of the execution paths in the code and keep a ledger of
what calls they will make.

Sound intriguing? Read on, and we'll discuss all the bits in detail.

# Installing mock_wx and CallDiff

- [ ] TODO

# The Major Players

Let's go through the major moving parts before we dive any deeper:

## Test Files

As you create your tests, you'll write one test file for each file of source code—the ones that have classes with member
functions, at least. If your source file is named `src/view/widget.py`, then you should name your test file
`test/view/test_widget.py`. I strongly recommend mirroring your source files with test files arranged in the same
directory structure, but your test filenames *must* fit the pattern `test_*.py`. Any other files will be skipped by the
test file scanner.

## `import mock_wx`

Each of your test files *must* `import` from mock_wx, even if they're not using it. This is important because the
mock_wx module patches the import paths to replace wx with its own mocked-up version. If anything from the actual wx
library gets imported before mock_wx does, then all the mock_wx tests will fail.

## `wxTestCase`

Inside your test files, create a test suite for each class in the source file that you wish to test. If you're writing
tests for `class Widget:`, then create a `class TestWidget(wxTestCase):` in your test file. The class name *must* start
with `Test`, and it *must* subclass `wxTestCase`.

## `def setUp(self):`

Typically, each test suite will include a `setUp()` function that instantiates a device under test or "DUT". If the
function exists, then the test runner will execute `setUp()` before each test in the suite is run, so each test starts
with a clean, freshly instantiated DUT. This function *must* be named `setUp()`—with the capital "U".

## `self.dut`

Every test operates on a DUT saved in `self.dut`. If you want different tests to instantiate the DUT with different
parameters, you should either:

* Instantiate `self.dut` in the tests themselves instead of in `setUp()`
* Use multiple test suites, each with their own `setUp()` that instantiates the DUT how you prefer

Either way, you'll still need to save the DUT in `self.dut`.

## `self.app`

Every wxPython application has an application object, and in a mock_wx test, that object is saved as `self.app`. This
object is instantiated for you.

If your test suite is testing the application object itself, both `self.dut` and `self.app` will point to the same
objects. This is discussed later in its own section.

## `self.SETUP`

Instantiating the DUT generally adds a few calls into the ledger. I like to store that list in `self.SETUP` so it's
available for use in each test.

## `with self.create_dut():`

The `with self.create_dut():` context is where you should create the DUT. This handles resetting the ledger and any 
necessary patching required.

## `def test_construct(self):`

If your `setUp()` function put any call instructions in `self.SETUP`, then you'll want to create a `test_construct()`
boilerplate function to test it.

## `@note_func(...)`

`note_func()` is a decorator that tells mock_wx to "take note" of calls to one of your functions—i.e. save a copy of the
call in the ledger.

> ``📝`` Note: There's no need to call `note_func()` on any of the wx functions. Calls to the wx functions will always
> be kept in the ledger. This is just for your own functions. Typically, you will use this decorator once on each test
> function, but you may also "note" any other functions that will be called—directly or indirectly—in the test. Contrast
> this with `@patch()`, described below.

## `expect = self.SETUP`

Each test starts by initializing an expectation list. This should get a copy of all the calls made when the DUT was
constructed.

## `expect += [...]`

After each call that adds more entries to the ledger, update your expectations by adding to it with the `+=` operator.
It's important that you don't use `.append()` as we want to create a copy of `self.SETUP`. We don't want any of the 
unit tests to modify the setup calls in-place.

## `self.mock`

`self.mock` is where mock_wx stores the ledger. You will also access `self.mock` to configure `return_value` and 
`side_effect` values.

> ``⚠️`` Warning: Be careful to reset all `side_effect` values to `None` after you're done. These will persist past
> the end of a unit test, and it's important that one test cannot change any other test's behavior. See the section on
> `side_effect` for details.
- [ ] TODO

## `self.check(expect)`

Each test should end with a call to `self.check(expect)`. This will compare your expectations against the ledger. Do not
forget this step! Your test is worthless if it doesn't actually verify the ledger.

## `@patch()`

The `patch()` decorator is very similar to the version in `unittest.mock` but retooled for use with mock_wx.

## `template.txt`

`template.txt` is a template you can copy whenever you create a new test. It gives you a good starting place and 
includes all these fiddly bits you won't want to forget.

# Building `call` Lists
- [ ] TODO
