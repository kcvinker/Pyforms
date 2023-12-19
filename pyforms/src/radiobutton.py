# RadioButton module - Created on 09-Dec-2022 16:03:20

from ctypes import byref, cast, addressof
from pyforms.src.control import Control
from pyforms.src.commons import MyMessages
from pyforms.src.enums import ControlType
from pyforms.src.apis import LRESULT, LPNMCUSTOMDRAW, SUBCLASSPROC
import pyforms.src.apis as api
from pyforms.src.colors import Color
import pyforms.src.constants as con
from pyforms.src.events import EventArgs

rbDict = {}
rbStyle = con.WS_CHILD | con.WS_VISIBLE | con.WS_TABSTOP | con.BS_AUTORADIOBUTTON
txtFlag = con.DT_SINGLELINE | con.DT_VCENTER | con.DT_CENTER | con.DT_NOPREFIX


class RadioButton(Control):

    _count = 1
    __slots__ = ( "_rightAlign", "_txtStyle", "_isChecked", "onCheckedChanged", "_checkOnClick", "_value")

    def __init__(self, parent, txt: str, xpos: int = 10, ypos: int = 10, width: int = 120, height: int = 23, auto = False, check=False) -> None:
        super().__init__()
        self._clsName = "Button"
        self.name = f"RadioButton_{RadioButton._count}"
        self._ctlType = ControlType.RADIO_BUTTON
        self._text = self.name if txt == "" else txt
        self._parent = parent
        self._font = parent._font
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._isTextable = True
        self._style = rbStyle
        self._exStyle = con.WS_EX_LTRREADING | con.WS_EX_LEFT
        self._txtStyle = con.DT_SINGLELINE | con.DT_VCENTER
        self._bgColor = Color(parent._bgColor)
        self._bkgBrush = self._bgColor.createHBrush()
        self._checkOnClick = True
        self._rightAlign = False
        self._isChecked = False
        self.onCheckedChanged = None
        self._hwnd = None
        self._value = check
        parent._controls.append(self)
        RadioButton._count += 1
        if auto: self.createHandle()


    def createHandle(self):
        """Create Button's handle"""
        if self._rightAlign:
            self._style |= con.BS_RIGHTBUTTON
            self._txtStyle |= con.DT_RIGHT

        if not self._checkOnClick: self._style ^= con.BS_AUTORADIOBUTTON

        self._createControl()
        if self._hwnd:
            rbDict[self._hwnd] = self
            self._setSubclass(rbWndProc)
            self._setFontInternal()
            ss = api.SIZE()
            api.SendMessage(self._hwnd, con.BCM_GETIDEALSIZE, 0, addressof(ss))
            self._width = ss.cx + 2
            self._height = ss.cy
            api.MoveWindow(self._hwnd, self._xpos, self._ypos, self._width, self._height, True)
            if self._value: api.SendMessage(self._hwnd, con.BM_SETCHECK, self._value, 0)



    @Control.backColor.setter
    def backColor(self, value):
        """Set back color of radio button."""
        self._bgColor.updateColor(value)
        self._bkgBrush = api.CreateSolidBrush(self._bgColor.ref)
        if not self._drawFlag & (1 << 1): self._drawFlag += 2


    @Control.text.getter
    def text(self):
        """Set text of radio button."""
        if self._isCreated:
            return self._getCtrlText()
        else:
            return self._text

    @property
    def checked(self) :
        if self._isCreated:
            self._isChecked = bool(api.SendMessage(self._hwnd, con.BM_GETCHECK, 0, 0))
        return self._isChecked

    @checked.setter
    def checked(self, value: bool) :
        self._isChecked = value
        if self._isCreated: api.SendMessage(self._hwnd, con.BM_SETCHECK, self._value, 0)

#End RadioButton

@SUBCLASSPROC
def rbWndProc(hw, msg, wp, lp, scID, refData) -> LRESULT:
    # printWinMsg(msg)
    rb = rbDict[hw]
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, rbWndProc, scID)
            del rbDict[hw]

        case con.WM_SETFOCUS: rb._gotFocusHandler()
        case con.WM_KILLFOCUS: rb._lostFocusHandler()
        case con.WM_LBUTTONDOWN: rb._leftMouseDownHandler(msg, wp, lp)
        case con.WM_LBUTTONUP: rb._leftMouseUpHandler(msg, wp, lp)
        case con.WM_RBUTTONDOWN: rb._rightMouseDownHandler(msg, wp, lp)
        case con.WM_RBUTTONUP: rb._rightMouseUpHandler(msg, wp, lp)
        case con.WM_MOUSEWHEEL: rb._mouseWheenHandler(msg, wp, lp)
        case con.WM_MOUSEMOVE: rb._mouseMoveHandler(msg, wp, lp)
        case con.WM_MOUSELEAVE: rb._mouseLeaveHandler()

        case MyMessages.LABEL_COLOR:
            # if rb._drawFlag & 1: api.SetTextColor(wp, rb._fgColor.ref)
            if rb._drawFlag & 2: api.SetBkColor(wp, rb._bgColor.ref)
            return rb._bkgBrush

        case MyMessages.CTRL_NOTIFY:
            nmc = cast(lp, LPNMCUSTOMDRAW).contents
            match nmc.dwDrawStage:
                case con.CDDS_PREERASE: return con.CDRF_NOTIFYPOSTERASE
                case con.CDDS_PREPAINT:
                    rct = nmc.rc
                    if not rb._rightAlign:
                        rct.left += 17 # Adjusting rect,otherwise text will be drawn upon the check area
                    else: rct.right -= 17

                    api.SetTextColor(nmc.hdc, rb._fgColor.ref)
                    api.SetBkMode(nmc.hdc, 1)
                    api.DrawText(nmc.hdc, rb._text, len(rb._text), byref(rct), rb._txtStyle )
                    return con.CDRF_SKIPDEFAULT

        case MyMessages.CTL_COMMAND:
            # print(f"Radio {rb.text = }, {rb._isChecked = }")
            if rb.onCheckedChanged: rb.onCheckedChanged(rb, EventArgs() )

    return api.DefSubclassProc(hw, msg, wp, lp)

