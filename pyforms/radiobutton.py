


# RadioButton module - Created on 09-Dec-2022 16:03:20

from ctypes.wintypes import HWND, UINT
from ctypes import WINFUNCTYPE, byref, cast, addressof

from .control import Control
from .commons import MyMessages
from .enums import ControlType
from .apis import LRESULT, UINT_PTR, DWORD_PTR, LPNMCUSTOMDRAW, WPARAM, LPARAM
from . import apis as api
from .colors import Color, RgbColor
from . import constants as con
from .events import EventArgs

rb_dict = {}
rb_style = con.WS_CHILD | con.WS_VISIBLE | con.WS_TABSTOP | con.BS_AUTORADIOBUTTON
txtFlag = con.DT_SINGLELINE | con.DT_VCENTER | con.DT_CENTER | con.DT_NOPREFIX


class RadioButton(Control):

    _count = 1
    __slots__ = ( "_right_align", "_txt_style", "_bg_brush", "_is_checked", "on_checked_changed", "_check_on_click")

    def __init__(self, parent, txt: str, xpos: int = 10, ypos: int = 10, width: int = 120, height: int = 23) -> None:
        super().__init__()
        self._cls_name = "Button"
        self.name = f"RadioButton_{RadioButton._count}"
        self._ctl_type = ControlType.RADIO_BUTTON
        self._text = self.name if txt == "" else txt
        self._parent = parent
        self._font = parent._font
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._is_textable = True
        self._style = rb_style
        self._ex_style = con.WS_EX_LTRREADING | con.WS_EX_LEFT
        self._txt_style = con.DT_SINGLELINE | con.DT_VCENTER

        # self._fg_color = Color(0)
        self._bg_color = Color(parent._bg_color)
        self._bg_brush = api.CreateSolidBrush(self._bg_color.ref)
        self._check_on_click = True

        # self._draw_mode = ControlDrawMode.NO_DRAW
        # self._draw_flag = 0
        self._right_align = False
        self._is_checked = False
        self.on_checked_changed = 0
        # self._txt_case = TextCase.NORMAL
        # self._txt_type = TextType.NORMAL
        # self._txt_align = TextAlignment.LEFT

        RadioButton._count += 1


    def create_handle(self):
        if self._right_align:
            self._style |= con.BS_RIGHTBUTTON
            self._txt_style |= con.DT_RIGHT
        if not self._check_on_click: self._style ^= con.BS_AUTORADIOBUTTON

        self._create_control()
        if self._hwnd:
            rb_dict[self._hwnd] = self
            self._set_subclass(rb_wnd_proc)
            self._set_font_internal()
            ss = api.SIZE()
            api.SendMessage(self._hwnd, con.BCM_GETIDEALSIZE, 0, addressof(ss))

            self._width = ss.cx
            self._height = ss.cy
            api.MoveWindow(self._hwnd, self._xpos, self._ypos, self._width, self._height, True)




    @Control.back_color.setter
    def back_color(self, value):
        self._bg_color.update_color(value)
        self._bg_brush = api.CreateSolidBrush(self._bg_color.ref)
        if not self._draw_flag & (1 << 1): self._draw_flag += 2


    @Control.text.getter
    def text(self):
        if self._is_created:
            return self._get_ctrl_text()
        else:
            return self._text


#End RadioButton

@WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR)
def rb_wnd_proc(hw, msg, wp, lp, scID, refData) -> LRESULT:
    # printWinMsg(msg)
    rb = rb_dict[hw]
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, rb_wnd_proc, scID)
            # print("remove subclass of ", rb.name)



        case con.WM_SETFOCUS: rb._got_focus_handler()
        case con.WM_KILLFOCUS: rb._lost_focus_handler()
        case con.WM_LBUTTONDOWN: rb._left_mouse_down_handler(msg, wp, lp)
        case con.WM_LBUTTONUP: rb._left_mouse_up_handler(msg, wp, lp)
        case MyMessages.MOUSE_CLICK: rb._mouse_click_handler()
        case con.WM_RBUTTONDOWN: rb._right_mouse_down_handler(msg, wp, lp)
        case con.WM_RBUTTONUP: rb._right_mouse_up_handler(msg, wp, lp)
        case MyMessages.RIGHT_CLICK: rb._right_mouse_click_handler()
        case con.WM_MOUSEWHEEL: rb._mouse_wheel_handler(msg, wp, lp)
        case con.WM_MOUSEMOVE: rb._mouse_move_handler(msg, wp, lp)
        case con.WM_MOUSELEAVE: rb._mouse_leave_handler()

        case MyMessages.LABEL_COLOR:
            # if rb._draw_flag & 1: api.SetTextColor(wp, rb._fg_color.ref)
            if rb._draw_flag & 2: api.SetBkColor(wp, rb._bg_color.ref)
            return rb._bg_brush

        case MyMessages.CTRL_NOTIFY:
            nmc = cast(lp, LPNMCUSTOMDRAW).contents
            match nmc.dwDrawStage:
                case con.CDDS_PREERASE: return con.CDRF_NOTIFYPOSTERASE
                case con.CDDS_PREPAINT:
                    rct = nmc.rc
                    if not rb._right_align:
                        rct.left += 17 # Adjusting rect,otherwise text will be drawn upon the check area
                    else: rct.right -= 17

                    api.SetTextColor(nmc.hdc, rb._fg_color.ref)
                    api.SetBkMode(nmc.hdc, 1)
                    api.DrawText(nmc.hdc, rb._text, len(rb._text), byref(rct), rb._txt_style )
                    return con.CDRF_SKIPDEFAULT


        case MyMessages.CTL_COMMAND:
            rb._is_checked = bool(api.SendMessage(hw, con.BM_GETCHECK, 0, 0))
            if rb.on_checked_changed: rb.on_checked_changed(rb, EventArgs() )


    return api.DefSubclassProc(hw, msg, wp, lp)






