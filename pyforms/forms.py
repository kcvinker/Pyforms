
# Created on 08-Nov-2022 00:05:26
# import ctypes
from ctypes import cast, byref, sizeof, POINTER, pointer, py_object
from ctypes.wintypes import LPCWSTR, HDC
# from functools import lru_cache

from horology import Timing
from . import constants as con
from . import apis as api
from .apis import WNDPROC, RECT, WNDCLASSEX, LPNMHDR, WPARAM, LPARAM, LRESULT, HBRUSH

from . import apis as api

from .control import Control, MenuEventData
from .enums import FormPosition, FormStyle, FormState, FormDrawMode
from .commons import Font, MyMessages, getMouseXpoint, getMouseYpoint, MyMessages
from .events import EventArgs, MouseEventArgs, SizeEventArgs
from .colors import create_gradient_brush2, RgbColor, Color
from . import winmsgs


class StaticData: # A singleton object which used to hold essential data for a form to start
    h_instance = 0
    class_name = "PyForms_Window"
    loop_started = False
    screen_width = api.GetSystemMetrics(0) # Need to calculate the form position
    screen_height = api.GetSystemMetrics(1)
    def_win_color = Color(0xf0f0f0)# Color.from_RGB(230, 230, 230)
    curr_form = None




form_dict = {} # This dictionary contains all the form class. We can get them in wnd_proc_main function
pp_counter = 1 # IMPORTANT: This variable is used in `print_pont` function.

# @lru_cache(maxsize=50)
# def get_form(hwnd): return form_dict.get(hwnd, StaticData.curr_form)

# def get_form1(hwnd): return form_dict.get(hwnd, StaticData.curr_form)

# primeMsgs = [con.WM_GETMINMAXINFO, con.WM_NCCREATE, con.WM_NCDESTROY, con.WM_NCCALCSIZE, con.WM_CREATE]

#//////////////////////////////////////////////////////////////
#//   Main Window Procedure, the heart of this library
#//////////////////////////////////////////////////////////////
@WNDPROC
def wnd_proc_main(hw, message, wParam, lParam) -> LRESULT:
    # print("message ", message) # 36, 129, 130
    # winmsgs.log_msg(message, "Form")
    this = form_dict.get(hw, StaticData.curr_form)

    match message:
        case con.WM_NCDESTROY:
            if this._is_main_window :
                api.PostQuitMessage(0)
                return 1
        # case con.WM_MENUSELECT:
        #     print(f"WM_MENUSELECT {lParam = }, {api.LOWORD(wParam) = }")

        # case con.WM_GETMINMAXINFO: print("WM_GETMINMAXINFO and hwnd is ", hw)

        # case con.WM_PAINT:
        #     frm = get_form(hw)
        #     this.on_paint_special()

#   -region No problem messages
        case con.WM_SHOWWINDOW: this._formShownHandler()
        case con.WM_ACTIVATEAPP: this._formActivateHandler(wParam)
        case con.WM_KEYDOWN | con.WM_SYSKEYDOWN: this._key_down_handler(wParam)
        case con.WM_KEYUP | con.WM_SYSKEYUP: this._key_up_handler(wParam)
        case con.WM_CHAR: this._key_press_handler(wParam)
        case con.WM_LBUTTONDOWN: this._left_mouse_down_handler(message, wParam, lParam)
        case con.WM_LBUTTONUP: this._left_mouse_up_handler(message, wParam, lParam)
        case MyMessages.MOUSE_CLICK: this._mouse_click_handler()
        case con.WM_RBUTTONDOWN: this._right_mouse_down_handler(message, wParam, lParam)
        case con.WM_RBUTTONUP: this._right_mouse_up_handler(message, wParam, lParam)
        case MyMessages.RIGHT_CLICK: this._right_mouse_click_handler()
        case con.WM_MOUSEWHEEL: this._mouse_wheel_handler(message, wParam, lParam)
        case con.WM_MOUSEMOVE: this._formMouseMoveHandler(hw, message, wParam, lParam)
        case con.WM_MOUSELEAVE: this._formMouseLeaveHandler()
        case con.WM_MOUSEHOVER: this._formMouseHoverHandler(message, wParam, lParam)
        case con.WM_SIZING:
            return this._formSizingHandler(message, wParam, lParam)
        case con.WM_SIZE:
            return this._formSizedHandler(message, wParam, lParam)
        case con.WM_MOVING: return this._formMovingHandler(lParam)
        case con.WM_MOVE: return this._formMovedHandler(lParam)
        case con.WM_ERASEBKGND:
            # print("hwnd From HDC ", api.WindowFromDC(wParam))
            if this._draw_flag:
                this._formEraseBkgHandler(hw, wParam)
                return 1
            # return api.DefWindowProc(hw, message, wParam, lParam)
        case con.WM_SYSCOMMAND: this._frmSysCommandHandler(wParam)
        case con.WM_CLOSE: this._formClosingHandler()
        case con.WM_DESTROY: this._formClosedHandler()

#   -endregion No problem messages


        case con.WM_CTLCOLOREDIT:
            # Here we need this work around because, otherwise textbox in windows 10...
            # will not work properly until we click on it.
            # func = this.tbdraw_dict.get(lParam, 0)
            # if func: return func(wParam)
            return api.SendMessage(lParam, MyMessages.EDIT_COLOR, wParam, lParam)
            # return hbr.value

        case con.WM_CTLCOLORSTATIC:
            # win = api.WindowFromDC(wParam)
            # print("WM_CTLCOLORSTATIC in main wndproc", lParam)
            return api.SendMessage(lParam, MyMessages.LABEL_COLOR, wParam, lParam)

        case con.WM_CTLCOLORLISTBOX:
            # print("combo list clr")
            from_combo = this._combo_dict.get(lParam, 0)
            if from_combo:
                return api.SendMessage(from_combo, MyMessages.LIST_COLOR, wParam, lParam)
            else:
                return api.SendMessage(lParam, MyMessages.EDIT_COLOR, wParam, lParam)


        case con.WM_COMMAND:
            match api.HIWORD(wParam):
                case 0: return this._menu_click_handler(api.LOWORD(wParam))
                case 1: pass # accelerator key commands
                case _:
                    # ctlHwnd = HWND(lParam)
                    return api.SendMessage(lParam, MyMessages.CTL_COMMAND, wParam, lParam)

        case con.WM_HSCROLL:
            # print(f"{lParam = }")
            return api.SendMessage(lParam, MyMessages.HORI_SCROLL, wParam, lParam)

        case con.WM_VSCROLL:
            return api.SendMessage(lParam, MyMessages.VERT_SCROLL, wParam, lParam)




        # case con.WM_HOTKEY: pass
        case con.WM_NOTIFY:
            nm = cast(lParam, LPNMHDR).contents
            # this.log("notify msg from ", nm.hwndFrom)
            # if nm.hwndFrom == this.trk_hwnd:
            #     ret = this.trk_func(lParam)
            # else:
            return  api.SendMessage(nm.hwndFrom, MyMessages.CTRL_NOTIFY, wParam, lParam)
            # if nm.hwndFrom == this.trk_hwnd: this.log("result of wm notify ", ret)
            # return ret

        case MyMessages.MENU_EVENT_SET:
            menu = cast(lParam, py_object).value
            this._menu_event_dict[menu._id] = menu

        # case con.WM_MENUCOMMAND:
        #     # menu = this._menu_event_dict.get(lParam, 0)
        #     print(f"WM_MENUCOMMAND {lParam = }, {wParam = }")
        #     # if menu: menu.on_click(menu, EventArgs())







        # case con.WM_PARENTNOTIFY:
        #     this.log(f"parent notify {api.LOWORD(wParam) = }, {lParam = }" )
        #     return 0

    return api.DefWindowProc(hw, message, wParam, lParam)


#//////////////////////////////////////////////////////////////
#//   Create a Window class for our library.
#//////////////////////////////////////////////////////////////
def make_window_class(proc):
    hins = api.GetModuleHandle(LPCWSTR(0))
    wc = WNDCLASSEX()
    wc.cbSize = sizeof(WNDCLASSEX)
    wc.style = con.CS_HREDRAW | con.CS_VREDRAW | con.CS_OWNDC
    wc.lpfnWndProc = proc # WNDPROC(proc)
    wc.hInstance = hins
    wc.hCursor =  api.LoadCursor(0, LPCWSTR(con.IDC_ARROW))
    wc.hbrBackground = api.CreateSolidBrush(StaticData.def_win_color.ref)
    wc.lpszClassName = StaticData.class_name
    print("DTN_FIRST  ", con.DTN_FIRST)
    return wc



#//////////////////////////////////////////////////////////////
#//   Form class, This class represents a window
#//////////////////////////////////////////////////////////////
class Form(Control):

    """Form class represents a Window."""

    wnd_class = make_window_class(wnd_proc_main)
    atom = api.RegisterClassEx(byref(wnd_class))
    _count = 1
    __slots__ = (   "cls_str", "_form_pos", "_form_style", "_form_state", "_top_most", "_maximize_box", "_minimizeBox",
                    "_main_win_handle", "_is_main_window", "_is_mouse_tracking", "_draw_mode", "_is_normal_draw", "_upd_rct",
                    "_form_id", "_combo_dict", "on_load", "on_minimized", "on_maximized", "on_restored", "on_closing",
                    "on_closed", "on_activate", "on_deactivate", "on_moving", "on_moved", "on_sizing", "on_sized",
                     "_menu_event_dict" )

    def __init__(self, txt = "", width = 500, height = 400) -> None:
        super().__init__()
        self.cls_str = ""

        self.name = f"Form_{Form._count}"
        self._text = self.name if txt == "" else txt
        self._width = width
        self._height = height
        self._style = con.WS_OVERLAPPEDWINDOW | con.WS_CLIPCHILDREN | con.WS_VISIBLE
        self._is_textable = True # If this is True, users can get or set text property
        self._font = Font() # Font handle is not created yet. It's just a font class
        self._bg_color = Color(StaticData.def_win_color) # Defining a globar window color for all windows

        self._form_pos = FormPosition.CENTER # Defining where to appear on the screen
        self._form_style = FormStyle.SIZABLE # Defining the style of this form
        self._form_state = FormState.NORMAL # Other options are minimize & maximize
        self._top_most = False
        self._maximize_box = True
        self._minimizeBox = True
        self._main_win_handle = 0
        self._is_main_window = False
        self._is_mouse_tracking = False # A flag to control mouse tracking in oreder to get the mouse move msg
        self._draw_mode = FormDrawMode.NORMAL # Other options are flat color & gradient
        self._is_normal_draw = True
        self._form_id = Form._count + 1000 # A unique ID for all forms.
        self._combo_dict = {} # Combo boxes demands to keep their listbox handle
        # self.tbdraw_dict = {} # A dictionary for holding textbox coloring functions
        self._upd_rct = 0
        self._menu_event_dict = {}
        # self._last_np = None # Last created NumberPicker.





        # Events
        self.on_load = 0
        self.on_minimized = 0
        self.on_maximized = 0
        self.on_restored = 0
        self.on_closing = 0
        self.on_closed = 0
        self.on_activate = 0
        self.on_deactivate = 0
        self.on_moving = 0
        self.on_moved = 0
        self.on_sizing = 0
        self.on_sized = 0

        Form._count += 1
    #------------------------------



    # -region Public functions
    def create_handle(self):
        """Creating window handle """
        print("over lapp ", con.WS_OVERLAPPEDWINDOW)
        self._set_location()
        self._set_style()
        StaticData.curr_form = self
        self._hwnd = api.CreateWindowEx(self._ex_style,
                                        self.wnd_class.lpszClassName,
                                        self._text,
                                        self._style,
                                        self._xpos, self._ypos,
                                        self._width, self._height,
                                        0, 0, self.wnd_class.hInstance, None)


        if self._hwnd:
            form_dict[self._hwnd] = self

            self._is_created = True
            # print("Created window handle ", self._hwnd)
            # Font handle is not created. We need create one with current font class.
            self._set_font_internal()
            StaticData.curr_form = None
        else:
            print("window creation failed")

    # Print mouse points. Useful for getting mouse points in order to place the controls.
    def print_point(self, me):
        global pp_counter
        print(f"[{pp_counter}] X : {me.xpos}, Y : {me.ypos}")
        pp_counter += 1

    def set_gradient_color(self, clr1, clr2, top2btm = True):
        self._mGClr1 = RgbColor(clr1)
        self._mGClr2 = RgbColor(clr2)
        self._mGt2b = top2btm
        self._draw_mode = FormDrawMode.GRADIENT
        self._is_normal_draw = False
        if self._is_created: pass

    def display(self):
        """Display a window. If it's the first window, then it will start the main loop"""
        api.ShowWindow(self._hwnd, con.SW_SHOW)

        if self.form_state == FormState.MINIMIZED :
            api.CloseWindow(self._hwnd)
        else:
            api.UpdateWindow(self._hwnd)
        # print("Update Window result ", res)

        if not StaticData.loop_started:
            self._is_main_window = True
            StaticData.loop_started = True
            tMsg = api.MSG()
            while api.GetMessage(byref(tMsg), None, 0, 0) > 0:
                api.TranslateMessage(byref(tMsg))
                api.DispatchMessage(byref(tMsg))

    # -endregion

    # -region Private functions
    def _set_location(self) :
        match self._form_pos:
            case FormPosition.CENTER:
                self._xpos = int((StaticData.screen_width - self._width) / 2)
                self._ypos = int((StaticData.screen_height - self._height) / 2)
            case FormPosition.TOP_LEFT:
                pass
            case FormPosition.TOP_MID:
                self._xpos = int((StaticData.screen_width - self._width) / 2)
            case FormPosition.TOP_RIGHT:
                self._xpos = StaticData.screen_width - self._width
            case FormPosition.MID_LEFT:
                self._ypos = int((StaticData.screen_height - self._height) / 2)
            case FormPosition.MID_RIGHT:
                self._xpos = StaticData.screen_width - self._width
                self._ypos = int((StaticData.screen_height - self._height) / 2)
            case FormPosition.BOTTOM_LEFT:
                self._ypos = StaticData.screen_height - self._height
            case FormPosition.BOTTOM_MID:
                self._xpos = int((StaticData.screen_width - self._width) / 2)
                self._ypos = StaticData.screen_height - self._height
            case FormPosition.BOTTOM_RIGHT:
                self._xpos = StaticData.screen_width - self._width
                self._ypos = StaticData.screen_height - self._height
            case FormPosition.MANUAL:
                pass

    def _set_style(self):
        mxFlag = False
        match self._form_style:
            case FormStyle.NONE:
                self._ex_style = 0x00050000
                self._style = 0x16010000
            case FormStyle.FIXED_SINGLE:
                self._ex_style = 0x00050100
                self._style = 0x16CB0000
                mxFlag = True
            case FormStyle.FIXED_3D:
                self._ex_style = 0x00050300
                self._style = 0x16CB0000
                mxFlag = True
            case FormStyle.FIXED_DIALOG:
                self._ex_style = 0x00050100
                self._style = 0x16CB0000
                mxFlag = True
            case FormStyle.FIXED_TOOL:
                self._ex_style = 0x00050100
                self._style = 0x16CF0000
            case FormStyle.SIZABLE:
                self._ex_style = 0x00050100
                self._style = 0x16CF0000 | con.WS_OVERLAPPEDWINDOW
            case FormStyle.SIZABLE_TOOL:
                self._ex_style = 0x00050180
                self._style = 0xCF0000 # con.WS_OVERLAPPEDWINDOW
                mxFlag = True
            case FormStyle.HIDDEN:
                self._ex_style = con.WS_EX_TOOLWINDOW
                self._style = con.WS_BORDER

        if mxFlag:
            if not self._maximize_box : self._style ^= con.WS_maximize_box
            if not self._minimizeBox : self._style ^= con.WS_MINIMIZEBOX
            # print(f"state of maximize box {self._maximize_box}")

        if self._top_most: self._ex_style = self._ex_style or con.WS_EX_top_most
        if self._form_state == FormState.MAXIMIZED: self._style |= con.WS_MAXIMIZE
        # print(f"Ex style bits of this form - {hex(self._ex_style)}")
        # print(f"style bits of this form - {hex(self._style)}")

    def _save_combo_info(self, lb_hwnd, cmb_hwnd): self._combo_dict[lb_hwnd] = cmb_hwnd

    def _draw_upd_frame(self, hdc):

        if self._upd_rct:
            # print("327")
            # res = api.DrawEdge(hdc, byref(self._upd_rct), con.BDR_RAISEDINNER, con.BF_RECT | con.BF_ADJUST)
            clr = Color(0xff0000)
            fpen = api.CreatePen(con.PS_SOLID, 1, clr.ref)
            api.SelectObject(hdc, fpen)
            api.Rectangle(hdc, self._upd_rct.left, self._upd_rct.top, self._upd_rct.right, self._upd_rct.bottom)
            api.DeleteObject(fpen)
            # print("edge ", res)


    def _menu_click_handler(self, menu_id):
        menu = self._menu_event_dict.get(menu_id, 0)
        if menu:
            menu.on_click(menu, EventArgs())
            return 0
        return 0

    # def _set_number_picker_info(self, np):
    #     # This is a work around for a strange problem.
    #     # If we create a single num picker, it will be okay.
    #     # But if we create another num picker, the first...
    #     # num picker's edit control get resized. I cannot...
    #     # find any fix other than this. By this fix, we...
    #     # are resizing the older num picker's edit and...
    #     # set the new num picker as last num picker.
    #     if self._last_np: self._last_np._resize_buddy()
    #     self._last_np = np


    # def saveComboInfo(self, ci):
    #     if len(self._cmbInfoList) > 0:

    # -endregion private functions

    # -region Event handlers
    def _formActivateHandler(self, wp):
        if self.on_activate or self.on_deactivate:
            ea = EventArgs()
            activate = bool(wp)
            if not activate:
                if self.on_deactivate: self.on_deactivate(self, ea)
            else:
                if self.on_activate: self.on_activate(self, ea)
        return 0

    def _formShownHandler(self):
        if self.on_load:
            ea = EventArgs()
            self.on_load(self, ea)
        return 0

    def _formMouseMoveHandler(self,hw, msg, wp, lp):
        if not self._is_mouse_tracking:
            self._is_mouse_tracking = True
            self._trackMouseEvents(hw)
            if not self._is_mouse_entered:
                if self.on_mouse_enter:
                    self._is_mouse_entered = True
                    ea = EventArgs()
                    self.on_mouse_enter(self, ea)
        if self.on_mouse_move:
            ea = MouseEventArgs(msg, wp, lp)
            self.on_mouse_move(self, ea)
        return 0

    def _formMouseLeaveHandler(self):
        if self._is_mouse_tracking:
            self._is_mouse_tracking = False
            self._is_mouse_entered = False

        if self.on_mouse_leave:
            ea = EventArgs()
            self.on_mouse_leave(self, ea)
        return 0

    def _formMouseHoverHandler(self, msg, wp, lp):
        if self._is_mouse_tracking: self._is_mouse_tracking = False
        if self.on_mouse_hover:
            ea = MouseEventArgs(msg, wp, lp)
            self.on_mouse_hover(self, ea)
        return 0

    def _trackMouseEvents(self, hw):
        tme = api.TRACKMOUSEEVENT()
        tme.cbSize = sizeof(api.TRACKMOUSEEVENT)
        tme.dwFlags = con.TME_HOVER | con.TME_LEAVE
        tme.dwHoverTime = con.HOVER_DEFAULT
        tme.hwndTrack = hw ;
        api.TrackMouseEvent(byref(tme))

    def _formSizingHandler(self, msg, wp, lp):
        ea = SizeEventArgs(msg, wp, lp)
        self._width = ea.formRect.right - ea.formRect.left
        self._height = ea.formRect.bottom - ea.formRect.top
        if self.on_sizing:
            self.on_sizing(self, ea)
        return 0


    def _formSizedHandler(self, msg, wp, lp):
        if self.on_sizing:
            ea = SizeEventArgs(msg, wp, lp)
            self.on_sizing(self, ea)
        return 0


    def _formMovingHandler(self, lp):
        rct = cast(lp, POINTER(RECT)).contents
        self._xpos = rct.left
        self._ypos = rct.top
        if self.on_moving:
            ea = EventArgs()
            self.on_moving(self, ea)
            # return 0
        return 0

    def _formMovedHandler(self, lp):
        self._xpos = getMouseXpoint(lp)
        self._ypos = getMouseYpoint(lp)
        if self.on_moved:
            ea = EventArgs()
            self.on_moved(self, ea)
        return 0

    def _frmSysCommandHandler(self, wp):
        uMsg = int(wp & 0xFFF0)
        match uMsg:
            case con.SC_MINIMIZE:
                if self.on_minimized:
                    ea = EventArgs()
                    self.on_minimized(self, ea)

            case con.SC_RESTORE:
                if self.on_restored:
                    ea = EventArgs()
                    self.on_restored(self, ea)

            case con.SC_MAXIMIZE:
                if self.on_maximized:
                    ea = EventArgs()
                    self.on_maximized(self, ea)


    def _formClosingHandler(self):
        if self.on_closing:
            ea = EventArgs()
            self.on_closing(self, ea)

    def _formClosedHandler(self):
        if self.on_closed:
            ea = EventArgs()
            self.on_closed(self, ea)

    def _formEraseBkgHandler(self, hwnd, wp):
        # if self._draw_mode != FormDrawMode.NORMAL:
        # dch = cast(wp, HDC).value
        rct = api.get_client_rect(hwnd)
        # api.GetClientRect(hwnd, byref(rct))

        if self._draw_mode == FormDrawMode.COLORED:
            hbr = api.CreateSolidBrush(self._bkClrRef)
        else:
            # with Timing("create gradient speed : "):
            hbr = create_gradient_brush2( wp, rct, self._mGClr1, self._mGClr2, self._mGt2b )
        api.FillRect(wp, byref(rct), hbr)
        api.DeleteObject(hbr)



    # -endregion


    # -region Properties

    @property
    def form_id(self): return self._form_id

    @property
    def form_pos(self): return self._form_pos

    @form_pos.setter
    def form_pos(self, value: FormPosition):
        self._form_pos = value
        if self._is_created:
            pass

    #---------------------------------------

    @property
    def form_style(self): return self._form_style

    @form_style.setter
    def form_style(self, value: FormStyle):
        self._form_style = value
        if self._is_created:
            pass

    #---------------------------------------

    @property
    def form_state(self): return self._form_state

    @form_state.setter
    def form_state(self, value: FormState):
        self._form_state = value
        if self._is_created:
            pass

    #---------------------------------------

    @Control.xpos.setter # Overriding base class's setter
    def xpos(self, value: int):
        self._xpos = value
        self._form_pos = FormPosition.MANUAL
        if self._is_created:
            pass

    #---------------------------------------

    @Control.ypos.setter # Overriding base class's setter
    def ypos(self, value: int):
        self._ypos = value
        self._form_pos = FormPosition.MANUAL
        if self._is_created:
            pass

    #---------------------------------------



    @Control.back_color.setter
    def back_color(self, value):
        self._bg_color.update_color(value)
        self._draw_mode = FormDrawMode.COLORED
        if not self._draw_flag: self._draw_flag = 1
        self._is_normal_draw = False
        self._manage_redraw() # This will re draw the window if needed



    # @property
    # def mainWindowHandle(self): return self.__mainHandle

    # @property
    # def isMainWindow(self): return self._is_main_window

    # @property
    # def handle(self): return self._hwnd

    # -endregion

#-----------------------------------------------END OF FORM CLASS-----------------------------------