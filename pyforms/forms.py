# Created on 08-Nov-2022 00:05:26

from ctypes import (cast, byref, sizeof, POINTER, 
                    py_object, create_unicode_buffer, 
                    WINFUNCTYPE, c_void_p, addressof)
from ctypes.wintypes import LPCWSTR, HBRUSH, LPWSTR, WPARAM, LPARAM
import pyforms.constants as con
import pyforms.apis as api
from pyforms.apis import (WNDPROC, RECT, WNDCLASSEX, 
                              LPNMHDR, LRESULT, LPMEASUREITEMSTRUCT, 
                              GetDC, MessageBox)
from pyforms.control import Control
from pyforms.enums import (FormPosition, FormStyle, 
                               FormState, FormDrawMode, 
                               MessageButtons, MessageIcons, 
                               ControlType, Keys)
from pyforms.commons import (
            Font, MyMessages, getMouseXpoint, getMouseYpoint, 
            menuTxtFlag, getMousePoints, getSystemDPI,
            StaticData, log_cnt)
from pyforms.events import (
    EventArgs, MouseEventArgs, SizeEventArgs, GEA)
from pyforms.colors import (_createGradientBrush, RgbColor, 
                                Color, COLOR_BLACK)
from pyforms.menubar import MenuType, MenuState
# from . import messagebox
import pyforms.winmsgs
from horology import Timing
import os


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
    # th = formDict.get(hw, StaticData.currForm)
    # log_cnt(f"{th.text=}, {message=}")
    match message:
        case con.WM_NCDESTROY:
            this = formDict.get(hw, StaticData.currForm)
            this.finalize()
            if this._isMainWindow :
                api.PostQuitMessage(0)
                return 1
            
        case MyMessages.THREAD_MSG:
            this = formDict.get(hw, StaticData.currForm)
            if this.onThreadMsg:
                this.onThreadMsg(wParam, lParam)

        case con.WM_TIMER: 
            this = formDict.get(hw, StaticData.currForm)
            this.handle_wmtimer(wParam)

        case MyMessages.MM_TIMER_DESTROY:
            this = formDict.get(hw, StaticData.currForm)
            if wParam in this._timerDic:
                del this._timerDic[wParam]
                
            return 0

        case con.WM_COPYDATA:
            this = formDict.get(hw, StaticData.currForm)
            if this.onCopyData:
                cd = cast(lParam, api.LPCOPYDATA).contents
                this.onCopyData(wParam, cd)

        case con.WM_HOTKEY:
            this = formDict.get(hw, StaticData.currForm)
            func = this._hotkeyDict.get(wParam)
            if func: func(this, GEA)


    # -region No problem messages
        # case con.WM_SHOWWINDOW: this._formShownHandler() # NOT NEEDED
        case con.WM_ACTIVATEAPP: 
            this = formDict.get(hw, StaticData.currForm)
            this._formActivateHandler(wParam)
        case con.WM_KEYDOWN | con.WM_SYSKEYDOWN: 
            this = formDict.get(hw, StaticData.currForm)
            this._keyDownHandler(wParam)
        case con.WM_KEYUP | con.WM_SYSKEYUP: 
            this = formDict.get(hw, StaticData.currForm)
            this._keyUpHandler(wParam)
        case con.WM_CHAR: 
            this = formDict.get(hw, StaticData.currForm)
            this._keyPressHandler(wParam)
        case con.WM_LBUTTONDOWN: 
            this = formDict.get(hw, StaticData.currForm)
            this._leftMouseDownHandler(message, wParam, lParam)
        case con.WM_LBUTTONUP: 
            this = formDict.get(hw, StaticData.currForm)
            this._leftMouseUpHandler(message, wParam, lParam)
        case con.WM_RBUTTONDOWN: 
            this = formDict.get(hw, StaticData.currForm)
            this._rightMouseDownHandler(message, wParam, lParam)
        case con.WM_RBUTTONUP: 
            this = formDict.get(hw, StaticData.currForm)
            this._rightMouseUpHandler(message, wParam, lParam)
        case con.WM_MOUSEWHEEL: 
            this = formDict.get(hw, StaticData.currForm)
            this._mouseWheenHandler(message, wParam, lParam)
        case con.WM_MOUSEMOVE: 
            this = formDict.get(hw, StaticData.currForm)
            this._formMouseMoveHandler(hw, message, wParam, lParam)
        case con.WM_MOUSELEAVE: 
            this = formDict.get(hw, StaticData.currForm)
            this._formMouseLeaveHandler()
        case con.WM_MOUSEHOVER: 
            this = formDict.get(hw, StaticData.currForm)
            this._formMouseHoverHandler(message, wParam, lParam)
        case con.WM_SIZING:
            this = formDict.get(hw, StaticData.currForm)
            return this._formSizingHandler(message, wParam, lParam)
        case con.WM_SIZE:
            this = formDict.get(hw, StaticData.currForm)
            return this._formSizedHandler(message, wParam, lParam)
        case con.WM_MOVING: 
            this = formDict.get(hw, StaticData.currForm)
            return this._formMovingHandler(lParam)
        case con.WM_MOVE: 
            this = formDict.get(hw, StaticData.currForm)
            return this._formMovedHandler(lParam)
        case con.WM_ERASEBKGND:
            this = formDict.get(hw, StaticData.currForm)
            if this._drawMode != FormDrawMode.NORMAL:
                this._formEraseBkgHandler(hw, wParam)
                return 1

        case con.WM_SYSCOMMAND: 
            this = formDict.get(hw, StaticData.currForm)
            this._frmSysCommandHandler(wParam, lParam)
        case con.WM_CLOSE: 
            this = formDict.get(hw, StaticData.currForm)
            this._formClosingHandler()

        case con.WM_DESTROY: 
            this = formDict.get(hw, StaticData.currForm)
            this._formClosedHandler()
    #   -endregion No problem messages

    # -region Diverted messages
        case con.WM_CTLCOLOREDIT:
            this = formDict.get(hw, StaticData.currForm)
            return api.SendMessage(lParam, MyMessages.EDIT_COLOR, wParam, lParam)

        case con.WM_CTLCOLORSTATIC:
            this = formDict.get(hw, StaticData.currForm)
            return api.SendMessage(lParam, MyMessages.LABEL_COLOR, wParam, lParam)

        case con.WM_CTLCOLORLISTBOX:
            this = formDict.get(hw, StaticData.currForm)
            from_combo = this._comboDict.get(lParam, lParam)
            # print("setting text color")
            # if from_combo:
            return api.SendMessage(from_combo, MyMessages.LIST_COLOR, wParam, lParam)
            # else:
                # return api.SendMessage(lParam, MyMessages.LIST_COLOR, wParam, lParam)

        case con.WM_COMMAND:
            this = formDict.get(hw, StaticData.currForm)
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
            pmi.itemWidth = mi._txtSize.cx + 10
            pmi.itemHeight = mi._txtSize.cy + 10
            return 1

        case con.WM_DRAWITEM:
            this = formDict.get(hw, StaticData.currForm)
            dis = cast(lParam, api.LPDRAWITEMSTRUCT).contents
            mi = cast(dis.itemData, py_object).value
            txtClrRef = mi._fgColor.ref
            if dis.itemState == 320 or dis.itemState == 257:
                if not mi._state == MenuState.DISABLED:
                    rc = api.RECT(dis.rcItem.left + 4, dis.rcItem.top + 2, dis.rcItem.right, dis.rcItem.bottom - 2)
                    api.FillRect(dis.hDC, byref(rc), this._menubar._hotBgBrush)
                    api.FrameRect(dis.hDC, byref(rc), this._menubar._frameBrush)
                    txtClrRef = 0x00000000
                else:
                    api.FillRect(dis.hDC, byref(rc), this._menubar._grayBrush)
                    txtClrRef = this._menubar._grayCref
            else:
                api.FillRect(dis.hDC, byref(dis.rcItem), this._menubar._defBgBrush)
                if mi._state == MenuState.DISABLED: txtClrRef = this._menubar._grayCref

            api.SetBkMode(dis.hDC, con.TRANSPARENT)
            if mi._type == MenuType.BASE_MENU:
                dis.rcItem.left += 10
            else:
                dis.rcItem.left += 25
            api.SelectObject(dis.hDC, this._menubar._font.handle)
            api.SetTextColor(dis.hDC, txtClrRef)
            api.DrawText(dis.hDC, mi._text, len(mi._text), byref(dis.rcItem), menuTxtFlag)
            return 0

        case MyMessages.MENU_ADDED:
            # When user adds a menu item to another menu item, the parent menu will inform us.
            this = formDict.get(hw, StaticData.currForm)
            this._menuDict[wParam] = cast(lParam, py_object).value            
            return 0

        case MyMessages.MM_FONT_CHANGED:
            # User changed any font property. We need to recreate the hfont.
            this = formDict.get(hw, StaticData.currForm)
            if this._font._handle != 0:
                api.DeleteObject(self._font._handle)
                this._font.createHandle()
                api.SendMessage(self._hwnd, con.WM_SETFONT, self._font._handle, True)


        # case con.WM_ENTERMENULOOP:
        #     print("case con.WM_ENTERMENULOOP ", wParam)
        # case con.WM_EXITMENULOOP:
        #     print("case con.WM_EXITMENULOOP:")

        case con.WM_MENUSELECT:
            this = formDict.get(hw, StaticData.currForm)
            pmenu = this._getMenuFromHmenu(lParam)
            mid = api.LOWORD(wParam) # Could be an id of a child menu or index of a child menu
            hwwpm = api.HIWORD(wParam)
            if pmenu:
                menu = None
                match hwwpm:
                    case 33152: # A normal child menu. We can use mid ad menu id.
                        menu = this._menuDict.get(mid, 0)
                    case 33168: # A popup child menu. We can use mid as index.
                        menu = pmenu.getChildFromIndex(mid)
                if menu and menu.onFocus: menu.onFocus(menu, GEA)

        case con.WM_INITMENUPOPUP:
            this = formDict.get(hw, StaticData.currForm)
            menu = this._getMenuFromHmenu(wParam)
            if menu and menu.onPopup:
                menu.onPopup(menu, GEA)

        case con.WM_UNINITMENUPOPUP:
            this = formDict.get(hw, StaticData.currForm)
            menu = this._getMenuFromHmenu(wParam)
            if menu and menu.onCloseup:
                menu.onCloseup(menu, GEA)
    # -endregion Menu section
        case MyMessages.MM_FORM_NOTIFY:
            this = formDict.get(hw, StaticData.currForm)            
            if this.onFormMsg: this.onFormMsg(wParam, lParam)
            return 1

    return api.DefWindowProc(hw, message, wParam, lParam)


#//////////////////////////////////////////////////////////////
#//   Create a Window class for our library.
#//////////////////////////////////////////////////////////////
def getPyformsIcon():
    file_dir = os.path.dirname(__file__)
    iconpath = f"{file_dir}\\pyforms_icon.ico"
    icofile = create_unicode_buffer(iconpath)
    return api.LoadImage(None, icofile, con.IMAGE_ICON, 0, 0, con.LR_LOADFROMFILE | con.LR_DEFAULTSIZE)

def make_window_class(proc):
    getSystemDPI()
    StaticData.pfInit()
    wc = WNDCLASSEX()
    wc.cbSize = sizeof(WNDCLASSEX)
    wc.style = con.CS_HREDRAW | con.CS_VREDRAW | con.CS_OWNDC
    wc.lpfnWndProc = proc # WNDPROC(proc)
    wc.hInstance = StaticData.hInstance
    wc.hCursor =  api.LoadCursor(0, LPCWSTR(con.IDC_ARROW))
    wc.hbrBackground = api.CreateSolidBrush(StaticData.defWinColor.ref)
    wc.hIcon = getPyformsIcon()
    wc.lpszClassName = StaticData.className
    
    # print(f"{StaticData.screenHeight = }")
    return wc

class Timer:
    def __init__(self, parentHwnd, tickInterval = 100, tickHandler = None) -> None:
        self.interval = tickInterval
        self.onTick = tickHandler
        self._isEnabled = False
        self._idNum = id(self)
        self._pHwnd = parentHwnd

    def start(self):
        if not self._isEnabled:
            self._isEnabled = True
            api.SetTimer(self._pHwnd, self._idNum, self.interval, api.TIMERPROC(0))

    def stop(self):
        if self._isEnabled:
            api.KillTimer(self._pHwnd, self._idNum)
            self._isEnabled = False

    def destroy(self):
        if self._isEnabled:
            api.KillTimer(self._pHwnd, self._idNum)
            api.SendMessage(self._pHwnd, MyMessages.MM_TIMER_DESTROY, self._idNum, 0)

    @property
    def isEnabled(self):
        return self._isEnabled


#//////////////////////////////////////////////////////////////
#//   Form class, This class represents a window
#//////////////////////////////////////////////////////////////
class Form(Control):

    """Form class represents a Window."""

    wnd_class = make_window_class(wndProcMain)
    atom = api.RegisterClassEx(byref(wnd_class))
    _count = 1
   
    __slots__ = (  "_classStr", "_formPos", "_formStyle", "_formState", 
                    "_topMost", "_maximizeBox", "_minimizeBox",
                    "_mainWinHwnd", "_isMainWindow", "_isMouseTracking", 
                    "_drawMode", "_isNormalDraw", "_updRect", "_formID", 
                    "_comboDict", "onLoad", "onMinimized", "onMaximized", 
                    "onRestored", "onClosing", "onClosed", "onActivate", 
                    "onDeActivate", "onMoving", "onMoved", "onSizing", 
                    "onSized", "onHotKeyPress", "onThreadMsg", 
                    "_menuGrayBrush", "onFormMsg", "_menuGrayCref", 
                    "_menuEventDict", "_menubar", "_menuDict",
                    "_controls", "_menuDefBgBrush", "_menuHotBgBrush", 
                    "_menuFont", "_menuFrameBrush", "_mGClr1", "_mGClr2",
                    "_mGt2b", "_timerDic", "createChilds", "_dummyEA",
                     "onCopyData", "_swFlag", "_hotkeyDict", "_childFGC" )

    def __init__(self, txt = "", width = 500, height = 400, autoCreate = False) -> None:
        # print(f"Form class inited - {Form.atom}")
        super().__init__(None, ControlType.NONE, width, height)
        self.name = f"Form_{Form._count}"
        self._text = self.name if txt == "" else txt
        self._style = con.WS_OVERLAPPEDWINDOW | con.WS_CLIPCHILDREN | con.WS_VISIBLE
        self._isTextable = True # If this is True, users can get or set text property
        # self._font = Font(StaticData.defHfont) 
        self._bgColor = Color(StaticData.defWinColor)
        self._formPos = FormPosition.CENTER # Defining where to appear on the screen
        self._formStyle = FormStyle.SIZABLE # Defining the style of this form
        self._formState = FormState.NORMAL # Other options are minimize & maximize
        self._topMost = False
        self._maximizeBox = True
        self._minimizeBox = True
        self._mainWinHwnd = None
        self._isMainWindow = False
        self._isMouseTracking = False # to control mouse tracking 
        self._drawMode = FormDrawMode.NORMAL # Other options are flat color & gradient
        self._isNormalDraw = True
        self.createChilds = False
        self._formID = Form._count + 1000 # A unique ID for all forms.
        self._comboDict = {} # Combo boxes demands to keep their listbox handle
        self._menuDict = {}
        self._updRect = None
        self._menuEventDict = {}
        self._menubar = None
        self._menuFrameBrush = None
        self._menuGrayBrush = None
        self._menuGrayCref = None
        self._mGClr1 = None
        self._mGClr2 = None
        self._mGt2b = None # Handling gradient color, deprecate it.
        self._controls = []
        self._hotkeyDict = {}
        self._timerDic = {}
        self._dummyEA = EventArgs()
        self._swFlag = con.SW_SHOW
        self._childFGC = (False, 0)
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
        self.onCopyData = None
        self.onHotKeyPress = None
        self.onFormMsg = None
        Form._count += 1
        if autoCreate: self.createHandle()
        # print(f"{con.DTN_FIRST=}")
    #-------------------------------------


    def finalize(self):
        if self._menubar:
            self._menubar.finalize()
            
        if len(self._timerDic) > 0:
            self.cleanTimers()
        
        for hkid in self._hotkeyDict:
            x = api.UnregisterHotKey(self._hwnd, hkid)
            print(f"unreg hot key res: {x}")
            
        self._hotkeyDict.clear()


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
            self._font._pHwnd = self._hwnd
            self._setFontInternal()
            StaticData.currForm = None
            print(f"Form font size {self._font._size}, handle {self._font._handle}")
        else:
            print("window creation failed")

    def close(self):
        self._sendMsg(con.WM_CLOSE, 0, 0)
        # api.DestroyWindow(self._hwnd)

    def bringToFront(self):
        api.SetForegroundWindow(self._hwnd)
        api.SetFocus(self._hwnd)
        

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
        if self._isCreated: api.InvalidateRect(self._hwnd, None, True)

    def display(self):
        """Display a window. If it's the first window, then it will start the main loop"""
    
        # self._createChildHandles() # Create child control hwnds
        if self._menubar and not self._menubar._isCreated:
            self._menubar.create()

        api.ShowWindow(self._hwnd, self._swFlag)
        if self.formState == FormState.MINIMIZED :
            api.CloseWindow(self._hwnd)
        else:
            api.UpdateWindow(self._hwnd)

        # We moved onLoad event to here. WM_SHOWWINDOW is not working.
        if self.onLoad: self._formShownHandler() 
        if self._tabOrderHwnd: api.SetFocus(self._tabOrderHwnd)
        if not StaticData.loopStarted:
            self._isMainWindow = True
            StaticData.loopStarted = True
            tMsg = api.MSG()
            while api.GetMessage(byref(tMsg), None, 0, 0) > 0:
                api.TranslateMessage(byref(tMsg))
                api.DispatchMessage(byref(tMsg))

            StaticData.finalize()

    def show(self):
        if self._swFlag != con.SW_SHOW: self._swFlag = con.SW_SHOW
        api.ShowWindow(self._hwnd, self._swFlag)

    def setHotKey(self, keyList, callback=None, noRepeat=True):
        result = -1
        if self._isCreated:
            fmod = 0
            vkey = None
            for k in keyList:
                if k == Keys.CTRL:
                    fmod |= 0x0002
                elif k == Keys.ALT:
                    fmod |= 0x0001
                elif k == Keys.SHIFT:
                    fmod |= 0x0004
                elif k == Keys.LEFT_WIN or k == Keys.RIGHT_WIN:
                    fmod |= 0x0008
                elif k.value < 256:  # assuming key codes are < 256
                    vkey = int(k)
            if noRepeat: fmod |= 0x4000
            fres = api.RegisterHotKey(self._hwnd, StaticData.gHkeyID, fmod, vkey)
            if fres:
                self._hotkeyDict[StaticData.gHkeyID] = callback 
                result = StaticData.gHkeyID
                StaticData.gHkeyID += 1
                # print(f"HotKey : {fres}")
                return result
            else:
                print(f"Reg Hot Key Error: {api.GetLastError()}")
        else:
            print("Set Hotkey Error: Hwnd is not valid.")
        return result

    
    def removeHotKey(self, hotkeyId):
        if hotkeyId in self._hotkeyDict:
            x = api.UnregisterHotKey(self._hwnd, hotkeyId)
            del self._hotkeyDict[hotkeyId]

    def removeHotKeys(self, *hkids):
        for hotkeyId in hkids:
            if hotkeyId in self._hotkeyDict:
                x = api.UnregisterHotKey(self._hwnd, hotkeyId)
                del self._hotkeyDict[hotkeyId]

    def requestCopyData(self, rcvrHwnd, request, data=None, dsize=0):
        cd = api.COPYDATASTRUCT()
        cd.dwData = request
        cd.cbData = dsize
        if data:
            cd.lpData = cast(data, api.PVOID)
        else:
            cd.lpData = None 
        return api.SendMessage(rcvrHwnd, con.WM_COPYDATA, 
                               self._hwnd, addressof(cd))

    def setPos(self, xp, yp):
        self._xpos = xp
        self._ypos = yp
        self._formPos = FormPosition.MANUAL

    def restoreForm(self):
        api.ShowWindow(self._hwnd, 9)

    def msgbox(self, msg: str, title: str = "PyForms Message",
			        btns: MessageButtons = MessageButtons.OKAY,
			        icon: MessageIcons = MessageIcons.NONE ):
        return MessageBox(0, msg, title, btns.value | icon.value)

    def addTimer(self, tickInterval = 100, tickHandler = None):
        timer = Timer(self._hwnd, tickInterval, tickHandler)
        self._timerDic[timer._idNum] = timer
        return timer
    
    def sendFormMsg(self, hwnd, data1, data2):
        return api.SendMessage(hwnd, MyMessages.MM_FORM_NOTIFY, 
                                WPARAM(data1), LPARAM(data2))
        
    
        
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
                self._exStyle = 0x00000088  
                self._style = 0x80000000
            case FormStyle.FIXED_SINGLE:
                self._exStyle = 0
                self._style = con.WS_OVERLAPPED # 0x16CB0000
                mxFlag = True
            case FormStyle.FIXED_3D:
                self._exStyle = con.WS_EX_CLIENTEDGE
                self._style = 0x16CB0000
                mxFlag = True
            case FormStyle.FIXED_DIALOG:
                self._exStyle = con.WS_EX_DLGMODALFRAME
                self._style = 0x16CB0000
                mxFlag = True
            case FormStyle.FIXED_TOOL:
                self._exStyle = 0x00050100
                self._style = 0x16CF0000
            case FormStyle.SIZABLE:
                self._exStyle = con.WS_EX_CONTROLPARENT
                self._style = con.WS_OVERLAPPEDWINDOW
            case FormStyle.SIZABLE_TOOL:
                self._exStyle = con.WS_EX_TOOLWINDOW
                self._style = con.WS_OVERLAPPEDWINDOW # con.WS_OVERLAPPEDWINDOW
                mxFlag = True
            case FormStyle.HIDDEN:
                self._exStyle = con.WS_EX_TOOLWINDOW
                self._style = con.WS_BORDER
            case FormStyle.PANEL:
                self._exStyle = con.WS_EX_TOPMOST | con.WS_EX_TOOLWINDOW  
                self._style = 0x80000000 | con.WS_VISIBLE


        if mxFlag:
            if not self._maximizeBox : self._style ^= con.WS_MAXIMIZEBOX
            if not self._minimizeBox : self._style ^= con.WS_MINIMIZEBOX
            # print(f"state of maximize box {self._maximizeBox}")

        if self._topMost: self._exStyle |= con.WS_EX_TOPMOST
        if self._formState == FormState.MAXIMIZED: self._style |= con.WS_MAXIMIZE
        # self._checkStyle(con.WS_VISIBLE)
        if not self._visible: 
            self._style &= ~con.WS_VISIBLE
            self._swFlag = con.SW_HIDE
        # self._checkStyle(con.WS_VISIBLE)


        # print(f"Ex style bits of this form - {hex(self._exStyle)}")
        # print(f"style bits of this form - {hex(self._style)}")
        # print(self._topMost)

    def _checkStyle(self, styleValue):
        if self._style & styleValue:
            print(f"Style {styleValue} is in Form")
        else:
            print(f"Style {styleValue} is not in Form")

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
        menu = self._menuDict.get(menu_id, 0)
        if menu:
            if menu.onClick: menu.onClick(menu, GEA)
        return 0

    def _getMenuFromHmenu(self, menuHandle):
        for menu in self._menuDict.values():
            if menu._handle == menuHandle: return menu
        return None

    def _createChildHandles(self):
        if len(self._controls) > 0:
            for ctl in self._controls:
                # if not self._isNormalDraw:
                    # if ctl._ctlType == ControlType.GROUP_BOX:
                    #     ctl._setBackColorFromParent(self._bgColor)
                if ctl._hwnd == None: ctl.createHandle()

    def handle_wmtimer(self, wpm):
        timer = self._timerDic.get(wpm, None)
        if not timer is None and timer.onTick:
            timer.onTick(self, self._dummyEA)

    def cleanTimers(self):        
        for timer in self._timerDic.values():
            timer.destroy()
    # -endregion private functions

    # -region Event handlers
    def _formActivateHandler(self, wp):
        if self.onActivate or self.onDeActivate:
            # ea = EventArgs()
            activate = bool(wp)
            if not activate:
                if self.onDeActivate: self.onDeActivate(self, GEA)
            else:
                if self.onActivate: self.onActivate(self, GEA)
        return 0

    def _formShownHandler(self):
        # if self.onLoad:
        # ea = EventArgs()
        self.onLoad(self, GEA)
        return 0

    def _formMouseMoveHandler(self,hw, msg, wp, lp):
        if not self._isMouseTracking:
            self._isMouseTracking = True
            self._trackMouseEvents(hw)
            if not self._isMouseEntered:
                if self._onMouseEnter:
                    self._isMouseEntered = True
                    # ea = EventArgs()
                    self._onMouseEnter(self, GEA)
        if self.onMouseMove:
            ea = MouseEventArgs(msg, wp, lp)
            self.onMouseMove(self, ea)
        return 0

    def _formMouseLeaveHandler(self):
        if self._isMouseTracking:
            self._isMouseTracking = False
            self._isMouseEntered = False

        if self._onMouseLeave:
            # ea = EventArgs()
            self._onMouseLeave(self, GEA)
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
            # ea = EventArgs()
            self.onMoving(self, GEA)
            # return 0
        return 0

    def _formMovedHandler(self, lp):
        self._xpos = getMouseXpoint(lp)
        self._ypos = getMouseYpoint(lp)
        if self.onMoved:
            # ea = EventArgs()
            self.onMoved(self, GEA)
        return 0

    def _frmSysCommandHandler(self, wp, lp):
        uMsg = int(wp & 0xFFF0)
        match uMsg:
            case con.SC_MINIMIZE:
                if self.onMinimized:
                    # ea = EventArgs()
                    self.onMinimized(self, GEA)

            case con.SC_RESTORE:
                if self.onRestored:
                    # ea = EventArgs()
                    self.onRestored(self, GEA)

            case con.SC_MAXIMIZE:
                if self.onMaximized:
                    # ea = EventArgs()
                    self.onMaximized(self, GEA)

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
        # print("_formEraseBkgHandler started")
        rct = api.get_client_rect(hwnd)
        if self._drawMode == FormDrawMode.COLORED:
            hbr = api.CreateSolidBrush(self._bgColor.ref)
            # api.FillRect(wp, byref(rct), hbr)
            # api.DeleteObject(hbr)
        elif self._drawMode == FormDrawMode.GRADIENT:
            # with Timing("create gradient speed : "):
            # print("612 worked")
            # self._formGradientNew(hwnd, wp, rct)
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
            sw_flag = 1 # SW_SHOWNORMAL
            if value == FormState.MAXIMIZED:
                sw_flag = 3 # SW_MAXIMIZE
            elif value == FormState.MINIMIZED:
                sw_flag = 6 # SW_MINIMIZE
            api.ShowWindow(self._hwnd, sw_flag)


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
        self._bgColor.updateColor(value)
        self._drawMode = FormDrawMode.COLORED
        if not self._drawFlag: self._drawFlag = 1
        self._isNormalDraw = False
        if StaticData.defBackBrush:
            api.DeleteObject(StaticData.defBackBrush)
        StaticData.defBackBrush = api.CreateSolidBrush(self._bgColor.ref)
        self._manageRedraw() # This will re draw the window if needed


    def enablePrintPoint(self):
        self.onMouseDown = printPoint2

    @property
    def topMost(self):
        return self._topMost
    
    @topMost.setter
    def topMost(self, value:bool):
        self._topMost = value

    @property   
    def childFGC(self):
        return self._childFGC

    @childFGC.setter
    def childFGC(self, value):
        self._childFGC = (True, value)
    # -endregion

#-----------------------------------------------END OF FORM CLASS-----------------------------------