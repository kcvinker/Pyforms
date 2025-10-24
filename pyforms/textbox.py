# textbox module - Created on 22-Nov-2022 00:54:20

from pyforms.control import Control, CommonBuffer
from pyforms.commons import MyMessages
from pyforms.enums import ControlType, TextCase, TextType, TextAlignment
from pyforms.apis import SUBCLASSPROC
import pyforms.apis as api
from pyforms.colors import Color
import pyforms.constants as con
from pyforms.events import GEA
from ctypes import addressof
# from . import winmsgs

tbDict = {}
# tbStyle = con.ES_LEFT|con.ES_AUTOHSCROLL
tbExStyle = con.WS_EX_LEFT | con.WS_EX_LTRREADING | con.WS_EX_CLIENTEDGE


class TextBox(Control):

    _count = 1
    _buffer = CommonBuffer() # start with 64 chars
    __slots__ = ( "_multiLine", "_hideSel", "_readOnly", "_textCase", "_textType", "_textAlign", "_cueBanner", "onTextChanged")

    def __init__(self, parent, xpos: int = 10, ypos: int = 10, 
                 width: int = 120, height: int = 23, txt="", multiLine=False) -> None:
        super().__init__(parent, ControlType.TEXT_BOX, width, height)
        self.name = f"TextBox_{TextBox._count}"
        self._xpos = xpos
        self._ypos = ypos
        self._isTextable = True
        self._style = 0x50010080 | con.WS_CLIPCHILDREN
        self._exStyle = 0x00000204
        self._drawFlag = 0
        self._multiLine = multiLine
        self._hideSel = False
        self._readOnly = False
        self._textCase = TextCase.NORMAL
        self._textType = TextType.NORMAL
        self._textAlign = TextAlignment.LEFT
        self._text = txt
        # self._fgColor = Color(0x000000)
        self._cueBanner = ""
        self.onTextChanged = None
        self._bkgBrush = self._bgColor.createHBrush()
        parent._controls.append(self)
        TextBox._count += 1
        if parent.createChilds: self.createHandle()


    def createHandle(self):
        """Create text box's handle"""
        self._setStyles()
        self._createControl()
        if self._hwnd:
            tbDict[self._hwnd] = self
            self._setSubclass(tbWndProc)
            self._setFontInternal()
            if len(self._cueBanner):
                Control._smBuffer.fillBuffer(self._cueBanner)
                api.SendMessage(self._hwnd, con.EM_SETCUEBANNER, 1, Control._smBuffer.addr)

            # Without this line, textbox looks ugly style. It won't receive WM_NCPAINT message.
            # So we just redraw the non client area and it will receive WM_NCPAINT
            api.RedrawWindow(self._hwnd, None, None, con.RDW_FRAME| con.RDW_INVALIDATE)

    def selectAll(self):
        if self._isCreated:
            api.SendMessage(self._hwnd, con.EM_SETSEL, 0, -1)

    # Setting text box's style bits
    def _setStyles(self):
        if self._multiLine:
            self._style |= con.ES_MULTILINE | con.ES_WANTRETURN | con.ES_AUTOVSCROLL | con.ES_AUTOVSCROLL
            #| con.WS_VSCROLL | con.WS_HSCROLL
        if self._hideSel: self._style |= con.ES_NOHIDESEL
        if self._readOnly: self._style |= con.ES_READONLY

        if self._textCase == TextCase.LOWER:
            self._style |= con.ES_LOWERCASE
        elif self._textCase == TextCase.UPPER:
            self._style |= con.ES_UPPERCASE

        if self._textType == TextType.NUM_ONLY:
            self._style |= con.ES_NUMBER
        elif self._textType == TextType.PASSWORD:
            self._style |= con.ES_PASSWORD

        if self._textAlign == TextAlignment.CENTER:
            self._style |= con.ES_CENTER
        elif self._textAlign == TextAlignment.RIGHT:
            self._style |= con.ES_RIGHT

        

    def addLine(self, linetext):
        if self._isCreated:
            Control._smBuffer.fillBuffer(linetext)
            api.SendMessage(self._hwnd, con.EM_REPLACESEL, 0, Control._smBuffer.addr)

    @Control.text.getter
    def text(self):
        """Returns the text property of text box"""
        if self._isCreated:
            return TextBox._buffer.getTextFromAPI(self._hwnd)
        else:
            return self._text


    @property
    def textAlign(self):  return self._textAlign

    @textAlign.setter
    def textAlign(self, value: TextAlignment): self._textAlign = value


    @property
    def textCase(self): return self._textCase

    @textCase.setter
    def textCase(self, value: TextCase): self._textCase = value

    @property
    def textType(self): return self._textType

    @textType.setter
    def textType(self, value: TextType):  
        self._textType = value
        if self._isCreated:
            self._style |= con.ES_NUMBER
            api.SetWindowLong(self._hwnd, con.GWL_STYLE, self._style)
            flag = con.SWP_NOMOVE|con.SWP_NOSIZE|con.SWP_NOZORDER|con.SWP_FRAMECHANGED
            self.setPosInternal(flag)

    @property
    def cueBanner(self): return self._cueBanner

    @cueBanner.setter
    def cueBanner(self, value:str) :
        self._cueBanner = value
        if self._isCreated:
            Control._smBuffer.fillBuffer(self._cueBanner)
            api.SendMessage(self._hwnd, con.EM_SETCUEBANNER, 1, Control._smBuffer.addr)

    @property
    def multiLine(self): return self._multiLine

    @multiLine.setter
    def multiLine(self, value: bool) : self._multiLine = value

    @property
    def hideSelection(self): return self._hideSel

    @hideSelection.setter
    def hideSelection(self, value: bool): self._hideSel = value

    @property
    def readOnly(self): return  self._readOnly

    @readOnly.setter
    def readOnly(self, value: bool) : self._readOnly = value

#End TextBox

@SUBCLASSPROC
def tbWndProc(hw, msg, wp, lp, scID, refData):
    # winmsgs.log_msg(msg)
    match msg:
        case con.WM_DESTROY:
            # api.DeleteObject(tb._bkgBrush)
            api.RemoveWindowSubclass(hw, tbWndProc, scID)
            del tbDict[hw]

        # case con.WM_SETFOCUS: tb._gotFocusHandler()
        # case con.WM_KILLFOCUS: tb._lostFocusHandler()
        case con.WM_LBUTTONDOWN: 
            tb = tbDict[hw]
            tb._leftMouseDownHandler(msg, wp, lp)
            
        case con.WM_LBUTTONUP: 
            tb = tbDict[hw]
            tb._leftMouseUpHandler(msg, wp, lp)

        case con.WM_RBUTTONDOWN: 
            tb = tbDict[hw]
            tb._rightMouseDownHandler(msg, wp, lp)

        case con.WM_RBUTTONUP: 
            tb = tbDict[hw]
            tb._rightMouseUpHandler(msg, wp, lp)

        case con.WM_MOUSEWHEEL: 
            tb = tbDict[hw]
            tb._mouseWheenHandler(msg, wp, lp)

        case con.WM_MOUSEMOVE: 
            tb = tbDict[hw]
            tb._mouseMoveHandler(msg, wp, lp)

        case con.WM_MOUSELEAVE: 
            tb = tbDict[hw]
            tb._mouseLeaveHandler()

        case con.WM_KEYDOWN:
            if wp == 0x09:
                tb = tbDict[hw]
                # shift = (api.GetKeyState(0x10) & 0x8000) != 0
                # x = api.SendMessage(tb._parent._hwnd, 0x0028, int(shift), 0)
                # print(f"{x=}, {shift=}")
                if tb._tabOrderHwnd: 
                    x = api.SetFocus(tb._tabOrderHwnd)
                    # print(f"{x=}")
                return 0

        case MyMessages.CTL_COMMAND:
            ncode = api.HIWORD(wp)
            # print(f"{ncode = }")
            if ncode == con.EN_CHANGE:
                tb = tbDict[hw]
                if tb.onTextChanged: tb.onTextChanged(tb, GEA)

        case MyMessages.LABEL_COLOR:
            tb = tbDict[hw]
            return tb._bkgBrush

        case MyMessages.EDIT_COLOR:
            tb = tbDict[hw]
            if tb._drawFlag:
                if tb._drawFlag & 1: api.SetTextColor(wp, tb._fgColor.ref)
                if tb._drawFlag & 2: api.SetBkColor(wp, tb._bgColor.ref)

            return tb._bkgBrush

        case MyMessages.MM_FONT_CHANGED:
            # User changed any font property. We need to recreate the font handle.
            tb = tbDict[hw]
            tb.updateFontInternal()
            return 0

    return api.DefSubclassProc(hw, msg, wp, lp)

