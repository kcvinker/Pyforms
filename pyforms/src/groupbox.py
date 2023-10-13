# Created on 20-Jan-2023 07:49:20

from ctypes import byref, create_unicode_buffer
from pyforms.src.control import Control
import pyforms.src.constants as con
from pyforms.src.commons import MyMessages
from pyforms.src.enums import ControlType
from pyforms.src.apis import SUBCLASSPROC
import pyforms.src.apis as api
from pyforms.src.colors import Color, COLOR_BLACK
# from horology import Timing
# from .winmsgs import log_msg

gbDict = {}
gbStyle = con.WS_CHILD | con.WS_VISIBLE | con.BS_GROUPBOX | con.BS_NOTIFY | con.BS_TOP | con.WS_OVERLAPPED |con.WS_CLIPCHILDREN| con.WS_CLIPSIBLINGS
gbExStyle = con.WS_EX_RIGHTSCROLLBAR| con.WS_EX_CONTROLPARENT

class GroupBox(Control):

    _count = 1
    __slots__ = ("_pen", "_tmpTxt", "_rect", "_txtWidth")
    def __init__(self, parent, txt: str = "", xpos: int = 10, ypos: int = 10, width: int = 300, height: int = 300, bCreate = False ) -> None:
        super().__init__()
        self._clsName = "Button"
        self.name = f"GroupBox_{GroupBox._count}"
        self._text = self.name if txt == "" else txt
        self._ctlType = enums.ControlType.GROUP_BOX
        self._parent = parent
        self._bgColor = Color(parent._bgColor)
        # self._fgColor = COLOR_BLACK # Control class is taking care of this
        self._font = parent._font
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._isTextable = True
        self._style = gbStyle
        self._exStyle = gbExStyle
        self._drawFlag = 0
        self._txtWidth = 0
        GroupBox._count += 1
        if bCreate: self.createHandle()


    # -region Public funcs
    def createHandle(self):
        self._bkgBrush = self._bgColor.createHBrush()
        self._pen = self._bgColor.createHPen()
        self._rect = api.RECT(0, 10, self._width, self._height - 2)
        self._createControl()
        if self._hwnd:
            gbDict[self._hwnd] = self
            self._setFontInternal()
            self._getTextSize()
            self._setSubclass(gbWndProc)

    # -endregion Public funcs


    def _getTextSize(self):
        # with Timing("Time for normal hdc  : "):
        hdc = api.GetDC(self._hwnd)
        size = api.SIZE()
        api.SelectObject(hdc, self._font._hwnd)
        api.GetTextExtentPoint32(hdc, self._text, len(self._text), byref(size))
        api.ReleaseDC(self._hwnd, hdc)
        self._txtWidth = size.cx + 10

    def _draw_text(self):
        # By drawing text on our own, we can control the look of...
        # goup box very effectively. Now, upper half of the text...
        # back ground looks transparent. If user doesn't change...
        # back color, text will remain fully transparent bkg.
        # If anyone complaints about flickering, consider double buffering.
        yp = 9
        hdc = api.GetDC(self._hwnd)
        api.SelectObject(hdc, self._pen)
        api.MoveToEx(hdc, 10, yp, None)
        api.LineTo(hdc, self._txtWidth, yp)

        api.SetBkMode(hdc, con.TRANSPARENT)
        api.SelectObject(hdc, self._font._hwnd)
        api.SetTextColor(hdc, self._fgColor.ref)
        api.TextOut(hdc, 10, 0, create_unicode_buffer(self._text), len(self._text))
        api.ReleaseDC(self._hwnd, hdc)

    # -endregion Private funcs

    # -region Properties

    @Control.text.setter
    def text(self, value: str):
        """Set the text for group box"""
        self._text = value
        if self._isCreated:
            self._getTextSize()
            self._manageRedraw()


    # @property
    # def multi_line(self): return self._multi_line

    # @multi_line.setter
    # def multi_line(self, value: bool): self._multi_line = value

    # @property
    # def text_align(self): return self._txt_align

    # @text_align.setter
    # def text_align(self, value: TextAlignment): self._txt_align = value

    # @property
    # def border_style(self): return self._border_style

    # @border_style.setter
    # def border_style(self, value: GroupBoxBorder): self._border_style = value

    # -endregion Properties

#End GroupBox

# @WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR)
@SUBCLASSPROC
def gbWndProc(hw, msg, wp, lp, scID, refData):
    # printWinMsg(msg)
    # log_msg(msg)
    gb = gbDict[hw]
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, gbWndProc, scID)
            del gbDict[hw]

        case con.WM_SETFOCUS: gb._gotFocusHandler()
        case con.WM_KILLFOCUS: gb._lostFocusHandler()
        case con.WM_LBUTTONDOWN: gb._leftMouseDownHandler(msg, wp, lp)
        case con.WM_LBUTTONUP: gb._leftMouseUpHandler(msg, wp, lp)
        case con.WM_RBUTTONDOWN: gb._rightMouseDownHandler(msg, wp, lp)
        case con.WM_RBUTTONUP: gb._rightMouseUpHandler(msg, wp, lp)
        case con.WM_MOUSEWHEEL: gb._mouseWheenHandler(msg, wp, lp)
        case con.WM_MOUSEMOVE: gb._mouseMoveHandler(msg, wp, lp)
        case con.WM_MOUSELEAVE: gb._mouseLeaveHandler()
        case con.WM_ERASEBKGND:
            if gb._drawFlag:
                rc = api.get_client_rect(hw)
                api.FillRect(wp, byref(rc), gb._bkgBrush)
                return 1
            # NOTE: Do not return anything outside the 'if', as it will make every static control a mess.

        case con.WM_PAINT:
            # Let the control do it's painting works.
            ret = api.DefSubclassProc(hw, msg, wp, lp)

            # Now, we can draw the text over this group box.
            gb._draw_text()
            return ret

        case con.WM_GETTEXTLENGTH: return 0

    return api.DefSubclassProc(hw, msg, wp, lp)

