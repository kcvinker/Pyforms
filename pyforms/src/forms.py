# Created on 08-Nov-2022 00:05:26

from ctypes import cast, byref, sizeof, POINTER, py_object, create_unicode_buffer
from ctypes.wintypes import LPCWSTR
import pyforms.src.constants as con
import pyforms.src.apis as api
from pyforms.src.apis import WNDPROC, RECT, WNDCLASSEX, LPNMHDR, LRESULT, LPMEASUREITEMSTRUCT, GetDC, MessageBox
import pyforms.src.apis as api
from pyforms.src.control import Control
from pyforms.src.enums import FormPosition, FormStyle, FormState, FormDrawMode, MessageButtons, MessageIcons
from pyforms.src.commons import Font, MyMessages, getMouseXpoint, getMouseYpoint, MyMessages, menuTxtFlag, getMousePoints
from pyforms.src.events import EventArgs, MouseEventArgs, SizeEventArgs
from pyforms.src.colors import _createGradientBrush, RgbColor, Color, COLOR_BLACK
from pyforms.src.menubar import MenuType
# from . import messagebox
import pyforms.src.winmsgs


class StaticData: # A singleton object which used to hold essential data for a form to start
    hInstance = 0
    className = "PyForms_Window"
    loopStarted = False
    screenWidth = api.GetSystemMetrics(0) # Need to calculate the form position
    screenHeight = api.GetSystemMetrics(1)
    defWinColor = Color(0xf0f0f0)# Color.from_RGB(230, 230, 230)
    currForm = None


formDict = {} # This dictionary contains all the form class. We can get them in wndProcMain function
pp_counter = 1 # IMPORTANT: This variable is used in `print_pont` function.

def printPoint2(frm, mea):
    global pp_counter
    print(f"[{pp_counter}] X : {mea.xpos}, Y : {mea.ypos}")
    pp_counter += 1

# @lru_cache(maxsize=50)
# def get_form(hwnd): return formDict.get(hwnd, StaticData.currForm)

# def get_form1(hwnd): return formDict.get(hwnd, StaticData.currForm)

# primeMsgs = [con.WM_GETMINMAXINFO, con.WM_NCCREATE, con.WM_NCDESTROY, con.WM_NCCALCSIZE, con.WM_CREATE]

#//////////////////////////////////////////////////////////////
#//   Main Window Procedure, the heart of this library
#//////////////////////////////////////////////////////////////
@WNDPROC
def wndProcMain(hw, message, wParam, lParam) -> LRESULT:
    # winmsgs.log_msg(message, "Form")
    this = formDict.get(hw, StaticData.currForm)

    match message:
        case con.WM_NCDESTROY:
            if this._isMainWindow :
                api.PostQuitMessage(0)
                return 1
        case MyMessages.THREAD_MSG:
            if this.onThreadMsg:
                this.onThreadMsg(wParam, lParam)

#   -region No problem messages
        # case con.WM_SHOWWINDOW: this._formShownHandler()
        case con.WM_ACTIVATEAPP: this._formActivateHandler(wParam)
        case con.WM_KEYDOWN | con.WM_SYSKEYDOWN: this._keyDownHandler(wParam)
        case con.WM_KEYUP | con.WM_SYSKEYUP: this._keyUpHandler(wParam)
        case con.WM_CHAR: this._keyPressHandler(wParam)
        case con.WM_LBUTTONDOWN: this._leftMouseDownHandler(message, wParam, lParam)
        case con.WM_LBUTTONUP: this._leftMouseUpHandler(message, wParam, lParam)
        case con.WM_RBUTTONDOWN: this._rightMouseDownHandler(message, wParam, lParam)
        case con.WM_RBUTTONUP: this._rightMouseUpHandler(message, wParam, lParam)
        case con.WM_MOUSEWHEEL: this._mouseWheenHandler(message, wParam, lParam)
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
            if this._drawFlag:
                this._formEraseBkgHandler(hw, wParam)
                return 1

        case con.WM_SYSCOMMAND: this._frmSysCommandHandler(wParam, lParam)
        case con.WM_CLOSE: this._formClosingHandler()
        case con.WM_DESTROY: this._formClosedHandler()
#   -endregion No problem messages

# -region Diverted messages
        case con.WM_CTLCOLOREDIT:
            return api.SendMessage(lParam, MyMessages.EDIT_COLOR, wParam, lParam)

        case con.WM_CTLCOLORSTATIC:
            return api.SendMessage(lParam, MyMessages.LABEL_COLOR, wParam, lParam)

        case con.WM_CTLCOLORLISTBOX:
            from_combo = this._comboDict.get(lParam, 0)
            # print("setting text color")
            if from_combo:
                return api.SendMessage(from_combo, MyMessages.LIST_COLOR, wParam, lParam)
            else:
                return api.SendMessage(lParam, MyMessages.LIST_COLOR, wParam, lParam)

        case con.WM_COMMAND:
            # print(f"wm command : {api.HIWORD(wParam) = }, {api.LOWORD(wParam) = }, {lParam = }")
            match lParam:
                case 0:
                    if api.HIWORD(wParam) == 0:
                        return this._menuClickHandler(api.LOWORD(wParam))
                    elif api.HIWORD(wParam) == 1:
                        pass # accelerator key commands

                case _:
                    # ctlHwnd = HWND(lParam)
                    return api.SendMessage(lParam, MyMessages.CTL_COMMAND, wParam, lParam)

        case con.WM_HSCROLL:
            return api.SendMessage(lParam, MyMessages.HORI_SCROLL, wParam, lParam)

        case con.WM_VSCROLL:
            return api.SendMessage(lParam, MyMessages.VERT_SCROLL, wParam, lParam)

        case con.WM_NOTIFY:
            nm = cast(lParam, LPNMHDR).contents
            return  api.SendMessage(nm.hwndFrom, MyMessages.CTRL_NOTIFY, wParam, lParam)

# -endregion

        # case MyMessages.MENU_EVENT_SET:
        #     menu = cast(lParam, py_object).value
        #     this._menuEventDict[menu._id] = menu

# -region Menu Section
        case con.WM_MEASUREITEM:
            pmi = cast(lParam, LPMEASUREITEMSTRUCT).contents
            mi = cast(pmi.itemData, py_object).value
            if mi._type == MenuType.BASE_MENU:
                hdc = GetDC(hw)
                size = api.SIZE()
                api.GetTextExtentPoint32(hdc, mi._wTxt, len(mi._text), byref(size))
                api.ReleaseDC(hw, hdc)
                pmi.itemWidth = size.cx #+ 10
                pmi.itemHeight = size.cy
            else:

                pmi.itemWidth = 100 #size.cx #+ 10
                pmi.itemHeight = 25
            return True

        case con.WM_DRAWITEM:
            dis = cast(lParam, api.LPDRAWITEMSTRUCT).contents
            mi = cast(dis.itemData, py_object).value
            txtClrRef = mi._fgColor.ref

            if dis.itemState == 320 or dis.itemState == 257:
                if mi._isEnabled:
                    rc = api.RECT(dis.rcItem.left + 4, dis.rcItem.top + 2, dis.rcItem.right, dis.rcItem.bottom - 2)
                    api.FillRect(dis.hDC, byref(rc), this._menuHotBgBrush)
                    api.FrameRect(dis.hDC, byref(rc), this._menuFrameBrush)
                    txtClrRef = 0x00000000
                else:
                    api.FillRect(dis.hDC, byref(rc), this._menuGrayBrush)
                    txtClrRef = this._menuGrayCref
            else:
                api.FillRect(dis.hDC, byref(dis.rcItem), this._menuDefBgBrush)
                if not mi._isEnabled: txtClrRef = this._menuGrayCref

            api.SetBkMode(dis.hDC, con.TRANSPARENT)
            if mi._type == MenuType.BASE_MENU:
                dis.rcItem.left += 10
            else:
                dis.rcItem.left += 25
            api.SelectObject(dis.hDC, this._menuFont.handle)
            api.SetTextColor(dis.hDC, txtClrRef)
            api.DrawText(dis.hDC, mi._wideText, -1, byref(dis.rcItem), menuTxtFlag)
            return 0

        case MyMessages.MENU_ADDED:
            # When user adds a menu item to another menu item, the parent menu will inform us.
            this._menuItemDict[wParam] = cast(lParam, py_object).value
            return 0



        # case con.WM_ENTERMENULOOP:
        #     print("case con.WM_ENTERMENULOOP ", wParam)
        # case con.WM_EXITMENULOOP:
        #     print("case con.WM_EXITMENULOOP:")

        case con.WM_MENUSELECT:
            pmenu = this._getMenuFromHmenu(lParam)
            mid = api.LOWORD(wParam) # Could be an id of a child menu or index of a child menu
            hwwpm = api.HIWORD(wParam)
            if pmenu:
                menu = None
                match hwwpm:
                    case 33152: # A normal child menu. We can use mid ad menu id.
                        menu = this._menuItemDict.get(mid, 0)
                    case 33168: # A popup child menu. We can use mid as index.
                        menu = pmenu.getChildFromIndex(mid)
                if menu and menu.onFocus: menu.onFocus(menu, EventArgs())

        case con.WM_INITMENUPOPUP:
            menu = this._getMenuFromHmenu(wParam)
            if menu and menu.onPopup:
                menu.onPopup(menu, EventArgs())

        case con.WM_UNINITMENUPOPUP:
            menu = this._getMenuFromHmenu(wParam)
            if menu and menu.onCloseup:
                menu.onCloseup(menu, EventArgs())
# -endregion Menu section



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
    wc.hbrBackground = api.CreateSolidBrush(StaticData.defWinColor.ref)
    wc.lpszClassName = StaticData.className
    # print("style-----  ", wc.style)
    return wc



#//////////////////////////////////////////////////////////////
#//   Form class, This class represents a window
#//////////////////////////////////////////////////////////////
class Form(Control):

    """Form class represents a Window."""

    wnd_class = make_window_class(wndProcMain)
    atom = api.RegisterClassEx(byref(wnd_class))
    _count = 1
    __slots__ = (   "_classStr", "_formPos", "_formStyle", "_formState", "_topMost", "_maximizeBox", "_minimizeBox",
                    "_mainWinHwnd", "_isMainWindow", "_isMouseTracking", "_drawMode", "_isNormalDraw", "_updRect",
                    "_formID", "_comboDict", "onLoad", "onMinimized", "onMaximized", "onRestored", "onClosing",
                    "onClosed", "onActivate", "onDeActivate", "onMoving", "onMoved", "onSizing", "onSized",
                    "onThreadMsg", "_menuGrayBrush", "_menuGrayCref", "_menuEventDict", "_menuItemDict",
                    "_menuDefBgBrush", "_menuHotBgBrush", "_menuFont", "_menuFrameBrush")

    def __init__(self, txt = "", width = 500, height = 400, bCreate = False) -> None:
        super().__init__()
        self._classStr = ""
        self.name = f"Form_{Form._count}"
        self._text = self.name if txt == "" else txt
        self._width = width
        self._height = height
        self._style = con.WS_OVERLAPPEDWINDOW | con.WS_CLIPCHILDREN | con.WS_VISIBLE
        self._isTextable = True # If this is True, users can get or set text property
        self._font = Font() # Font handle is not created yet. It's just a font class
        self._bgColor = Color(StaticData.defWinColor) # Defining a globar window color for all windows
        self._fgColor = COLOR_BLACK
        self._formPos = FormPosition.CENTER # Defining where to appear on the screen
        self._formStyle = FormStyle.SIZABLE # Defining the style of this form
        self._formState = FormState.NORMAL # Other options are minimize & maximize
        self._topMost = False
        self._maximizeBox = True
        self._minimizeBox = True
        self._mainWinHwnd = None
        self._isMainWindow = False
        self._isMouseTracking = False # A flag to control mouse tracking in oreder to get the mouse move msg
        self._drawMode = FormDrawMode.NORMAL # Other options are flat color & gradient
        self._isNormalDraw = True
        self._formID = Form._count + 1000 # A unique ID for all forms.
        self._comboDict = {} # Combo boxes demands to keep their listbox handle
        self._updRect = None
        self._menuEventDict = {}
        self._menuItemDict = {}
        self._menuFrameBrush = None
        self._menuGrayBrush = None
        self._menuGrayCref = None
        # print("form inited")


        # Events
        self.onLoad = None
        self.onMinimized = None
        self.onMaximized = None
        self.onRestored = None
        self.onClosing = None
        self.onClosed = None
        self.onActivate = None
        self.onDeActivate = None
        self.onMoving = None
        self.onMoved = None
        self.onSizing = None
        self.onSized = None
        self.onThreadMsg = None

        Form._count += 1
        if bCreate: self.createHandle()
    #------------------------------



    # -region Public functions
    def createHandle(self):
        """Creating window handle """

        self._setLocation()
        self._setStyles()
        StaticData.currForm = self
        self._hwnd = api.CreateWindowEx(self._exStyle,
                                        self.wnd_class.lpszClassName,
                                        self._text,
                                        self._style,
                                        self._xpos, self._ypos,
                                        self._width, self._height,
                                        0, 0, self.wnd_class.hInstance, None)

        if self._hwnd:
            formDict[self._hwnd] = self
            self._isCreated = True
            self._setFontInternal()
            StaticData.currForm = None
        else:
            print("window creation failed")

    def close(self):
        api.DestroyWindow(self._hwnd)

    # Print mouse points. Useful for getting mouse points in order to place the controls.
    def printPoint(self, me):
        global pp_counter
        print(f"[{pp_counter}] X : {me.xpos}, Y : {me.ypos}")
        pp_counter += 1

    def setGradientColor(self, clr1, clr2, top2btm = True):
        self._mGClr1 = RgbColor(clr1)
        self._mGClr2 = RgbColor(clr2)
        self._mGt2b = top2btm
        self._drawMode = FormDrawMode.GRADIENT
        self._isNormalDraw = False
        if self._isCreated: pass

    def display(self):
        """Display a window. If it's the first window, then it will start the main loop"""

        api.ShowWindow(self._hwnd, con.SW_SHOW)

        if self.formState == FormState.MINIMIZED :
            api.CloseWindow(self._hwnd)
        else:
            api.UpdateWindow(self._hwnd)

        if self.onLoad: self._formShownHandler() # We moved onLoad event to here. WM_SHOWWINDOW is not working.

        if not StaticData.loopStarted:
            self._isMainWindow = True
            StaticData.loopStarted = True
            tMsg = api.MSG()
            while api.GetMessage(byref(tMsg), None, 0, 0) > 0:
                api.TranslateMessage(byref(tMsg))
                api.DispatchMessage(byref(tMsg))

    def msgbox(self, msg: str, title: str = "PyForms Message",
			btns: MessageButtons = MessageButtons.OKAY,
			icon: MessageIcons = MessageIcons.NONE ):
            wMsg = create_unicode_buffer(msg)
            wCap = create_unicode_buffer(title)
            return MessageBox(0, wMsg, wCap, btns.value | icon.value)


    # -endregion

    # -region Private functions
    def _setLocation(self) :
        match self._formPos:
            case FormPosition.CENTER:
                self._xpos = int((StaticData.screenWidth - self._width) / 2)
                self._ypos = int((StaticData.screenHeight - self._height) / 2)
            case FormPosition.TOP_LEFT:
                pass
            case FormPosition.TOP_MID:
                self._xpos = int((StaticData.screenWidth - self._width) / 2)
            case FormPosition.TOP_RIGHT:
                self._xpos = StaticData.screenWidth - self._width
            case FormPosition.MID_LEFT:
                self._ypos = int((StaticData.screenHeight - self._height) / 2)
            case FormPosition.MID_RIGHT:
                self._xpos = StaticData.screenWidth - self._width
                self._ypos = int((StaticData.screenHeight - self._height) / 2)
            case FormPosition.BOTTOM_LEFT:
                self._ypos = StaticData.screenHeight - self._height
            case FormPosition.BOTTOM_MID:
                self._xpos = int((StaticData.screenWidth - self._width) / 2)
                self._ypos = StaticData.screenHeight - self._height
            case FormPosition.BOTTOM_RIGHT:
                self._xpos = StaticData.screenWidth - self._width
                self._ypos = StaticData.screenHeight - self._height
            case FormPosition.MANUAL:
                pass

    def _setStyles(self):
        mxFlag = False
        match self._formStyle:
            case FormStyle.NONE:
                self._exStyle = 0x00050000
                self._style = 0x16010000
            case FormStyle.FIXED_SINGLE:
                self._exStyle = 0x00050100
                self._style = 0x16CB0000
                mxFlag = True
            case FormStyle.FIXED_3D:
                self._exStyle = 0x00050300
                self._style = 0x16CB0000
                mxFlag = True
            case FormStyle.FIXED_DIALOG:
                self._exStyle = 0x00050100
                self._style = 0x16CB0000
                mxFlag = True
            case FormStyle.FIXED_TOOL:
                self._exStyle = 0x00050100
                self._style = 0x16CF0000
            case FormStyle.SIZABLE:
                self._exStyle = 0x00050100
                self._style = 0x16CF0000 | con.WS_OVERLAPPEDWINDOW
            case FormStyle.SIZABLE_TOOL:
                self._exStyle = 0x00050180
                self._style = 0xCF0000 # con.WS_OVERLAPPEDWINDOW
                mxFlag = True
            case FormStyle.HIDDEN:
                self._exStyle = con.WS_EX_TOOLWINDOW
                self._style = con.WS_BORDER

        if mxFlag:
            if not self._maximizeBox : self._style ^= con.WS_maximize_box
            if not self._minimizeBox : self._style ^= con.WS_MINIMIZEBOX
            # print(f"state of maximize box {self._maximizeBox}")

        if self._topMost: self._exStyle = self._exStyle or con.WS_EX_top_most
        if self._formState == FormState.MAXIMIZED: self._style |= con.WS_MAXIMIZE
        # print(f"Ex style bits of this form - {hex(self._exStyle)}")
        # print(f"style bits of this form - {hex(self._style)}")

    def _saveComboInfo(self, lb_hwnd, cmb_hwnd): self._comboDict[lb_hwnd] = cmb_hwnd

    def _drawUpdFrame(self, hdc):

        if self._updRect:
            # print("327")
            # res = api.DrawEdge(hdc, byref(self._updRect), con.BDR_RAISEDINNER, con.BF_RECT | con.BF_ADJUST)
            clr = Color(0xff0000)
            fpen = api.CreatePen(con.PS_SOLID, 1, clr.ref)
            api.SelectObject(hdc, fpen)
            api.Rectangle(hdc, self._updRect.left, self._updRect.top, self._updRect.right, self._updRect.bottom)
            api.DeleteObject(fpen)
            # print("edge ", res)

    def _menuClickHandler(self, menu_id):
        menu = self._menuItemDict.get(menu_id, 0)
        if menu:
            if menu.onClick: menu.onClick(menu, EventArgs())
        return 0



    def _getMenuFromHmenu(self, menuHandle):
        for menu in self._menuItemDict.values():
            if menu._hmenu == menuHandle: return menu
        return None


    # -endregion private functions

    # -region Event handlers
    def _formActivateHandler(self, wp):
        if self.onActivate or self.onDeActivate:
            ea = EventArgs()
            activate = bool(wp)
            if not activate:
                if self.onDeActivate: self.onDeActivate(self, ea)
            else:
                if self.onActivate: self.onActivate(self, ea)
        return 0

    def _formShownHandler(self):
        # if self.onLoad:
        ea = EventArgs()
        self.onLoad(self, ea)
        return 0

    def _formMouseMoveHandler(self,hw, msg, wp, lp):
        if not self._isMouseTracking:
            self._isMouseTracking = True
            self._trackMouseEvents(hw)
            if not self._isMouseEntered:
                if self._onMouseEnter:
                    self._isMouseEntered = True
                    ea = EventArgs()
                    self._onMouseEnter(self, ea)
        if self.onMouseMove:
            ea = MouseEventArgs(msg, wp, lp)
            self.onMouseMove(self, ea)
        return 0

    def _formMouseLeaveHandler(self):
        if self._isMouseTracking:
            self._isMouseTracking = False
            self._isMouseEntered = False

        if self._onMouseLeave:
            ea = EventArgs()
            self._onMouseLeave(self, ea)
        return 0

    def _formMouseHoverHandler(self, msg, wp, lp):
        if self._isMouseTracking: self._isMouseTracking = False
        if self.onMouseHover:
            ea = MouseEventArgs(msg, wp, lp)
            self.onMouseHover(self, ea)
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
        if self.onSizing:
            self.onSizing(self, ea)
        return 0


    def _formSizedHandler(self, msg, wp, lp):
        if self.onSizing:
            ea = SizeEventArgs(msg, wp, lp)
            self.onSizing(self, ea)
        return 0


    def _formMovingHandler(self, lp):
        rct = cast(lp, POINTER(RECT)).contents
        self._xpos = rct.left
        self._ypos = rct.top
        if self.onMoving:
            ea = EventArgs()
            self.onMoving(self, ea)
            # return 0
        return 0

    def _formMovedHandler(self, lp):
        self._xpos = getMouseXpoint(lp)
        self._ypos = getMouseYpoint(lp)
        if self.onMoved:
            ea = EventArgs()
            self.onMoved(self, ea)
        return 0

    def _frmSysCommandHandler(self, wp, lp):
        uMsg = int(wp & 0xFFF0)
        match uMsg:
            case con.SC_MINIMIZE:
                if self.onMinimized:
                    ea = EventArgs()
                    self.onMinimized(self, ea)

            case con.SC_RESTORE:
                if self.onRestored:
                    ea = EventArgs()
                    self.onRestored(self, ea)

            case con.SC_MAXIMIZE:
                if self.onMaximized:
                    ea = EventArgs()
                    self.onMaximized(self, ea)

            # case 0xF090 | 0xF100:
            #     self._selMenuPt = getMousePoints(lp)
                # print(pt.x, pt.y)



    def _formClosingHandler(self):
        if self.onClosing:
            ea = EventArgs()
            self.onClosing(self, ea)

    def _formClosedHandler(self):
        if self.onClosed:
            ea = EventArgs()
            self.onClosed(self, ea)

    def _formEraseBkgHandler(self, hwnd, wp):
        # if self._drawMode != FormDrawMode.NORMAL:
        # dch = cast(wp, HDC).value
        rct = api.get_client_rect(hwnd)
        # api.GetClientRect(hwnd, byref(rct))

        if self._drawMode == FormDrawMode.COLORED:
            hbr = api.CreateSolidBrush(self._bkClrRef)
        else:
            # with Timing("create gradient speed : "):
            hbr = _createGradientBrush( wp, rct, self._mGClr1, self._mGClr2, self._mGt2b )
        api.FillRect(wp, byref(rct), hbr)
        api.DeleteObject(hbr)

    # -endregion

    # -region Properties

    @property
    def formID(self): return self._formID

    @property
    def formPos(self): return self._formPos

    @formPos.setter
    def formPos(self, value: FormPosition):
        self._formPos = value
        if self._isCreated:
            pass

    #---------------------------------------

    @property
    def formStyle(self): return self._formStyle

    @formStyle.setter
    def formStyle(self, value: FormStyle):
        self._formStyle = value
        if self._isCreated:
            pass

    #---------------------------------------

    @property
    def formState(self): return self._formState

    @formState.setter
    def formState(self, value: FormState):
        self._formState = value
        if self._isCreated:
            pass

    #---------------------------------------

    @Control.xpos.setter # Overriding base class's setter
    def xpos(self, value: int):
        self._xpos = value
        self._formPos = FormPosition.MANUAL
        if self._isCreated:
            pass

    #---------------------------------------

    @Control.ypos.setter # Overriding base class's setter
    def ypos(self, value: int):
        self._ypos = value
        self._formPos = FormPosition.MANUAL
        if self._isCreated:
            pass

    #---------------------------------------



    @Control.backColor.setter
    def backColor(self, value):
        self._bgColor.update_color(value)
        self._drawMode = FormDrawMode.COLORED
        if not self._drawFlag: self._drawFlag = 1
        self._isNormalDraw = False
        self._manageRedraw() # This will re draw the window if needed



    def enablePrintPoint(self):
        self.onMouseDown = printPoint2

    # -endregion

#-----------------------------------------------END OF FORM CLASS-----------------------------------