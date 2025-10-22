from wx import Frame, BookCtrlEvent, EvtHandler, Event, NotifyEvent, Control, Panel, BookCtrlBase
from mock_wx.test_case import BaseClass
AUI_MGR_ALLOW_ACTIVE_PANE = {"AUI_MGR_ALLOW_ACTIVE_PANE"}
AUI_MGR_ALLOW_FLOATING = {"AUI_MGR_ALLOW_FLOATING"}
AUI_MGR_DEFAULT = {"AUI_MGR_DEFAULT"}
AUI_MGR_HINT_FADE = {"AUI_MGR_HINT_FADE"}
AUI_MGR_LIVE_RESIZE = {"AUI_MGR_LIVE_RESIZE"}
AUI_MGR_NO_VENETIAN_BLINDS_FADE = {"AUI_MGR_NO_VENETIAN_BLINDS_FADE"}
AUI_MGR_RECTANGLE_HINT = {"AUI_MGR_RECTANGLE_HINT"}
AUI_MGR_TRANSPARENT_DRAG = {"AUI_MGR_TRANSPARENT_DRAG"}
AUI_MGR_TRANSPARENT_HINT = {"AUI_MGR_TRANSPARENT_HINT"}
AUI_MGR_VENETIAN_BLINDS_HINT = {"AUI_MGR_VENETIAN_BLINDS_HINT"}
AUI_NB_BOTTOM = {"AUI_NB_BOTTOM"}
AUI_NB_CLOSE_BUTTON = {"AUI_NB_CLOSE_BUTTON"}
AUI_NB_CLOSE_ON_ACTIVE_TAB = {"AUI_NB_CLOSE_ON_ACTIVE_TAB"}
AUI_NB_CLOSE_ON_ALL_TABS = {"AUI_NB_CLOSE_ON_ALL_TABS"}
AUI_NB_DEFAULT_STYLE = {"AUI_NB_DEFAULT_STYLE"}
AUI_NB_MIDDLE_CLICK_CLOSE = {"AUI_NB_MIDDLE_CLICK_CLOSE"}
AUI_NB_SCROLL_BUTTONS = {"AUI_NB_SCROLL_BUTTONS"}
AUI_NB_TAB_EXTERNAL_MOVE = {"AUI_NB_TAB_EXTERNAL_MOVE"}
AUI_NB_TAB_FIXED_WIDTH = {"AUI_NB_TAB_FIXED_WIDTH"}
AUI_NB_TAB_MOVE = {"AUI_NB_TAB_MOVE"}
AUI_NB_TAB_SPLIT = {"AUI_NB_TAB_SPLIT"}
AUI_NB_TOP = {"AUI_NB_TOP"}
AUI_NB_WINDOWLIST_BUTTON = {"AUI_NB_WINDOWLIST_BUTTON"}
AUI_TB_DEFAULT_STYLE = {"AUI_TB_DEFAULT_STYLE"}
AUI_TB_GRIPPER = {"AUI_TB_GRIPPER"}
AUI_TB_HORIZONTAL = {"AUI_TB_HORIZONTAL"}
AUI_TB_HORZ_LAYOUT = {"AUI_TB_HORZ_LAYOUT"}
AUI_TB_HORZ_TEXT = {"AUI_TB_HORZ_TEXT"}
AUI_TB_NO_AUTORESIZE = {"AUI_TB_NO_AUTORESIZE"}
AUI_TB_NO_TOOLTIPS = {"AUI_TB_NO_TOOLTIPS"}
AUI_TB_OVERFLOW = {"AUI_TB_OVERFLOW"}
AUI_TB_PLAIN_BACKGROUND = {"AUI_TB_PLAIN_BACKGROUND"}
AUI_TB_TEXT = {"AUI_TB_TEXT"}
AUI_TB_VERTICAL = {"AUI_TB_VERTICAL"}
AuiManagerOption = {"AuiManagerOption"}
AuiPaneInfoArray = {"AuiPaneInfoArray"}
BOTTOM = {"BOTTOM"}
EVT_AUINOTEBOOK_ALLOW_DND = {"EVT_AUINOTEBOOK_ALLOW_DND"}
EVT_AUINOTEBOOK_BEGIN_DRAG = {"EVT_AUINOTEBOOK_BEGIN_DRAG"}
EVT_AUINOTEBOOK_BG_DCLICK = {"EVT_AUINOTEBOOK_BG_DCLICK"}
EVT_AUINOTEBOOK_BUTTON = {"EVT_AUINOTEBOOK_BUTTON"}
EVT_AUINOTEBOOK_DRAG_DONE = {"EVT_AUINOTEBOOK_DRAG_DONE"}
EVT_AUINOTEBOOK_DRAG_MOTION = {"EVT_AUINOTEBOOK_DRAG_MOTION"}
EVT_AUINOTEBOOK_END_DRAG = {"EVT_AUINOTEBOOK_END_DRAG"}
EVT_AUINOTEBOOK_PAGE_CHANGED = {"EVT_AUINOTEBOOK_PAGE_CHANGED"}
EVT_AUINOTEBOOK_PAGE_CHANGING = {"EVT_AUINOTEBOOK_PAGE_CHANGING"}
EVT_AUINOTEBOOK_PAGE_CLOSE = {"EVT_AUINOTEBOOK_PAGE_CLOSE"}
EVT_AUINOTEBOOK_PAGE_CLOSED = {"EVT_AUINOTEBOOK_PAGE_CLOSED"}
EVT_AUINOTEBOOK_TAB_MIDDLE_DOWN = {"EVT_AUINOTEBOOK_TAB_MIDDLE_DOWN"}
EVT_AUINOTEBOOK_TAB_MIDDLE_UP = {"EVT_AUINOTEBOOK_TAB_MIDDLE_UP"}
EVT_AUINOTEBOOK_TAB_RIGHT_DOWN = {"EVT_AUINOTEBOOK_TAB_RIGHT_DOWN"}
EVT_AUINOTEBOOK_TAB_RIGHT_UP = {"EVT_AUINOTEBOOK_TAB_RIGHT_UP"}
EVT_AUITOOLBAR_BEGIN_DRAG = {"EVT_AUITOOLBAR_BEGIN_DRAG"}
EVT_AUITOOLBAR_MIDDLE_CLICK = {"EVT_AUITOOLBAR_MIDDLE_CLICK"}
EVT_AUITOOLBAR_OVERFLOW_CLICK = {"EVT_AUITOOLBAR_OVERFLOW_CLICK"}
EVT_AUITOOLBAR_RIGHT_CLICK = {"EVT_AUITOOLBAR_RIGHT_CLICK"}
EVT_AUITOOLBAR_TOOL_DROPDOWN = {"EVT_AUITOOLBAR_TOOL_DROPDOWN"}
EVT_AUI_PANE_ACTIVATED = {"EVT_AUI_PANE_ACTIVATED"}
EVT_AUI_PANE_BUTTON = {"EVT_AUI_PANE_BUTTON"}
EVT_AUI_PANE_CLOSE = {"EVT_AUI_PANE_CLOSE"}
EVT_AUI_PANE_MAXIMIZE = {"EVT_AUI_PANE_MAXIMIZE"}
EVT_AUI_PANE_RESTORE = {"EVT_AUI_PANE_RESTORE"}
EVT_AUI_RENDER = {"EVT_AUI_RENDER"}
ITEM_NORMAL = {"ITEM_NORMAL"}
LEFT = {"LEFT"}
NOT_FOUND = {"NOT_FOUND"}
RIGHT = {"RIGHT"}
TOP = {"TOP"}
class AuiDockArt(BaseClass): ...
class AuiDefaultDockArt(AuiDockArt): ...
class AuiFloatingFrame(Frame):
    AuiManager = {"AuiManager"}
    OwnerManager = {"OwnerManager"}
class AuiMDIChildFrame(Panel):
    Icon = {"Icon"}
    Icons = {"Icons"}
    MDIParentFrame = {"MDIParentFrame"}
    MenuBar = {"MenuBar"}
    StatusBar = {"StatusBar"}
    Title = {"Title"}
    ToolBar = {"ToolBar"}
class AuiMDIParentFrame(Frame):
    ActiveChild = {"ActiveChild"}
    ArtProvider = {"ArtProvider"}
    ClientWindow = {"ClientWindow"}
    Notebook = {"Notebook"}
    WindowMenu = {"WindowMenu"}
class AuiManager(EvtHandler):
    AllPanes = {"AllPanes"}
    ArtProvider = {"ArtProvider"}
    Flags = {"Flags"}
    ManagedWindow = {"ManagedWindow"}
class AuiManagerEvent(Event):
    Button = {"Button"}
    DC = {"DC"}
    Manager = {"Manager"}
    Pane = {"Pane"}
class AuiNotebook(BookCtrlBase):
    ActiveTabCtrl = {"ActiveTabCtrl"}
    ArtProvider = {"ArtProvider"}
    CurrentPage = {"CurrentPage"}
    PageCount = {"PageCount"}
    Selection = {"Selection"}
    TabCtrlHeight = {"TabCtrlHeight"}
class AuiMDIClientWindow(AuiNotebook):
    ActiveChild = {"ActiveChild"}
class AuiNotebookEvent(BookCtrlEvent): ...
class AuiNotebookPage(BaseClass):
    active = {"active"}
    bitmap = {"bitmap"}
    caption = {"caption"}
    rect = {"rect"}
    tooltip = {"tooltip"}
    window = {"window"}
class AuiPaneInfo(BaseClass):
    best_size = {"best_size"}
    caption = {"caption"}
    dock_direction = {"dock_direction"}
    dock_layer = {"dock_layer"}
    dock_pos = {"dock_pos"}
    dock_proportion = {"dock_proportion"}
    dock_row = {"dock_row"}
    floating_pos = {"floating_pos"}
    floating_size = {"floating_size"}
    frame = {"frame"}
    icon = {"icon"}
    max_size = {"max_size"}
    min_size = {"min_size"}
    name = {"name"}
    rect = {"rect"}
    state = {"state"}
    window = {"window"}
class AuiTabArt(BaseClass):
    IndentSize = {"IndentSize"}
class AuiDefaultTabArt(AuiTabArt):
    IndentSize = {"IndentSize"}
class AuiSimpleTabArt(AuiTabArt):
    IndentSize = {"IndentSize"}
class AuiTabCtrl(BaseClass): ...
class AuiToolBar(Control):
    ArtProvider = {"ArtProvider"}
    GripperVisible = {"GripperVisible"}
    OverflowVisible = {"OverflowVisible"}
    ToolBarFits = {"ToolBarFits"}
    ToolBitmapSize = {"ToolBitmapSize"}
    ToolBorderPadding = {"ToolBorderPadding"}
    ToolCount = {"ToolCount"}
    ToolPacking = {"ToolPacking"}
    ToolSeparation = {"ToolSeparation"}
    ToolTextOrientation = {"ToolTextOrientation"}
    WindowStyleFlag = {"WindowStyleFlag"}
class AuiToolBarArt(BaseClass):
    Flags = {"Flags"}
    Font = {"Font"}
    TextOrientation = {"TextOrientation"}
class AuiDefaultToolBarArt(AuiToolBarArt):
    Flags = {"Flags"}
    Font = {"Font"}
    TextOrientation = {"TextOrientation"}
class AuiToolBarEvent(NotifyEvent):
    ClickPoint = {"ClickPoint"}
    ItemRect = {"ItemRect"}
    ToolId = {"ToolId"}
class AuiToolBarItem(BaseClass):
    Alignment = {"Alignment"}
    Bitmap = {"Bitmap"}
    DisabledBitmap = {"DisabledBitmap"}
    HoverBitmap = {"HoverBitmap"}
    Id = {"Id"}
    Kind = {"Kind"}
    Label = {"Label"}
    LongHelp = {"LongHelp"}
    MinSize = {"MinSize"}
    Proportion = {"Proportion"}
    ShortHelp = {"ShortHelp"}
    SizerItem = {"SizerItem"}
    SpacerPixels = {"SpacerPixels"}
    State = {"State"}
    UserData = {"UserData"}
    Window = {"Window"}
