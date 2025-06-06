
# Created on 03-Jun-2025 19:21

from pyforms.src.enums import TrayMenuTrigger, BalloonIcon
from pyforms.src.apis import NOTIFYICONDATA, WNDCLASSEX, LRESULT, WNDPROC, DestroyIcon
from pyforms.src.apis import DefWindowProc, RegisterClassEx, CreateWindowEx, Shell_NotifyIcon
from pyforms.src.apis import LoadIcon, LoadImage, Shell_NotifyIcon, LPCWSTR
from pyforms.src.commons import MyMessages, StaticData
from pyforms.src.events import EventArgs

import pyforms.src.constants as con

from ctypes import sizeof, addressof, byref
from ctypes.wintypes import HWND

TIMW_CLS = "PyFormsTrayMsgWin" # Tray Icon Message Window Class

trayDict = {}

@WNDPROC
def trayIconWndProc(hw, message, wParam, lParam) -> LRESULT:
    # print("tray")
    match message:
        case con.WM_NCDESTROY:
            this = trayDict[hw]
            this.finalize()
            del trayDict[hw]
            print("PyForms Tray is closing...")

        case MyMessages.MM_TRAY_MSG:
            match lParam:
                case con.NIN_BALLOONSHOW:
                    this = trayDict[hw]
                    if this.onBalloonShow: this.onBalloonShow(this, EventArgs())

                case con.NIN_BALLOONTIMEOUT:
                    this = trayDict[hw]
                    if this.onBalloonClose: this.onBalloonClose(this, EventArgs())
                    if this.mResetIcon: this._resetIconInternal()

                case con.NIN_BALLOONUSERCLICK:
                    this = trayDict[hw]
                    if this.onBalloonClick: this.onBalloonClick(this, EventArgs())
                    if this.mResetIcon: this._resetIconInternal()

                case con.WM_LBUTTONDOWN:
                    this = trayDict[hw]
                    if this.onLeftMouseDown: this.onLeftMouseDown(this, EventArgs())

                case con.WM_LBUTTONUP:
                    this = trayDict[hw]
                    if this.onLeftMouseUp: this.onLeftMouseUp(this, EventArgs())
                    if this.onLeftClick: this.onLeftClick(this, EventArgs())
                    if this._cmenuUsed and (this._trig and 1) == 1: 
                        this._cmenu.showMenu(0)

                case con.WM_LBUTTONDBLCLK:
                    this = trayDict[hw]
                    if this.onLeftDoubleClick: this.onLeftDoubleClick(this, EventArgs())
                    if this._cmenuUsed and (this._trig and 2) == 2:
                        this._cmenu.showMenu(0)

                case con.WM_RBUTTONDOWN:
                    this = trayDict[hw]
                    if this.onRightMouseDown: this.onRightMouseDown(this, EventArgs())

                case con.WM_RBUTTONUP:
                    this = trayDict[hw]
                    if this.onRightMouseUp: this.onRightMouseUp(this, EventArgs())
                    if this.onRightClick: this.onRightClick(this, EventArgs())
                    if this._cmenuUsed and (this._trig and 4) == 4:
                        this._cmenu.showMenu(0)

                case con.WM_MOUSEMOVE:
                    this = trayDict[hw]
                    if this.onMouseMove: this.onMouseMove(this, EventArgs())

    return DefWindowProc(hw, message, wParam, lParam)


class TrayIcon:
    _isWinClassReg = False
    _trayID = 1001
    __slots__ = ("_resetIcon", "_cmenuUsed", "_retainIcon", "_trig",
                 "_menuTrigger", "_hTrayIcon", "_msgHwnd", "_cmenu", 
                 "_tooltip", "_iconpath", "userData", "_nid", 
                 "onBalloonShow", "onBalloonClose", "onBalloonClick", 
                 "onMouseMove", "onLeftMouseDown", "onLeftMouseUp", 
                 "onRightMouseDown", "onRightMouseUp", "onLeftClick", 
                 "onRightClick", "onLeftDoubleClick")
    
    def __init__(self, tooltip, iconpath = ""):
        self._resetIcon = False
        self._cmenuUsed = False
        self._retainIcon = False
        self._trig = 0
        self._menuTrigger = TrayMenuTrigger.NONE
        self._msgHwnd = None
        self._cmenu = None
        self.userData = None
        self._nid = NOTIFYICONDATA()

        self.onBalloonShow = None
        self.onBalloonClose = None
        self.onBalloonClick = None
        self.onMouseMove = None
        self.onLeftMouseDown = None
        self.onLeftMouseUp = None
        self.onRightMouseDown = None
        self.onRightMouseUp = None
        self.onLeftClick = None
        self.onRightClick = None
        self.onLeftDoubleClick = None
        self._tooltip = tooltip
        self._iconpath = iconpath
        self._createMsgWindow()
        if iconpath == "":
            self._hTrayIcon = LoadIcon(None, LPCWSTR(con.IDI_SHIELD))
        else:
            self._hTrayIcon = LoadImage(None, iconpath, con.IMAGE_ICON, 0, 0, con.LIMG_FLAG)
            if not self._hTrayIcon:
                self._hTrayIcon = LoadIcon(None, LPCWSTR(con.IDI_SHIELD))
                print("Can't create the icon")
        #------------------------------------------
        self._nid.cbSize = sizeof(NOTIFYICONDATA)
        self._nid.hWnd = self._msgHwnd
        self._nid.uID = TrayIcon._trayID
        self._nid.uVersionOrTimeout = 4
        self._nid.uFlags = con.NIF_ICON | con.NIF_MESSAGE | con.NIF_TIP
        self._nid.uCallbackMessage = MyMessages.MM_TRAY_MSG
        self._nid.hIcon = self._hTrayIcon  
        self._nid.toolTipText = self._tooltip
        Shell_NotifyIcon(con.NIM_ADD, byref(self._nid))
        TrayIcon._trayID += 1


    def _createMsgWindow(self):
        if not TrayIcon._isWinClassReg:
            StaticData.registerMsgWinClass(TIMW_CLS, trayIconWndProc)
            TrayIcon._isWinClassReg = True

        self._msgHwnd = CreateWindowEx(0, TIMW_CLS, None, 0, 0, 0, 0, 0, con.HWND_MESSAGE, 
                                          None, StaticData.hInstance, None)
        if self._msgHwnd:
            # Storing the handle in global list so that we can destroy the window later.
            trayDict[self._msgHwnd] = self
            StaticData.trayHandles.append(self._msgHwnd)
        print(f"{self._msgHwnd = }")

    

    

    def _resetIconInternal(self):
        self._nid.uFlags = con.NIF_ICON | con.NIF_MESSAGE | con.NIF_TIP
        self._nid.hIcon = self._hTrayIcon
        Shell_NotifyIcon(con.NIM_MODIFY, byref(self._nid))
        self._resetIcon = False # Revert to the default state


    def finalize(self):
        Shell_NotifyIcon(con.NIM_DELETE, byref(self._nid))
        if self._hTrayIcon: DestroyIcon(self._hTrayIcon)

