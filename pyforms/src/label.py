#Label module - Created on 23-Nov-2022 17:09:20

from ctypes import byref
from pyforms.src.control import Control
import pyforms.src.constants as con
from pyforms.src.commons import MyMessages
from pyforms.src.enums import ControlType, TextAlignment, LabelBorder, LabelAlignment
from pyforms.src.apis import SIZE, SUBCLASSPROC
import pyforms.src.apis as api
from pyforms.src.colors import Color

lbDict = {}
lbStyle = con.WS_VISIBLE | con.WS_CHILD | con.WS_CLIPCHILDREN | con.WS_CLIPSIBLINGS | con.SS_NOTIFY


class Label(Control):

    _count = 1
    __slots__ = ("_autoSize", "_multiLine", "_txtAlign", "_borderStyle", "_dwAlignFlag")
    def __init__(self, parent, txt: str = "", xpos: int = 10, ypos: int = 10, width: int = 0, height: int = 0, auto = False ) -> None:
        super().__init__()
        self._clsName = "Static"
        self.name = f"Label_{Label._count}"
        self._text = self.name if txt == "" else txt
        self._ctlType = ControlType.LABEL
        self._parent = parent
        self._bgColor = Color(parent._bgColor)
        self._font = parent._font
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._isTextable = True
        self._style = lbStyle
        self._exStyle = 0x00000000
        self._autoSize = True
        self._multiLine = False
        self._txtAlign = LabelAlignment.MIDLEFT
        self._borderStyle = LabelBorder.NONE
        self._dwAlignFlag = 0
        self._hasBrush = True
        self._hwnd = None
        parent._controls.append(self)
        Label._count += 1
        if auto: self.createHandle()


    # -region Public funcs
    def createHandle(self):
        """Create handle for this label"""
        if self._borderStyle != LabelBorder.NONE: self._adjustBorder()
        self._bkgBrush = api.CreateSolidBrush(self._bgColor.ref)
        self._isAutoSizeNeeded()
        self._createControl()
        if self._hwnd:
            lbDict[self._hwnd] = self
            self._setSubclass(lbWndProc)
            self._setFontInternal()
            if self._autoSize: self._setAutoSize(False)


    # -endregion Public funcs

    # -region Private funcs

    # Set the border for this Label
    def _adjustBorder(self):
        if self._borderStyle == LabelBorder.SUNKEN:
            self._style |= con.SS_SUNKEN
        else:
            self._style = con.WS_BORDER

    # Set the text alignment for this label
    def _setTextAlignment(self):
        match self._txtAlign:
            case LabelAlignment.TOPLEFT:
                self._dwAlignFlag = con.DT_TOP | con.DT_LEFT
            case LabelAlignment.TOPCENTER:
                self._dwAlignFlag = con.DT_TOP | con.DT_CENTER
            case LabelAlignment.TOPRIGHT:
                self._dwAlignFlag = con.DT_TOP | con.DT_RIGHT

            case LabelAlignment.MIDLEFT:
                self._dwAlignFlag = con.DT_VCENTER | con.DT_LEFT
            case LabelAlignment.CENTER:
                self._dwAlignFlag = con.DT_VCENTER | con.DT_CENTER
            case LabelAlignment.MIDRIGHT:
                self._dwAlignFlag = con.DT_VCENTER | con.DT_RIGHT

            case LabelAlignment.BOTTOMLEFT:
                self._dwAlignFlag = con.DT_BOTTOM | con.DT_LEFT
            case LabelAlignment.BOTTOMCENTER:
                self._dwAlignFlag = con.DT_BOTTOM | con.DT_CENTER
            case LabelAlignment.BOTTOMRIGHT:
                self._dwAlignFlag = con.DT_BOTTOM | con.DT_RIGHT

        if self._multiLine:
            self._dwAlignFlag |= con.DT_WORDBREAK
        else:
            self._dwAlignFlag |= con.DT_SINGLELINE


    # Check if auto sizing needed or not
    def _isAutoSizeNeeded(self):
        if self._multiLine: self._autoSize = False
        if self._width > 0: self._autoSize = False
        if self._height > 0: self._autoSize = False


    # Set appropriate size for this Label
    def _setAutoSize(self, redraw):
        hdc = api.GetDC(self._hwnd)
        ss = SIZE()
        rct = api.RECT()

        api.SelectObject(hdc, self._font._hwnd)
        api.GetTextExtentPoint32(hdc, self._text, len(self._text), byref(ss))
        api.ReleaseDC(self._hwnd, hdc)
        self._width = ss.cx + 5
        self._height = ss.cy + 5
        api.SetWindowPos(self._hwnd, None, self._xpos, self._ypos, self._width, self._height, con.SWP_NOMOVE)
        api.GetClientRect(self._hwnd, byref(rct))
        if redraw: api.InvalidateRect(self._hwnd, byref(rct), True)


    # Reser the back gound brush for this Label
    def resetBrush(self): self._bkgBrush = self._bgColor.createHBrush()

    # -endregion Private funcs

    # -region Properties

    @property
    def autoSize(self):
        """Returns true if auto size is set"""
        return self._autoSize

    @autoSize.setter
    def autoSize(self, value: bool):
        """Set true if auto size set"""
        self._autoSize = value

    @property
    def multiLine(self):
        """Returns true if multi line enabled"""
        return self._multiLine

    @multiLine.setter
    def multiLine(self, value: bool):
        """Set true for multi line"""
        self._multiLine = value

    @property
    def textAlign(self):
        """Returns the text alignment mode. Check for TextAlignment enum"""
        return self._txtAlign

    @textAlign.setter
    def textAlign(self, value: TextAlignment):
        """Set the text alignment mode. Check for TextAlignment enum"""
        self._txtAlign = value

    @property
    def borderStyle(self):
        """Returns the border style. Check for LabelBorder enum"""
        return self._borderStyle

    @borderStyle.setter
    def borderStyle(self, value: LabelBorder):
        """set the border style. Check for LabelBorder enum"""
        self._borderStyle = value

    # -endregion Properties

#End Label


@SUBCLASSPROC
def lbWndProc(hw, msg, wp, lp, scID, refData):
    # printWinMsg(msg)
    lb = lbDict[hw]
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, lbWndProc, scID)
            del lbDict[hw]

        case MyMessages.LABEL_COLOR:
            if lb._drawFlag & 1: api.SetTextColor(wp, lb._fgColor.ref)
            api.SetBkColor(wp, lb._bgColor.ref)
            return lb._bkgBrush

        case con.WM_SETFOCUS: lb._gotFocusHandler()
        case con.WM_KILLFOCUS: lb._lostFocusHandler()
        case con.WM_LBUTTONDOWN: lb._leftMouseDownHandler(msg, wp, lp)
        case con.WM_LBUTTONUP: lb._leftMouseUpHandler(msg, wp, lp)
        case con.WM_RBUTTONDOWN: lb._rightMouseDownHandler(msg, wp, lp)
        case con.WM_RBUTTONUP: lb._rightMouseUpHandler(msg, wp, lp)
        case con.WM_MOUSEWHEEL: lb._mouseWheenHandler(msg, wp, lp)
        case con.WM_MOUSEMOVE: lb._mouseMoveHandler(msg, wp, lp)
        case con.WM_MOUSELEAVE: lb._mouseLeaveHandler()

    return api.DefSubclassProc(hw, msg, wp, lp)

