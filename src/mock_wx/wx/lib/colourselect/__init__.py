from mock_wx.test_case import BaseClass
from wx.lib.buttons import GenBitmapButton
EVT_BUTTON = {"EVT_BUTTON"}
class ColourSelect(GenBitmapButton):
    Colour = {"Colour"}
    CustomColours = {"CustomColours"}
    Label = {"Label"}
    Value = {"Value"}
class CustomColourData(BaseClass):
    Colours = {"Colours"}
