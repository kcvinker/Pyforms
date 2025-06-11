
# CheckBox module - Created on 08-Dec-2022 18:49:20

from ctypes import WINFUNCTYPE, byref, cast, addressof
from pyforms.src.control import Control
from pyforms.src.commons import MyMessages, StaticData
from pyforms.src.enums import ControlType
from pyforms.src.apis import LRESULT, LPNMCUSTOMDRAW, SUBCLASSPROC
import pyforms.src.apis as api
from pyforms.src.colors import Color
import pyforms.src.constants as con
from pyforms.src.events import GEA

cb_dict = {}
cb_style = con.WS_CHILD | con.WS_VISIBLE | con.WS_TABSTOP | con.BS_AUTOCHECKBOX


class CheckBox(Control):
    """Represents CheckBox control"""
    _count = 1
    __slots__ = ( "_rightAlign", "_autosize", "_txtStyle", "_isChecked", "onCheckedChanged")

    def __init__(self, parent, txt: str, xpos: int = 10, 
                 ypos: int = 10, width: int = 0, height: int = 0) -> None:
        super().__init__(parent, ControlType.CHECK_BOX, width, height)
        self.name = f"CheckBox_{CheckBox._count}"
        self._text = self.name if txt == "" else txt
        self._xpos = xpos
        self._ypos = ypos
        self._isTextable = True
        self._style = cb_style
        self._exStyle = con.WS_EX_LTRREADING | con.WS_EX_LEFT
        self._txtStyle = con.DT_SINGLELINE | con.DT_VCENTER
        self._rightAlign = False
        self._isChecked = False
        self._autosize = True
        self._bkgBrush = StaticData.defBackBrush # self._bgColor.createHBrush()
        self._bgColor = Color(parent._bgColor)
        # Events
        self.onCheckedChanged = None
        parent._controls.append(self)
        CheckBox._count += 1
        if parent.createChilds: self.createHandle()

    def _setAutoSize(self):
        ss = api.SIZE()
        api.SendMessage(self._hwnd, con.BCM_GETIDEALSIZE, 0, addressof(ss))
        self._width = ss.cx
        self._height = ss.cy
        api.MoveWindow(self._hwnd, self._xpos, self._ypos, self._width, self._height, True)


    def createHandle(self):
        if self._rightAlign:
            self._style |= con.BS_RIGHTBUTTON
            self._txtStyle |= con.BS_RIGHTBUTTON

        if self._width > 0 or self.height > 0: self._autosize = False
        self._createControl()
        if self._hwnd:
            cb_dict[self._hwnd] = self
            self._setSubclass(cbWndProc)
            self._setFontInternal()
            if self._autosize: self._setAutoSize()



    @property
    def checked(self): return self._isChecked

    @checked.setter
    def checked(self, value: bool):
        self._isChecked = value
        if self._isCreated: api.SendMessage(self._hwnd, con.BM_SETCHECK, value, 0)

    @property
    def rightAlign(self): return self._rightAlign

    @rightAlign.setter
    def rightAlign(self, value: bool): self._rightAlign = value

    # @Control.backColor.setter
    # def backColor(self, value):
    #     self._bgColor.update_color(value)
    #     self._bg_brush = api.CreateSolidBrush(self._bgColor.ref)
    #     if not self._drawFlag & (1 << 1): self._drawFlag += 2


    @Control.text.setter
    def text(self, value: str):
        self._text = value
        if self._isCreated:
            api.SetWindowText(self._hwnd, value)
            if self._autosize: self._setAutoSize()



#End CheckBox


@SUBCLASSPROC
def cbWndProc(hw, msg, wp, lp, scID, refData) -> LRESULT:
    # printWinMsg(msg)
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, cbWndProc, scID)
            del cb_dict[hw]

        case con.WM_SETFOCUS: 
            cb = cb_dict[hw]
            cb._gotFocusHandler()
        case con.WM_KILLFOCUS: 
            cb = cb_dict[hw]
            cb._lostFocusHandler()
        case con.WM_LBUTTONDOWN: 
            cb = cb_dict[hw]
            cb._leftMouseDownHandler(msg, wp, lp)
        case con.WM_LBUTTONUP: 
            cb = cb_dict[hw]
            cb._leftMouseUpHandler(msg, wp, lp)
        case con.WM_RBUTTONDOWN: 
            cb = cb_dict[hw]
            cb._rightMouseDownHandler(msg, wp, lp)
        case con.WM_RBUTTONUP: 
            cb = cb_dict[hw]
            cb._rightMouseUpHandler(msg, wp, lp)
        case con.WM_MOUSEWHEEL: 
            cb = cb_dict[hw]
            cb._mouseWheenHandler(msg, wp, lp)
        case con.WM_MOUSEMOVE: 
            cb = cb_dict[hw]
            cb._mouseMoveHandler(msg, wp, lp)
        case con.WM_MOUSELEAVE: 
            cb = cb_dict[hw]
            cb._mouseLeaveHandler()

        case MyMessages.LABEL_COLOR:
            cb = cb_dict[hw]
            # Unfortunately changing fore color here won't work.
            if cb._drawFlag & 2: api.SetBkColor(wp, cb._bgColor.ref)
            return cb._bkgBrush

        case MyMessages.CTRL_NOTIFY:
            cb = cb_dict[hw]
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
            cb = cb_dict[hw]
            cb._isChecked = bool(api.SendMessage(hw, con.BM_GETCHECK, 0, 0))
            if cb.onCheckedChanged: cb.onCheckedChanged(cb, GEA )

    return api.DefSubclassProc(hw, msg, wp, lp)

