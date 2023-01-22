

# datetimepicker module - Created on 10-Dec-2022 17:45:20

from ctypes.wintypes import HWND, UINT
from ctypes import WINFUNCTYPE, byref, sizeof, addressof, create_unicode_buffer, cast, create_string_buffer
# import ctypes as ctp

from .control import Control
from . import constants as con
from .commons import MyMessages
from .enums import ControlType, DateFormat
from .events import EventArgs, DateTimeEventArgs
from .apis import LRESULT, UINT_PTR, DWORD_PTR, LPNMHDR, LPNMDATETIMECHANGE, WPARAM, LPARAM, SUBCLASSPROC
from . import apis as api
from .colors import Color
from datetime import datetime

dtp_dict = {}
dtp_style = con.WS_CHILD | con.WS_VISIBLE
OBJ_BRUSH = 0x00000002

# print("size of cuint ", sizeof(c_uint) )

class DateTimePicker(Control):

    """DateTimePicker control """
    Control.icc.init_comm_ctls(con.ICC_DATE_CLASSES)
    _count = 1
    __slots__ = ( "_show_week_num", "_no_today_circle", "_no_today", "_no_trail_dates", "_short_date_names", "_show_updown", "_format", "_format_str",
                    "_fd_year",  "_fg_color", "_bg_color", "on_selection_committed", "on_list_closed", "_value", "_event_handled", "_bk_brush",
                    "_right_align", "_cal_style", "_auto_size", "on_calendar_opened", "on_value_changed", "on_calendar_closed"  )


    def __init__(self, parent, xpos: int = 10, ypos: int = 10) -> None:
        super().__init__()

        self._cls_name = "SysDateTimePick32"
        self.name = f"DateTimePicker{DateTimePicker._count}"
        self._ctl_type = ControlType.DATE_TIME_PICKER
        self._parent = parent
        self._bg_color = Color(0xFFFFFF)
        self._fg_color = Color(0x000000)
        self._font = parent._font
        self._width = 0
        self._height = 0
        self._xpos = xpos
        self._ypos = ypos
        # self._is_textable = True
        self._style = dtp_style
        self._ex_style = 0

        self._show_week_num = False
        self._no_today_circle = False
        self._no_today = False
        self._no_trail_dates = False
        self._short_date_names = False
        self._value = 0
        self._format = DateFormat.CUSTOM_DATE
        self._format_str = "dd-MMM-yyyy"
        self._show_updown = False
        self._fd_year = False
        self._right_align = False
        self._cal_style = 0
        self._event_handled = False
        self._auto_size = True


        # Events
        self.on_value_changed = 0
        self.on_calendar_opened = 0
        self.on_calendar_closed = 0

        DateTimePicker._count += 1


    # Create's combo box handle
    def create_handle(self):

        """Create's calendar handle"""

        self._set_style()
        self._create_control()
        if self._hwnd:
            dtp_dict[self._hwnd] = self
            self._is_created = True

            self._set_font_internal()
            #
            if self._format == DateFormat.CUSTOM_DATE:
                buff = create_unicode_buffer(self._format_str)
                api.SendMessage(self._hwnd, con.DTM_SETFORMATW, 0, addressof(buff))

            if self._cal_style > 0:
                api.SendMessage(self._hwnd, con.DTM_SETMCSTYLE, 0, self._cal_style)

            if self._auto_size:
                ss = api.SIZE()
                api.SendMessage(self._hwnd, con.DTM_GETIDEALSIZE, 0, addressof(ss))
                self._width = ss.cx + 2
                self._height = ss.cy + 5
                api.SetWindowPos(self._hwnd, None, self._xpos, self._ypos, self._width, self._height, con.SWP_NOZORDER)

            # Get current selection from date picker
            st = api.SYSTEMTIME()
            res = api.SendMessage(self._hwnd, con.DTM_GETSYSTEMTIME, 0, addressof(st))
            self._set_subclass(dtp_wnd_proc)
            if res == 0: self._value = self._make_date_time(st)
            # print("dtp handle ", self._hwnd)
            # print("dtp bkg ", self._bg_color)


    # -region private_funcs

    def _set_style(self):
        match self._format:
            case DateFormat.CUSTOM_DATE:
                self._style = con.WS_TABSTOP | con.WS_CHILD| con.WS_VISIBLE | con.DTS_LONGDATEFORMAT | con.DTS_APPCANPARSE
            case DateFormat.LONG_DATE:
                self._style = con.WS_TABSTOP | con.WS_CHILD| con.WS_VISIBLE| con.DTS_LONGDATEFORMAT
            case DateFormat.SHORT_DATE:
                if self._fd_year:
                    self._style = con.WS_TABSTOP | con.WS_CHILD| con.WS_VISIBLE| con.DTS_SHORTDATECENTURYFORMAT
                else:
                    self._style = con.WS_TABSTOP | con.WS_CHILD| con.WS_VISIBLE| con.DTS_SHORTDATEFORMAT
            case DateFormat.TIME_ONLY:
                self._style = con.WS_TABSTOP | con.WS_CHILD| con.WS_VISIBLE| con.DTS_TIMEFORMAT

        if self._show_week_num: self._style |= con.MCS_WEEKNUMBERS
        if self._no_today_circle: self._style |= con.MCS_NOTODAYCIRCLE
        if self._no_today: self._style  |= con.MCS_NOTODAY
        if self._no_trail_dates: self._style |= con.MCS_NOTRAILINGDATES
        if self._short_date_names: self._style |= con.MCS_SHORTDAYSOFWEEK
        if self._right_align: self._style |= con.DTS_RIGHTALIGN
        if self._show_updown: self._style ^= con.DTS_UPDOWN
        self._bk_brush = api.CreateSolidBrush(self._bg_color.ref)




    # -endregion Private funcs

    # -region Properties

    @property
    def format_str(self): return self._format_str

    @format_str.setter
    def format_str(self, value: str):
        self._format_str = value
        self._format = DateFormat.CUSTOM_DATE
        if self._is_created:
            buff = create_string_buffer(self._format_str.encode())
            api.SendMessage(self._hwnd, con.DTM_SETFORMATA, 0, addressof(buff))
    #-----------------------------------------------------------------------------1

    @property
    def format(self)-> DateFormat: return self._format

    @format.setter
    def format(self, value: DateFormat): self._format = value
    #------------------------------------------------------------------------2

    @property
    def right_align(self)-> bool: return self._right_align

    @right_align.setter
    def right_align(self, value: bool): self._right_align = value
    #------------------------------------------------------------------------3

    @property
    def four_digit_year(self)-> bool: return self._fd_year

    @four_digit_year.setter
    def four_digit_year(self, value: bool): self._fd_year = value
    #------------------------------------------------------------------------4

    @property
    def show_updown(self)-> bool: return self._show_updown

    @show_updown.setter
    def show_updown(self, value: bool): self._show_updown = value
    #------------------------------------------------------------------------5

    @property
    def value(self)-> datetime: return self._value

    @value.setter
    def value(self, value: datetime):
        self._value = value
        st = self._make_sys_time(value)
        if self._is_created: api.SendMessage(self._hwnd, con.DTM_SETSYSTEMTIME, 0, addressof(st))
    #--------------------------------------------------------------------------------------------6

    @property
    def show_week_number(self)-> bool: return self._show_week_num

    @show_week_number.setter
    def show_week_number(self, value): self._show_week_num = value
    #----------------------------------------------------------------------7

    @property
    def no_today_circle(self)-> bool: return self._no_today_circle

    @no_today_circle.setter
    def no_today_circle(self, value): self._no_today_circle = value
    #-------------------------------------------------------------------------8

    @property
    def no_today(self)-> bool: return self._no_today

    @no_today.setter
    def no_today(self, value): self._no_today = value
    #---------------------------------------------------------9

    @property
    def no_trailing_dates(self)-> bool: return self._no_trail_dates

    @no_trailing_dates.setter
    def no_trailing_dates(self, value): self._no_trail_dates = value
    #-------------------------------------------------------------------------10

    @property
    def short_date_names(self)-> bool: return self._short_date_names

    @short_date_names.setter
    def short_date_names(self, value): self._short_date_names = value
    #---------------------------------------------------------------------------11

    # -endregion Properties
    x = 100 # Dummy
    #dummy line


# End DateTimePicker

# @WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR)
@SUBCLASSPROC
def dtp_wnd_proc(hw, msg, wp, lp, scID, refData):
    # printWinMsg(msg)
    dtp = dtp_dict[hw]
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, dtp_wnd_proc, scID)
            # print("remove subclass for - ", dtp.name)

        case MyMessages.CTRL_NOTIFY:
            nm = cast(lp, LPNMHDR).contents
            # print(f"reach 246 {con.DTN_WMKEYDOWNW = } {nm.code = }" )
            match nm.code:
                case con.DTN_USERSTRINGW:
                     # if dtp.on_text_changed:
                     dts = cast(lp, api.LPNMDATETIMESTRINGW).contents
                     dea = DateTimeEventArgs(dts.pszUserString, dts.st)
                    #  print(dts.st.wYear)
                     return 0

                # case con.DTN_WMKEYDOWNW:
                #     print("wm key down ")

                case con.DTN_DROPDOWN:
                    if dtp.on_calendar_opened:
                        dtp.on_calendar_opened(dtp, EventArgs())
                        return 0

                case con.DTN_CLOSEUP:
                    if dtp.on_calendar_closed:
                        dtp.on_calendar_closed(dtp, EventArgs())
                        return 0

                case con.DTN_DATETIMECHANGE:
                    # For unknown reason, this notification occurs two times back to back.
                    # So, we need to use a boolean flag to suppress one notification.
                    if dtp._event_handled:
                        dtp._event_handled = False
                    else:
                        # print("273")
                        dtp._event_handled = True
                        dic = cast(lp, LPNMDATETIMECHANGE).contents
                        dtp._value = dtp._make_date_time(dic.st)
                        if dtp.on_value_changed:
                            dtp.on_value_changed(dtp, EventArgs())
                            return 0

        case con.WM_SETFOCUS: dtp._got_focus_handler()
        case con.WM_KILLFOCUS: dtp._lost_focus_handler()
        case con.WM_LBUTTONDOWN: dtp._left_mouse_down_handler(msg, wp, lp)
        case con.WM_LBUTTONUP: dtp._left_mouse_up_handler(msg, wp, lp)
        case MyMessages.MOUSE_CLICK: dtp._mouse_click_handler()
        case con.WM_RBUTTONDOWN: dtp._right_mouse_down_handler(msg, wp, lp)
        case con.WM_RBUTTONUP: dtp._right_mouse_up_handler(msg, wp, lp)
        case MyMessages.RIGHT_CLICK: dtp._right_mouse_click_handler()
        case con.WM_MOUSEWHEEL: dtp._mouse_wheel_handler(msg, wp, lp)
        case con.WM_MOUSEMOVE: dtp._mouse_move_handler(msg, wp, lp)
        case con.WM_MOUSELEAVE: dtp._mouse_leave_handler()

        # case MyMessages.LABEL_COLOR:
        #     print("label color")
        # #     if dtp._draw_flag:

        # #         if dtp._draw_flag & 1: api.SetTextColor(wp, dtp._fg_color.ref)
        # #         if dtp._draw_flag & 2:

        # #             api.SetBkColor(wp, dtp._bg_color.ref)
        # #     # print("2. brush in mymessage: ", dtp._bk_brush)
        #     api.SetBkColor(wp, dtp._bg_color.ref)
        #     return dtp._bk_brush

        # # case MyMessages.EDIT_COLOR:
        # #     print("edit clooll")
        # case con.WM_CTLCOLOREDIT:
        #     print("edit color")
        #     return dtp._bk_brush
        # case con.WM_CTLCOLORSTATIC:
        #     print("22222 color")


        # case con.WM_ERASEBKGND:
        #     # api.SelectObject(wp, dtp._bk_brush)
        #     api.DefSubclassProc(hw, msg, wp, lp)

        #     rc = api.get_client_rect(hw)
        #     api.FillRect(wp, byref(rc), dtp._bk_brush)
        #     api.InvalidateRect(hw, byref(rc), True)

        #     return True
        # case con.WM_PAINT:
        #     api.DefSubclassProc(hw, msg, wp, lp)
        #     ps = api.PAINTSTRUCT()
        #     hdc = api.BeginPaint(hw, byref(ps))
        #     api.FillRect(wp, byref(ps.rcPaint), dtp._bk_brush)
        #     print(dtp._get_ctrl_text())
        #     api.InvalidateRect(hw, byref(ps.rcPaint), False)
        #     api.EndPaint(hw, byref(ps))

        #     return True


    return api.DefSubclassProc(hw, msg, wp, lp)