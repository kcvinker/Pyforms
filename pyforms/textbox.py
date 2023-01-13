
# Created on 22-Nov-2022 00:54:20

from ctypes.wintypes import HWND, UINT, HDC
from ctypes import WINFUNCTYPE
# import ctypes as ctp


from .control import Control
from .commons import MyMessages
from .enums import ControlType, TextCase, TextType, TextAlignment
from .apis import LRESULT, UINT_PTR, DWORD_PTR, WPARAM, LPARAM
from . import apis as api
from .colors import Color
from . import constants as con
# from . import winmsgs
import sys

tb_dict = {}
tb_style = con.WS_CHILD | con.WS_VISIBLE | con.ES_LEFT | con.WS_TABSTOP | con.ES_AUTOHSCROLL | con.WS_MAXIMIZEBOX | con.WS_OVERLAPPED
tb_ex_style = con.WS_EX_LEFT | con.WS_EX_LTRREADING  | con.WS_EX_CLIENTEDGE | con.WS_EX_NOPARENTNOTIFY


class TextBox(Control):

    _count = 1
    __slots__ = ( "_multi_line", "_hide_sel", "_read_only", "_txt_case", "_txt_type", "_txt_align", "_bk_brush")

    def __init__(self, parent, xpos: int = 10, ypos: int = 10, width: int = 120, height: int = 23) -> None:
        super().__init__()
        self._cls_name = "Edit"
        self.name = f"TextBox_{TextBox._count}"
        self._ctl_type = ControlType.TEXT_BOX
        self._parent = parent
        self._font = parent._font
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._is_textable = True
        self._style = tb_style
        self._ex_style = tb_ex_style

        # self._fg_color = Color(0)
        self._bg_color = Color(0xFFFFFF)
        self._bk_brush = api.CreateSolidBrush(self._bg_color.ref)

        # self._draw_mode = ControlDrawMode.NO_DRAW
        # self._draw_flag = 0
        self._multi_line = False
        self._hide_sel = False
        self._read_only = False
        self._txt_case = TextCase.NORMAL
        self._txt_type = TextType.NORMAL
        self._txt_align = TextAlignment.LEFT
        # self._text = "ert"

        TextBox._count += 1

    def create_handle(self):
        self._set_style()
        self._create_control()
        if self._hwnd:
            tb_dict[self._hwnd] = self
            self._set_subclass(tb_wnd_proc)
            self._set_font_internal()
            # print("edit hwnd ", self._hwnd)


    def _set_style(self):
        if self._multi_line: self._style |= con.ES_MULTILINE | con.ES_WANTRETURN
        if self._hide_sel: self._style |= con.ES_NOHIDESEL
        if self._read_only: self._style |= con.ES_READONLY

        if self._txt_case == TextCase.LOWER:
            self._style |= con.ES_LOWERCASE
        elif self._txt_case == TextCase.UPPER:
            self._style |= con.ES_UPPERCASE

        if self._txt_type == TextType.NUM_ONLY:
            self._style |= con.ES_NUMBER
        elif self._txt_type == TextType.PASSWORD:
            self._style |= con.ES_PASSWORD

        if self._txt_align == TextAlignment.CENTER:
            self._style |= con.ES_CENTER
        elif self._txt_align == TextAlignment.RIGHT:
            self._style |= con.ES_RIGHT

    def _tb_color_msg_handler(self, wp):
        hdc = HDC(wp)
        api.SetBkMode(hdc, 1) # TRANSPARENT
        res = api.CreateSolidBrush(self._bg_color.clrRef)
        # print(f"{type(res) = }")


    @Control.text.getter
    def text(self):
        if self._is_created:
            #api.SendMessage(self._hwnd, con.WM_GETTEXT, 0, 0)
            return self._get_ctrl_text()
        else:
            return self._text

    # @Control.text.setter
    # def text(self, value: str):
    #     self._text = value
    #     if self._is_created: self._set_ctrl_text(value)



#End TextBox

@WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR)
def tb_wnd_proc(hw, msg, wp, lp, scID, refData):
    # printWinMsg(msg)
    # winmsgs.log_msg(msg)
    tb = tb_dict[hw]
    match msg:
        case con.WM_DESTROY:
            api.DeleteObject(tb._bk_brush)
            api.RemoveWindowSubclass(hw, tb_wnd_proc, scID)
            # print("remove subclass of ", tb.name)

        # case con.WM_SETFOCUS: tb._got_focus_handler()
        # case con.WM_KILLFOCUS: tb._lost_focus_handler()
        case con.WM_LBUTTONDOWN: tb._left_mouse_down_handler(msg, wp, lp)
        case con.WM_LBUTTONUP: tb._left_mouse_up_handler(msg, wp, lp)
        case MyMessages.MOUSE_CLICK: tb._mouse_click_handler()
        case con.WM_RBUTTONDOWN: tb._right_mouse_down_handler(msg, wp, lp)
        case con.WM_RBUTTONUP: tb._right_mouse_up_handler(msg, wp, lp)
        case MyMessages.RIGHT_CLICK: tb._right_mouse_click_handler()
        case con.WM_MOUSEWHEEL: tb._mouse_wheel_handler(msg, wp, lp)
        case con.WM_MOUSEMOVE: tb._mouse_move_handler(msg, wp, lp)
        case con.WM_MOUSELEAVE: tb._mouse_leave_handler()

        # case MyMessages.LABEL_COLOR:
        #     print("lbl clr")
        #     api.DefSubclassProc(hw, msg, wp, lp)
        #     return 0

        case MyMessages.EDIT_COLOR:
            if tb._draw_flag:
                if tb._draw_flag & 1: api.SetTextColor(wp, tb._fg_color.ref)
                if tb._draw_flag & 2: api.SetBkColor(wp, tb._bg_color.ref)
                # if tb._draw_flag == 1:
                #     return api.GetStockObject(con.DC_BRUSH)
                # else:
            return tb._bk_brush


        case MyMessages.CTL_COMMAND:
            ncode = api.HIWORD(wp)
            match ncode:
                case con.EM_GETRECT:
                    return 1
                case con.EM_SETRECT:
                    return 1

        # case con.WM_NCPAINT:
        #     return 0


        # case con.WM_GETTEXT:
        #     # This is a hack. We can save lot of CPU time by this.
        #     # If we manually get the text with GetWindowText function, it take 250+ us.
        #     # But in this way, getting the text will take only 4-5 us.

        #     api.DefSubclassProc(hw, msg, wp, lp)
        #     tb._text = cast(lp, ctp.c_wchar_p).value

        # case MyMessages.CTRL_NOTIFY:
        #     tb.log("notify msg")




    return api.DefSubclassProc(hw, msg, wp, lp)






