
# Created on 22-Nov-2022 00:54:20

# from ctypes.wintypes import HWND, UINT, HDC
from ctypes import byref
# import ctypes as ctp


from .control import Control
from .commons import MyMessages
from .enums import ControlType, TextCase, TextType, TextAlignment
from .apis import SUBCLASSPROC
from . import apis as api
from .colors import Color
from . import constants as con
from . import winmsgs
# import sys

tb_dict = {}
tb_style = con.WS_CHILD | con.WS_VISIBLE | con.ES_LEFT | con.WS_TABSTOP | con.ES_AUTOHSCROLL
tb_ex_style = con.WS_EX_LEFT | con.WS_EX_LTRREADING | con.WS_EX_CLIENTEDGE


class TextBox(Control):

    _count = 1
    __slots__ = ( "_multi_line", "_hide_sel", "_read_only", "_txt_case", "_txt_type", "_txt_align", "_bk_brush")

    def __init__(self, parent, xpos: int = 10, ypos: int = 10, width: int = 120, height: int = 23) -> None:
        super().__init__()
        self._cls_name = "EDIT"
        self.name = f"TextBox_{TextBox._count}"
        self._ctl_type = ControlType.TEXT_BOX
        self._parent = parent
        self._font = parent._font
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._is_textable = True
        self._style = 0x50010080 | con.WS_CLIPCHILDREN
        self._ex_style = 0x00000204

        # self._fg_color = Color(0)
        self._bg_color = Color(0xFFFFFF)


        # self._draw_mode = ControlDrawMode.NO_DRAW
        self._draw_flag = 0
        self._multi_line = False
        self._hide_sel = False
        self._read_only = False
        self._txt_case = TextCase.NORMAL
        self._txt_type = TextType.NORMAL
        self._txt_align = TextAlignment.LEFT
        # self._bk_brush = HBRUSH(0)
        # self._text = "ert"

        TextBox._count += 1

    def create_handle(self):
        self._set_style()
        self._create_control()
        if self._hwnd:
            # self._parent.tbdraw_dict[self._hwnd] = self._tb_color_msg_handler
            tb_dict[self._hwnd] = self

            self._set_subclass(tb_wnd_proc)
            self._set_font_internal()
            # api.InvalidateRect(self._hwnd, None, False)
            # rc = api.get_client_rect(self._hwnd)
            api.RedrawWindow(self._hwnd, None, None, con.RDW_FRAME| con.RDW_INVALIDATE)

            # print("edit hwnd ", self._hwnd)
            # print(f"{sizeof(c_longlong) = }, {sizeof(c_long) = }, {sizeof(c_void_p) = }")


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

        self._bk_brush = api.CreateSolidBrush(self._bg_color.ref)


    # def _tb_color_msg_handler(self, wp):
    #     if self._draw_flag:
    #         if self._draw_flag & 1: api.SetTextColor(wp, self._fg_color.ref)
    #         if self._draw_flag & 2: api.SetBkColor(wp, self._bg_color.ref)
    #         # if self._draw_flag == 1:
    #         #     return api.GetStockObject(con.DC_BRUSH)
    #         # else:
    #     return self._bk_brush


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

# @WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR)
@SUBCLASSPROC
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

        case MyMessages.LABEL_COLOR:
            return tb._bk_brush
            # print("lbl clr")
            # api.DefSubclassProc(hw, msg, wp, lp)
            # return 0

        case MyMessages.EDIT_COLOR:
            if tb._draw_flag:
                if tb._draw_flag & 1: api.SetTextColor(wp, tb._fg_color.ref)
                if tb._draw_flag & 2: api.SetBkColor(wp, tb._bg_color.ref)
                # if tb._draw_flag == 1:
                #     return api.GetStockObject(con.DC_BRUSH)
                # else:
            # tb._parent._tb_brush = HBRUSH(tb._bk_brush)
            return tb._bk_brush

        # case con.WM_PAINT:
        #     return 0#api.DefSubclassProc(hw, msg, wp, lp)

        # case con.WM_ERASEBKGND:
        #     return api.DefSubclassProc(hw, msg, wp, lp)


        # case MyMessages.CTL_COMMAND:
        #     ncode = api.HIWORD(wp)
        #     match ncode:
        #         case con.EM_GETRECT:

        #         case con.EM_SETRECT:
        #             return 1

        case _: return api.DefSubclassProc(hw, msg, wp, lp)







    return api.DefSubclassProc(hw, msg, wp, lp)






