# Created on 10-Nov-2022 16:16:20


from ctypes.wintypes import HPEN
from ctypes import byref, cast

# import horology
from pyforms.apis import LRESULT, LPNMCUSTOMDRAW, SUBCLASSPROC
from pyforms.control import Control
from pyforms.commons import MyMessages, inflateRect
from pyforms.enums import ControlType
from pyforms.events import GEA

import pyforms.apis as api
from pyforms.colors import Color, RgbColor, _createGradientBrush
import pyforms.constants as con


btnDic = {}
# btnStyle = con.BS_NOTIFY | con.BS_PUSHBUTTON
txtFlag = con.DT_SINGLELINE | con.DT_VCENTER | con.DT_CENTER | con.DT_NOPREFIX


class Button(Control):
    """Represents Button control"""
    _count = 1
    __slots__ = ("_fdraw", "_gdraw", "_focused")

    def __init__(self, parent, txt: str = "", xpos = 20, ypos = 20, 
                 width = 120, height = 33, onclick = None ) -> None:
        super().__init__(parent, ControlType.BUTTON, width, height)
        self.name = f"Button_{Button._count}"     
        self._xpos = xpos
        self._ypos = ypos
        self._isTextable = True
        self._text = self.name if txt == "" else txt
        self._style |= con.BS_NOTIFY | con.BS_PUSHBUTTON
        self._exStyle = 0 #0x00000004
        self._fdraw = None
        self._gdraw = None
        self._focused = False
        parent._controls.append(self)
        if onclick: self.onClick = onclick
        Button._count += 1
        if parent.createChilds: self.createHandle()
        

    def createHandle(self):
        self._createControl()
        if self._hwnd:
            btnDic[self._hwnd] = self
            self._setFontInternal()
            self._setSubclass(btnwndproc)


    @Control.backColor.setter
    def backColor(self, value):
        self._bgColor = Color(value) if isinstance(value, int) else value
        if self._fdraw == None: 
            self._fdraw = FlatDraw()
        else:
            self._fdraw.finalize()

        self._fdraw.setData(self._bgColor) #, self._width, self._height)
        if (self._drawFlag & 2) != 2: self._drawFlag += 2
        self._manageRedraw()



    def setGradientColor(self, clr1 : int, clr2 : int):
        if self._gdraw == None: 
            self._gdraw = GradDraw()
        else:
            self._gdraw.finalize()

        self._gdraw.setData(clr1, clr2)
        if not self._drawFlag & 4: self._drawFlag += 4
        self._manageRedraw()


    # Drawing text color in wm_notify message.
    def _drawforecolor(self, nmcd):
        api.SetTextColor(nmcd.hdc, self._fgColor.ref)
        api.SetBkMode(nmcd.hdc, 1)
        api.DrawText(nmcd.hdc, self._text, len(self._text), 
                     byref(nmcd.rc), txtFlag )


    def _drawBkgColor(self, nc, hbr, pen):
        api.SelectObject(nc.hdc, hbr)
        api.SelectObject(nc.hdc, pen)
        api.RoundRect(nc.hdc, nc.rc.left, nc.rc.top, 
                      nc.rc.right, nc.rc.bottom, 5, 5)
        api.FillPath(nc.hdc)


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
                            self._fdraw.drawButtonBackColor(nmcd, True)
                        elif (nmcd.uItemState & 0b1000000) == 0b1000000:    # mouse over
                            self._fdraw.drawButtonBackColor(nmcd, False)
                        else:                                               # Normal button state
                            self._fdraw.drawButtonBackColor(nmcd, True)

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
                                self._gdraw.defbrush = _createGradientBrush(nmcd.hdc, 
                                                                            nmcd.rc,
                                                                            self._gdraw.gcDef.c1,
                                                                            self._gdraw.gcDef.c2, 
                                                                            True)

                            self._drawBkgColor(nmcd, self._gdraw.defbrush, 
                                               self._gdraw.defpen)

                        elif (nmcd.uItemState & 0b1000000) == 0b1000000: #---mouse over
                            if self._gdraw.hotbrush == None:
                                self._gdraw.hotbrush = _createGradientBrush(nmcd.hdc, 
                                                                            nmcd.rc,
                                                                            self._gdraw.gcHot.c1,
                                                                            self._gdraw.gcHot.c2, 
                                                                            True)

                            self._drawBkgColor(nmcd, self._gdraw.hotbrush, 
                                               self._gdraw.hotpen)

                        else: #--------------------------------------------- Normal button state
                            if self._gdraw.defbrush == None:
                                self._gdraw.defbrush = _createGradientBrush(nmcd.hdc, 
                                                                            nmcd.rc,
                                                                            self._gdraw.gcDef.c1,
                                                                            self._gdraw.gcDef.c2, 
                                                                            True)

                            self._drawBkgColor(nmcd, self._gdraw.defbrush, 
                                               self._gdraw.defpen)

                        if self._drawFlag & 1:
                            self._drawforecolor(nmcd)
                            return con.CDRF_SKIPDEFAULT

                        return con.CDRF_DODEFAULT

        return con.CDRF_DODEFAULT


    def finalize(self, scID):
        api.RemoveWindowSubclass(self._hwnd, btnwndproc, scID)
        match self._drawFlag:
            case 2 | 3: self._fdraw.finalize() # Freeing flat draw resources
            case 4 | 5: self._gdraw.finalize() # Freeing grad draw resources
        
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


    def drawButtonBackColor(self, nc, defaultBrush):
        # condition = self.defDrawn if defaultBrush else self.hotDrawn
        hbr = self.defbrush if defaultBrush else self.hotbrush
        api.SelectObject(nc.hdc, hbr)
        # api.SelectObject(nc.hdc, pen)
        api.RoundRect(nc.hdc, nc.rc.left, nc.rc.top, nc.rc.right, nc.rc.bottom, 5, 5)
        api.FillPath(nc.hdc)

    def finalize(self):
        if self.defbrush: api.DeleteObject(self.defbrush)
        if self.hotbrush: api.DeleteObject(self.hotbrush)
        if self.defpen: api.DeleteObject(self.defpen)
        if self.hotpen: api.DeleteObject(self.hotpen)
        self.defbrush = None
        self.hotbrush = None
        self.defpen = None
        self.hotpen = None



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
        if self.defpen: api.DeleteObject(self.defpen)
        if self.hotpen: api.DeleteObject(self.hotpen)
        if self.defbrush: api.DeleteObject(self.defbrush)
        if self.hotbrush: api.DeleteObject(self.hotbrush)
        self.defpen = None
        self.hotpen = None
        self.defbrush = None
        self.hotbrush = None



@SUBCLASSPROC
def btnwndproc(hw, msg, wp, lp, scID, refData) -> LRESULT:
    # winmsgs.log_msg(msg, "Button")
    match msg:
        case con.WM_DESTROY:
            this = btnDic[hw] 
            this.finalize(scID)
            del this

        case con.WM_KEYDOWN:
            this = btnDic[hw]
            if wp == 0x0D : #and this._focused:
                if this.onClick: this.onClick(this, GEA)          

            if wp == 0x09 and this._tabOrderHwnd: 
                api.SetFocus(this._tabOrderHwnd)
            return 0

        # case con.WM_SETFOCUS:
        #     this = btnDic[hw]
        #     this._focused = True
            # return api.DefWindowProc(hw, msg, wp, lp)
            # return 0
            # print("btn focused")
        #     this = btnDic[hw] 
        #     return this._gotFocusHandler()

        # case con.WM_KILLFOCUS:
        #     this = btnDic[hw]
        #     this._focused = False
        #     return api.DefWindowProc(hw, msg, wp, lp)
        #     return this._lostFocusHandler()

        case con.WM_LBUTTONDOWN:
            this = btnDic[hw]
            this._leftMouseDownHandler(msg, wp, lp)
        case con.WM_LBUTTONUP:
            this = btnDic[hw]
            this._leftMouseUpHandler(msg, wp, lp)
        case con.WM_RBUTTONDOWN:
            this = btnDic[hw]
            this._rightMouseDownHandler(msg, wp, lp)
        case con.WM_RBUTTONUP:
            this = btnDic[hw]
            this._rightMouseUpHandler(msg, wp, lp)
        case con.WM_MOUSEWHEEL:
            this = btnDic[hw]
            this._mouseWheenHandler(msg, wp, lp)
        case con.WM_MOUSEMOVE:
            this = btnDic[hw]
            this._mouseMoveHandler(msg, wp, lp)
        case con.WM_MOUSELEAVE:
            this = btnDic[hw]
            this._mouseLeaveHandler()
        case MyMessages.CTRL_NOTIFY :
            this = btnDic[hw]
            return this._wmNotifyHandler(lp)
        case con.WM_SIZE:
            this = btnDic[hw]
            if this._gDraw:
                this._gDraw.finalize()

        case MyMessages.MM_FONT_CHANGED:
            # User changed any font property. We need to recreate the font handle.
            btn = btnDict[hw]
            btn.updateFontInternal()
            return 0

        # We are using pre prepared gradient brushes for drawing gradient button background
        # So, whenever, we get a wm_size message, we need to set the brushes to zero value.
        # Otherwise, brushes will remain old button size and we get a weird background drawing.

    return api.DefSubclassProc(hw, msg, wp, lp)
