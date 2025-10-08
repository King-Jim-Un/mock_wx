from wx.base_class import BaseClass
from wx import NotifyEvent, Window, RefCounter, Object, SettableHeaderColumn, Control
CHK_CHECKED = {"CHK_CHECKED"}
CHK_UNCHECKED = {"CHK_UNCHECKED"}
CHK_UNDETERMINED = {"CHK_UNDETERMINED"}
COL_RESIZABLE = {"COL_RESIZABLE"}
COL_SORTABLE = {"COL_SORTABLE"}
COL_WIDTH_AUTOSIZE = {"COL_WIDTH_AUTOSIZE"}
DATAVIEW_CELL_ACTIVATABLE = {"DATAVIEW_CELL_ACTIVATABLE"}
DATAVIEW_CELL_EDITABLE = {"DATAVIEW_CELL_EDITABLE"}
DATAVIEW_CELL_FOCUSED = {"DATAVIEW_CELL_FOCUSED"}
DATAVIEW_CELL_INERT = {"DATAVIEW_CELL_INERT"}
DATAVIEW_CELL_INSENSITIVE = {"DATAVIEW_CELL_INSENSITIVE"}
DATAVIEW_CELL_PRELIT = {"DATAVIEW_CELL_PRELIT"}
DATAVIEW_CELL_SELECTED = {"DATAVIEW_CELL_SELECTED"}
DATAVIEW_COL_HIDDEN = {"DATAVIEW_COL_HIDDEN"}
DATAVIEW_COL_REORDERABLE = {"DATAVIEW_COL_REORDERABLE"}
DATAVIEW_COL_RESIZABLE = {"DATAVIEW_COL_RESIZABLE"}
DATAVIEW_COL_SORTABLE = {"DATAVIEW_COL_SORTABLE"}
DF_INVALID = {"DF_INVALID"}
DVCVariant = {"DVCVariant"}
DV_HORIZ_RULES = {"DV_HORIZ_RULES"}
DV_MULTIPLE = {"DV_MULTIPLE"}
DV_NO_HEADER = {"DV_NO_HEADER"}
DV_ROW_LINES = {"DV_ROW_LINES"}
DV_SINGLE = {"DV_SINGLE"}
DV_VARIABLE_LINE_HEIGHT = {"DV_VARIABLE_LINE_HEIGHT"}
DV_VERT_RULES = {"DV_VERT_RULES"}
DataViewCellMode = {"DataViewCellMode"}
DataViewCellRenderState = {"DataViewCellRenderState"}
DataViewColumnFlags = {"DataViewColumnFlags"}
DataViewItemArray = {"DataViewItemArray"}
ELLIPSIZE_MIDDLE = {"ELLIPSIZE_MIDDLE"}
ELLIPSIZE_NONE = {"ELLIPSIZE_NONE"}
EVT_DATAVIEW_CACHE_HINT = {"EVT_DATAVIEW_CACHE_HINT"}
EVT_DATAVIEW_COLUMN_HEADER_CLICK = {"EVT_DATAVIEW_COLUMN_HEADER_CLICK"}
EVT_DATAVIEW_COLUMN_HEADER_RIGHT_CLICK = {"EVT_DATAVIEW_COLUMN_HEADER_RIGHT_CLICK"}
EVT_DATAVIEW_COLUMN_REORDERED = {"EVT_DATAVIEW_COLUMN_REORDERED"}
EVT_DATAVIEW_COLUMN_SORTED = {"EVT_DATAVIEW_COLUMN_SORTED"}
EVT_DATAVIEW_ITEM_ACTIVATED = {"EVT_DATAVIEW_ITEM_ACTIVATED"}
EVT_DATAVIEW_ITEM_BEGIN_DRAG = {"EVT_DATAVIEW_ITEM_BEGIN_DRAG"}
EVT_DATAVIEW_ITEM_COLLAPSED = {"EVT_DATAVIEW_ITEM_COLLAPSED"}
EVT_DATAVIEW_ITEM_COLLAPSING = {"EVT_DATAVIEW_ITEM_COLLAPSING"}
EVT_DATAVIEW_ITEM_CONTEXT_MENU = {"EVT_DATAVIEW_ITEM_CONTEXT_MENU"}
EVT_DATAVIEW_ITEM_DROP = {"EVT_DATAVIEW_ITEM_DROP"}
EVT_DATAVIEW_ITEM_DROP_POSSIBLE = {"EVT_DATAVIEW_ITEM_DROP_POSSIBLE"}
EVT_DATAVIEW_ITEM_EDITING_DONE = {"EVT_DATAVIEW_ITEM_EDITING_DONE"}
EVT_DATAVIEW_ITEM_EDITING_STARTED = {"EVT_DATAVIEW_ITEM_EDITING_STARTED"}
EVT_DATAVIEW_ITEM_EXPANDED = {"EVT_DATAVIEW_ITEM_EXPANDED"}
EVT_DATAVIEW_ITEM_EXPANDING = {"EVT_DATAVIEW_ITEM_EXPANDING"}
EVT_DATAVIEW_ITEM_START_EDITING = {"EVT_DATAVIEW_ITEM_START_EDITING"}
EVT_DATAVIEW_ITEM_VALUE_CHANGED = {"EVT_DATAVIEW_ITEM_VALUE_CHANGED"}
EVT_DATAVIEW_SELECTION_CHANGED = {"EVT_DATAVIEW_SELECTION_CHANGED"}
EVT_TREELIST_COLUMN_SORTED = {"EVT_TREELIST_COLUMN_SORTED"}
EVT_TREELIST_ITEM_ACTIVATED = {"EVT_TREELIST_ITEM_ACTIVATED"}
EVT_TREELIST_ITEM_CHECKED = {"EVT_TREELIST_ITEM_CHECKED"}
EVT_TREELIST_ITEM_CONTEXT_MENU = {"EVT_TREELIST_ITEM_CONTEXT_MENU"}
EVT_TREELIST_ITEM_EXPANDED = {"EVT_TREELIST_ITEM_EXPANDED"}
EVT_TREELIST_ITEM_EXPANDING = {"EVT_TREELIST_ITEM_EXPANDING"}
EVT_TREELIST_SELECTION_CHANGED = {"EVT_TREELIST_SELECTION_CHANGED"}
NOT_FOUND = {"NOT_FOUND"}
NO_IMAGE = {"NO_IMAGE"}
TLI_FIRST = {"TLI_FIRST"}
TLI_LAST = {"TLI_LAST"}
TL_3STATE = {"TL_3STATE"}
TL_CHECKBOX = {"TL_CHECKBOX"}
TL_DEFAULT_STYLE = {"TL_DEFAULT_STYLE"}
TL_MULTIPLE = {"TL_MULTIPLE"}
TL_NO_HEADER = {"TL_NO_HEADER"}
TL_SINGLE = {"TL_SINGLE"}
TL_USER_3STATE = {"TL_USER_3STATE"}
class DataViewColumn(SettableHeaderColumn):
    Alignment = {"Alignment"}
    Bitmap = {"Bitmap"}
    Flags = {"Flags"}
    MinWidth = {"MinWidth"}
    ModelColumn = {"ModelColumn"}
    Owner = {"Owner"}
    Renderer = {"Renderer"}
    SortOrder = {"SortOrder"}
    Title = {"Title"}
    Width = {"Width"}
class DataViewCtrl(Control):
    ColumnCount = {"ColumnCount"}
    Columns = {"Columns"}
    CountPerPage = {"CountPerPage"}
    CurrentColumn = {"CurrentColumn"}
    CurrentItem = {"CurrentItem"}
    ExpanderColumn = {"ExpanderColumn"}
    Indent = {"Indent"}
    MainWindow = {"MainWindow"}
    Model = {"Model"}
    SelectedItemsCount = {"SelectedItemsCount"}
    Selection = {"Selection"}
    Selections = {"Selections"}
    SortingColumn = {"SortingColumn"}
    TopItem = {"TopItem"}
class DataViewEvent(NotifyEvent):
    CacheFrom = {"CacheFrom"}
    CacheTo = {"CacheTo"}
    Column = {"Column"}
    DataBuffer = {"DataBuffer"}
    DataFormat = {"DataFormat"}
    DataObject = {"DataObject"}
    DataSize = {"DataSize"}
    DataViewColumn = {"DataViewColumn"}
    DragFlags = {"DragFlags"}
    DropEffect = {"DropEffect"}
    Item = {"Item"}
    Model = {"Model"}
    Position = {"Position"}
    ProposedDropIndex = {"ProposedDropIndex"}
    Value = {"Value"}
class DataViewIconText(Object):
    BitmapBundle = {"BitmapBundle"}
    Icon = {"Icon"}
    Text = {"Text"}
class DataViewItem(BaseClass):
    ID = {"ID"}
class DataViewItemAttr(BaseClass):
    BackgroundColour = {"BackgroundColour"}
    Bold = {"Bold"}
    Colour = {"Colour"}
    Italic = {"Italic"}
class DataViewListCtrl(DataViewCtrl):
    ItemCount = {"ItemCount"}
    SelectedRow = {"SelectedRow"}
    Store = {"Store"}
class DataViewModel(RefCounter): ...
class DataViewListModel(DataViewModel):
    Count = {"Count"}
class DataViewIndexListModel(DataViewListModel): ...
class DataViewListStore(DataViewIndexListModel):
    ItemCount = {"ItemCount"}
class DataViewModelNotifier(BaseClass):
    Owner = {"Owner"}
class DataViewRenderer(Object):
    Alignment = {"Alignment"}
    EditorCtrl = {"EditorCtrl"}
    EllipsizeMode = {"EllipsizeMode"}
    Mode = {"Mode"}
    Owner = {"Owner"}
    VariantType = {"VariantType"}
    View = {"View"}
class DataViewBitmapRenderer(DataViewRenderer): ...
class DataViewCheckIconTextRenderer(DataViewRenderer): ...
class DataViewChoiceRenderer(DataViewRenderer):
    Choices = {"Choices"}
class DataViewCustomRenderer(DataViewRenderer):
    Attr = {"Attr"}
    Size = {"Size"}
class DataViewDateRenderer(DataViewRenderer): ...
class DataViewIconTextRenderer(DataViewRenderer): ...
class DataViewProgressRenderer(DataViewRenderer): ...
class DataViewSpinRenderer(DataViewCustomRenderer): ...
class DataViewTextRenderer(DataViewRenderer): ...
class DataViewToggleRenderer(DataViewRenderer): ...
class DataViewTreeCtrl(DataViewCtrl):
    ImageList = {"ImageList"}
    Store = {"Store"}
class DataViewTreeStore(DataViewModel): ...
class DataViewValueAdjuster(BaseClass): ...
class DataViewVirtualListModel(DataViewListModel): ...
class TreeListCtrl(Window):
    ColumnCount = {"ColumnCount"}
    DataView = {"DataView"}
    FirstItem = {"FirstItem"}
    NO_IMAGE = {"NO_IMAGE"}
    RootItem = {"RootItem"}
    Selection = {"Selection"}
    Selections = {"Selections"}
    SortColumn = {"SortColumn"}
    View = {"View"}
class TreeListEvent(NotifyEvent):
    Column = {"Column"}
    Item = {"Item"}
    OldCheckedState = {"OldCheckedState"}
class TreeListItem(BaseClass): ...
class TreeListItemComparator(BaseClass): ...
