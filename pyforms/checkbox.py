
# CheckBox module - Created on 08-Dec-2022 18:49:20

from ctypes import WINFUNCTYPE, byref, cast, addressof
from .control import Control
from .commons import MyMessages
from .enums import ControlType
from .apis import LRESULT, LPNMCUSTOMDRAW, SUBCLASSPROC
from . import apis as api
from .colors import Color
from . import constants as con
from .events import EventArgs

cb_dict = {}
cb_style = con.WS_CHILD | con.WS_VISIBLE | con.WS_TABSTOP | con.BS_AUTOCHECKBOX


class CheckBox(Control):
    """Represents CheckBox control"""
    _count = 1
    __slots__ = ( "_rightAlign", "_txtStyle", "_isChecked", "onCheckedChanged")

    def __init__(self, parent, txt: str, xpos: int = 10, ypos: int = 10, width: int = 120, height: int = 23) -> None:
        super().__init__()
        self._clsName = "Button"
        self.name = f"CheckBox_{CheckBox._count}"
        self._ctlType = ControlType.CHECK_BOX
        self._text = self.name if txt == "" else txt
        self._parent = parent
        self._font = parent._font
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._isTextable = True
        self._style = cb_style
        self._exStyle = con.WS_EX_LTRREADING | con.WS_EX_LEFT
        self._txtStyle = con.DT_SINGLELINE | con.DT_VCENTER
        self._bgColor = Color(parent._bgColor)
        self._rightAlign = False
        self._isChecked = False
        self.onCheckedChanged = 0
        CheckBox._count += 1


    def createHandle(self):
        if self._rightAlign:
            self._style |= con.BS_RIGHTBUTTON
            self._txtStyle |= con.BS_RIGHTBUTTON

        self._bkgBrush = self._bgColor.createHBrush()
        self._createControl()
        if self._hwnd:
            cb_dict[self._hwnd] = self
            self._setSubclass(cbWndProc)
            self._setFontInternal()

            ss = api.SIZE()
            api.SendMessage(self._hwnd, con.BCM_GETIDEALSIZE, 0, addressof(ss))
            self._width = ss.cx
            self._height = ss.cy
            api.MoveWindow(self._hwnd, self._xpos, self._ypos, self._width, self._height, True)


    @Control.backColor.setter
    def backColor(self, value):
        self._bgColor.update_color(value)
        self._bg_brush = api.CreateSolidBrush(self._bgColor.ref)
        if not self._drawFlag & (1 << 1): self._drawFlag += 2


    @Control.text.getter
    def text(self):
        if self._isCreated:
            return self._getCtrlText()
        else:
            return self._text


#End CheckBox


@SUBCLASSPROC
def cbWndProc(hw, msg, wp, lp, scID, refData) -> LRESULT:
    # printWinMsg(msg)
    cb = cb_dict[hw]
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, cbWndProc, scID)
            del cb_dict[hw]

        case con.WM_SETFOCUS: cb._gotFocusHandler()
        case con.WM_KILLFOCUS: cb._lostFocusHandler()
        case con.WM_LBUTTONDOWN: cb._leftMouseDownHandler(msg, wp, lp)
        case con.WM_LBUTTONUP: cb._leftMouseUpHandler(msg, wp, lp)
        case MyMessages.MOUSE_CLICK: cb._mouse_click_handler()
        case con.WM_RBUTTONDOWN: cb._rightMouseDownHandler(msg, wp, lp)
        case con.WM_RBUTTONUP: cb._rightMouseUpHandler(msg, wp, lp)
        case MyMessages.RIGHT_CLICK: cb._right_mouse_click_handler()
        case con.WM_MOUSEWHEEL: cb._mouseWheenHandler(msg, wp, lp)
        case con.WM_MOUSEMOVE: cb._mouseMoveHandler(msg, wp, lp)
        case con.WM_MOUSELEAVE: cb._mouseLeaveHandler()

        case MyMessages.LABEL_COLOR:
            # Unfortunately changing fore color here won't work.
            if cb._drawFlag & 2: api.SetBkColor(wp, cb._bgColor.ref)
            return cb._bkgBrush

        case MyMessages.CTRL_NOTIFY:
            nmc = cast(lp, LPNMCUSTOMDRAW).contents
            match nmc.dwDrawStage:
                case con.CDDS_PREERASE: return con.CDRF_NOTIFYPOSTERASE
                case con.CDDS_PREPAINT:
                    rct = nmc.rc
                    if not cb._rightAlign:
                        rct.left += 17 # Adjusting rect,otherwise text will be drawn upon the check area
                    else:
                        rct.right -= 17

                    if cb._drawFlag & 1: api.SetTextColor(nmc.hdc, cb._fgColor.ref)
                    api.SetBkMode(nmc.hdc, 1)
                    api.DrawText(nmc.hdc, cb._text, len(cb._text), byref(rct), cb._txtStyle )

                    return con.CDRF_SKIPDEFAULT

        case MyMessages.CTL_COMMAND:
            cb._isChecked = bool(api.SendMessage(hw, con.BM_GETCHECK, 0, 0))
            if cb.onCheckedChanged: cb.onCheckedChanged(cb, EventArgs() )

    return api.DefSubclassProc(hw, msg, wp, lp)

