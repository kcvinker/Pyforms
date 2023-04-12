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
from .colors import Color, RgbColor, _createGradientBrush
from . import constants as con


btnDic = {}
btnStyle = con.WS_CHILD | con.BS_NOTIFY | con.WS_TABSTOP | con.WS_VISIBLE | con.BS_PUSHBUTTON
txtFlag = con.DT_SINGLELINE | con.DT_VCENTER | con.DT_CENTER | con.DT_NOPREFIX


class Button(Control):
    """Represents Button control"""
    _count = 1
    __slots__ = (  "_fdraw", "_gdraw")

    def __init__(self, parent, txt: str = "", xpos = 20, ypos = 20, width = 120, height = 40) -> None:
        super().__init__()
        self.name = f"Button_{Button._count}"
        self._parent = parent
        self._font = parent._font
        self._clsName = "Button"
        self._ctlType = ControlType.BUTTON
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._isTextable = True
        self._text = self.name if txt == "" else txt
        self._style = btnStyle
        self._exStyle = 0x00000004
        # self._flatBkg = False
        # self._gd_brush_click = 0
        # self._gd_brush_hover = 0
        # self._gd_brush_main = 0
        self._fdraw = None
        self._gdraw = None

        Button._count += 1
        # print(f"{btnStyle = }")

    def createHandle(self):
        self._createControl()
        if self._hwnd:
            btnDic[self._hwnd] = self
            self._setFontInternal()
            self._setSubclass(btnwndproc)


    @Control.backColor.setter
    def backColor(self, value):
        self._bgColor = Color(value) if isinstance(value, int) else value
        if self._fdraw == None: self._fdraw = FlatDraw()
        self._fdraw.setData(self._bgColor)
        if (self._drawFlag & 2) != 2: self._drawFlag += 2
        self._manageRedraw()


    def setGradientColor(self, clr1 : int, clr2 : int):
        if self._gdraw == None: self._gdraw = GradDraw()
        self._gdraw.setData(clr1, clr2)
        if not self._drawFlag & 4: self._drawFlag += 4
        self._manageRedraw()


    # Drawing text color in wm_notify message.
    def _drawforecolor(self, nmcd):
        api.SetTextColor(nmcd.hdc, self._fgColor.ref)
        api.SetBkMode(nmcd.hdc, 1)
        api.DrawText(nmcd.hdc, self._text, len(self._text), byref(nmcd.rc), txtFlag )



    def _drawBkgColor(self, nc, hbr, pen):
        api.SelectObject(nc.hdc, hbr)
        api.SelectObject(nc.hdc, pen)
        api.RoundRect(nc.hdc, nc.rc.left, nc.rc.top, nc.rc.right, nc.rc.bottom, 5, 5)
        api.FillPath(nc.hdc)



    # Drawing btn frame in wm_notify message
    # def _drawBtnFrame(self, nmc, rc, frmRcSize: int):
    #     rc2 = inflateRect(rc, frmRcSize) if frmRcSize != 0 and self._parent._is_normal_draw else rc
    #     framePen: HPEN = api.CreatePen(con.PS_SOLID, 1, self._mframecolor.ref)
    #     api.SelectObject(nmc.hdc, framePen)
    #     api.Rectangle(nmc.hdc, rc2.left, rc2.top, rc2.right, rc2.bottom)
    #     api.DeleteObject(framePen)


    # Handler for wm_notify message. Almost all button drawing is happening here
    def _wmNotifyHandler(self, lp):
        if self._drawFlag:
            nmcd = cast(lp, LPNMCUSTOMDRAW).contents
            match self._drawFlag:
                case 1: # Only fore color
                    self._drawforecolor(nmcd)
                    return con.CDRF_NOTIFYPOSTPAINT

                case 2 | 3: # Flat back color and/or fore color
                    if nmcd.dwDrawStage == con.CDDS_PREERASE:
                        return con.CDRF_NOTIFYPOSTERASE

                    elif nmcd.dwDrawStage == con.CDDS_PREPAINT:
                        if (nmcd.uItemState & 0b1) == 0b1:                  # mouse click
                            self._drawBkgColor(nmcd, self._fdraw.defbrush, self._fdraw.defpen)
                        elif (nmcd.uItemState & 0b1000000) == 0b1000000:    # mouse over
                            self._drawBkgColor(nmcd, self._fdraw.hotbrush, self._fdraw.hotpen)
                        else:                                               # Normal button state
                            self._drawBkgColor(nmcd, self._fdraw.defbrush, self._fdraw.defpen)

                        if self._drawFlag & 1:
                            self._drawforecolor(nmcd)
                            return con.CDRF_SKIPDEFAULT

                        return con.CDRF_DODEFAULT

                case 4 | 5: # Gradient back color and/or for color
                    if nmcd.dwDrawStage == con.CDDS_PREERASE:
                        return con.CDRF_NOTIFYPOSTERASE
                    elif nmcd.dwDrawStage == con.CDDS_PREPAINT:
                        if (nmcd.uItemState & 0b1) == 0b1: #--------------mouse click   (plain form clr = -1), (grad form =
                            if self._gdraw.defbrush == None:
                                # print("going to create gradient brush for mouse click")
                                self._gdraw.defbrush = _createGradientBrush(nmcd.hdc, nmcd.rc,
                                                                                self._gdraw.gcDef.c1,
                                                                                self._gdraw.gcDef.c2, True)

                            self._drawBkgColor(nmcd, self._gdraw.defbrush, self._gdraw.defpen)

                        elif (nmcd.uItemState & 0b1000000) == 0b1000000: #---mouse over
                            if self._gdraw.hotbrush == None:
                                self._gdraw.hotbrush = _createGradientBrush(nmcd.hdc, nmcd.rc,
                                                                                self._gdraw.gcHot.c1,
                                                                                self._gdraw.gcHot.c2, True)

                            self._drawBkgColor(nmcd, self._gdraw.hotbrush, self._gdraw.hotpen)

                        else: #--------------------------------------------- Normal button state
                            if self._gdraw.defbrush == None:
                                self._gdraw.defbrush = _createGradientBrush(nmcd.hdc, nmcd.rc,
                                                                                self._gdraw.gcDef.c1,
                                                                                self._gdraw.gcDef.c2, True)

                            self._drawBkgColor(nmcd, self._gdraw.defbrush, self._gdraw.defpen)

                        if self._drawFlag & 1:
                            self._drawforecolor(nmcd)
                            return con.CDRF_SKIPDEFAULT

                        return con.CDRF_DODEFAULT

        return con.CDRF_DODEFAULT

    def _resetBrushes(self):
        # Button size changed. So we need to reset our...
        # gradient brushes to zero. So that we can...
        # recreate these brushes with new size.
        if self._drawFlag > 3:
            self.defbrush = 0
            self.hotbrush = 0

    def finalize(self, scID):
        match self._drawFlag:
            case 2 | 3: self._fdraw.finalize() # Freeing flat draw resources
            case 4 | 5: self._gdraw.finalize() # Freeing grad draw resources

        api.RemoveWindowSubclass(self._hwnd, btnwndproc, scID)
        del btnDic[self._hwnd]




#End Button Class

class FlatDraw:
    __slots__ = ("defbrush", "hotbrush", "defpen", "hotpen")
    def __init__(self) -> None:
        self.defbrush = None
        self.hotbrush = None
        self.defpen = None
        self.hotpen = None

    def setData(self, c: Color):
        adj = 1.5 if c.isDark() else 1.2
        self.defbrush = c.createHBrush()
        self.hotbrush = c.createHBrush(adj)
        self.defpen = c.createHPen(0.8)
        self.hotpen = c.createHPen(0.4)

    def finalize(self):
        if self.defbrush: api.DeleteObject(self.defbrush)
        if self.hotbrush: api.DeleteObject(self.hotbrush)
        if self.defpen: api.DeleteObject(self.defpen)
        if self.hotpen: api.DeleteObject(self.hotpen)



class GradColor:
    def __init__(self) -> None:
        self.c1 = Color()
        self.c2 = Color()

class GradDraw:
    def __init__(self) -> None:
        self.gcDef = GradColor()
        self.gcHot = GradColor()
        self.defpen = None
        self.hotpen = None
        self.defbrush = None
        self.hotbrush = None

    def setData(self, uc1, uc2):
        self.gcDef.c1.updateColor(uc1)
        self.gcDef.c2.updateColor(uc2)
        hadj1 = 1.5 if self.gcDef.c1.isDark() else 1.2
        hadj2 = 1.5 if self.gcDef.c2.isDark() else 1.2
        self.gcHot.c1 = self.gcDef.c1.getShadedColor(hadj1)
        self.gcHot.c2 = self.gcDef.c2.getShadedColor(hadj2)

        self.defpen = self.gcDef.c1.createHPen(0.8)
        self.hotpen = self.gcHot.c1.createHPen(0.4)

    def finalize(self):
        print("btn destro")
        if self.defpen: api.DeleteObject(self.defpen)
        if self.hotpen: api.DeleteObject(self.hotpen)
        if self.defbrush: api.DeleteObject(self.defbrush)
        if self.hotbrush: api.DeleteObject(self.hotbrush)




@SUBCLASSPROC
def btnwndproc(hw, msg, wp, lp, scID, refData) -> LRESULT:
    # winmsgs.log_msg(msg, "Button")

    btn = btnDic[hw]
    match msg:
        case con.WM_NCDESTROY: btn.finalize(scID)

        case con.WM_SETFOCUS: return btn._gotFocusHandler()
        case con.WM_KILLFOCUS: return btn._lostFocusHandler()
        case con.WM_LBUTTONDOWN:btn._leftMouseDownHandler(msg, wp, lp)

        case con.WM_LBUTTONUP: btn._leftMouseUpHandler(msg, wp, lp)
        case MyMessages.MOUSE_CLICK: btn._mouse_click_handler()
        case con.WM_RBUTTONDOWN: btn._rightMouseDownHandler(msg, wp, lp)
        case con.WM_RBUTTONUP: btn._rightMouseUpHandler(msg, wp, lp)
        case MyMessages.RIGHT_CLICK: btn._right_mouse_click_handler()
        case con.WM_MOUSEWHEEL: btn._mouseWheenHandler(msg, wp, lp)
        case con.WM_MOUSEMOVE: btn._mouseMoveHandler(msg, wp, lp)
        case con.WM_MOUSELEAVE: btn._mouseLeaveHandler()
        case MyMessages.CTRL_NOTIFY : return btn._wmNotifyHandler(lp)
        case con.WM_SIZE: btn._resetBrushes()
        # We are using pre prepared gradient brushes for drawing gradient button background
        # So, whenever, we get a wm_size message, we need to set the brushes to zero value.
        # Otherwise, brushes will remain old button size and we get a weird background drawing.

    return api.DefSubclassProc(hw, msg, wp, lp)
