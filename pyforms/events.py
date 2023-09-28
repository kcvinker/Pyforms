# Created on 14-Nov-2022 00:02:00

import ctypes
import datetime as dt
from ctypes import POINTER, cast
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
    def __init__(self, ctl, isDown, wp) -> None:
        super().__init__()
        self.keyCode = Keys(wp)
        self.keyValue = self.keyCode.value
        self.shiftPressed = False
        self.ctrlPressed = False
        self.altPressed = False

        match self.keyCode:
            case Keys.SHIFT:
                # self.shiftPressed = isDown
                self.modifier = Keys.SHIFT_MODIFIER
                ctl._keyMod += 1 if isDown else -1

            case Keys.CTRL:
                # self.ctrlPressed = isDown
                self.modifier = Keys.CTRL_MODIFIER
                ctl._keyMod += 2 if isDown else -2
            case Keys.ALT:
                # self.altPressed = isDown
                self.modifier = Keys.ALT_MODIFIER
                ctl._keyMod += 4 if isDown else -4

        self.shiftPressed = bool(ctl._keyMod & 1)
        self.ctrlPressed = bool(ctl._keyMod & 2)
        self.altPressed = bool(ctl._keyMod & 4)



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
    __slot__ = ("_dateStr", "_dateTime")
    def __init__(self, dtpStr, st) -> None:
        super().__init__()
        self._dateStr = dtpStr
        self._dateTime = dt.datetime(st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond, st.wMilliseconds)

    @property
    def dateString(self) -> str: return self._dateStr

    @property
    def dateTime(self) -> dt.datetime: return self._dateTime


class HeaderEventArgs(EventArgs):
    __slot__ = ("_index", "_btn")
    def __init__(self, lpm) -> None:
        super().__init__()
        hdr = cast(lpm, api.LPNMHEADER).contents
        self._index = hdr.iItem
        self._btn = hdr.iButton

    @property
    def index(self): return self._index

    @property
    def button(self): return self._btn


