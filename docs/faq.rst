FAQ (Frequently Asked Questions)
================================

Q: Why is wxPython feature XXX not working?
-------------------------------------------

A: As you write tests, keep in mind that while using mock_wx, the wxPython classes are no longer wxPython classes. They
are merely mocks that follow the same sort of ancestry. For example:

.. code-block:: python

    point = wx.Point(10, 20)
    assert point.x == 10

``point.x`` should be equal to ``10``, right? Well, if this were wxPython, the sure, obviously it would, but the mock_wx
version of ``Point`` doesn't know anything about ``x`` and ``y``. It's just a mock object. If you want ``x`` to be
``10``, then you're going to have to set that in your test.

.. code-block:: python

    self.mock.Point.return_value.x = 10

Q: Why are these constants a set of strings? They're supposed to be integers!
-----------------------------------------------------------------------------

A: Yes, of course, but look again at the example test, above. Do you see where I instantiated that
``wx.MessageDialog()``?

.. code-block:: python

    dialog = wx.MessageDialog(
        self,
        _("You'll lose your unsaved changes if you quit now. Quit anyway?"),
        _("Unsaved Changes"),
        wx.ICON_WARNING | wx.YES_NO | wx.NO_DEFAULT,
    )

But in the ECL, that turned into:

.. code-block:: python

    call.MessageDialog(
        self.dut,
        "You'll lose your unsaved changes if you quit now. Quit anyway?",
        "Unsaved Changes",
        {"ICON_WARNING", "YES_NO", "NO_DEFAULT"},
    ),

If I'd just used integers like they are in wx.Python, the style would have been ``394``. Can you look at 394 and know
it's correct (``256 | 10 | 128``)? No, of course not. ``{"ICON_WARNING", "YES_NO", "NO_DEFAULT"}`` is infinitely more
clear, legible, and maintainable. Without this cheat, you'd have to put comments throughout your expectation lists to
explain what each constant meant.
