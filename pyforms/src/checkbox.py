
# CheckBox module - Created on 08-Dec-2022 18:49:20

from ctypes import WINFUNCTYPE, byref, cast, addressof, create_unicode_buffer
from pyforms.src.control import Control
from pyforms.src.commons import MyMessages
from pyforms.src.enums import ControlType
from pyforms.src.apis import LRESULT, LPNMCUSTOMDRAW, SUBCLASSPROC
import pyforms.src.apis as api
from pyforms.src.colors import Color
import pyforms.src.constants as con
from pyforms.src.events import EventArgs

cb_dict = {}
cb_style = con.WS_CHILD | con.WS_VISIBLE | con.WS_TABSTOP | con.BS_AUTOCHECKBOX


class CheckBox(Control):
    """Represents CheckBox control"""
    _count = 1
    __slots__ = ( "_rightAlign", "_autosize", "_txtStyle", "_isChecked", "onCheckedChanged")

    def __init__(self, parent, txt: str, xpos: int = 10, ypos: int = 10, width: int = 0, height: int = 0, auto: bool = False) -> None:
        super().__init__()
        self._clsName = "Button"
        self.name = f"CheckBox_{CheckBox._count}"
        self._ctlType = ControlType.CHECK_BOX
        self._text = self.name if txt == "" else txt
        self._parent = parent
        # self._font = parent._font
        self._font.colneFrom(parent._font)
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
        self._autosize = True
        # Events
        self.onCheckedChanged = None
        self._hwnd = None
        parent._controls.append(self)
        CheckBox._count += 1
        if auto: self.createHandle()

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

        self._bkgBrush = self._bgColor.createHBrush()
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
            # wbuffer = create_unicode_buffer(value)
            api.SetWindowText(self._hwnd, value)
            if self._autosize: self._setAutoSize()



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
        case con.WM_RBUTTONDOWN: cb._rightMouseDownHandler(msg, wp, lp)
        case con.WM_RBUTTONUP: cb._rightMouseUpHandler(msg, wp, lp)
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

