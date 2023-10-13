# textbox module - Created on 22-Nov-2022 00:54:20

from pyforms.src.control import Control
from pyforms.src.commons import MyMessages
from pyforms.src.enums import ControlType, TextCase, TextType, TextAlignment
from pyforms.src.apis import SUBCLASSPROC
import pyforms.src.apis as api
from pyforms.src.colors import Color
import pyforms.src.constants as con
from pyforms.src.events import EventArgs
from ctypes import create_unicode_buffer, addressof
# from . import winmsgs

tbDict = {}
tbStyle = con.WS_CHILD | con.WS_VISIBLE | con.ES_LEFT | con.WS_TABSTOP | con.ES_AUTOHSCROLL
tbExStyle = con.WS_EX_LEFT | con.WS_EX_LTRREADING | con.WS_EX_CLIENTEDGE


class TextBox(Control):

    _count = 1
    __slots__ = ( "_multiLine", "_hideSel", "_readOnly", "_textCase", "_textType", "_textAlign", "_cueBanner", "onTextChanged")

    def __init__(self, parent, xpos: int = 10, ypos: int = 10, width: int = 120, height: int = 23, bCreate = False) -> None:
        super().__init__()
        self._clsName = "EDIT"
        self.name = f"TextBox_{TextBox._count}"
        self._ctlType = ControlType.TEXT_BOX
        self._parent = parent
        self._font = parent._font
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._isTextable = True
        self._style = 0x50010080 | con.WS_CLIPCHILDREN
        self._exStyle = 0x00000204
        self._bgColor = Color(0xFFFFFF)
        self._drawFlag = 0
        self._multiLine = False
        self._hideSel = False
        self._readOnly = False
        self._textCase = TextCase.NORMAL
        self._textType = TextType.NORMAL
        self._textAlign = TextAlignment.LEFT
        self._cueBanner = ""
        self.onTextChanged = None
        TextBox._count += 1
        if bCreate: self.createHandle()


    def createHandle(self):
        """Create text box's handle"""
        self._setStyles()
        self._createControl()
        if self._hwnd:
            tbDict[self._hwnd] = self
            self._setSubclass(tbWndProc)
            self._setFontInternal()
            if len(self._cueBanner):
                cueStr = create_unicode_buffer(self._cueBanner)
                api.SendMessage(self._hwnd, con.EM_SETCUEBANNER, 1, addressof(cueStr))

            # Without this line, textbox looks ugly style. It won't receive WM_NCPAINT message.
            # So we just redraw the non client area and it will receive WM_NCPAINT
            api.RedrawWindow(self._hwnd, None, None, con.RDW_FRAME| con.RDW_INVALIDATE)


    # Setting text box's style bits
    def _setStyles(self):
        if self._multiLine: self._style |= con.ES_MULTILINE | con.ES_WANTRETURN
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

        self._bkgBrush = self._bgColor.createHBrush()



    @Control.text.getter
    def text(self):
        """Returns the text property of text box"""
        if self._isCreated:
            return self._getCtrlText()
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
    def textType(self, value: TextType):  self._textType = value

    @property
    def cueBanner(self): return self._cueBanner

    @cueBanner.setter
    def cueBanner(self, value:str) :
        self._cueBanner = value
        if self._isCreated:
            cueStr = create_unicode_buffer(self._cueBanner)
            api.SendMessage(self._hwnd, con.EM_SETCUEBANNER, 1, addressof(cueStr))

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
    tb = tbDict[hw]
    match msg:
        case con.WM_DESTROY:
            api.DeleteObject(tb._bkgBrush)
            api.RemoveWindowSubclass(hw, tbWndProc, scID)
            del tbDict[hw]

        # case con.WM_SETFOCUS: tb._gotFocusHandler()
        # case con.WM_KILLFOCUS: tb._lostFocusHandler()
        case con.WM_LBUTTONDOWN: tb._leftMouseDownHandler(msg, wp, lp)
        case con.WM_LBUTTONUP: tb._leftMouseUpHandler(msg, wp, lp)
        case con.WM_RBUTTONDOWN: tb._rightMouseDownHandler(msg, wp, lp)
        case con.WM_RBUTTONUP: tb._rightMouseUpHandler(msg, wp, lp)
        case con.WM_MOUSEWHEEL: tb._mouseWheenHandler(msg, wp, lp)
        case con.WM_MOUSEMOVE: tb._mouseMoveHandler(msg, wp, lp)
        case con.WM_MOUSELEAVE: tb._mouseLeaveHandler()

        case con.WM_COMMAND:
            ncode = api.HIWORD(wp)
            if ncode == con.EN_CHANGE:
                if tb.onTextChanged: tb.onTextChanged(tb, EventArgs())

        case MyMessages.LABEL_COLOR:
            return tb._bkgBrush

        case MyMessages.EDIT_COLOR:
            if tb._drawFlag:
                if tb._drawFlag & 1: api.SetTextColor(wp, tb._fgColor.ref)
                if tb._drawFlag & 2: api.SetBkColor(wp, tb._bgColor.ref)

            return tb._bkgBrush

    return api.DefSubclassProc(hw, msg, wp, lp)

