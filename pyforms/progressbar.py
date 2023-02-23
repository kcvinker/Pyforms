
# Created on 21-Jan-2023 00:41:20

from ctypes import byref, create_unicode_buffer
from .control import Control
from . import constants as con
from .commons import MyMessages
from .enums import ControlType, ProgressBarStyle, ProgressBarState
from .apis import SUBCLASSPROC
from . import apis as api
from .colors import Color
# from .winmsgs import log_msg

pgb_dict = {}
pgb_style = con.WS_CHILD | con.WS_VISIBLE | con.PBS_SMOOTH | con.WS_OVERLAPPED
pgb_exstyle = 0# con.WS_EX_CLIENTEDGE

class ProgressBar(Control):

    _count = 1
    __slots__ = ("_bk_brush", "_bar_style", "_vertical", "_min_value", "_max_value", "_step", "_value", "_percentage", "_state",
                "_speed")
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
        self._state = ProgressBarState.NORMAL
        self._vertical = False
        self._min_value = 0
        self._max_value = 100
        self._step = 1
        self._value = 0
        self._speed = 30
        self._percentage = False
        ProgressBar._count += 1


    # -region Public funcs

    def create_handle(self):
        """Create progress bar's handle"""
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
        """Increment value to one step"""
        self._value = self._step if self._value == self._max_value else self._value + self._step
        if self._is_created: api.SendMessage(self._hwnd, con.PBM_STEPIT, 0, 0)

    def start_marquee(self):
        """Srat marquee animation in progress bar."""
        if self._is_created and self._bar_style == ProgressBarStyle.MARQUEE_STYLE:
            api.SendMessage(self._hwnd, con.PBM_SETMARQUEE, 1, self._speed)

    def stop_marquee(self):
        """Stop marquee animation of progress bar."""
        if self._is_created and self._bar_style == ProgressBarStyle.MARQUEE_STYLE:
            api.SendMessage(self._hwnd, con.PBM_SETMARQUEE, 0, 0)

    # -endregion Public funcs

    # -region Private funcs

    # Draw percentage text on progress bar
    def draw_percentage(self):
        ss = api.SIZE()
        txt = create_unicode_buffer(f"{self._value}%")
        hdc = api.GetDC(self._hwnd)
        api.SelectObject(hdc, self._font._hwnd)
        api.GetTextExtentPoint32(hdc, txt, len(txt), byref(ss))
        x = (self._width - ss.cx) // 2
        y = (self._height - ss.cy) // 2
        api.SetBkMode(hdc, con.TRANSPARENT)
        api.SetTextColor(hdc, self._fg_color.ref)
        api.TextOut(hdc, x, y, txt, len(txt) )
        api.ReleaseDC(self._hwnd, hdc)


    # -endregion Private funcs

    # -region Properties

    @property
    def value(self):
        """Returns the value of progress bar"""
        return self._value

    @value.setter
    def value(self, value: int):
        """Set the value of progress bar"""
        self._value = value
        if self._is_created: api.SendMessage(self._hwnd, con.PBM_SETPOS, value, 0)
    #-------------------------------------------------------------------------------[1]

    @property
    def step(self):
        """Returns the step property of progress bar"""
        return self._step

    @step.setter
    def step(self, value: int):
        """Set the step property of progress bar"""
        self._step = value
    #-------------------------------------------------------------------------------[2]

    @property
    def state(self):
        """Set the state of progress bar. Check ProgressBarState enum."""
        return self._state

    @state.setter
    def state(self, value: ProgressBarState):
        """Set the state of progress bar. Check ProgressBarState enum."""
        self._state = value
        api.SendMessage(self._hwnd, con.PBM_SETSTATE, value, 0);
    #-------------------------------------------------------------------------------[3]

    @property
    def style(self) -> ProgressBarStyle:
        """Returns the style of progress bar. Check ProgressBarStyle enum."""
        return self._bar_style

    @style.setter
    def style(self, value: ProgressBarStyle):
        """Set the style of progress bar. Check ProgressBarStyle enum."""
        if self._bar_style != value and self._is_created:
            self.value = 0
            if value == ProgressBarStyle.BLOCK_STYLE:
                self._style ^= con.PBS_MARQUEE
                self._style |= con.PBS_SMOOTH
            else:
                self._style ^= con.PBS_SMOOTH
                self._style |= con.PBS_MARQUEE

            api.SetWindowLongPtr(self.handle, con.GWL_STYLE, self._style)
            if value == ProgressBarStyle.MARQUEE_STYLE:
                api.SendMessage(self._hwnd, con.PBM_SETMARQUEE, 1, self._speed)

        self._bar_style = value

    # -endregion Properties

#End ProgressBar

@SUBCLASSPROC
def pgb_wnd_proc(hw, msg, wp, lp, scID, refData):
    # log_msg(msg)
    pgb = pgb_dict[hw]
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, pgb_wnd_proc, scID)
            del pgb_dict[hw]

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
            if pgb._percentage and pgb._bar_style != ProgressBarStyle.MARQUEE_STYLE: pgb.draw_percentage()
            return ret

    return api.DefSubclassProc(hw, msg, wp, lp)

