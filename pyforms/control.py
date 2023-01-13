# Created on 08-Nov-2022 00:08:28


# import ctypes

from ctypes.wintypes import UINT, HWND
from ctypes import create_unicode_buffer, byref, addressof, sizeof
import ctypes as ctp
# from win32gui import SendMessage

from .enums import ControlType
from .commons import Font, MyMessages
from .apis import INITCOMMONCONTROLSEX, WPARAM, LPARAM, SUBCLASSPROC, UINT_PTR, DWORD_PTR
from . import apis as api
from . import constants as con
from .events import EventArgs, MouseEventArgs, KeyEventArgs, KeyPressEventArgs
from .colors import get_ref, Color
import datetime
from horology import Timing
# from .forms import StaticData




def initCommonCtls(icx, cls_value):
    icx.dwICC = cls_value
    api.InitCommonControlsEx(byref(icx))
    return 1

class InitComCtls:
    """
    Most of the Windows controls uses CommCtrl32 dll for functioning.
    So we need to initiate that dll with proper class names.
    This task is needed to be done at once per class.
    So this class will handle the job for us. First, it will initiate...
    standard control classes like button, edit etc. Then we need to...
    intentionaly call the 'init_comm_ctls' function for special controls.
    """
    started = False
    icc_ex = INITCOMMONCONTROLSEX()
    # is_date_init = False # DateTimePicker & CalendarBox uses the same ICC value. So we need this flag.

    def __init__(self) -> None:
        self.icc_ex.dwICC = con.ICC_STANDARD_CLASSES
        self.is_date_init = False
        api.InitCommonControlsEx(byref(self.icc_ex))
        InitComCtls.started = True

    def init_comm_ctls(self, ctl_value):
        flag = False
        if ctl_value == 0x100: # If it's ICC_DATECLASS, we need to take special care.
            if self.is_date_init:
                flag = False
            else:
                flag = True
                self.is_date_init = True
        else:
            flag = True

        if flag:
            self.icc_ex.dwICC = ctl_value
            self.icc_ex.dwSize = sizeof(INITCOMMONCONTROLSEX)
            res = api.InitCommonControlsEx(byref(self.icc_ex))


class Control:
    """
    Control class is the base for all other controls and even Form too.
    It supplys plenty of common features like text, background color etc.
    """
    _ctl_id = 101
    _subclass_id = 1001
    icc = InitComCtls()
    __slots__ = ("tvar", "name", "_hwnd", "_text", "_width", "_height", "_style", "_ex_style", "_h_inst", "_visible", "_cls_name", "_cid",
                    "_xpos", "_ypos", "_parent", "_is_created", "_is_textable", "_lbtn_down", "_rbtn_down", "_is_mouse_entered", "_ctl_type",
                    "_font", "_fg_color", "_bg_color", "_draw_flag", "_on_mouse_enter", "on_mouse_down", "on_mouse_up", "on_right_mouse_down",
                    "on_right_mouse_up", "on_right_click", "_on_mouse_leave", "on_double_click", "on_mouse_wheel", "on_mouse_move", "on_mouse_hover",
                    "on_key_down", "on_key_up", "on_key_press", "on_paint", "on_got_focus", "on_lost_focus", "on_click")


    def __init__(self) -> None:
        self.name = ""
        self._hwnd = 0
        self._text = ""
        self._width = 0
        self._height = 0
        self._style = 0
        self._ex_style = 0
        self._h_inst = 0
        self._visible = True
        self._cls_name = ""
        self._xpos = 0
        self._ypos = 0
        self._parent = 0
        self._is_created = False
        self._is_textable = False
        self._lbtn_down = False
        self._rbtn_down = False
        self._is_mouse_entered = False
        self._ctl_type = ControlType.NONE
        self._font = Font()
        self._fg_color = Color(0)
        self._bg_color = Color(0)
        self._draw_flag = 0
        self.tvar = 1 # Only for testing purpose. Can be deleted at last

        # print("iccex ", Control._iccex.dwICC)
        # Events
        self._on_mouse_enter = 0
        self.on_mouse_down = 0
        self.on_mouse_up = 0
        self.on_click = 0
        self.on_right_mouse_down = 0
        self.on_right_mouse_up = 0
        self.on_right_click = 0
        self._on_mouse_leave = 0
        self.on_double_click = 0
        self.on_mouse_wheel = 0
        self.on_mouse_move = 0
        self.on_mouse_hover = 0
        self.on_key_down = 0
        self.on_key_up = 0
        self.on_key_press = 0
        self.on_paint = 0
        self.on_got_focus = 0
        self.on_lost_focus = 0



    # -region Public funcs

    # def send_msg(self, uMsg: UINT, wp: WPARAM, lp: LPARAM):
    #     return api.SendMessage(HWND(self._hwnd), UINT(uMsg), WPARAM(wp), LPARAM(lp))


    def set_size(self, width : int, height : int):
        """Set the size of this control. Give the width & height."""
        self._width = width
        self._height = height
        if self._is_created:
            api.SetWindowPos(self._hwnd, None, self._xpos, self._ypos, self._width, self._height, con.SWP_NOZORDER)
    #----------------------------------------------

    def set_position(self, xpos : int, ypos : int):
        """Set the position of this control. Give the X & Y points."""
        self._xpos = xpos
        self._ypos = ypos
        if self._is_created:
            api.SetWindowPos(self._hwnd, None, self._xpos, self._ypos, self._width, self._height, con.SWP_NOZORDER)

    # -endregion


    # -region Private funcs

    def _create_control(self):
        """This function will create control handles with 'CreateWindowEx' function.
        And it will set the '_is_created' property to True.
        We can use this single function to create all of our controls.
        """
        self._set_ctl_id()
        self._hwnd = api.CreateWindowEx(  self._ex_style,
                                                self._cls_name,
                                                self._text,
                                                self._style,
                                                self._xpos,
                                                self._ypos,
                                                self._width,
                                                self._height,
                                                self._parent._hwnd,
                                                self._cid,
                                                self._parent.wnd_class.hInstance, None )

        if self._hwnd:
            self._is_created = True
            # print(f"Created {self.name} with handle {self._hwnd}")
    #-----------------------------------------------------------------------------------END

    def _set_ctl_id(self):
        """Before creating control, we need to set the control ID."""
        self._cid = Control._ctl_id
        Control._ctl_id += 1


    # Creating font handle if needed and apply it in the control.
    def _set_font_internal(self):

        """Setting font for this control."""

        if self._font._hwnd == 0:
            # print("going to create a font handle for ", self.name)
            self._font.create_handle(self._hwnd)

        api.SendMessage(self._hwnd, con.WM_SETFONT, self._font._hwnd, True)


    # Setting subclass for this control.
    def _set_subclass(self, subClsFunc):
        """Replacing the 'WndProc' function for this control."""
        api.SetWindowSubclass(self._hwnd, subClsFunc, Control._subclass_id, 0)
        Control._subclass_id += 1

    def _get_ctrl_text(self):
        """Return the text from this control."""
        # with Timing("get text time : "):
        tLen = api.GetWindowTextLength(self._hwnd) + 1
        buffer = create_unicode_buffer(tLen)
        api.GetWindowText(self._hwnd, buffer, tLen)
        return buffer.value

    def _set_ctrl_text(self, value: str):
        """Set the text for this control."""
        api.SetWindowText(self._hwnd, value)
        if self._ctl_type == ControlType.LABEL:
            if self._autoSize: self._setAutoSize(True)

    def _get_ctrl_text_ex(self, hwnd):
        """Returns the control text with given hwnd.
        Used in combination controls like ComboBox, NumberPicker etc."""
        tLen = api.GetWindowTextLength(hwnd) + 1
        buffer = create_unicode_buffer(tLen)
        api.GetWindowText(hwnd, buffer, tLen)
        return buffer.value

    def _manage_redraw(self):
        """If this control is created, send a command to redraw it"""
        if self._is_created: api.InvalidateRect(self._hwnd, None, False)

    def _make_sys_time(self, tm: datetime) -> api.SYSTEMTIME:
        """Create a SYSTEMTIME struct from given datetime object"""
        st = api.SYSTEMTIME()
        st.wYear = tm.year
        st.wMonth = tm.month
        st.wDayOfWeek = tm.weekday()
        st.wDay = tm.day
        st.wHour = tm.hour
        st.wMinute = tm.minute
        st.wSecond = tm.second
        st.wMilliseconds = tm.microsecond // 1000
        return st

    def _make_date_time(self, st: api.SYSTEMTIME):
        """Create a datetime object from given SYSTEMTIME object"""
        return datetime.datetime(st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond, st.wMilliseconds)




    def log(self, msg: UINT, arg = None):
        """Print the given message with a counter variable."""
        if arg != None:
            print(f"Log from {self.name} [{self.tvar}] {msg}, {arg}")
        else:
            print(f"Log from {self.name} [{self.tvar}] {msg}")
        self.tvar += 1



    # def setPos(self, x: int, y: int):
    #     self._xpos = x
    #     self._ypos = y
    #     if self._is_created: pass

    # def set_size(self, width: int, height: int):
    #     self._width = width
    #     self._height = height
    #     if self._is_created: pass

    # -endregion

    # -region Props

    @property
    def handle(self):
        """Returns the hwnd of this control"""
        return self._hwnd

    @property
    def parent(self):
        """Returns the parent Form of this control"""
        return self._parent


    @property
    def font(self): return self._font

    @font.setter
    def font(self, value : Font):
        """Set the font for this control
            Args :
                value : Font object
        """
        self._font = value
        if self._is_created:
            pass
    #-------------------------------------------------[1]------

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value:str):
        self._text = value
        if self._is_created and self._is_textable: self._set_ctrl_text(value)
    #--------------------------------------------------------------------------[2]------


    @property
    def xpos(self): return self._xpos

    @xpos.setter
    def xpos(self, value : int):
        self._xpos = value
        if self._is_created:
            pass
    #--------------------------------------------[3]-----

    @property
    def ypos(self): return self._ypos

    @ypos.setter
    def ypos(self, value : int):
        self._ypos = value
        if self._is_created:
            pass
    #--------------------------------------------[4]----

    @property
    def width(self): return self._width

    @width.setter
    def width(self, value : int):
        self._width = value
        if self._is_created:
            pass
    #--------------------------------------------[5]-----

    @property
    def height(self): return self._height

    @height.setter
    def height(self, value : int):
        self._height = value
        if self._is_created:
            pass
    #--------------------------------------------[6]------

    @property
    def visibile(self): return self._visibile

    @visibile.setter
    def visibile(self, value : bool):
        self._visibile = value
        if self._is_created:
            pass
    #--------------------------------------------[7]---------

    @property
    def back_color(self): return self._bg_color

    @back_color.setter
    def back_color(self, value : int):
        self._bg_color.update_color(value)
        if not self._draw_flag & (1 << 1): self._draw_flag += 2
        self._manage_redraw()
    #--------------------------------------------[8]---------

    @property
    def fore_color(self): return self._fg_color.value

    @fore_color.setter
    def fore_color(self, value : int):
        self._fg_color.update_color(value)
        if not self._draw_flag & 1: self._draw_flag += 1
        self._manage_redraw()
    #--------------------------------------------[9]---------

    @property
    def on_mouse_enter(self): return self._on_mouse_enter

    @on_mouse_enter.setter
    def on_mouse_enter(self, value): self._on_mouse_enter = value
    #--------------------------------------------[10]---------

    @property
    def on_mouse_leave(self): return self._on_mouse_leave

    @on_mouse_leave.setter
    def on_mouse_leave(self, value): self._on_mouse_leave = value
    #--------------------------------------------[11]---------

    # -endregion






    # -region Event handlers
    def _left_mouse_down_handler(self, msg, wpm, lpm):
        self._lbtn_down = True
        if self.on_mouse_down:
            self.on_mouse_down(self, MouseEventArgs(msg, wpm, lpm))
            return 0


    def _left_mouse_up_handler(self, msg, wpm, lpm):
        if self.on_mouse_up:
            self.on_mouse_up(self, MouseEventArgs(msg, wpm, lpm))


        if self._lbtn_down:
            self._lbtn_down = False
            api.SendMessage(self._hwnd, MyMessages.MOUSE_CLICK, 0, 0)
            return 0


    def _mouse_click_handler(self):
        if self.on_click: self.on_click(self, EventArgs())


    def _right_mouse_down_handler(self, msg, wpm, lpm):
        self._rbtn_down = True
        if self.on_right_mouse_down: self.on_right_mouse_down(self, MouseEventArgs(msg, wpm, lpm))


    def _right_mouse_up_handler(self, msg, wpm, lpm):
        if self.on_right_mouse_up: self.on_right_mouse_up(self, MouseEventArgs(msg, wpm, lpm))
        if self._rbtn_down:
            self._rbtn_down = False
            self.send_msg(MyMessages.RIGHT_CLICK, 0, 0)



    def _right_mouse_click_handler(self):
        if self.on_right_click: self.on_right_click(self, EventArgs())
        return 0


    def _mouse_wheel_handler(self, msg, wpm, lpm):
        if self.on_mouse_wheel: self.on_mouse_wheel(self, MouseEventArgs(msg, wpm, lpm))



    def _mouse_move_handler(self, msg, wpm, lpm):
        if self._is_mouse_entered:
            if self.on_mouse_move: self.on_mouse_move(self, MouseEventArgs(msg, wpm, lpm))
        if not self._is_mouse_entered:
            self._is_mouse_entered = True
            if self.on_mouse_enter: self.on_mouse_enter(self, EventArgs())



    def _mouse_leave_handler(self):
        self._is_mouse_entered = False
        if self.on_mouse_leave: self.on_mouse_leave(self, EventArgs())



    def _key_down_handler(self, wpm):
        if self.on_key_down: self.on_key_down(self, KeyEventArgs(wpm))
        return 0

    def _key_up_handler(self, wpm):
        if self.on_key_up: self.on_key_up(self, KeyEventArgs(wpm))
        return 0

    def _key_press_handler(self, wp):
        if self.on_key_press: self.on_key_press(self, KeyPressEventArgs(wp))
        return 0

    def _got_focus_handler(self):
        if self.on_got_focus: self.on_got_focus(self, EventArgs())
        return 0


    def _lost_focus_handler(self):
        if self.on_lost_focus: self.on_lost_focus(self, EventArgs())
        return 0


    # -endregion event funcs



def connect(obj: Control, event: str):
    def wrapper(func):
        setattr(obj, event, func)

    return wrapper
