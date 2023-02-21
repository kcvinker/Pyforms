

# CheckBox module - Created on 08-Dec-2022 18:49:20


from ctypes import WINFUNCTYPE, byref, cast, addressof


from .control import Control
from .commons import MyMessages
from .enums import ControlType
from .apis import LRESULT, LPNMCUSTOMDRAW, SUBCLASSPROC
from . import apis as api
from .colors import Color
from . import constants as con
from .events import EventArgs

cb_dict = {}
cb_style = con.WS_CHILD | con.WS_VISIBLE | con.WS_TABSTOP | con.BS_AUTOCHECKBOX
# txtFlag = con.DT_SINGLELINE | con.DT_VCENTER | con.DT_CENTER | con.DT_NOPREFIX


class CheckBox(Control):
    """Represents CheckBox control"""
    _count = 1
    __slots__ = ( "_right_align", "_txt_style", "_bg_brush", "_is_checked", "on_checked_changed")

    def __init__(self, parent, txt: str, xpos: int = 10, ypos: int = 10, width: int = 120, height: int = 23) -> None:
        super().__init__()
        self._cls_name = "Button"
        self.name = f"CheckBox_{CheckBox._count}"
        self._ctl_type = ControlType.CHECK_BOX
        self._text = self.name if txt == "" else txt
        self._parent = parent
        self._font = parent._font
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._is_textable = True
        self._style = cb_style
        self._ex_style = con.WS_EX_LTRREADING | con.WS_EX_LEFT
        self._txt_style = con.DT_SINGLELINE | con.DT_VCENTER

        self._bg_color = Color(parent._bg_color)
        self._bg_brush = api.CreateSolidBrush(self._bg_color.ref)

        self._right_align = False
        self._is_checked = False
        self.on_checked_changed = 0

        CheckBox._count += 1


    def create_handle(self):
        if self._right_align:
            self._style |= con.BS_RIGHTBUTTON
            self._txt_style |= con.BS_RIGHTBUTTON

        self._create_control()
        if self._hwnd:
            cb_dict[self._hwnd] = self
            self._set_subclass(cb_wnd_proc)
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


#End CheckBox


@SUBCLASSPROC
def cb_wnd_proc(hw, msg, wp, lp, scID, refData) -> LRESULT:
    # printWinMsg(msg)
    cb = cb_dict[hw]
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, cb_wnd_proc, scID)
            del cb_dict[hw]

        case con.WM_SETFOCUS: cb._got_focus_handler()
        case con.WM_KILLFOCUS: cb._lost_focus_handler()
        case con.WM_LBUTTONDOWN: cb._left_mouse_down_handler(msg, wp, lp)
        case con.WM_LBUTTONUP: cb._left_mouse_up_handler(msg, wp, lp)
        case MyMessages.MOUSE_CLICK: cb._mouse_click_handler()
        case con.WM_RBUTTONDOWN: cb._right_mouse_down_handler(msg, wp, lp)
        case con.WM_RBUTTONUP: cb._right_mouse_up_handler(msg, wp, lp)
        case MyMessages.RIGHT_CLICK: cb._right_mouse_click_handler()
        case con.WM_MOUSEWHEEL: cb._mouse_wheel_handler(msg, wp, lp)
        case con.WM_MOUSEMOVE: cb._mouse_move_handler(msg, wp, lp)
        case con.WM_MOUSELEAVE: cb._mouse_leave_handler()

        case MyMessages.LABEL_COLOR:
            # Unfortunately changing fore color here won't work.
            if cb._draw_flag & 2: api.SetBkColor(wp, cb._bg_color.ref)
            return cb._bg_brush

        case MyMessages.CTRL_NOTIFY:
            nmc = cast(lp, LPNMCUSTOMDRAW).contents
            match nmc.dwDrawStage:
                case con.CDDS_PREERASE: return con.CDRF_NOTIFYPOSTERASE
                case con.CDDS_PREPAINT:
                    rct = nmc.rc
                    if not cb._right_align:
                        rct.left += 17 # Adjusting rect,otherwise text will be drawn upon the check area
                    else:
                        rct.right -= 17

                    if cb._draw_flag & 1: api.SetTextColor(nmc.hdc, cb._fg_color.ref)
                    api.SetBkMode(nmc.hdc, 1)
                    api.DrawText(nmc.hdc, cb._text, len(cb._text), byref(rct), cb._txt_style )

                    return con.CDRF_SKIPDEFAULT

        case MyMessages.CTL_COMMAND:
            cb._is_checked = bool(api.SendMessage(hw, con.BM_GETCHECK, 0, 0))
            if cb.on_checked_changed: cb.on_checked_changed(cb, EventArgs() )

    return api.DefSubclassProc(hw, msg, wp, lp)






