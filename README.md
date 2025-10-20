# What is mock_wx?

mock_wx is a framework for ledger testing that has been designed for wxPython applications.

# What is ledger testing?

Ledger testing is a new type of unit testing where each test assembles a list of steps that they expect the test
function to perform. Then, at the end of the test, the framework checks that expectation call list or "ECL" against the
ledger of actual calls.

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
    ecl = self.ecl

    # No unsaved changes
    # Unsaved changes, the user clicks "No" on the dialog
    # Same but the user clicks "Yes"

    self.check(ecl)
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

Finally, this portion of the test will need to add to the ECL. Note that creating the `wx.CloseEvent` will get journaled
just like everything else wx-related, so it sets some expectations too:

```python
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
```

Note how each entry added to the expectations follows what we expect the code to do. We call the `on_close()` function,
we check `CanVeto()`, we call `wx.GetApp()`, we check `IsDirty()`, and then we fall through with an `event.skip()`.

If you're getting nervous about how you'll have to write ECL entries, then take a deep breath and relax. You won't have
to. This call list will actually be computer-generated. You'll only have to copy them, read them over and verify that
they're what you'd expect, and to do a little tweaking when they're imperfect. I promise!

The other two parts of this test are similar except that we also have to specify what `ShowModal()` will return:

```python
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
```

And that's what ledger testing looks like. You create one test file to test each file of source code. In them, you
create one test suite to test each class defined in your source code. And then you create one or more test functions to
test each method in your classes. The tests work through each of the execution paths in the code and keep a ledger of
what calls they will make.

Sound intriguing? Read on, and we'll discuss all the bits in detail.

# FAQ

## Q: Why is wxPython feature XXX not working?

A: As you write tests, keep in mind that while using mock_wx, the wxPython classes are no longer wxPython classes. They
are merely mocks that follow the same sort of ancestry. For example:

```python
point = wx.Point(10, 20)
assert point.x == 10
```

`point.x` should be equal to `10`, right? Well, if this were wxPython, the sure, obviously it would, but the mock_wx
version of `Point` doesn't know anything about `x` and `y`. It's just a mock object. If you want `x` to be `10`, then
you're going to have to set that in your test.

```python
self.mock.Point.return_value.x = 10
```

## Q: Why are these constants a set of strings? They're supposed to be integers!

A: Yes, of course, but look again at the example test, above. Do you see where I instantiated that `wx.MessageDialog()`?

```python
dialog = wx.MessageDialog(
    self,
    _("You'll lose your unsaved changes if you quit now. Quit anyway?"),
    _("Unsaved Changes"),
    wx.ICON_WARNING | wx.YES_NO | wx.NO_DEFAULT,
)
```

But in the ECL, that turned into:

```python
call.MessageDialog(
    self.dut,
    "You'll lose your unsaved changes if you quit now. Quit anyway?",
    "Unsaved Changes",
    {"ICON_WARNING", "YES_NO", "NO_DEFAULT"},
),
```

If I'd just used integers like they are in wx.Python, the style would have been `394`. Can you look at 394 and know
it's correct (`256 | 10 | 128`)? No, of course not. `{"ICON_WARNING", "YES_NO", "NO_DEFAULT"}` is infinitely more clear,
legible, and maintainable. Without this cheat, you'd have to put comments throughout your expectation lists to explain
what each constant meant.

# Contributing

As of this writing, we're still really early in the project's timeline. It seems to work, but what we need most is for
users to try writing tests with it on their own wxPython code. There are *so many* classes and members in wxPython, and
some of them have quirks that may need special coding to handle them.

When you find something you can't test, reduce the problem down to the simplest example you can and open a ticket. You
don't have to offer a solution, but unless I know about a problem, I can't hope to fix it.

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

## `self.ecl`

Instantiating the DUT generally adds a few calls into the ledger. I like to store those ECL entries in `self.ecl` so
it's available for use in each test.

## `with self.create_dut():`

The `with self.create_dut():` context is where you should create the DUT. This handles resetting the ledger and any
necessary patching required.

## `def test_construct(self):`

If your `setUp()` function put any call instructions in `self.ecl`, then you'll want to create a `test_construct()`
boilerplate function to test it.

## `@note_func(...)`

`note_func()` is a decorator that tells mock_wx to "take note" of calls to one of your functions—i.e. save a copy of the
call in the ledger.

> ``📝`` Note: There's no need to call `note_func()` on any of the wx functions. Calls to the wx functions will always
> be kept in the ledger. This is just for your own functions. Typically, you will use this decorator once on each test
> function, but you may also "note" any other functions that will be called—directly or indirectly—in the test. Contrast
> this with `@patch()`, described below.

## `expect = self.ecl`

Each test starts by initializing the ECL. This should get a copy of all the calls made when the DUT was constructed.

## `ecl += [...]`

After each call that adds more entries to the ledger, update your ECL by adding to it with the `+=` operator. It's
important that you don't use `.append()` as we want to create a copy of `self.ecl`. We don't want any of the unit tests
to modify the `self.ecl` calls in-place.

## `self.mock`

`self.mock` is where mock_wx stores the ledger. You will also access `self.mock` to configure `return_value` and
`side_effect` values.

> ``⚠️`` Warning: Be careful to reset all `side_effect` values to `None` after you're done. These will persist past
> the end of a unit test, and it's important that one test cannot change any other test's behavior. See the section on
> `side_effect` for details.

- [ ] TODO

> ``⚠️`` Warning: When specifying `return_value` and `side_effect` values in `self.mock`, always write `.return_value`
> instead of `()`. Although you could write:
>
> `self.mock.MessageDialog().ShowModal.return_value = wx.ID_YES`
>
> instead of:
>
> `self.mock.MessageDialog.return_value.ShowModal.return_value = wx.ID_YES`
>
> There is an important difference between the two. The prior example will create an unintentional entry in the ledger
> while the latter will not!

## `self.check(ecl)`

Each test should end with a call to `self.check(ecl)`. This will compare your ECL against the ledger. Do not forget this
step! Your test is worthless if it doesn't actually verify the ledger.

## `@patch()`

The `patch()` decorator is very similar to the version in `unittest.mock` but retooled for use with mock_wx.

## `template.txt`

`template.txt` is a template you can copy whenever you create a new test. It gives you a good starting place and
includes all these fiddly bits you won't want to forget.

# Building `call` Lists

"You said it was easy to build these ECLs. Okay, so how do we do it?"

Let's flesh out the rest of that example source code. Normally, all four of the `MainFrame`, `Command`, `MyApp`, and
main code would be in separate files, but I've lumped them together for expediency:

```python
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
```

Please note how I've used the `name` attribute in this code. I've used `name` when the new object gets saved in a 
`self.XXX` member and haven't when it wasn't. When I did, I always made the `name` match the member's name. This helps
mock_wx identify objects and will make it easier to copy ECLs into your code.

We want to test `MyFrame.on_close()`, but first, we'll need to copy the template and edit in the obvious bits:

```python
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
```

I've commented out `test_on_close()` for now so we can focus on self.ecl. The ECL defaults to `call()` because we know
that's incorrect. Let's run the test as-is and look at the output:

```commandline
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
```

And there it is, almost perfect, mock_wx is showing us the actual call list. There's only four bits that it couldn't
quite guess:
* `<function MainFrame.on_submit at 0x000002130E412DE0>` should have been `self.dut.on_submit`
* `<function MainFrame.on_undo at 0x000002130E412E80>` should have been `self.dut.on_undo`
* `<function MainFrame.on_redo at 0x000002130E412F20>` should have been `self.dut.on_redo`
* `<bound method MainFrame.on_close of self.dut>` should have been `self.dut.on_close`

Let's copy those actual calls into our ECL and fix the function names:

```python
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
```

Once again, note the I used the `name` attribute when creating the DUT. This won't always be possible, but we'll get the
best results when we can.

Now, the test should now pass.

```commandline
> python -m unittest test_sample2.py
.
----------------------------------------------------------------------
Ran 1 test in 0.010s

OK
```

Let's fill in the fist part of our `test_on_close()` function as discussed earlier but without the "giving you the 
answer" bit of me including the ECLs. Instead, we'll just use one `call()` like before:

```python
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
```

When we run the test this time, we'll see:

```commandline
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
```

The `test_constructor()` function is still passing, but the new `test_on_close()` doesn't. We can see the ECL had all
the calls from the constructor, and there's the two `call()` elements we added as placeholders. Below that is the actual
calls. This includes the constructor calls, a call to create the event, and calls that match what we'd expect when we
trace through the function by hand.

We don't even need to massage these calls. They already look exactly as we'd hope. So, let's paste them into their
appropriate slots:

```python
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
```

Once again, the tests pass:

```commandline
> python -m unittest test_sample2.py
..
----------------------------------------------------------------------
Ran 2 tests in 0.010s

OK
```

And that's 90% of mock_wx testing!
* Write the tests with `call()` placeholders in the ECLs.
* Run the test.
* Read and verify the actual calls to make sure the code is executing as you expect.
* Copy and edit the calls into your ECLs.
* Re-run the test to make sure it passes now.
* Proceed onto the next part of the test—lather, rinse, repeat.
