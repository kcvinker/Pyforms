# Created on 10-Nov-2022 16:16:20


from ctypes.wintypes import HWND, UINT, HPEN
from ctypes import WINFUNCTYPE, byref, cast

import horology
from .apis import LRESULT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR, LPNMCUSTOMDRAW, SUBCLASSPROC
from .control import Control
from .commons import MyMessages, inflateRect, Timing
from .enums import ControlType
from . import winmsgs
from . import apis as api
from .colors import Color, RgbColor, ButtonGradientColors, create_gradient_brush2
from . import constants as con
# from functools import cache

btnDic = {}
btnStyle = con.WS_CHILD | con.BS_NOTIFY | con.WS_TABSTOP | con.WS_VISIBLE | con.BS_PUSHBUTTON
txtFlag = con.DT_SINGLELINE | con.DT_VCENTER | con.DT_CENTER | con.DT_NOPREFIX


class Button(Control):

    _count = 1
    __slots__ = ( "_flatBkg", "_mfore_color", "_mback_color", "_mfocus_color", "_mclick_color", "_mframe_color",
                "_mgrad_def_clr1", "_mgrad_def_clr2", "_mgrad_foc_clr1", "_mgrad_foc_clr2", "_mgrad_clk_clr1",
                "_mgrad_clk_clr2", "_mgrad_top2btm", "_gd_brush_main", "_gd_brush_hover", "_gd_brush_click")

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

        # self._draw_flag = 0
        self._flatBkg = False
        self._gd_brush_click = 0
        self._gd_brush_hover = 0
        self._gd_brush_main = 0

        Button._count += 1



    def create_handle(self):
        # with Timing("btn create win ex speed "):
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


    def set_back_color(self, def_color, focus_color = -1, click_color = -1, frame_color = -1):
        self._mback_color = Color(def_color)
        self._mfocus_color = Color.from_color(def_color, -2) if focus_color == -1 else Color(focus_color)
        self._mclick_color = Color.from_color(def_color, -1) if click_color == -1 else Color(click_color)
        self._mframe_color = Color.from_color(def_color, -4) if frame_color == -1 else Color(frame_color)
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

    def set_gradient_color(self, clr1 : int, clr2 : int, top2Btm : bool = True):
        self._mgrad_top2btm = top2Btm
        self._mgrad_def_clr1 = RgbColor(clr1)
        self._mgrad_def_clr2 = RgbColor(clr2)
        self._mgrad_foc_clr1 = RgbColor.getNewShade(self._mgrad_def_clr1, 2)
        self._mgrad_foc_clr2 = RgbColor.getNewShade(self._mgrad_def_clr2, 2)
        self._mgrad_clk_clr1 = RgbColor.getNewShade(self._mgrad_def_clr1, -3)
        self._mgrad_clk_clr2 = RgbColor.getNewShade(self._mgrad_def_clr2, -3)
        self._mframe_color = Color.from_color(clr1, -4)
        if not self._draw_flag & 4: self._draw_flag += 4
        if self._is_created: pass

    def set_gradient_color_ex(self, bgc : ButtonGradientColors):
        self._mgrad_def_clr1 = bgc.def_color1
        self._mgrad_def_clr2 = bgc.def_color2
        self._mgrad_foc_clr1 = bgc.focus_color1
        self._mgrad_foc_clr2 = bgc.focus_color2
        self._mgrad_clk_clr1 = bgc.click_color1
        self._mgrad_clk_clr2 = bgc.click_color2
        self._mframe_color = bgc.frame_color
        self._mgrad_top2btm = bgc.top_to_bottom
        if not self._draw_flag & 4: self._draw_flag += 4
        if self._is_created: pass


    # Drawing text color in wm_notify message.
    def _draw_fore_color(self, nmcd):
        api.SetTextColor(nmcd.hdc, self._mfore_color.ref)
        api.SetBkMode(nmcd.hdc, 1)
        api.DrawText(nmcd.hdc, self._text, len(self._text), byref(nmcd.rc), txtFlag )

    # Drawing a flat back color in wm_notify message. Frame drawing is happening too.
    def _draw_back_color(self, nmc, btClr, btnRcSize, frmRcSize, penWidth = 1):
        rc = inflateRect(nmc.rc, btnRcSize) if btnRcSize != 0 and self._parent._is_normal_draw else nmc.rc
        hbr = api.CreateSolidBrush(btClr)
        api.SelectObject(nmc.hdc, hbr)
        api.FillRect(nmc.hdc, byref(rc), hbr)
        api.DeleteObject(hbr)

        rc2 = inflateRect(rc, frmRcSize) if frmRcSize != 0 and self._parent._is_normal_draw else rc
        framePen = api.CreatePen(con.PS_SOLID, penWidth, self._mframe_color.ref)
        # print(framePen.unused)
        api.SelectObject(nmc.hdc, framePen)
        api.Rectangle(nmc.hdc, rc2.left, rc2.top, rc2.right, rc2.bottom)
        api.DeleteObject(framePen)


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
                            self._draw_back_color(nmcd,
                                                btClr= self._mclick_color.ref,
                                                btnRcSize= -1,
                                                frmRcSize= 0,
                                                penWidth= 1)

                        elif (nmcd.uItemState & 0b1000000) == 0b1000000:    # mouse over
                            self._draw_back_color(nmcd,
                                                btClr= self._mfocus_color.ref,
                                                btnRcSize= -1,
                                                frmRcSize= 1,
                                                penWidth= 1)

                        else:                                               # Normal button state
                            self._draw_back_color(nmcd,
                                                btClr= self._mback_color.ref,
                                                btnRcSize= 0,
                                                frmRcSize= 0,
                                                penWidth= 1)

                        if self._draw_flag & 1:
                            self._draw_fore_color(nmcd)
                            return con.CDRF_SKIPDEFAULT

                        return con.CDRF_DODEFAULT

                case 4 | 5: # Gradient back color and/or for color
                    if nmcd.dwDrawStage == con.CDDS_PREERASE:
                        return con.CDRF_NOTIFYPOSTERASE
                    elif nmcd.dwDrawStage == con.CDDS_PREPAINT:
                        frame_size = 0
                        if (nmcd.uItemState & 0b1) == 0b1: #--------------mouse click   (plain form clr = -1), (grad form =
                            rc = inflateRect(nmcd.rc, -1) if self._parent._is_normal_draw else nmcd.rc
                            if self._gd_brush_click == 0:
                                # print("going to create gradient brush for mouse click")
                                self._gd_brush_click = create_gradient_brush2(nmcd.hdc, rc,
                                                                            self._mgrad_clk_clr1, self._mgrad_clk_clr2,
                                                                            self._mgrad_top2btm)
                            gBrush = self._gd_brush_click


                        elif (nmcd.uItemState & 0b1000000) == 0b1000000: #---mouse over
                            rc = inflateRect(nmcd.rc, -1) if self._parent._is_normal_draw else nmcd.rc
                            frame_size = 1
                            if self._gd_brush_hover == 0:
                                # print("going to create gradient brush for mouse hover")
                                self._gd_brush_hover = create_gradient_brush2(  nmcd.hdc, rc,
                                                                                self._mgrad_foc_clr1, self._mgrad_foc_clr2,
                                                                                self._mgrad_top2btm)
                            gBrush = self._gd_brush_hover

                        else: #--------------------------------------------- Normal button state
                            rc = nmcd.rc
                            if self._gd_brush_main == 0:
                                # print("going to create gradient brush for main use")
                                self._gd_brush_main = create_gradient_brush2(   nmcd.hdc, nmcd.rc,
                                                                                self._mgrad_def_clr1, self._mgrad_def_clr2,
                                                                                self._mgrad_top2btm)
                            gBrush = self._gd_brush_main

                        api.SelectObject(nmcd.hdc, gBrush)
                        api.FillRect(nmcd.hdc, rc, gBrush)
                        # api.DeleteObject(gBrush)
                        self._draw_btn_frame(nmcd, rc, frame_size )

                        if self._draw_flag & 1:
                            self._draw_fore_color(nmcd)
                            return con.CDRF_SKIPDEFAULT

                        return con.CDRF_DODEFAULT



        return con.CDRF_DODEFAULT

    # @property
    # def isMouseEnter(self): return self._is_mouse_entered



#End Button Class





# TODO : Delete unwanted print commands and other lines

# @WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR) # This line is crucial. Without this program will crash.
@SUBCLASSPROC
def btn_wnd_proc(hw, msg, wp, lp, scID, refData) -> LRESULT:
    # winmsgs.log_msg(msg, "Button")

    btn = btnDic[hw]
    # print("in btn wndproc ", msg)
    match msg:
        case con.WM_NCDESTROY:
            api.RemoveWindowSubclass(hw, btn_wnd_proc, scID)
            # print("remove subclass of ", btn.name)

        # case con.WM_DESTROY:
        #     print(f"{btn.name}'s [WNDPROC] gradient brush is {btn._gd_brush_click}")

        case con.WM_SETFOCUS: return btn._got_focus_handler()
        case con.WM_KILLFOCUS: return btn._lost_focus_handler()
        case con.WM_LBUTTONDOWN:btn._left_mouse_down_handler(msg, wp, lp)
        # case con.BM_SETSTATE:
        #     print("BMSET")
        case con.WM_LBUTTONUP: btn._left_mouse_up_handler(msg, wp, lp)
        case MyMessages.MOUSE_CLICK:
            # print("my click")
            btn._mouse_click_handler()
        case con.WM_RBUTTONDOWN: btn._right_mouse_down_handler(msg, wp, lp)
        case con.WM_RBUTTONUP: btn._right_mouse_up_handler(msg, wp, lp)
        case MyMessages.RIGHT_CLICK: btn._right_mouse_click_handler()
        case con.WM_MOUSEWHEEL: btn._mouse_wheel_handler(msg, wp, lp)
        case con.WM_MOUSEMOVE: btn._mouse_move_handler(msg, wp, lp)
        case con.WM_MOUSELEAVE: btn._mouse_leave_handler()
        case MyMessages.CTRL_NOTIFY :
            # with horology.Timing("wm notify btn"):
            return btn._wm_notify_handler(lp)
            # if not btn._draw_flag:
            #     hbr = api.CreateSolidBrush(0x0000ccBB)
            #     api.SelectObject(wp, hbr)
            #     return hbr
            # else:





        # case MyMessages.CTL_COMMAND:
        #     ncode = api.HIWORD(wp)
        #     print(ncode, " ncode")
        #     match ncode:
        #         case con.BN_CLICKED:
        #             print("bn clickd")


        case con.WM_SIZE:
            # We are using pre prepared gradient brushes for drawing gradient button background
            # So, whenever, we get a wm_size message, we need to set the brushes to zero value.
            # Otherwise, brushes will remain old button size and we get a weird background drawing.
            if btn._draw_flag == 4 or btn._draw_flag == 5:
                btn._gd_brush_main = 0
                btn._gd_brush_hover = 0
                btn._gd_brush_click = 0
            return 0

    return api.DefSubclassProc(hw, msg, wp, lp)
