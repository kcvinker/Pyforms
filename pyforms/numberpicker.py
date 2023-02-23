
# numberpicker module Created on 12-Dec-2022 23:04:20

from ctypes.wintypes import HWND, UINT, HDC
from ctypes import WINFUNCTYPE, byref, cast

from .control import Control
from . import constants as con
from .commons import MyMessages
from .enums import ControlType, TextAlignment
from .events import EventArgs
from . import apis as api
from .apis import LRESULT, UINT_PTR, DWORD_PTR, WPARAM, LPARAM, SUBCLASSPROC
from .colors import Color, clamp

# from .winmsgs import log_msg

nump_dict = {}
nump_tb_dict = {}
nump_style = con.WS_VISIBLE | con.WS_CHILD  | con.UDS_ALIGNRIGHT | con.UDS_ARROWKEYS | con.UDS_AUTOBUDDY | con.UDS_HOTTRACK
# txtFlag = con.DT_SINGLELINE | con.DT_VCENTER | con.DT_CENTER | con.DT_NOPREFIX


class NumberPicker(Control):
    """NumberPicker class is sometimes known as Spinner or Updown control.
        In .NET family, it's name is NumericUpDown.
    """
    Control.icc.init_comm_ctls(con.ICC_UPDOWN_CLASS)
    _count = 1
    __slots__ = ( "_hide_caret", "_track_mouse_leave", "_btn_on_left", "_has_sep", "_top_edge_flag", "_bot_edge_flag",
                    "_auto_rotate", "_min_range", "_max_range", "_value", "_step", "_deci_precis", "_buddy_rect",
                    "_buddy_style", "_buddy_ex_style", "_buddy_hwnd", "_buddy_cid", "_buddy_subcls_id", "_linex", "_destroy_count",
                    "_buddy_subcls_proc", "_txt_pos", "on_value_changed", "_my_rect", "_ud_rect", "_key_pressed" )

    def __init__(self, parent, xpos: int = 10, ypos: int = 10, width: int = 80, height: int = 24 ) -> None:
        super().__init__()
        self._cls_name = "msctls_updown32"
        self.name = f"NumberPicker_{NumberPicker._count}"
        self._ctl_type = ControlType.NUM_PICKER
        self._parent = parent
        self._bg_color = Color(0xFFFFFF)
        self._font = parent._font
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._style = nump_style
        self._ex_style = 0x00000000
        self._btn_on_left = False
        self._max_range = 100
        self._min_range = 0
        self._deci_precis = 0
        self._auto_rotate = False
        self._step = 1
        self._buddy_style = con.WS_CHILD | con.WS_VISIBLE | con.ES_NUMBER | con.WS_BORDER
        self._buddy_ex_style = con.WS_EX_LEFT | con.WS_EX_LTRREADING
        self._value = self._min_range
        self._txt_pos = TextAlignment.LEFT
        self._buddy_cid = 0
        self._has_sep = False
        self._buddy_rect = api.RECT()
        self._my_rect = api.RECT()
        self._ud_rect = api.RECT()
        self._track_mouse_leave = False
        self._key_pressed = False
        self._top_edge_flag = con.BF_TOPLEFT
        self._bot_edge_flag = con.BF_BOTTOM
        self._hide_caret = False
        self._linex = 0
        self._destroy_count = 0

        #Events
        self.on_value_changed = 0

        NumberPicker._count += 1


    # -region Public funcs
    def create_handle(self):
        self._np_set_styles()
        self._set_ctl_id()
        self._hwnd = api.CreateWindowEx(self._ex_style,
                                        self._cls_name,
                                        self._text,
                                        self._style,
                                        0, 0, 0, 0,
                                        self._parent._hwnd,
                                        self._cid,
                                        self._parent.wnd_class.hInstance, None )
        if self._hwnd:
            nump_dict[self._hwnd] = self
            self._set_subclass(np_wnd_proc)
            self._set_font_internal()

            self._buddy_cid = Control._ctl_id
            self._buddy_subcls_id = Control._subclass_id
            Control._subclass_id += 1
            if self._btn_on_left: self.width -= 2
            self._buddy_hwnd = api.CreateWindowEx(  self._buddy_ex_style,
                                                    "Edit",
                                                    self._text,
                                                    self._buddy_style,
                                                    self._xpos,
                                                    self._ypos,
                                                    self._width,
                                                    self._height,
                                                    self._parent._hwnd,
                                                    self._buddy_cid,
                                                    self._parent.wnd_class.hInstance, None )

            if self._buddy_hwnd:
                self._is_created = True

                Control._ctl_id += 1
                api.SetWindowSubclass(self._buddy_hwnd, buddy_wnd_proc, self._buddy_subcls_id, self._hwnd)
                api.SendMessage(self._buddy_hwnd, con.WM_SETFONT, self.font.handle, 1)
                old_buddy = api.SendMessage(self._hwnd, con.UDM_SETBUDDY, self._buddy_hwnd, 0)
                api.SendMessage(self._hwnd, con.UDM_SETRANGE32, self._min_range, self._max_range)

                api.GetClientRect(self._buddy_hwnd, byref(self._buddy_rect))
                api.GetClientRect(self._hwnd, byref(self._ud_rect))
                api.SetRect(byref(self._my_rect), self._xpos, self._ypos, (self._xpos + self._width), (self._ypos + self._height))
                self._display_value()
                self._resize_buddy()
                if old_buddy: api.SendMessage(old_buddy, MyMessages.BUDDY_RESET, 0, 0)



    # -endregion Public funcs

    # -region Private funcs
    # Set number picker style bits
    def _np_set_styles(self):
        if self._btn_on_left:
            self._style ^= con.UDS_ALIGNRIGHT
            self._style |= con.UDS_ALIGNLEFT
            self._top_edge_flag = con.BF_TOP
            self._bot_edge_flag = con.BF_BOTTOMRIGHT
            if self._txt_pos == TextAlignment.LEFT: self._txt_pos = TextAlignment.RIGHT

        match self._txt_pos:
            case TextAlignment.LEFT: self._buddy_style |= con.ES_LEFT
            case TextAlignment.CENTER: self._buddy_style |= con.ES_CENTER
            case TextAlignment.RIGHT: self._buddy_style |= con.ES_RIGHT

    # Internal function to display value
    def _display_value(self):
        if self._has_sep:
            self._text = f"{self._value:,.{self._deci_precis}f}"
        else:
            self._text = f"{self._value:.{self._deci_precis}f}"
        api.SetWindowText(self._buddy_hwnd, self._text )

    # Internal function to calculate value
    def _set_numpick_value(self, delta: int):
        value = self._value + (delta * self._step)
        if self._auto_rotate:
            if value > self._max_range:
                self._value = self._min_range
            elif value < self._min_range:
                self._value = self._max_range
            else:
                self._value = value
        else:
            self._value = clamp(value, self.min_range, self._max_range)

    # Internal function to check if mouse is over us.
    def _is_mouse_upon_me(self) -> bool:
        # If this returns False, mouse_leave event will triggered
        # Since, updown control is a combo of an edit and button controls...
        # we have no better options to control the mouse enter & leave mechanism.
        # Now, we create an imaginary rect over the bondaries of these two controls.
        # If mouse is inside that rect, there is no mouse leave. Perfect hack.
        pt = api.POINT()
        api.GetCursorPos(byref(pt))
        api.ScreenToClient(self._parent._hwnd, byref(pt))
        res = api.PtInRect(byref(self._my_rect), pt)
        return res

    # Internal function to resize buddy edit
    def _resize_buddy(self):
        swp_flag = con.SWP_NOACTIVATE | con.SWP_NOZORDER
        if self._btn_on_left:
            api.SetWindowPos(self._buddy_hwnd, None,
                            self._xpos + self._ud_rect.right,
                            self._ypos,
                            self._buddy_rect.right,
                            self._buddy_rect.bottom, swp_flag)
            self._linex = self._buddy_rect.left
        else:
            api.SetWindowPos(self._buddy_hwnd, None,
                            self._xpos,
                            self._ypos,
                            self._buddy_rect.right - 2,
                            self._buddy_rect.bottom, swp_flag)

            self._linex = self._buddy_rect.right - 3

    # -endregion Private funcs

    # -region Properties


    @property
    def decimal_points(self):
        """Get the decimal points of NumberPicker"""
        return self._deci_precis

    @decimal_points.setter
    def decimal_points(self, value: int):
        """Set the decimal points of NumberPicker"""
        self._deci_precis = value
    #-----------------------------------------------------------------------[1]

    @property
    def min_range(self):
        """Get minimum value of NumberPicker's range"""
        return self._min_range

    @min_range.setter
    def min_range(self, value: int | float):
        """Set minimum value of NumberPicker's range"""
        self._min_range = value
        if self._is_created:
            api.SendMessage(self._hwnd, con.UDM_SETRANGE32, self._min_range, self._max_range)
    #----------------------------------------------------------------------------------------[2]

    @property
    def max_range(self):
        """Get maximum value of NumberPicker's range"""
        return self._max_range

    @max_range.setter
    def max_range(self, value: int | float):
        """Set maximum value of NumberPicker's range"""
        self._max_range = value
        api.SendMessage(self._hwnd, con.UDM_SETRANGE32, self._min_range, self._max_range)
    #-----------------------------------------------------------------------------------[3]

    @property
    def auto_rotate(self):
        """Returns true if auto rotate is enabled. This means, it jumped from min value to max and vice versa."""
        return self._auto_rotate

    @auto_rotate.setter
    def auto_rotate(self, value: bool):
        """Set true if auto rotate is enabled. This means, it jumped from min value to max and vice versa."""
        self._auto_rotate = value
    #-----------------------------------------------------------------------[4]

    @property
    def step(self):
        """Get the step value of NumberPicker. Step is the amount of value jumped at one click."""
        return self._step

    @step.setter
    def step(self, value: int):
        """Set the step value of NumberPicker. Step is the amount of value jumped at one click."""
        self._step = value
    #-----------------------------------------------------[5]

    @property
    def value(self) -> float:
        """Get the NumberPicker's value"""
        return self._value

    @value.setter
    def value(self, value: float):
        """Set the NumberPicker's value"""
        self._value = value
        if self._is_created:
            api.SetWindowText(self._buddy_hwnd, f"{self._value:.{self._deci_precis}f}")
    #----------------------------------------------------------------------------------[6]


    @property
    def button_on_left(self):
        """Returns true if button is set on left side"""
        return self._btn_on_left

    @button_on_left.setter
    def button_on_left(self, value: bool):
        """Set true if button is set on left side"""
        self._btn_on_left = value
        if self._is_created: pass # api.SendMessage(self._buddy_hwnd, con.EM_SETSEL, -1, 0)
        # TODO : Change window style constants here to update the control.
    #-------------------------------------------------------------------[8]

    @property
    def has_seperator(self):
        """Returns true if seperator is enabled"""
        return self._has_sep

    @has_seperator.setter
    def has_seperator(self, value: bool):
        """Set true if seperator is enabled"""
        self._has_sep = value
    #-----------------------------------------------------[9]

    @property
    def hide_caret(self):
        """Returns true if caret is hidden"""
        return self._hide_caret

    @hide_caret.setter
    def hide_caret(self, value: bool):
        """Set true to hide the caret"""
        self._hide_caret = value
    #-----------------------------------------------------[10]

    @Control.on_mouse_enter.setter
    def on_mouse_enter(self, value):
        """Set mouse evnte event handler"""
        self._on_mouse_enter = value
        self._track_mouse_leave = True
    #--------------------------------------------[11]


    @Control.on_mouse_leave.setter
    def on_mouse_leave(self, value):
        """Set mouse leave event handler"""
        self._on_mouse_leave = value
        self._track_mouse_leave = True
    #--------------------------------------------[12]
    # -endregion Properties


#End NumberPicker


@SUBCLASSPROC
def np_wnd_proc(hw, msg, wp, lp, scID, refData) -> LRESULT:

    np = nump_dict[hw]
    # log_msg(msg, f"Main proc {np.name}")
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, np_wnd_proc, scID)
            np._destroy_count += 1
            if np._destroy_count == 2: del nump_dict[hw]

        case MyMessages.CTRL_NOTIFY:
            nm = cast(lp, api.LPNMUPDOWN).contents
            if nm.hdr.code == con.UDN_DELTAPOS:
                np._value = float(np._get_ctrl_text_ex(np._buddy_hwnd))
                np._set_numpick_value(nm.iDelta)
                np._display_value()
                if np.on_value_changed: np.on_value_changed(np, EventArgs())

        case con.WM_SETFOCUS: np._got_focus_handler()
        case con.WM_KILLFOCUS: np._lost_focus_handler()
        case con.WM_LBUTTONDOWN: np._left_mouse_down_handler(msg, wp, lp)
        case con.WM_LBUTTONUP: np._left_mouse_up_handler(msg, wp, lp)
        case MyMessages.MOUSE_CLICK: np._mouse_click_handler()
        case con.WM_RBUTTONDOWN: np._right_mouse_down_handler(msg, wp, lp)
        case con.WM_RBUTTONUP: np._right_mouse_up_handler(msg, wp, lp)
        case MyMessages.RIGHT_CLICK: np._right_mouse_click_handler()
        case con.WM_MOUSEWHEEL: np._mouse_wheel_handler(msg, wp, lp)
        case con.WM_MOUSEMOVE: np._mouse_move_handler(msg, wp, lp)
        case con.WM_MOUSELEAVE:
            if np._track_mouse_leave:
                if not np._is_mouse_upon_me():
                    np._is_mouse_entered = False
                    if np.on_mouse_leave: np.on_mouse_leave(np, EventArgs())

    return api.DefSubclassProc(hw, msg, wp, lp)



@WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR)
def buddy_wnd_proc(hw, msg, wp, lp, scID, refData) -> LRESULT:

    np = nump_dict[refData]
    # log_msg(msg, np.name)
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, buddy_wnd_proc, scID)
            np._destroy_count += 1
            if np._destroy_count == 2: del nump_dict[refData]

        case MyMessages.EDIT_COLOR:
            # Whether user selects a back color or not, we must set the back color.
            # Otherwise, NumberPicker will be drawn in default control back color by DefWndProc
            # hdc = HDC(wp)
            if np._draw_flag & 1: api.SetTextColor(wp, np._fg_color.ref)
            api.SetBkColor(wp, np._bg_color.ref)
            return api.CreateSolidBrush(np._bg_color.ref)

        case con.WM_MOUSELEAVE:
            if np._track_mouse_leave:
                if not np._is_mouse_upon_me():
                    np._is_mouse_entered = False
                    if np.on_mouse_leave: np.on_mouse_leave(np, EventArgs())

        case con.WM_MOUSEMOVE: np._mouse_move_handler(msg, wp, lp)

        case con.EM_SETSEL:
            # Edit control in NumberPicker is not support auto selection.
            return False

        case MyMessages.CTL_COMMAND:
            code = api.HIWORD(wp)
            # print("wm command ", code)
            match code:
                case con.EN_CHANGE:pass
                case con.EN_UPDATE:
                    if np._hide_caret: api.HideCaret(hw)

        case con.WM_KEYDOWN:
            np._key_pressed = True
            np._key_down_handler(wp)

        case con.WM_KEYUP: np._key_up_handler(wp)
        case con.WM_CHAR: np._key_press_handler(wp)
        case con.WM_SETFOCUS: np._got_focus_handler()
        case con.WM_KILLFOCUS:
            # When user manually enter numbers, we need to check that value
            # And displays it in as per our current value protocol.
            if np._key_pressed:
                np._value = float(np._get_ctrl_text_ex(hw))
                np._set_numpick_value(0)
                np._key_pressed = False
                np._display_value()
            np._lost_focus_handler()

        case con.WM_LBUTTONDOWN:
            # Some of the drawing job in edit control is not through the wm_paint message.
            # If we click on it, it will start drawing without sending wm_paint.
            # So, when a click is received in an edit control, we need an immediate redraw.
            # Otherwise, we will lost our beautiful top edge.
            # api.RedrawWindow(hw, None, None, con.RDW_INTERNALPAINT)
            np._left_mouse_down_handler(msg, wp, lp)
        case con.WM_LBUTTONUP: np._left_mouse_up_handler(msg, wp, lp)
        case MyMessages.MOUSE_CLICK: np._mouse_click_handler()
        case con.WM_RBUTTONDOWN: np._right_mouse_down_handler(msg, wp, lp)
        case con.WM_RBUTTONUP: np._right_mouse_up_handler(msg, wp, lp)
        case MyMessages.RIGHT_CLICK: np._right_mouse_click_handler()
        case con.WM_MOUSEWHEEL: np._mouse_wheel_handler(msg, wp, lp)

        case con.WM_PAINT:
            # Edit control needs to be painted by DefSubclassProc function.
            # Otherwise, cursor and text will not be visible, So we need to call it.
            api.DefSubclassProc(hw, msg, wp, lp)

            # Now, Edit's painting job is done and control is ready for our drawing.
            # So, first, we are going to draw 3 edges for this Edit control.
            # Then we, will draw a single line to mask the control border.
            # with Timing("paint time : "): # 60-70 micro secs average
            hdc = api.GetDC(hw)
            api.DrawEdge(hdc, byref(np._buddy_rect), con.BDR_SUNKENOUTER, np._top_edge_flag) # Right code
            api.DrawEdge(hdc, byref(np._buddy_rect), con.BDR_RAISEDINNER, np._bot_edge_flag )
            fpen = api.CreatePen(con.PS_SOLID, 1, np._bg_color.ref) # We use Edit's back color.
            api.SelectObject(hdc, fpen)
            api.MoveToEx(hdc, np._linex, 1, None)
            api.LineTo(hdc, np._linex, np._height - 1)
            api.ReleaseDC(hw, hdc)
            api.DeleteObject(fpen)
            return 1
        case MyMessages.BUDDY_RESET:
            np._resize_buddy()

    return api.DefSubclassProc(hw, msg, wp, lp)