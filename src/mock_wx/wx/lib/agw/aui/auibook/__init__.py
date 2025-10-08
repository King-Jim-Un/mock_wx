from wx.base_class import BaseClass
from wx import PyCommandEvent, Dialog, Window, Panel, Control
from wx.lib.expando import ExpandoTextCtrl
BOTTOM = {"BOTTOM"}
DefaultSize = {"DefaultSize"}
EVT_CHAR = {"EVT_CHAR"}
EVT_CHILD_FOCUS = {"EVT_CHILD_FOCUS"}
EVT_CLOSE = {"EVT_CLOSE"}
EVT_ENTER_WINDOW = {"EVT_ENTER_WINDOW"}
EVT_ERASE_BACKGROUND = {"EVT_ERASE_BACKGROUND"}
EVT_KEY_DOWN = {"EVT_KEY_DOWN"}
EVT_KEY_UP = {"EVT_KEY_UP"}
EVT_KILL_FOCUS = {"EVT_KILL_FOCUS"}
EVT_LEAVE_WINDOW = {"EVT_LEAVE_WINDOW"}
EVT_LEFT_DCLICK = {"EVT_LEFT_DCLICK"}
EVT_LEFT_DOWN = {"EVT_LEFT_DOWN"}
EVT_LEFT_UP = {"EVT_LEFT_UP"}
EVT_LISTBOX_DCLICK = {"EVT_LISTBOX_DCLICK"}
EVT_MIDDLE_DOWN = {"EVT_MIDDLE_DOWN"}
EVT_MIDDLE_UP = {"EVT_MIDDLE_UP"}
EVT_MOTION = {"EVT_MOTION"}
EVT_MOUSE_CAPTURE_LOST = {"EVT_MOUSE_CAPTURE_LOST"}
EVT_NAVIGATION_KEY = {"EVT_NAVIGATION_KEY"}
EVT_PAINT = {"EVT_PAINT"}
EVT_RIGHT_DOWN = {"EVT_RIGHT_DOWN"}
EVT_RIGHT_UP = {"EVT_RIGHT_UP"}
EVT_SET_FOCUS = {"EVT_SET_FOCUS"}
EVT_SIZE = {"EVT_SIZE"}
LEFT = {"LEFT"}
NOT_FOUND = {"NOT_FOUND"}
RIGHT = {"RIGHT"}
SIZE_ALLOW_MINUS_ONE = {"SIZE_ALLOW_MINUS_ONE"}
SIZE_AUTO = {"SIZE_AUTO"}
SIZE_AUTO_HEIGHT = {"SIZE_AUTO_HEIGHT"}
SIZE_AUTO_WIDTH = {"SIZE_AUTO_WIDTH"}
SIZE_FORCE = {"SIZE_FORCE"}
SIZE_USE_EXISTING = {"SIZE_USE_EXISTING"}
TOP = {"TOP"}
class AuiNotebook(Panel): ...
class AuiNotebookPage(BaseClass): ...
class AuiTabContainer(BaseClass): ...
class AuiTabContainerButton(BaseClass): ...
class AuiTabCtrl(Control, AuiTabContainer): ...
class CommandNotebookEvent(PyCommandEvent): ...
class AuiNotebookEvent(CommandNotebookEvent): ...
class TabFrame(Window): ...
class TabNavigatorProps(BaseClass):
    Font = {"Font"}
    Icon = {"Icon"}
    MinSize = {"MinSize"}
class TabNavigatorWindow(Dialog): ...
class TabTextCtrl(ExpandoTextCtrl): ...
