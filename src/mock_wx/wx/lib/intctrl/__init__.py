from wx import PyCommandEvent, TextCtrl, Validator
EVT_INT = {"EVT_INT"}
WXK_CTRL_V = {"WXK_CTRL_V"}
WXK_CTRL_X = {"WXK_CTRL_X"}
class IntCtrl(TextCtrl):
    Limited = {"Limited"}
    LongAllowed = {"LongAllowed"}
    Max = {"Max"}
    Min = {"Min"}
    NoneAllowed = {"NoneAllowed"}
    Value = {"Value"}
class IntUpdatedEvent(PyCommandEvent): ...
class IntValidator(Validator): ...
