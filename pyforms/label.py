
# Created on 23-Nov-2022 17:09:20

from ctypes.wintypes import HWND, UINT
from ctypes import byref
# import ctypes as ctp

from .control import Control
from . import constants as con
from .commons import MyMessages
from .enums import ControlType, TextAlignment, LabelBorder, LabelAlignment
# from .events import EventArgs
from .apis import SIZE, LRESULT, UINT_PTR, DWORD_PTR, WPARAM, LPARAM, SUBCLASSPROC
from . import apis as api
from .colors import Color

from horology import Timing

label_dict = {}
lb_style = con.WS_VISIBLE | con.WS_CHILD | con.WS_CLIPCHILDREN | con.WS_CLIPSIBLINGS | con.SS_NOTIFY


class Label(Control):

    _count = 1
    __slots__ = ("_auto_size", "_multi_line", "_txt_align", "_border_style", "_dw_align_flag")
    def __init__(self, parent, txt: str = "", xpos: int = 10, ypos: int = 10, width: int = 120, height: int = 30 ) -> None:
        super().__init__()
        self._cls_name = "Static"
        self.name = f"Label{Label._count}"
        self._text = self.name if txt == "" else txt
        self._ctl_type = ControlType.LABEL
        self._parent = parent
        self._bg_color = Color(parent._bg_color)
        self._font = parent._font
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._is_textable = True
        self._style = lb_style
        self._ex_style = 0x00000000

        self._auto_size = True
        self._multi_line = False
        self._txt_align = LabelAlignment.MIDLEFT
        self._border_style = LabelBorder.NONE
        self._dw_align_flag = 0
        self._has_brush = True

        Label._count += 1


    # -region Public funcs
    def create_handle(self):
        if self._border_style != LabelBorder.NONE: self._adjustBorder()
        self._bkg_brush = api.CreateSolidBrush(self._bg_color.ref)
        self._isAutoSizeNeeded()
        self._create_control()
        if self._hwnd:
            label_dict[self._hwnd] = self

            if self._auto_size: self._setAutoSize(False)
            self._set_font_internal()
            self._set_subclass(lb_wnd_proc)

    # -endregion Public funcs

    # -region Private funcs
    def _adjustBorder(self):
        if self._border_style == LabelBorder.SUNKEN:
            self._style |= con.SS_SUNKEN
        else:
            self._style = con.WS_BORDER

    def _setTextAlignment(self):
        match self._txt_align:
            case LabelAlignment.TOPLEFT:
                self._dw_align_flag = con.DT_TOP | con.DT_LEFT
            case LabelAlignment.TOPCENTER:
                self._dw_align_flag = con.DT_TOP | con.DT_CENTER
            case LabelAlignment.TOPRIGHT:
                self._dw_align_flag = con.DT_TOP | con.DT_RIGHT

            case LabelAlignment.MIDLEFT:
                self._dw_align_flag = con.DT_VCENTER | con.DT_LEFT
            case LabelAlignment.CENTER:
                self._dw_align_flag = con.DT_VCENTER | con.DT_CENTER
            case LabelAlignment.MIDRIGHT:
                self._dw_align_flag = con.DT_VCENTER | con.DT_RIGHT

            case LabelAlignment.BOTTOMLEFT:
                self._dw_align_flag = con.DT_BOTTOM | con.DT_LEFT
            case LabelAlignment.BOTTOMCENTER:
                self._dw_align_flag = con.DT_BOTTOM | con.DT_CENTER
            case LabelAlignment.BOTTOMRIGHT:
                self._dw_align_flag = con.DT_BOTTOM | con.DT_RIGHT

        if self._multi_line:
            self._dw_align_flag |= con.DT_WORDBREAK
        else:
            self._dw_align_flag |= con.DT_SINGLELINE

    def _isAutoSizeNeeded(self):
        # if self._multi_line: self._auto_size = True
        # if self._width != 0: self._auto_size = True
        # if self._height != 0: self._auto_size = True
        if any([self._multi_line, self._width, self._height]): self._auto_size = True

    def _setAutoSize(self, redraw):
        # with Timing("Time for normal hdc  : "):
        hdc = api.GetDC(self._hwnd)
        ss = SIZE()
        api.SelectObject(hdc, self._font._hwnd)
        api.GetTextExtentPoint32(hdc, self._text, len(self._text), byref(ss))
        api.ReleaseDC(self._hwnd, hdc)
        self._width = ss.cx + 3
        self._height = ss.cy
        api.SetWindowPos(self._hwnd, None, self._xpos, self._ypos, self._width, self._height, con.SWP_NOMOVE)
        if redraw: api.InvalidateRect(self._hwnd, None, True)


    def reset_brush(self): self._bk_brush = api.CreateSolidBrush(self._bg_color.ref)

    # -endregion Private funcs

    # -region Properties

    @property
    def auto_size(self): return self._auto_size

    @property
    def multi_line(self): return self._multi_line

    @multi_line.setter
    def multi_line(self, value: bool): self._multi_line = value

    @property
    def text_align(self): return self._txt_align

    @text_align.setter
    def text_align(self, value: TextAlignment): self._txt_align = value

    @property
    def border_style(self): return self._border_style

    @border_style.setter
    def border_style(self, value: LabelBorder): self._border_style = value

    # -endregion Properties
    dummy = 100








#End Label

# @WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR)
@SUBCLASSPROC
def lb_wnd_proc(hw, msg, wp, lp, scID, refData):
    # printWinMsg(msg)
    lb = label_dict[hw]
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, lb_wnd_proc, scID)

        case MyMessages.LABEL_COLOR:
            # Whether user selects a back color or not, we must set the back color.
            # Otherwise, Label will be drawn in default control back color by DefWndProc
            # hdc = HDC(wp)
            if lb._draw_flag & 1: api.SetTextColor(wp, lb._fg_color.ref)
            api.SetBkColor(wp, lb._bg_color.ref)
            return lb._bkg_brush

        case con.WM_SETFOCUS: lb._got_focus_handler()
        case con.WM_KILLFOCUS: lb._lost_focus_handler()
        case con.WM_LBUTTONDOWN: lb._left_mouse_down_handler(msg, wp, lp)
        case con.WM_LBUTTONUP: lb._left_mouse_up_handler(msg, wp, lp)
        case MyMessages.MOUSE_CLICK: lb._mouse_click_handler()
        case con.WM_RBUTTONDOWN: lb._right_mouse_down_handler(msg, wp, lp)
        case con.WM_RBUTTONUP: lb._right_mouse_up_handler(msg, wp, lp)
        case MyMessages.RIGHT_CLICK: lb._right_mouse_click_handler()
        case con.WM_MOUSEWHEEL: lb._mouse_wheel_handler(msg, wp, lp)
        case con.WM_MOUSEMOVE: lb._mouse_move_handler(msg, wp, lp)
        case con.WM_MOUSELEAVE: lb._mouse_leave_handler()

    return api.DefSubclassProc(hw, msg, wp, lp)


# class DeviceContext:
#     def __init__(self, handle) -> None:
#         self.hwnd = handle
#         print("Device context is init with hwnd - ", handle)

#     def __enter__(self):
#         self.hdc = GetDC(self.hwnd)
#         print("hdc created and value is ", self.hdc)
#         return self.hdc

#     def __exit__(self, tp, v, tb):
#         if self.hdc:
#             ReleaseDC(self.hwnd, self.hdc)
#             print("hdc is released and value is ", self.hdc)


