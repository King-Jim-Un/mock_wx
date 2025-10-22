from wx import ItemContainer, CommandEvent, Object, Frame, Window, HelpControllerBase, Dialog, Printout, Scrolled, VListBox
from mock_wx.test_case import BaseClass
BORDER_SUNKEN = {"BORDER_SUNKEN"}
EVT_HTML_CELL_CLICKED = {"EVT_HTML_CELL_CLICKED"}
EVT_HTML_CELL_HOVER = {"EVT_HTML_CELL_HOVER"}
EVT_HTML_LINK_CLICKED = {"EVT_HTML_LINK_CLICKED"}
EVT_LISTBOX = {"EVT_LISTBOX"}
EVT_LISTBOX_DCLICK = {"EVT_LISTBOX_DCLICK"}
HF_BOOKMARKS = {"HF_BOOKMARKS"}
HF_CONTENTS = {"HF_CONTENTS"}
HF_DEFAULT_STYLE = {"HF_DEFAULT_STYLE"}
HF_DIALOG = {"HF_DIALOG"}
HF_EMBEDDED = {"HF_EMBEDDED"}
HF_FLAT_TOOLBAR = {"HF_FLAT_TOOLBAR"}
HF_FRAME = {"HF_FRAME"}
HF_ICONS_BOOK = {"HF_ICONS_BOOK"}
HF_ICONS_BOOK_CHAPTER = {"HF_ICONS_BOOK_CHAPTER"}
HF_ICONS_FOLDER = {"HF_ICONS_FOLDER"}
HF_INDEX = {"HF_INDEX"}
HF_MERGE_BOOKS = {"HF_MERGE_BOOKS"}
HF_MODAL = {"HF_MODAL"}
HF_OPEN_FILES = {"HF_OPEN_FILES"}
HF_PRINT = {"HF_PRINT"}
HF_SEARCH = {"HF_SEARCH"}
HF_TOOLBAR = {"HF_TOOLBAR"}
HLB_DEFAULT_STYLE = {"HLB_DEFAULT_STYLE"}
HLB_MULTIPLE = {"HLB_MULTIPLE"}
HTMLCursor = {"HTMLCursor"}
HTML_ALIGN_BOTTOM = {"HTML_ALIGN_BOTTOM"}
HTML_ALIGN_CENTER = {"HTML_ALIGN_CENTER"}
HTML_ALIGN_JUSTIFY = {"HTML_ALIGN_JUSTIFY"}
HTML_ALIGN_LEFT = {"HTML_ALIGN_LEFT"}
HTML_ALIGN_RIGHT = {"HTML_ALIGN_RIGHT"}
HTML_ALIGN_TOP = {"HTML_ALIGN_TOP"}
HTML_BLOCK = {"HTML_BLOCK"}
HTML_CLR_BACKGROUND = {"HTML_CLR_BACKGROUND"}
HTML_CLR_FOREGROUND = {"HTML_CLR_FOREGROUND"}
HTML_COND_ISANCHOR = {"HTML_COND_ISANCHOR"}
HTML_INDENT_ALL = {"HTML_INDENT_ALL"}
HTML_INDENT_BOTTOM = {"HTML_INDENT_BOTTOM"}
HTML_INDENT_HORIZONTAL = {"HTML_INDENT_HORIZONTAL"}
HTML_INDENT_LEFT = {"HTML_INDENT_LEFT"}
HTML_INDENT_RIGHT = {"HTML_INDENT_RIGHT"}
HTML_INDENT_TOP = {"HTML_INDENT_TOP"}
HTML_INDENT_VERTICAL = {"HTML_INDENT_VERTICAL"}
HTML_OPEN = {"HTML_OPEN"}
HTML_REDIRECT = {"HTML_REDIRECT"}
HTML_SEL_CHANGING = {"HTML_SEL_CHANGING"}
HTML_SEL_IN = {"HTML_SEL_IN"}
HTML_SEL_OUT = {"HTML_SEL_OUT"}
HTML_UNITS_PERCENT = {"HTML_UNITS_PERCENT"}
HTML_UNITS_PIXELS = {"HTML_UNITS_PIXELS"}
HTML_URL_IMAGE = {"HTML_URL_IMAGE"}
HTML_URL_OTHER = {"HTML_URL_OTHER"}
HTML_URL_PAGE = {"HTML_URL_PAGE"}
HW_NO_SELECTION = {"HW_NO_SELECTION"}
HW_SCROLLBAR_AUTO = {"HW_SCROLLBAR_AUTO"}
HW_SCROLLBAR_NEVER = {"HW_SCROLLBAR_NEVER"}
HtmlBookRecArray = {"HtmlBookRecArray"}
HtmlHelpDataItems = {"HtmlHelpDataItems"}
HtmlOpeningStatus = {"HtmlOpeningStatus"}
HtmlSelectionState = {"HtmlSelectionState"}
HtmlURLType = {"HtmlURLType"}
OR = {"OR"}
PAGE_ALL = {"PAGE_ALL"}
PAGE_EVEN = {"PAGE_EVEN"}
PAGE_ODD = {"PAGE_ODD"}
PromptMode = {"PromptMode"}
class HtmlBookRecord(BaseClass):
    BasePath = {"BasePath"}
    BookFile = {"BookFile"}
    ContentsEnd = {"ContentsEnd"}
    ContentsStart = {"ContentsStart"}
    Start = {"Start"}
    Title = {"Title"}
class HtmlCell(Object):
    AbsPos = {"AbsPos"}
    Descent = {"Descent"}
    FirstChild = {"FirstChild"}
    Height = {"Height"}
    Id = {"Id"}
    Link = {"Link"}
    Next = {"Next"}
    Parent = {"Parent"}
    PosX = {"PosX"}
    PosY = {"PosY"}
    RootCell = {"RootCell"}
    Width = {"Width"}
class HtmlCellEvent(CommandEvent):
    Cell = {"Cell"}
    LinkClicked = {"LinkClicked"}
    MouseEvent = {"MouseEvent"}
    Point = {"Point"}
class HtmlColourCell(HtmlCell): ...
class HtmlContainerCell(HtmlCell):
    AlignHor = {"AlignHor"}
    AlignVer = {"AlignVer"}
    BackgroundColour = {"BackgroundColour"}
class HtmlDCRenderer(Object):
    TotalHeight = {"TotalHeight"}
    TotalWidth = {"TotalWidth"}
class HtmlEasyPrinting(Object):
    Name = {"Name"}
    PageSetupData = {"PageSetupData"}
    ParentWindow = {"ParentWindow"}
    PrintData = {"PrintData"}
class HtmlFilter(Object): ...
class HtmlFontCell(HtmlCell): ...
class HtmlHelpController(HelpControllerBase):
    Dialog = {"Dialog"}
    Frame = {"Frame"}
    HelpWindow = {"HelpWindow"}
class HtmlHelpData(Object):
    BookRecArray = {"BookRecArray"}
    ContentsArray = {"ContentsArray"}
    IndexArray = {"IndexArray"}
class HtmlHelpDataItem(BaseClass):
    FullPath = {"FullPath"}
    IndentedName = {"IndentedName"}
    book = {"book"}
    id = {"id"}
    level = {"level"}
    name = {"name"}
    page = {"page"}
    parent = {"parent"}
class HtmlHelpDialog(Dialog):
    Controller = {"Controller"}
class HtmlHelpFrame(Frame):
    Controller = {"Controller"}
class HtmlHelpWindow(Window):
    Controller = {"Controller"}
    Data = {"Data"}
class HtmlLinkEvent(CommandEvent):
    LinkInfo = {"LinkInfo"}
class HtmlLinkInfo(Object):
    Event = {"Event"}
    Href = {"Href"}
    HtmlCell = {"HtmlCell"}
    Target = {"Target"}
class HtmlListBox(VListBox):
    FileSystem = {"FileSystem"}
class HtmlModalHelp(BaseClass): ...
class HtmlParser(BaseClass):
    FS = {"FS"}
    Product = {"Product"}
    Source = {"Source"}
class HtmlPrintout(Printout): ...
class HtmlRenderingInfo(BaseClass):
    Selection = {"Selection"}
    State = {"State"}
    Style = {"Style"}
class HtmlRenderingState(BaseClass):
    BgColour = {"BgColour"}
    BgMode = {"BgMode"}
    FgColour = {"FgColour"}
    SelectionState = {"SelectionState"}
class HtmlRenderingStyle(BaseClass): ...
class HtmlSelection(BaseClass):
    FromCell = {"FromCell"}
    FromCharacterPos = {"FromCharacterPos"}
    FromPos = {"FromPos"}
    ToCell = {"ToCell"}
    ToCharacterPos = {"ToCharacterPos"}
    ToPos = {"ToPos"}
class HtmlTag(BaseClass):
    AllParams = {"AllParams"}
    Name = {"Name"}
class HtmlTagHandler(Object):
    Parser = {"Parser"}
    SupportedTags = {"SupportedTags"}
class HtmlWidgetCell(HtmlCell): ...
class HtmlWinParser(HtmlParser):
    ActualColor = {"ActualColor"}
    Align = {"Align"}
    CharHeight = {"CharHeight"}
    CharWidth = {"CharWidth"}
    Container = {"Container"}
    DC = {"DC"}
    FontBold = {"FontBold"}
    FontFace = {"FontFace"}
    FontFixed = {"FontFixed"}
    FontItalic = {"FontItalic"}
    FontSize = {"FontSize"}
    FontUnderlined = {"FontUnderlined"}
    Link = {"Link"}
    LinkColor = {"LinkColor"}
    WindowInterface = {"WindowInterface"}
class HtmlWinTagHandler(HtmlTagHandler):
    Parser = {"Parser"}
class HtmlWindowInterface(BaseClass):
    HTMLBackgroundColour = {"HTMLBackgroundColour"}
    HTMLWindow = {"HTMLWindow"}
class HtmlWindow(Scrolled, HtmlWindowInterface):
    InternalRepresentation = {"InternalRepresentation"}
    OpenedAnchor = {"OpenedAnchor"}
    OpenedPage = {"OpenedPage"}
    OpenedPageTitle = {"OpenedPageTitle"}
    Parser = {"Parser"}
    RelatedFrame = {"RelatedFrame"}
class HtmlWordCell(HtmlCell): ...
class HtmlWordWithTabsCell(HtmlWordCell): ...
class SimpleHtmlListBox(HtmlListBox, ItemContainer): ...
