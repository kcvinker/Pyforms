

# Created on 21-Jan-2023 00:41:20

# from ctypes.wintypes import HWND, UINT
from ctypes import byref, create_unicode_buffer
# import ctypes as ctp

from .control import Control
from . import constants as con
from .commons import MyMessages
from .enums import ControlType, ProgressBarStyle
# from .events import EventArgs
from .apis import LRESULT, SUBCLASSPROC
from . import apis as api
from .colors import Color, COLOR_BLACK

# from horology import Timing
from .winmsgs import log_msg

pgb_dict = {}
pgb_style = con.WS_CHILD | con.WS_VISIBLE | con.PBS_SMOOTH | con.WS_OVERLAPPED
pgb_exstyle = 0# con.WS_EX_CLIENTEDGE

class ProgressBar(Control):

    _count = 1
    __slots__ = ("_bk_brush", "_bar_style", "_vertical", "_min_value", "_max_value", "_step", "_value", "_percentage")
    def __init__(self, parent, xpos: int = 10, ypos: int = 10, width: int = 180, height: int = 25 ) -> None:
        super().__init__()
        self._cls_name = "msctls_progress32"
        self.name = f"ProgressBar_{ProgressBar._count}"
        # self._text = self.name if txt == "" else txt
        self._ctl_type = ControlType.PROGRESS_BAR
        self._parent = parent
        # self._bg_color = Color(parent._bg_color)
        self._fg_color = Color(0x000000)
        self._font = parent._font
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._is_textable = False
        self._style = pgb_style
        self._ex_style = pgb_exstyle
        self._draw_flag = 0

        self._bar_style = ProgressBarStyle.BLOCK_STYLE
        self._vertical = False
        self._min_value = 0
        self._max_value = 100
        self._step = 1
        self._value = 0
        self._percentage = False
        # self._draw_perc = False


        ProgressBar._count += 1


    # -region Public funcs
    def create_handle(self):
        if self._bar_style == ProgressBarStyle.MARQUEE_STYLE: self._style |= con.PBS_MARQUEE
        if self._vertical: self._style |= con.PBS_VERTICAL

        self._create_control()
        if self._hwnd:
            pgb_dict[self._hwnd] = self
            self._set_subclass(pgb_wnd_proc)
            self._set_font_internal()
            if self._min_value != 0 or self._max_value != 100:
                api.SendMessage(self._hwnd, con.PBM_SETRANGE32, self._min_value, self._max_value)
            api.SendMessage(self._hwnd, con.PBM_SETSTEP, self._step, 0)


    def increment(self):
        if self._is_created: api.SendMessage(self._hwnd, con.PBM_STEPIT, 0, 0)






    # -endregion Public funcs

    # -region Private funcs
    # def _adjustBorder(self):
    #     if self._border_style == ProgressBarBorder.SUNKEN:
    #         self._style |= con.SS_SUNKEN
    #     else:
    #         self._style = con.WS_BORDER

    def draw_percentage(self):
        ss = api.SIZE()



        # rc = api.RECT(left, 3, 25, self.height - 1)
        value = api.SendMessage(self._hwnd, con.PBM_GETPOS, 0, 0)
        txt = create_unicode_buffer(f"{value}%")
        hdc = api.GetDC(self._hwnd)
        api.SelectObject(hdc, self._font._hwnd)
        api.GetTextExtentPoint32(hdc, txt, len(txt), byref(ss))
        x = (self._width - ss.cx) // 2
        y = (self._height - ss.cy) // 2
        api.SetBkMode(hdc, con.TRANSPARENT)
        api.SetTextColor(hdc, self._fg_color.ref)
        # api.DrawText(hdc, , -1, byref(rc), con.DT_CENTER| con.DT_SINGLELINE )
        api.TextOut(hdc, x, y, txt, len(txt) )
        api.ReleaseDC(self._hwnd, hdc)









    # -endregion Private funcs

    # -region Properties

    # @property
    # def auto_size(self): return self._auto_size

    @property
    def value(self): return self._value

    @value.setter
    def value(self, value: int):
        self._value = value
        if self._is_created: api.SendMessage(self._hwnd, con.PBM_SETPOS, value, 0)

    @property
    def step(self): return self._step

    @step.setter
    def step(self, value: int): self._step = value

    # @property
    # def border_style(self): return self._border_style

    # @border_style.setter
    # def border_style(self, value: ProgressBarBorder): self._border_style = value

    # -endregion Properties
    dummy = 100








#End ProgressBar

# @WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR)
@SUBCLASSPROC
def pgb_wnd_proc(hw, msg, wp, lp, scID, refData):
    # printWinMsg(msg)
    log_msg(msg)
    pgb = pgb_dict[hw]
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, pgb_wnd_proc, scID)

        case con.WM_SETFOCUS: pgb._got_focus_handler()
        case con.WM_KILLFOCUS: pgb._lost_focus_handler()
        case con.WM_LBUTTONDOWN: pgb._left_mouse_down_handler(msg, wp, lp)
        case con.WM_LBUTTONUP: pgb._left_mouse_up_handler(msg, wp, lp)
        case MyMessages.MOUSE_CLICK: pgb._mouse_click_handler()
        case con.WM_RBUTTONDOWN: pgb._right_mouse_down_handler(msg, wp, lp)
        case con.WM_RBUTTONUP: pgb._right_mouse_up_handler(msg, wp, lp)
        case MyMessages.RIGHT_CLICK: pgb._right_mouse_click_handler()
        case con.WM_MOUSEWHEEL: pgb._mouse_wheel_handler(msg, wp, lp)
        case con.WM_MOUSEMOVE: pgb._mouse_move_handler(msg, wp, lp)
        case con.WM_MOUSELEAVE: pgb._mouse_leave_handler()
        case con.WM_PAINT:
            ret = api.DefSubclassProc(hw, msg, wp, lp)
            if pgb._percentage:
                pgb.draw_percentage()
                # pgb._draw_perc = False
            return ret


    return api.DefSubclassProc(hw, msg, wp, lp)



