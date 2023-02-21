# Created on 10-Nov-2022 16:16:20


from ctypes.wintypes import HPEN
from ctypes import byref, cast

import horology
from .apis import LRESULT, LPNMCUSTOMDRAW, SUBCLASSPROC
from .control import Control
from .commons import MyMessages, inflateRect
from .enums import ControlType
# from . import winmsgs
from . import apis as api
from .colors import Color, RgbColor, create_gradient_brush2
from . import constants as con


btnDic = {}
btnStyle = con.WS_CHILD | con.BS_NOTIFY | con.WS_TABSTOP | con.WS_VISIBLE | con.BS_PUSHBUTTON
txtFlag = con.DT_SINGLELINE | con.DT_VCENTER | con.DT_CENTER | con.DT_NOPREFIX


class Button(Control):
    """Represents Button control"""
    _count = 1
    __slots__ = ( "_flatBkg", "_mfore_color", "_mback_color", "_mfocus_color", "_mclick_color", "_mframe_color",
                "_mgrad_def_clr1", "_mgrad_def_clr2", "_mgrad_foc_clr1", "_mgrad_foc_clr2", "_mgrad_clk_clr1",
                "_mgrad_clk_clr2", "_mgrad_top2btm", "_gd_brush_main", "_gd_brush_hover", "_gd_brush_click", "_fdraw", "_gdraw")

    def __init__(self, parent, txt: str = "", xpos = 50, ypos = 50, width = 120, height = 40) -> None:
        super().__init__()
        self.name = f"Button_{Button._count}"
        self._parent = parent
        self._font = parent._font
        self._cls_name = "Button"
        self._ctl_type = ControlType.BUTTON
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._is_textable = True
        self._text = self.name if txt == "" else txt
        self._style = btnStyle
        self._ex_style = 0x00000004
        self._flatBkg = False
        self._gd_brush_click = 0
        self._gd_brush_hover = 0
        self._gd_brush_main = 0
        self._fdraw = FlatDraw()
        self._gdraw = GradDraw()

        Button._count += 1


    def create_handle(self):
        self._create_control()
        if self._hwnd:
            btnDic[self._hwnd] = self
            self._set_font_internal()
            self._set_subclass(btn_wnd_proc)


    @Control.fore_color.setter
    def fore_color(self, value):
        self._mfore_color = Color(value)
        if not self._draw_flag & 1: self._draw_flag += 1
        if self._is_created:
            pass


    def set_back_color(self, def_color):
        self._mback_color = Color(def_color)
        self._fdraw.set_data(Color(def_color))
        if not self._draw_flag & 2: self._draw_flag += 2
        if self._is_created:
            pass

    def set_back_color_ex(self, def_color, focus_color, click_color, frame_color):
        self._mback_color = Color(def_color)
        self._mfocus_color = Color(focus_color)
        self._mclick_color = Color(click_color)
        self._mframe_color = Color(frame_color)
        if not self._draw_flag & 2: self._draw_flag += 2

        if self._is_created:
            pass

    def set_gradient_color(self, clr1 : int, clr2 : int):
        self._gdraw.set_data(clr1, clr2)
        if not self._draw_flag & 4: self._draw_flag += 4
        if self._is_created: pass


    # Drawing text color in wm_notify message.
    def _draw_fore_color(self, nmcd):
        api.SetTextColor(nmcd.hdc, self._mfore_color.ref)
        api.SetBkMode(nmcd.hdc, 1)
        api.DrawText(nmcd.hdc, self._text, len(self._text), byref(nmcd.rc), txtFlag )



    def _draw_background_color(self, nc, hbr, pen):
        api.SelectObject(nc.hdc, hbr);
        api.SelectObject(nc.hdc, pen);
        api.RoundRect(nc.hdc, nc.rc.left, nc.rc.top, nc.rc.right, nc.rc.bottom, 5, 5);
        api.FillPath(nc.hdc)



    # Drawing btn frame in wm_notify message
    def _draw_btn_frame(self, nmc, rc, frmRcSize: int):
        rc2 = inflateRect(rc, frmRcSize) if frmRcSize != 0 and self._parent._is_normal_draw else rc
        framePen: HPEN = api.CreatePen(con.PS_SOLID, 1, self._mframe_color.ref)
        api.SelectObject(nmc.hdc, framePen)
        api.Rectangle(nmc.hdc, rc2.left, rc2.top, rc2.right, rc2.bottom)
        api.DeleteObject(framePen)


    # Handler for wm_notify message. Almost all button drawing is happening here
    def _wm_notify_handler(self, lp):
        if self._draw_flag:
            nmcd = cast(lp, LPNMCUSTOMDRAW).contents
            match self._draw_flag:
                case 1: # Only fore color
                    self._draw_fore_color(nmcd)
                    return con.CDRF_NOTIFYPOSTPAINT

                case 2 | 3: # Flat back color and/or fore color
                    if nmcd.dwDrawStage == con.CDDS_PREERASE:
                        return con.CDRF_NOTIFYPOSTERASE

                    elif nmcd.dwDrawStage == con.CDDS_PREPAINT:
                        if (nmcd.uItemState & 0b1) == 0b1:                  # mouse click
                            self._draw_background_color(nmcd, self._fdraw.def_brush, self._fdraw.hot_pen)
                        elif (nmcd.uItemState & 0b1000000) == 0b1000000:    # mouse over
                            self._draw_background_color(nmcd, self._fdraw.hot_brush, self._fdraw.hot_pen)
                        else:                                               # Normal button state
                            self._draw_background_color(nmcd, self._fdraw.def_brush, self._fdraw.def_pen)

                        if self._draw_flag & 1:
                            self._draw_fore_color(nmcd)
                            return con.CDRF_SKIPDEFAULT

                        return con.CDRF_DODEFAULT

                case 4 | 5: # Gradient back color and/or for color
                    if nmcd.dwDrawStage == con.CDDS_PREERASE:
                        return con.CDRF_NOTIFYPOSTERASE
                    elif nmcd.dwDrawStage == con.CDDS_PREPAINT:
                        if (nmcd.uItemState & 0b1) == 0b1: #--------------mouse click   (plain form clr = -1), (grad form =
                            if self._gdraw.def_brush == 0:
                                # print("going to create gradient brush for mouse click")
                                self._gdraw.def_brush = create_gradient_brush2(nmcd.hdc, nmcd.rc,
                                                                                self._gdraw.gc_def.c1,
                                                                                self._gdraw.gc_def.c2, True)

                            self._draw_background_color(nmcd, self._gdraw.def_brush, self._gdraw.hot_pen)

                        elif (nmcd.uItemState & 0b1000000) == 0b1000000: #---mouse over
                            if self._gdraw.hot_brush == 0:
                                self._gdraw.hot_brush = create_gradient_brush2(nmcd.hdc, nmcd.rc,
                                                                                self._gdraw.gc_hot.c1,
                                                                                self._gdraw.gc_hot.c2, True)

                            self._draw_background_color(nmcd, self._gdraw.hot_brush, self._gdraw.hot_pen)

                        else: #--------------------------------------------- Normal button state
                            if self._gdraw.def_brush == 0:
                                self._gdraw.def_brush = create_gradient_brush2(nmcd.hdc, nmcd.rc,
                                                                                self._gdraw.gc_def.c1,
                                                                                self._gdraw.gc_def.c2, True)

                            self._draw_background_color(nmcd, self._gdraw.def_brush, self._gdraw.hot_pen)

                        if self._draw_flag & 1:
                            self._draw_fore_color(nmcd)
                            return con.CDRF_SKIPDEFAULT

                        return con.CDRF_DODEFAULT

        return con.CDRF_DODEFAULT

    def _reset_brushes(self):
        # Button size changed. So we need to reset our...
        # gradient brushes to zero. So that we can...
        # recreate these brushes with new size.
        if self._draw_flag > 3:
            self.def_brush = 0
            self.hot_brush = 0

    def finalize(self, scID):
        match self._draw_flag:
            case 2 | 3: self._fdraw.finalize() # Freeing flat draw resources
            case 4 | 5: self._gdraw.finalize() # Freeing grad draw resources

        api.RemoveWindowSubclass(self._hwnd, btn_wnd_proc, scID)
        del btnDic[self._hwnd]




#End Button Class

class FlatDraw:
    __slots__ = ("def_brush", "hot_brush", "def_pen", "hot_pen")
    def __init__(self) -> None:
        self.def_brush = 0
        self.hot_brush = 0
        self.def_pen = 0
        self.hot_pen = 0

    def set_data(self, c: Color):
        hrc = c.make_RGB()
        frc = c.make_RGB()
        hadj = 1.5 if frc.is_dark() else 1.2

        self.def_brush = api.CreateSolidBrush(c.ref)
        self.hot_brush = api.CreateSolidBrush(hrc.change_shade_ref(hadj))
        self.def_pen = api.CreatePen(con.PS_SOLID, 1, frc.change_shade_ref(0.6))
        self.hot_pen = api.CreatePen(con.PS_SOLID, 1, frc.change_shade_ref(0.3))

    def finalize(self):
        if self.def_brush: api.DeleteObject(self.def_brush)
        if self.hot_brush: api.DeleteObject(self.hot_brush)
        if self.def_pen: api.DeleteObject(self.def_pen)
        if self.hot_pen: api.DeleteObject(self.hot_pen)



class GradColor:
    def __init__(self) -> None:
        self.c1 = RgbColor(0)
        self.c2 = RgbColor(0)

class GradDraw:
    def __init__(self) -> None:
        self.gc_def = GradColor()
        self.gc_hot = GradColor()
        self.def_pen = 0
        self.hot_pen = 0
        self.def_brush = 0
        self.hot_brush = 0


    def set_data(self, uc1, uc2):
        self.gc_def.c1 = RgbColor(uc1)
        self.gc_def.c2 = RgbColor(uc2)
        hadj1 = 1.5 if self.gc_def.c1.is_dark() else 1.2
        hadj2 = 1.5 if self.gc_def.c2.is_dark() else 1.2
        self.gc_hot.c1 = self.gc_def.c1.change_shade_rgb(hadj1)
        self.gc_hot.c2 = self.gc_def.c2.change_shade_rgb(hadj2)

        self.def_pen = api.CreatePen(con.PS_SOLID, 1, self.gc_def.c1.change_shade_ref(0.6))
        self.hot_pen = api.CreatePen(con.PS_SOLID, 1, self.gc_hot.c1.change_shade_ref(0.3))

    def finalize(self):
        if self.def_pen: api.DeleteObject(self.def_pen)
        if self.hot_pen: api.DeleteObject(self.hot_pen)
        if self.def_brush: api.DeleteObject(self.def_brush)
        if self.hot_brush: api.DeleteObject(self.hot_brush)




@SUBCLASSPROC
def btn_wnd_proc(hw, msg, wp, lp, scID, refData) -> LRESULT:
    # winmsgs.log_msg(msg, "Button")

    btn = btnDic[hw]
    match msg:
        case con.WM_NCDESTROY: btn.finalize(scID)

        case con.WM_SETFOCUS: return btn._got_focus_handler()
        case con.WM_KILLFOCUS: return btn._lost_focus_handler()
        case con.WM_LBUTTONDOWN:btn._left_mouse_down_handler(msg, wp, lp)

        case con.WM_LBUTTONUP: btn._left_mouse_up_handler(msg, wp, lp)
        case MyMessages.MOUSE_CLICK: btn._mouse_click_handler()
        case con.WM_RBUTTONDOWN: btn._right_mouse_down_handler(msg, wp, lp)
        case con.WM_RBUTTONUP: btn._right_mouse_up_handler(msg, wp, lp)
        case MyMessages.RIGHT_CLICK: btn._right_mouse_click_handler()
        case con.WM_MOUSEWHEEL: btn._mouse_wheel_handler(msg, wp, lp)
        case con.WM_MOUSEMOVE: btn._mouse_move_handler(msg, wp, lp)
        case con.WM_MOUSELEAVE: btn._mouse_leave_handler()
        case MyMessages.CTRL_NOTIFY : return btn._wm_notify_handler(lp)
        case con.WM_SIZE: btn._reset_brushes()
        # We are using pre prepared gradient brushes for drawing gradient button background
        # So, whenever, we get a wm_size message, we need to set the brushes to zero value.
        # Otherwise, brushes will remain old button size and we get a weird background drawing.

    return api.DefSubclassProc(hw, msg, wp, lp)
