#Label module - Created on 23-Nov-2022 17:09:20

from ctypes import byref, sizeof
from pyforms.control import Control
import pyforms.constants as con
from pyforms.commons import MyMessages, StaticData
from pyforms.enums import (ControlType, 
                           TextAlignment, LabelBorder, 
                           LabelAlignment, FontOwner)
from pyforms.events import GEA
from pyforms.apis import SIZE, SUBCLASSPROC
import pyforms.apis as api
from pyforms.colors import Color

lbDict = {}
lbStyle = con.WS_CLIPCHILDREN|con.WS_CLIPSIBLINGS|con.SS_NOTIFY


class Label(Control):

    _count = 1
    __slots__ = ("_autoSize", "_multiLine", "_txtAlign", "_borderStyle", "_dwAlignFlag",
                    "_trackMouse", "_tracking", "_focusClr", "_mLeaveClr", "_btnStyle")
    def __init__(self, parent, txt: str = "", xpos: int = 10, 
                 ypos: int = 10, width: int = 0, height: int = 0, 
                 fgc=0x000000, makeButton=False) -> None:
        super().__init__(parent, ControlType.LABEL, width, height)
        self.name = f"Label_{Label._count}"
        self._text = self.name if txt == "" else txt
        self._xpos = xpos
        self._ypos = ypos
        self._isTextable = True
        self._style |= lbStyle
        self._exStyle = 0x00000000
        self._autoSize = True
        self._multiLine = False
        self._txtAlign = TextAlignment.LEFT
        self._borderStyle = LabelBorder.NONE
        self._btnStyle = makeButton
        self._dwAlignFlag = 0
        self._hasBrush = True
        self._bkgBrush = StaticData.defBackBrush
        self._bgColor = Color(parent._bgColor)
        self._trackMouse = False
        self._tracking = False
        self._focusClr = None
        self._mLeaveClr = None
        if fgc > 0:
            self._fgColor = Color(fgc)
            self._drawFlag += 1

        # print(f"p clr 0X{parent._bgColor.value:X}")
        parent._controls.append(self)
        Label._count += 1
        if parent.createChilds: self.createHandle()
        if Label._count == 2:
            print(f"{self._font._size =}, {self._parent._font._handle =}")


    # -region Public funcs
    def createHandle(self):
        """Create handle for this label"""
        if self._borderStyle != LabelBorder.NONE: self._adjustBorder()
        if self._btnStyle: self._adjustBorder()
        if self._txtAlign > 0 and not self._btnStyle:
            self._style |= (0x0001 | 0x0200)
        self._isAutoSizeNeeded()
        self._createControl()
        if self._hwnd:
            lbDict[self._hwnd] = self
            self._setSubclass(lbWndProc)
            self._setFontInternal()
            if self._autoSize: self._setAutoSize(False)
            if self._text == "7":
                print(f"{self._style=}")


    def useAsButton(self, onClickFunc, backColor, focusColor):
        self.onClick = onClickFunc
        self._bgColor = Color(backColor)
        self._mLeaveClr = self._bgColor
        self._focusClr = Color(focusColor)     
        self._trackMouse = True
        if self._bkgBrush != None: 
            self._bkgBrush = api.CreateSolidBrush(self._bgColor.ref)
        if self._drawFlag & 2 != 2: self._drawFlag += 2
        self._manageRedraw()

    def setColors(self, backColor, focusColor):
        """This function sets the back color for normal stage & focused stage"""
        if self._trackMouse:
            self._bgColor = Color(backColor)
            self._mLeaveClr = self._bgColor
            self._focusClr = Color(focusColor)
            self._manageRedraw()

    # -endregion Public funcs

    # -region Private funcs

    # Set the border for this Label
    def _adjustBorder(self):
        if self._borderStyle == LabelBorder.SUNKEN:
            self._style |= con.SS_SUNKEN
        else:
            self._style |= con.WS_BORDER
        
        if self._btnStyle:
            self._style = 0x56810301
            


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
        # print(f"{self._text=}, {self._autoSize=}")


    # Set appropriate size for this Label
    def _setAutoSize(self, redraw):
        hdc = api.GetDC(self._hwnd)
        ss = SIZE()
        rct = api.RECT()

        api.SelectObject(hdc, self._font._handle)
        api.GetTextExtentPoint32(hdc, self._text, len(self._text), byref(ss))
        api.ReleaseDC(self._hwnd, hdc)
        self._width = ss.cx + 5
        self._height = ss.cy + 5
        api.SetWindowPos(self._hwnd, None, self._xpos, self._ypos, self._width, self._height, con.SWP_NOMOVE)
        api.GetClientRect(self._hwnd, byref(rct))
        if redraw: api.InvalidateRect(self._hwnd, byref(rct), True)


    # Reset the back gound brush for this Label
    def resetBrush(self): 
        if self._bkgBrush:
            api.DeleteObject(self._bkgBrush)
        self._bkgBrush = self._bgColor.createHBrush()

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

    @Control.font.setter
    def font(self, value):
        if self._font._ownership == FontOwner.OWNER:
            api.DeleteObject(self._font._handle)

        self._font = value
        if self._isCreated:
            if self._font._handle == 0:
                self._font.createHandle()
            self._sendMsg(con.WM_SETFONT, self._font._handle, 1)
            if self._autoSize: self._setAutoSize(True)

    @property
    def trackMouseLeave(self):
        return self._trackMouse

    @trackMouseLeave.setter
    def trackMouseLeave(self, value):
        self._trackMouse = value

    @property
    def focusColor(self):
        return self._focusClr

    @focusColor.setter
    def focusColor(self, value):
        if isinstance(value, int):
            self._focusClr.updateColor(value)
        elif isinstance(value, Color):
            self._focusClr = value


    # -endregion Properties

#End Label


@SUBCLASSPROC
def lbWndProc(hw, msg, wp, lp, scID, refData):
    # printWinMsg(msg)
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, lbWndProc, scID)            
            del lbDict[hw]

        case MyMessages.LABEL_COLOR:
            lb = lbDict[hw]
            if lb._drawFlag & 1: 
                # print(f"{lb._text=}")
                api.SetTextColor(wp, lb._fgColor.ref)
            api.SetBkColor(wp, lb._bgColor.ref)
            return lb._bkgBrush

        case con.WM_SETFOCUS: 
            lb = lbDict[hw]
            lb._gotFocusHandler()
        case con.WM_KILLFOCUS: 
            lb = lbDict[hw]
            lb._lostFocusHandler()
        case con.WM_LBUTTONDOWN: 
            lb = lbDict[hw]
            lb._leftMouseDownHandler(msg, wp, lp)
        case con.WM_LBUTTONUP: 
            lb = lbDict[hw]
            lb._leftMouseUpHandler(msg, wp, lp)
        case con.WM_RBUTTONDOWN: 
            lb = lbDict[hw]
            lb._rightMouseDownHandler(msg, wp, lp)
        case con.WM_RBUTTONUP: 
            lb = lbDict[hw]
            lb._rightMouseUpHandler(msg, wp, lp)
        case con.WM_MOUSEWHEEL: 
            lb = lbDict[hw]
            lb._mouseWheenHandler(msg, wp, lp)

        case con.WM_MOUSEMOVE: 
            lb = lbDict[hw]
            if lb._isMouseEntered:
                if lb.onMouseMove: 
                    lb.onMouseMove(lb, MouseEventArgs(msg, wpm, lpm))

            if not lb._isMouseEntered:
                lb._isMouseEntered = True
                if lb._onMouseEnter: 
                    lb._onMouseEnter(lb, GEA)

                if lb._trackMouse:   # <-- only if user wants it
                    lb.backColor = lb._focusClr
                    tme = api.TRACKMOUSEEVENT()
                    tme.cbSize = sizeof(api.TRACKMOUSEEVENT)
                    tme.dwFlags = con.TME_LEAVE
                    tme.hwndTrack = lb._hwnd
                    tme.dwHoverTime = 0
                    api.TrackMouseEvent(byref(tme))

        case con.WM_MOUSELEAVE: 
            lb = lbDict[hw]
            lb._isMouseEntered = False
            lb.backColor = lb._mLeaveClr
            if lb._onMouseLeave: 
                lb._onMouseLeave(lb, GEA)

    return api.DefSubclassProc(hw, msg, wp, lp)

