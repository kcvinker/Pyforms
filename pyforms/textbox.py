# textbox module - Created on 22-Nov-2022 00:54:20

from .control import Control
from .commons import MyMessages
from .enums import ControlType, TextCase, TextType, TextAlignment
from .apis import SUBCLASSPROC
from . import apis as api
from .colors import Color
from . import constants as con
# from . import winmsgs

tbDict = {}
tbStyle = con.WS_CHILD | con.WS_VISIBLE | con.ES_LEFT | con.WS_TABSTOP | con.ES_AUTOHSCROLL
tbExStyle = con.WS_EX_LEFT | con.WS_EX_LTRREADING | con.WS_EX_CLIENTEDGE


class TextBox(Control):

    _count = 1
    __slots__ = ( "_multiLine", "_hideSel", "_readOnly", "_textCase", "_textType", "_textAlign")

    def __init__(self, parent, xpos: int = 10, ypos: int = 10, width: int = 120, height: int = 23) -> None:
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
        TextBox._count += 1


    def createHandle(self):
        """Create text box's handle"""
        self._setStyles()
        self._createControl()
        if self._hwnd:
            tbDict[self._hwnd] = self
            self._setSubclass(tbWndProc)
            self._setFontInternal()

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

    @Control.backColor.setter
    def backColor(self, value):
        if isinstance(value, int):
            self._bgColor.update_color(value)
        elif isinstance(value, Color):
            self._bgColor = value

        if not self._drawFlag & (1 << 1): self._drawFlag += 2
        if self._isCreated: self._bkgBrush = self._bgColor.createHBrush()
        self._manageRedraw()

        # api.RedrawWindow(self._hwnd, None, None, con.RDW_INVALIDATE| con.RDW_FRAME)


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
        case MyMessages.MOUSE_CLICK: tb._mouse_click_handler()
        case con.WM_RBUTTONDOWN: tb._rightMouseDownHandler(msg, wp, lp)
        case con.WM_RBUTTONUP: tb._rightMouseUpHandler(msg, wp, lp)
        case MyMessages.RIGHT_CLICK: tb._right_mouse_click_handler()
        case con.WM_MOUSEWHEEL: tb._mouseWheenHandler(msg, wp, lp)
        case con.WM_MOUSEMOVE: tb._mouseMoveHandler(msg, wp, lp)
        case con.WM_MOUSELEAVE: tb._mouseLeaveHandler()

        case MyMessages.LABEL_COLOR:
            return tb._bkgBrush

        case MyMessages.EDIT_COLOR:
            if tb._drawFlag:
                if tb._drawFlag & 1: api.SetTextColor(wp, tb._fgColor.ref)
                if tb._drawFlag & 2: api.SetBkColor(wp, tb._bgColor.ref)

            return tb._bkgBrush

    return api.DefSubclassProc(hw, msg, wp, lp)

