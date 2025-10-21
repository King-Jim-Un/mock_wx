The Major Players
=================

Let's go through the major moving parts before we dive any deeper:

Test Files
----------

As you create your tests, you'll write one test file for each file of source code—the ones that have classes with member
functions, at least. If your source file is named ``src/view/widget.py``, then you should name your test file
``test/view/test_widget.py``. I strongly recommend mirroring your source files with test files arranged in the same
directory structure, but your test filenames *must* fit the pattern ``test_*.py``. Any other files will be skipped by the
test file scanner.

``import mock_wx``
------------------

Each of your test files *must* ``import`` from mock_wx, even if they're not using it. This is important because the
mock_wx module patches the import paths to replace wx with its own mocked-up version. If anything from the actual wx
library gets imported before mock_wx does, then all the mock_wx tests will fail.

``wxTestCase``
--------------

Inside your test files, create a test suite for each class in the source file that you wish to test. If you're writing
tests for ``class Widget:``, then create a ``class TestWidget(wxTestCase):`` in your test file. The class name *must* start
with ``Test``, and it *must* subclass ``wxTestCase``.

``def setUp(self):``
--------------------

Typically, each test suite will include a ``setUp()`` function that instantiates a device under test or "DUT". If the
function exists, then the test runner will execute ``setUp()`` before each test in the suite is run, so each test starts
with a clean, freshly instantiated DUT. This function *must* be named ``setUp()``—with the capital "U".

``self.dut``
------------

Every test operates on a DUT saved in ``self.dut``. If you want different tests to instantiate the DUT with different
parameters, you should either:

* Instantiate ``self.dut`` in the tests themselves instead of in ``setUp()``
* Use multiple test suites, each with their own ``setUp()`` that instantiates the DUT how you prefer

Either way, you'll still need to save the DUT in ``self.dut``.

``self.app``
------------

Every wxPython application has an application object, and in a mock_wx test, that object is saved as ``self.app``. This
object is instantiated for you.

If your test suite is testing the application object itself, both ``self.dut`` and ``self.app`` will point to the same
objects. This is discussed later in its own section.

``self.ecl``
------------

Instantiating the DUT generally adds a few calls into the ledger. I like to store those ECL entries in ``self.ecl`` so
it's available for use in each test.

``with self.create_dut():``
---------------------------

The ``with self.create_dut():`` context is where you should create the DUT. This handles resetting the ledger and any
necessary patching required.

``def test_construct(self):``
-----------------------------

If your ``setUp()`` function put any call instructions in ``self.ecl``, then you'll want to create a ``test_construct()``
boilerplate function to test it.

``@note_func(...)``
-------------------

``note_func()`` is a decorator that tells mock_wx to "take note" of calls to one of your functions—i.e. save a copy of the
call in the ledger.

..  note::
    There's no need to call ``note_func()`` on any of the wx functions. Calls to the wx functions will always
    be kept in the ledger. This is just for your own functions. Typically, you will use this decorator once on each test
    function, but you may also "note" any other functions that will be called—directly or indirectly—in the test. Contrast
    this with ``@patch()``, described below.

``expect = self.ecl``
---------------------

Each test starts by initializing the ECL. This should get a copy of all the calls made when the DUT was constructed.

``ecl += [...]``
----------------

After each call that adds more entries to the ledger, update your ECL by adding to it with the ``+=`` operator. It's
important that you don't use ``.append()`` as we want to create a copy of ``self.ecl``. We don't want any of the unit tests
to modify the ``self.ecl`` calls in-place.

``self.mock``
-------------

``self.mock`` is where mock_wx stores the ledger. You will also access ``self.mock`` to configure ``return_value`` and
``side_effect`` values.

..  warning::
    Be careful to reset all ``side_effect`` values to ``None`` after you're done. These will persist past
    the end of a unit test, and it's important that one test cannot change any other test's behavior. See the section on
    ``side_effect`` for details.

TODO

..  warning::
    When specifying ``return_value`` and ``side_effect`` values in ``self.mock``, always write ``.return_value``
    instead of ``()``. Although you could write:

    ``self.mock.MessageDialog().ShowModal.return_value = wx.ID_YES``

    instead of:

    ``self.mock.MessageDialog.return_value.ShowModal.return_value = wx.ID_YES``

    There is an important difference between the two. The prior example will create an unintentional entry in the ledger
    while the latter will not!

``self.check(ecl)``
-------------------

Each test should end with a call to ``self.check(ecl)``. This will compare your ECL against the ledger. Do not forget this
step! Your test is worthless if it doesn't actually verify the ledger.

``@patch()``
------------

The ``patch()`` decorator is very similar to the version in ``unittest.mock`` but retooled for use with mock_wx.

``template.txt``
----------------

``template.txt`` is a template you can copy whenever you create a new test. It gives you a good starting place and
includes all these fiddly bits you won't want to forget.
