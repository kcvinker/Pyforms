
# Created on 20-Jan-2023 07:49:20

# from ctypes.wintypes import HWND, UINT
from ctypes import byref, create_unicode_buffer
# import ctypes as ctp

from .control import Control
from . import constants as con
from .commons import MyMessages
from .enums import ControlType
# from .events import EventArgs
from .apis import SUBCLASSPROC
from . import apis as api
from .colors import Color, COLOR_BLACK
from .label import Label

from horology import Timing
from .winmsgs import log_msg

gb_dict = {}
gb_style = con.WS_CHILD | con.WS_VISIBLE | con.BS_GROUPBOX | con.BS_NOTIFY | con.BS_TOP | con.WS_OVERLAPPED |con.WS_CLIPCHILDREN| con.WS_CLIPSIBLINGS
gb_exstyle = con.WS_EX_RIGHTSCROLLBAR| con.WS_EX_TRANSPARENT| con.WS_EX_CONTROLPARENT

class GroupBox(Control):

    _count = 1
    __slots__ = ("_bk_brush", "_pen", "_tmp_text", "_txt_size", "_rect")
    def __init__(self, parent, txt: str = "", xpos: int = 10, ypos: int = 10, width: int = 300, height: int = 300 ) -> None:
        super().__init__()
        self._cls_name = "Button"
        self.name = f"GroupBox_{GroupBox._count}"
        self._text = self.name if txt == "" else txt
        self._ctl_type = ControlType.GROUP_BOX
        self._parent = parent
        self._bg_color = Color(parent._bg_color)
        self._fg_color = COLOR_BLACK
        self._font = parent._font
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._is_textable = True
        self._style = gb_style
        self._ex_style = gb_exstyle
        self._draw_flag = 0


        GroupBox._count += 1


    # -region Public funcs
    def create_handle(self):
        self._bk_brush = api.CreateSolidBrush(self._bg_color.ref);
        self._pen = api.CreatePen(con.PS_SOLID, 2, self._bg_color.ref)# self._bg_color.ref) 0x000000ff
        self._tmp_text = self._text
        self._text = ""
        # self._isAutoSizeNeeded()
        self._rect = api.RECT(0, 10, self._width, self._height - 2)
        self._create_control()
        if self._hwnd:
            gb_dict[self._hwnd] = self

            self._getTextSize()
            self._set_subclass(gb_wnd_proc)
            # self._make_label()
            # self._set_font_internal()


    # -endregion Public funcs

    # -region Private funcs
    # def _adjustBorder(self):
    #     if self._border_style == GroupBoxBorder.SUNKEN:
    #         self._style |= con.SS_SUNKEN
    #     else:
    #         self._style = con.WS_BORDER

    # def _make_label(self):
    #     # Create a label for groupbox text
    #     lbl = api.CreateWindowEx(0,
    #                 self._tmp_text, self._xpos + 10,
    #                 self._ypos )
    #     # lbl.back_color = self._bg_color
    #     lbl.create_handle()
    #     # lbl._bk_brush = api.GetStockObject(con.NULL_BRUSH)




    def _getTextSize(self):
        # with Timing("Time for normal hdc  : "):
        hdc = api.GetDC(self._hwnd)
        self._txt_size = api.SIZE()
        api.SelectObject(hdc, self._font._hwnd)
        api.GetTextExtentPoint32(hdc, self._tmp_text, len(self._tmp_text), byref(self._txt_size))
        api.ReleaseDC(self._hwnd, hdc)
        self._txt_size.cx += 10
        self._txt_size.cy += 10


    def _draw_text(self):
        # By drawing text on our own, we can control the look of...
        # goup box very effectively. Now, upper half of the text...
        # back ground looks transparent. If user doesn't change...
        # back color, text will remain fully transparent bkg.
        # If anyone complaints about flickering, consider double buffering.
        rc = api.RECT(10, 0, self._txt_size.cx, self._txt_size.cy)
        yp = 9
        hdc = api.GetDC(self._hwnd)
        api.SelectObject(hdc, self._pen)
        api.MoveToEx(hdc, 10, yp, None)
        api.LineTo(hdc, self._txt_size.cx, yp)
        api.SetBkMode(hdc, con.TRANSPARENT)
        api.SelectObject(hdc, self._font._hwnd)
        api.SetTextColor(hdc, self._fg_color.ref)
        api.DrawText(hdc, create_unicode_buffer(self._tmp_text), -1, byref(rc), con.DT_CENTER| con.DT_SINGLELINE )
        api.ReleaseDC(self._hwnd, hdc)



    # -endregion Private funcs

    # -region Properties

    # @property
    # def auto_size(self): return self._auto_size

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
    dummy = 100








#End GroupBox

# @WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR)
@SUBCLASSPROC
def gb_wnd_proc(hw, msg, wp, lp, scID, refData):
    # printWinMsg(msg)
    # log_msg(msg)
    gb = gb_dict[hw]
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, gb_wnd_proc, scID)

        # case MyMessages.GROUPBOX_COLOR:
        #     # Whether user selects a back color or not, we must set the back color.
        #     # Otherwise, GroupBox will be drawn in default control back color by DefWndProc
        #     # hdc = HDC(wp)
        #     if gb._draw_flag & 1: api.SetTextColor(wp, gb._fg_color.ref)
        #     api.SetBkColor(wp, gb._bg_color.ref)
        #     return api.CreateSolidBrush(gb._bg_color.ref)

        case con.WM_SETFOCUS: gb._got_focus_handler()
        case con.WM_KILLFOCUS: gb._lost_focus_handler()
        case con.WM_LBUTTONDOWN: gb._left_mouse_down_handler(msg, wp, lp)
        case con.WM_LBUTTONUP: gb._left_mouse_up_handler(msg, wp, lp)
        case MyMessages.MOUSE_CLICK: gb._mouse_click_handler()
        case con.WM_RBUTTONDOWN: gb._right_mouse_down_handler(msg, wp, lp)
        case con.WM_RBUTTONUP: gb._right_mouse_up_handler(msg, wp, lp)
        case MyMessages.RIGHT_CLICK: gb._right_mouse_click_handler()
        case con.WM_MOUSEWHEEL: gb._mouse_wheel_handler(msg, wp, lp)
        case con.WM_MOUSEMOVE: gb._mouse_move_handler(msg, wp, lp)
        case con.WM_MOUSELEAVE: gb._mouse_leave_handler()

        case con.WM_ERASEBKGND:
            if gb._draw_flag:
                rc = api.get_client_rect(hw)
                rc.top += 10 # We didn't want to fill the 10 points on top.
                rc.bottom -= 2 # And 2 points in bottom.
                api.FillRect(wp, byref(rc), gb._bk_brush)
                return 1
            # NOTE: Do not return anything outside the 'if', as it will make every static control a mess.

        case con.WM_PAINT:
            # Let the control do it's painting works.
            ret = api.DefSubclassProc(hw, msg, wp, lp)

            # Now, we can draw the text over this group box.
            gb._draw_text()
            return ret


    return api.DefSubclassProc(hw, msg, wp, lp)



