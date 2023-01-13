
# calendarbox module - Created on 30-Nov-2022 00:37:20

from ctypes.wintypes import HWND, UINT, LPCWSTR
from ctypes import WINFUNCTYPE, byref, sizeof, addressof, create_unicode_buffer, cast, c_uint, c_int, c_short
# import ctypes as ctp
import sys

from .control import Control
from . import constants as con
from .commons import MyMessages, get_mousepos_on_msg, point_in_rect
from .enums import ControlType, ViewMode
from .events import EventArgs
from .apis import LRESULT, UINT_PTR, DWORD_PTR, RECT, LPNMHDR, LPNMSELCHANGE, LPNMVIEWCHANGE, NMHDR, WPARAM, LPARAM
from . import apis as api
from .colors import Color
from datetime import datetime, date
# from horology import Timing

cal_dict = {}
cal_style = con.WS_CHILD | con.WS_VISIBLE

# print("size of cuint ", sizeof(c_uint) )

class CalendarBox(Control):

    """CalendarBox control """
    Control.icc.init_comm_ctls(con.ICC_DATE_CLASSES)
    _count = 1
    __slots__ = ( "_show_week_num", "_no_today_circle", "_no_today", "_no_trail_dates", "_short_date_names",
                    "_fg_color", "_bg_color", "on_selection_committed", "on_list_closed", "_value", "_view_mode", "_old_view",
                     "on_view_changed", "on_selection_changed", "on_value_changed"  )

    def __init__(self, parent, xpos: int = 10, ypos: int = 10, width: int = 180, height: int = 150) -> None:
        super().__init__()

        self._cls_name = "SysMonthCal32"
        self.name = f"CalendarBox{CalendarBox._count}"
        self._ctl_type = ControlType.CALENDAR_BOX
        self._parent = parent
        self._bg_color = Color(parent._bg_color)
        self._font = parent._font
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._style = cal_style
        self._ex_style = 0

        self._show_week_num = False
        self._no_today_circle = False
        self._no_today = False
        self._no_trail_dates = False
        self._short_date_names = False
        self._value = 0
        self._view_mode = ViewMode.MONTH_VIEW
        self._old_view = 0

        # Events
        self.on_value_changed = 0
        self.on_view_changed = 0
        self.on_selection_changed = 0

        CalendarBox._count += 1


    # Create's combo box handle
    def create_handle(self):

        """Create's calendar handle"""

        self._set_style()
        self._create_control()
        if self._hwnd:
            cal_dict[self._hwnd] = self
            self._is_created = True
            self._set_subclass(cal_wnd_proc)

            # Set the minimum size for date picker
            rc = RECT()
            api.SendMessage(self._hwnd, con.MCM_GETMINREQRECT, 0, addressof(rc))
            api.SetWindowPos(self._hwnd, None, self._xpos, self._ypos, rc.right, rc.bottom, con.SWP_NOZORDER)

            # Get current selection from date picker
            st = api.SYSTEMTIME()
            api.SendMessage(self._hwnd, con.MCM_GETCURSEL, 0, addressof(st))
            self._set_value(st)


    # -region private_funcs

    def _set_style(self):
        if self._show_week_num: self._styles |= con.MCS_WEEKNUMBERS
        if self._no_today_circle: self._styles |= con.MCS_NOTODAYCIRCLE
        if self._no_today: self._styles  |= con.MCS_NOTODAY
        if self._no_trail_dates: self._styles |= con.MCS_NOTRAILINGDATES
        if self._short_date_names: self._styles |= con.MCS_SHORTDAYSOFWEEK

    def _set_value(self, st):
        self._value = datetime(st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond, st.wMilliseconds)



    # -endregion Private funcs

    # -region Properties

    @property
    def value(self)-> datetime: return self._value

    @value.setter
    def value(self, value: datetime):
        self._value = value
        st = self._make_sys_time(value)
        if self._is_created: api.SendMessage(self._hwnd, con.MCM_SETCURSEL, 0, addressof(st))
    #----------------------------------------------------1

    @property
    def view_mode(self)-> ViewMode: return self._view_mode

    @view_mode.setter
    def view_mode(self, value: ViewMode):
        self._view_mode = value
        if self._is_created: api.SendMessage(self._hwnd, con.MCM_SETCURRENTVIEW, 0, self._view_mode.value)
    #----------------------------------------------------2

    @property
    def old_view_mode(self) -> ViewMode: return self._old_view
    #----------------------------------------------------3

    @property
    def show_week_number(self)-> bool: return self._show_week_num

    @show_week_number.setter
    def show_week_number(self, value): self._show_week_num = value
    #----------------------------------------------------4

    @property
    def no_today_circle(self)-> bool: return self._no_today_circle

    @no_today_circle.setter
    def no_today_circle(self, value): self._no_today_circle = value
    #----------------------------------------------------5

    @property
    def no_today(self)-> bool: return self._no_today

    @no_today.setter
    def no_today(self, value): self._no_today = value
    #----------------------------------------------------6

    @property
    def no_trailing_dates(self)-> bool: return self._no_trail_dates

    @no_trailing_dates.setter
    def no_trailing_dates(self, value): self._no_trail_dates = value
    #----------------------------------------------------7

    @property
    def short_date_names(self)-> bool: return self._short_date_names

    @short_date_names.setter
    def short_date_names(self, value): self._short_date_names = value
    #----------------------------------------------------8

    # -endregion Properties

    #dummy line


# End CalendarBox

@WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR)
def cal_wnd_proc(hw, msg, wp, lp, scID, refData):
    # printWinMsg(msg)
    cal = cal_dict[hw]
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, cal_wnd_proc, scID)
            # print("remove subclass for - ", cal.name)

        case MyMessages.CTRL_NOTIFY:
            nm = cast(lp, LPNMHDR).contents
            match nm.code:
                case con.MCN_SELECT: # 4294966550
                    nms = cast(lp, LPNMSELCHANGE).contents
                    cal._set_value(nms.stSelStart)
                    if cal.on_value_changed: cal.on_value_changed(cal, EventArgs())
                case con.MCN_SELCHANGE:
                    nms = cast(lp, LPNMSELCHANGE).contents
                    cal._set_value(nms.stSelStart)
                    if cal.on_selection_changed: cal.on_selection_changed(cal, EventArgs())

                case con.MCN_VIEWCHANGE:
                    nmv = cast(lp, LPNMVIEWCHANGE).contents
                    cal._view_mode = ViewMode(nmv.dwNewView)
                    cal._old_view = ViewMode(nmv.dwOldView)
                    if cal.on_view_changed: cal.on_view_changed(cal, EventArgs())

        case con.WM_SETFOCUS: cal._got_focus_handler()
        case con.WM_KILLFOCUS: cal._lost_focus_handler()
        case con.WM_LBUTTONDOWN: cal._left_mouse_down_handler(msg, wp, lp)
        case con.WM_LBUTTONUP: cal._left_mouse_up_handler(msg, wp, lp)
        case MyMessages.MOUSE_CLICK: cal._mouse_click_handler()
        case con.WM_RBUTTONDOWN: cal._right_mouse_down_handler(msg, wp, lp)
        case con.WM_RBUTTONUP: cal._right_mouse_up_handler(msg, wp, lp)
        case MyMessages.RIGHT_CLICK: cal._right_mouse_click_handler()
        case con.WM_MOUSEWHEEL: cal._mouse_wheel_handler(msg, wp, lp)
        case con.WM_MOUSEMOVE: cal._mouse_move_handler(msg, wp, lp)
        case con.WM_MOUSELEAVE: cal._mouse_leave_handler()

        # case MyMessages.EDIT_COLOR:
        #     if cal._draw_flag:
        #         if cal._draw_flag & 1: api.SetTextColor(wp, cal._fg_color.ref)
        #         if cal._draw_flag & 2: api.SetBkColor(wp, cal._bg_color.ref)
        #         # if cal._draw_flag == 1:
        #         #     return api.GetStockObject(con.DC_BRUSH)
        #         # else:
        #     return cal._bk_brush



    return api.DefSubclassProc(hw, msg, wp, lp)