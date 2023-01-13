
# Created on 14-Nov-2022 00:02:00


import ctypes
import datetime as dt
from ctypes import wintypes, POINTER
from . import constants as con
from . import apis as api
from .commons import getWheelDelta, getKeyState, Area
from .enums import MouseButtonState, MouseButton, Keys, SizedPositions



mouseMsgList = [con.WM_MOUSEWHEEL, con.WM_MOUSEMOVE, con.WM_MOUSEHOVER, con.WM_NCHITTEST,
                con.WM_LBUTTONDOWN, con.WM_LBUTTONUP, con.WM_RBUTTONDOWN, con.WM_RBUTTONUP]
class EventArgs:
    def __init__(self) -> None:
        self.handled = False
        self.data = None
        self.testvar = 100



class MouseEventArgs(EventArgs):
    def __init__(self, msg, wp, lp) -> None:
        super().__init__()
        _fwKeys = getKeyState(wp)
        self.delta = getWheelDelta(wp)
        match _fwKeys:
            case 5: self.shiftKey = MouseButtonState.PRESSED
            case 9: self.ctrlKey = MouseButtonState.PRESSED
            case 17: self.mouseButton = MouseButton.MIDDLE
            case 33: self.mouseButton = MouseButton.XBUTTON1

        if msg in mouseMsgList: # This list is declared upside of this file.
            self.xpos = int(api.LOWORD(lp))
            self.ypos = int(api.HIWORD(lp))

        match msg:
            case con.WM_LBUTTONDOWN, con.WM_LBUTTONUP:self.mouseButton = MouseButton.LEFT
            case con.WM_RBUTTONDOWN, con.WM_RBUTTONUP: self.mouseButton = MouseButton.RIGHT
#--------------------------------End of MouseEventArgs

class KeyEventArgs(EventArgs):
    def __init__(self, wp) -> None:
        super().__init__()
        self.keyCode = Keys(wp)
        match self.keyCode:
            case Keys.SHIFT:
                self.shiftPressed = True
                self.modifier = Keys.SHIFT_MODIFIER
            case Keys.CTRL:
                self.ctrlPressed = True
                self.modifier = Keys.CTRL_MODIFIER
            case Keys.ALT:
                self.altPressed = True
                self.modifier = Keys.ALT_MODIFIER

        self.keyValue = self.keyCode.value

#------------------------End of KeyEventArgs-----------

class KeyPressEventArgs(EventArgs):
    def __init__(self, wp) -> None:
        super().__init__()
        self.keyChar = chr(wp)

#--------------------End of KeyPressEventArgs------------

class SizeEventArgs(EventArgs):
    def __init__(self, msg, wp, lp) -> None:
        super().__init__()
        if msg == con.WM_SIZING:
            self.sizedOn = SizedPositions(wp)
            self.formRect = ctypes.cast(lp, POINTER(api.RECT)).contents
        else:
            self.clientArea = Area(int(api.LOWORD(lp)), int(api.HIWORD(lp)))


class DateTimeEventArgs(EventArgs):
    __slot__ = ("_date_str", "_date_time")
    def __init__(self, dtp_str, st) -> None:
        super().__init__()
        self._date_str = dtp_str
        self._date_time = dt.datetime(st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond, st.wMilliseconds)

    @property
    def date_string(self) -> str: return self._date_str

    @property
    def date_time(self) -> dt.datetime: return self._date_time





