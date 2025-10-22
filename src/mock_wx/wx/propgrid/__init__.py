from wx import ObjectRefData, Object, CommandEvent, EvtHandler, Window, Dialog, Scrolled, Panel
from mock_wx.test_case import BaseClass
ArrayPGProperty = {"ArrayPGProperty"}
BOTTOM = {"BOTTOM"}
EVT_PG_CHANGED = {"EVT_PG_CHANGED"}
EVT_PG_CHANGING = {"EVT_PG_CHANGING"}
EVT_PG_COL_BEGIN_DRAG = {"EVT_PG_COL_BEGIN_DRAG"}
EVT_PG_COL_DRAGGING = {"EVT_PG_COL_DRAGGING"}
EVT_PG_COL_END_DRAG = {"EVT_PG_COL_END_DRAG"}
EVT_PG_DOUBLE_CLICK = {"EVT_PG_DOUBLE_CLICK"}
EVT_PG_HIGHLIGHTED = {"EVT_PG_HIGHLIGHTED"}
EVT_PG_ITEM_COLLAPSED = {"EVT_PG_ITEM_COLLAPSED"}
EVT_PG_ITEM_EXPANDED = {"EVT_PG_ITEM_EXPANDED"}
EVT_PG_LABEL_EDIT_BEGIN = {"EVT_PG_LABEL_EDIT_BEGIN"}
EVT_PG_LABEL_EDIT_ENDING = {"EVT_PG_LABEL_EDIT_ENDING"}
EVT_PG_RIGHT_CLICK = {"EVT_PG_RIGHT_CLICK"}
EVT_PG_SELECTED = {"EVT_PG_SELECTED"}
FlagType = {"FlagType"}
NOT_FOUND = {"NOT_FOUND"}
PGPropertyFlags = {"PGPropertyFlags"}
PGVariant = {"PGVariant"}
PG_AUTO_SORT = {"PG_AUTO_SORT"}
PG_DONT_RECURSE = {"PG_DONT_RECURSE"}
PG_EX_HELP_AS_TOOLTIPS = {"PG_EX_HELP_AS_TOOLTIPS"}
PG_EX_MULTIPLE_SELECTION = {"PG_EX_MULTIPLE_SELECTION"}
PG_ITERATE_ALL = {"PG_ITERATE_ALL"}
PG_ITERATE_ALL_PARENTS = {"PG_ITERATE_ALL_PARENTS"}
PG_ITERATE_ALL_PARENTS_RECURSIVELY = {"PG_ITERATE_ALL_PARENTS_RECURSIVELY"}
PG_ITERATE_CATEGORIES = {"PG_ITERATE_CATEGORIES"}
PG_ITERATE_DEFAULT = {"PG_ITERATE_DEFAULT"}
PG_ITERATE_FIXED_CHILDREN = {"PG_ITERATE_FIXED_CHILDREN"}
PG_ITERATE_HIDDEN = {"PG_ITERATE_HIDDEN"}
PG_ITERATE_NORMAL = {"PG_ITERATE_NORMAL"}
PG_ITERATE_PROPERTIES = {"PG_ITERATE_PROPERTIES"}
PG_ITERATE_VISIBLE = {"PG_ITERATE_VISIBLE"}
PG_ITERATOR_FLAGS_ALL = {"PG_ITERATOR_FLAGS_ALL"}
PG_ITERATOR_MASK_OP_ITEM = {"PG_ITERATOR_MASK_OP_ITEM"}
PG_ITERATOR_MASK_OP_PARENT = {"PG_ITERATOR_MASK_OP_PARENT"}
PG_LABEL = {"PG_LABEL"}
PG_PROP_AGGREGATE = {"PG_PROP_AGGREGATE"}
PG_PROP_AUTO_UNSPECIFIED = {"PG_PROP_AUTO_UNSPECIFIED"}
PG_PROP_BEING_DELETED = {"PG_PROP_BEING_DELETED"}
PG_PROP_CATEGORY = {"PG_PROP_CATEGORY"}
PG_PROP_CHILDREN_ARE_COPIES = {"PG_PROP_CHILDREN_ARE_COPIES"}
PG_PROP_CLASS_SPECIFIC_1 = {"PG_PROP_CLASS_SPECIFIC_1"}
PG_PROP_CLASS_SPECIFIC_2 = {"PG_PROP_CLASS_SPECIFIC_2"}
PG_PROP_COLLAPSED = {"PG_PROP_COLLAPSED"}
PG_PROP_COMPOSED_VALUE = {"PG_PROP_COMPOSED_VALUE"}
PG_PROP_CUSTOMIMAGE = {"PG_PROP_CUSTOMIMAGE"}
PG_PROP_DISABLED = {"PG_PROP_DISABLED"}
PG_PROP_HIDDEN = {"PG_PROP_HIDDEN"}
PG_PROP_INVALID_VALUE = {"PG_PROP_INVALID_VALUE"}
PG_PROP_MISC_PARENT = {"PG_PROP_MISC_PARENT"}
PG_PROP_MODIFIED = {"PG_PROP_MODIFIED"}
PG_PROP_NOEDITOR = {"PG_PROP_NOEDITOR"}
PG_PROP_PROPERTY = {"PG_PROP_PROPERTY"}
PG_PROP_READONLY = {"PG_PROP_READONLY"}
PG_PROP_USES_COMMON_VALUE = {"PG_PROP_USES_COMMON_VALUE"}
PG_PROP_WAS_MODIFIED = {"PG_PROP_WAS_MODIFIED"}
PG_RECURSE = {"PG_RECURSE"}
PG_SORT_TOP_LEVEL_ONLY = {"PG_SORT_TOP_LEVEL_ONLY"}
PG_SPLITTER_AUTO_CENTER = {"PG_SPLITTER_AUTO_CENTER"}
PG_VFB_STAY_IN_PROPERTY = {"PG_VFB_STAY_IN_PROPERTY"}
SHOW_SB_ALWAYS = {"SHOW_SB_ALWAYS"}
SHOW_SB_DEFAULT = {"SHOW_SB_DEFAULT"}
SHOW_SB_NEVER = {"SHOW_SB_NEVER"}
TOP = {"TOP"}
byte = {"byte"}
class ColourPropertyValue(Object):
    m_colour = {"m_colour"}
    m_type = {"m_type"}
class PGArrayEditorDialog(Dialog):
    DialogValue = {"DialogValue"}
    Selection = {"Selection"}
    TextCtrlValidator = {"TextCtrlValidator"}
class PGArrayStringEditorDialog(PGArrayEditorDialog):
    DialogValue = {"DialogValue"}
class PGAttributeStorage(BaseClass):
    Count = {"Count"}
class PGCell(Object):
    BgCol = {"BgCol"}
    Bitmap = {"Bitmap"}
    Data = {"Data"}
    FgCol = {"FgCol"}
    Font = {"Font"}
    Text = {"Text"}
class PGCellData(ObjectRefData): ...
class PGCellRenderer(ObjectRefData): ...
class PGChoiceEntry(PGCell):
    Value = {"Value"}
class PGChoices(BaseClass):
    Count = {"Count"}
    Data = {"Data"}
    DataPtr = {"DataPtr"}
    Id = {"Id"}
    Labels = {"Labels"}
class PGChoicesData(ObjectRefData):
    Count = {"Count"}
class PGDefaultRenderer(PGCellRenderer): ...
class PGEditor(Object):
    Name = {"Name"}
    m_clientData = {"m_clientData"}
class PGCheckBoxEditor(PGEditor):
    Name = {"Name"}
class PGChoiceEditor(PGEditor):
    Name = {"Name"}
class PGChoiceAndButtonEditor(PGChoiceEditor):
    Name = {"Name"}
class PGComboBoxEditor(PGChoiceEditor):
    Name = {"Name"}
class PGEditorDialogAdapter(Object):
    Value = {"Value"}
    m_clientData = {"m_clientData"}
class PGMultiButton(Window):
    Count = {"Count"}
    PrimarySize = {"PrimarySize"}
class PGPaintData(BaseClass):
    m_choiceItem = {"m_choiceItem"}
    m_drawnHeight = {"m_drawnHeight"}
    m_drawnWidth = {"m_drawnWidth"}
    m_parent = {"m_parent"}
class PGPropArgCls(BaseClass):
    Name = {"Name"}
    Ptr = {"Ptr"}
    Ptr0 = {"Ptr0"}
class PGProperty(Object):
    m_clientData = {"m_clientData"}
    m_value = {"m_value"}
class BoolProperty(PGProperty): ...
class DateProperty(PGProperty):
    DatePickerStyle = {"DatePickerStyle"}
    DateValue = {"DateValue"}
    Format = {"Format"}
class EditorDialogProperty(PGProperty):
    EditorDialog = {"EditorDialog"}
class ArrayStringProperty(EditorDialogProperty): ...
class DirProperty(EditorDialogProperty): ...
class EnumProperty(PGProperty):
    ChoiceSelection = {"ChoiceSelection"}
    ItemCount = {"ItemCount"}
class CursorProperty(EnumProperty): ...
class EditEnumProperty(EnumProperty): ...
class FileProperty(EditorDialogProperty):
    FileName = {"FileName"}
class FlagsProperty(PGProperty):
    ChoiceSelection = {"ChoiceSelection"}
    ItemCount = {"ItemCount"}
class FontProperty(EditorDialogProperty): ...
class ImageFileProperty(FileProperty): ...
class LongStringProperty(EditorDialogProperty): ...
class MultiChoiceProperty(EditorDialogProperty):
    ValueAsArrayInt = {"ValueAsArrayInt"}
class NumericProperty(PGProperty): ...
class FloatProperty(NumericProperty): ...
class IntProperty(NumericProperty): ...
class PGTextCtrlEditor(PGEditor):
    Name = {"Name"}
class PGSpinCtrlEditor(PGTextCtrlEditor):
    Name = {"Name"}
class PGTextCtrlAndButtonEditor(PGTextCtrlEditor):
    Name = {"Name"}
class PGVIterator(BaseClass):
    Property = {"Property"}
class PGValidationInfo(BaseClass):
    FailureBehavior = {"FailureBehavior"}
    FailureMessage = {"FailureMessage"}
    Value = {"Value"}
class PGWindowList(BaseClass):
    Primary = {"Primary"}
    Secondary = {"Secondary"}
class PropertyCategory(PGProperty):
    ValueAsString = {"ValueAsString"}
class PropertyGridEvent(CommandEvent):
    Column = {"Column"}
    MainParent = {"MainParent"}
    Property = {"Property"}
    PropertyName = {"PropertyName"}
    PropertyValue = {"PropertyValue"}
    ValidationFailureBehavior = {"ValidationFailureBehavior"}
    Value = {"Value"}
class PropertyGridHitTestResult(BaseClass):
    Column = {"Column"}
    Property = {"Property"}
    Splitter = {"Splitter"}
    SplitterHitOffset = {"SplitterHitOffset"}
class PropertyGridInterface(BaseClass):
    Items = {"Items"}
    Properties = {"Properties"}
class PropertyGrid(Scrolled, PropertyGridInterface):
    CaptionBackgroundColour = {"CaptionBackgroundColour"}
    CaptionFont = {"CaptionFont"}
    CaptionForegroundColour = {"CaptionForegroundColour"}
    CellBackgroundColour = {"CellBackgroundColour"}
    CellDisabledTextColour = {"CellDisabledTextColour"}
    CellTextColour = {"CellTextColour"}
    ColumnCount = {"ColumnCount"}
    EditorTextCtrl = {"EditorTextCtrl"}
    EmptySpaceColour = {"EmptySpaceColour"}
    FontHeight = {"FontHeight"}
    Grid = {"Grid"}
    ImageSize = {"ImageSize"}
    LabelEditor = {"LabelEditor"}
    LastItem = {"LastItem"}
    LineColour = {"LineColour"}
    MarginColour = {"MarginColour"}
    MarginWidth = {"MarginWidth"}
    Panel = {"Panel"}
    Root = {"Root"}
    RowHeight = {"RowHeight"}
    ScaleX = {"ScaleX"}
    ScaleY = {"ScaleY"}
    SelectedProperty = {"SelectedProperty"}
    Selection = {"Selection"}
    SelectionBackgroundColour = {"SelectionBackgroundColour"}
    SelectionForegroundColour = {"SelectionForegroundColour"}
    SplitterPosition = {"SplitterPosition"}
    StatusBar = {"StatusBar"}
    TargetRect = {"TargetRect"}
    TargetWindow = {"TargetWindow"}
    UncommittedPropertyValue = {"UncommittedPropertyValue"}
    UnspecifiedValueAppearance = {"UnspecifiedValueAppearance"}
    UnspecifiedValueText = {"UnspecifiedValueText"}
    VerticalSpacing = {"VerticalSpacing"}
class PropertyGridIteratorBase: ...
class PropertyGridIterator(PropertyGridIteratorBase): ...
class PropertyGridManager(Panel, PropertyGridInterface):
    ColumnCount = {"ColumnCount"}
    CurrentPage = {"CurrentPage"}
    DescBoxHeight = {"DescBoxHeight"}
    Grid = {"Grid"}
    PageCount = {"PageCount"}
    SelectedPage = {"SelectedPage"}
    SelectedProperty = {"SelectedProperty"}
    Selection = {"Selection"}
    ToolBar = {"ToolBar"}
class PropertyGridPageState(BaseClass):
    ActualVirtualHeight = {"ActualVirtualHeight"}
    ColumnCount = {"ColumnCount"}
    Grid = {"Grid"}
    LastItem = {"LastItem"}
    Selection = {"Selection"}
    VirtualHeight = {"VirtualHeight"}
    VirtualWidth = {"VirtualWidth"}
class PropertyGridPage(EvtHandler, PropertyGridInterface, PropertyGridPageState):
    Index = {"Index"}
    Root = {"Root"}
    SplitterPosition = {"SplitterPosition"}
    StatePtr = {"StatePtr"}
    ToolId = {"ToolId"}
class StringProperty(PGProperty): ...
class SystemColourProperty(EnumProperty):
    CustomColourIndex = {"CustomColourIndex"}
    Val = {"Val"}
class ColourProperty(SystemColourProperty): ...
class UIntProperty(NumericProperty): ...
