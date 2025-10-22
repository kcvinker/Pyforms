
# Created on 03-Jun-2025 19:21

from pyforms.enums import TrayMenuTrigger, BalloonIcon
from pyforms.apis import (
    NOTIFYICONDATA, WNDCLASSEX, LRESULT, WNDPROC, DestroyIcon,
    DefWindowProc, RegisterClassEx, CreateWindowEx, Shell_NotifyIcon,
    LoadIcon, LoadImage, LPCWSTR, DestroyWindow)
from pyforms.commons import MyMessages, StaticData
from pyforms.menubar import ContextMenu
from pyforms.events import GEA
import pyforms.constants as con
from ctypes import sizeof, addressof, byref
from ctypes.wintypes import HWND

TIMW_CLS = "PyFormsTrayMsgWin" # Tray Icon Message Window Class
LIMG_FLAG = con.LR_DEFAULTCOLOR | con.LR_LOADFROMFILE
trayDict = {}

@WNDPROC
def trayIconWndProc(hw, message, wParam, lParam) -> LRESULT:
    # print("tray")
    match message:
        case con.WM_NCDESTROY:
            this = trayDict[hw]
            this.finalize()
            del trayDict[hw]
            print("PyForms TrayIcon is closing...")

        case MyMessages.MM_TRAY_MSG:
            match lParam:
                case con.NIN_BALLOONSHOW:
                    this = trayDict[hw]
                    if this.onBalloonShow: this.onBalloonShow(this, GEA)

                case con.NIN_BALLOONTIMEOUT:
                    # print("Balloon closing")
                    this = trayDict[hw]
                    if this.onBalloonClose: this.onBalloonClose(this, GEA)
                    if this._resetIcon: this._resetIconInternal()

                case con.NIN_BALLOONUSERCLICK:
                    this = trayDict[hw]
                    if this.onBalloonClick: this.onBalloonClick(this, GEA)
                    if this._resetIcon: this._resetIconInternal()

                case con.WM_LBUTTONDOWN:
                    this = trayDict[hw]
                    if this.onLeftMouseDown: this.onLeftMouseDown(this, GEA)

                case con.WM_LBUTTONUP:
                    this = trayDict[hw]
                    if this.onLeftMouseUp: this.onLeftMouseUp(this, GEA)
                    if this.onLeftClick: this.onLeftClick(this, GEA)
                    if this._cmenu and (this._menuTrigger.value & TrayMenuTrigger.LEFT_CLICK.value): 
                        # print("56")
                        this._cmenu.showMenu(0)
                    
                case con.WM_LBUTTONDBLCLK:
                    this = trayDict[hw]
                    if this.onLeftDoubleClick: this.onLeftDoubleClick(this, GEA)
                    if this._cmenu and (this._menuTrigger & TrayMenuTrigger.LEFT_DBLCLICK):
                        this._cmenu.showMenu(0)

                case con.WM_RBUTTONDOWN:
                    this = trayDict[hw]
                    if this.onRightMouseDown: this.onRightMouseDown(this, GEA)

                case con.WM_RBUTTONUP:
                    this = trayDict[hw]
                    if this.onRightMouseUp: this.onRightMouseUp(this, GEA)
                    if this.onRightClick: this.onRightClick(this, GEA)
                    if this._cmenu and (this._menuTrigger & TrayMenuTrigger.RIGHT_CLICK):
                        this._cmenu.showMenu(0)

                case con.WM_MOUSEMOVE:
                    this = trayDict[hw]
                    if this.onMouseMove: this.onMouseMove(this, GEA)

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
        """
        Creates TrayIcon class.
        Parameters
            tooltip(str) : Text to be displayed as a tool tip when mouse 
                            hover over the tray icon.
            iconpath(str): A file path to an icon.
        """
        self._resetIcon = False
        self._cmenuUsed = False
        self._retainIcon = False
        self._trig = 0
        self._menuTrigger = TrayMenuTrigger.NONE
        self._msgHwnd = None
        self._cmenu = None
        self.userData = None

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
            self._hTrayIcon = LoadIcon(None, LPCWSTR(con.IDI_INFO))
        else:
            self._hTrayIcon = (LoadImage(None, iconpath, con.IMAGE_ICON, 0, 0, LIMG_FLAG)  
                                or LoadIcon(None, LPCWSTR(con.IDI_INFO)))
        #------------------------------------------
        self._nid = NOTIFYICONDATA()
        self._nid.cbSize = sizeof(NOTIFYICONDATA)
        self._nid.hWnd = self._msgHwnd
        self._nid.uID = TrayIcon._trayID            
        self._nid.uFlags = con.NIF_ICON | con.NIF_MESSAGE | con.NIF_TIP
        self._nid.uCallbackMessage = MyMessages.MM_TRAY_MSG
        self._nid.hIcon = self._hTrayIcon  
        self._nid.szTip = self._tooltip
        self._nid.uVerOrTime.uVersion = 4         
        Shell_NotifyIcon(con.NIM_ADD, byref(self._nid))
        TrayIcon._trayID += 1
        


    def showBalloon(self, title, message, timeout, noSound=False, 
                    icon = BalloonIcon.INFO, iconpath=""):
        """
        Shows a balloon notification on system tray.
        Parameters:
            title(str)   : Title of the balloon.
            message(str) : Message to be shown in balloon.
            timeout(int) : The time in milliseconds to display the balloon notification.
            noSound(bool): If True, the system default notification sound will be **suppressed**.
                            If False, the system will play its default sound when the balloon appears.
            icon(BalloonIcon enum): The icon to be shown in balloon. Possible
                                    values are, NONE, INFO, WARNING, ERROR, CUSTOM.
                                    Default is **INFO**. If you choose **CUSTOM**, 
                                    you must provide a valid icon file path in 'iconpath'.
            iconpath(str): File path to an icon, this works only if user choose
                            BalloonIcon.CUSTOM for parameter 'icon'. 
        """
        
        self._nid.uFlags = con.NIF_ICON|con.NIF_MESSAGE|con.NIF_TIP|con.NIF_INFO
        self._nid.szInfoTitle = title
        self._nid.szInfo = message
        if icon == BalloonIcon.CUSTOM and iconpath != "":
            self._nid.hIcon =  LoadImage(None, iconpath, con.IMAGE_ICON, 0, 0, LIMG_FLAG)
            if self._nid.hIcon == None : 
                self._nid.hIcon = self.mhTrayIcon
            else:
                # We successfully created an icon handle from 'iconpath' parameter.
                # So, for this balloon, we will show this icon. But We need to... 
                # ...reset the old icon after this balloon vanished. 
                # Otherwise, from now on we need to use this icon in Balloons and tray.
                self._resetIcon = True
            #------------------------
        #----------------------------
        self._nid.dwInfoFlags = icon
        self._nid.uVerOrTime.uTimeout = timeout
        if noSound: self._nid.dwInfoFlags = self._nid.dwInfoFlags|con.NIIF_NOSOUND
        Shell_NotifyIcon(con.NIM_MODIFY, byref(self._nid))
        self._nid.dwInfoFlags = 0
        self._nid.uFlags = 0

    def addContextMenu(self, menuItemsList, trigger = TrayMenuTrigger.RIGHT_CLICK):
        self._cmenu = ContextMenu(*menuItemsList)
        self._menuTrigger = trigger
        # print(f"self trigger {self._menuTrigger:b}, {trigger:b}")

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
        # print(f"{self._msgHwnd = }")


    def _destroyMsgWindow(self):
        x = DestroyWindow(self._msgHwnd)
        if x:
            StaticData.trayHandles.remove(self._msgHwnd)
            print("TrayIcon._destroyMsgWindow worked")

       
    def _resetIconInternal(self):
        self._nid.uFlags = con.NIF_ICON|con.NIF_MESSAGE|con.NIF_TIP
        self._nid.hIcon = self._hTrayIcon
        Shell_NotifyIcon(con.NIM_MODIFY, byref(self._nid))
        self._resetIcon = False # Revert to the default state
        # print("reset work")

    @property
    def menuTrigger(self): return self._menuTrigger

    @menuTrigger.setter
    def menuTrigger(self, value):
        self._menuTrigger = value

    @property
    def tooltip(self): return self._tooltip

    @tooltip.setter
    def tooltip(self, value):
        self._tooltip = value
        self._nid.uFlags = con.NIF_ICON|con.NIF_MESSAGE|con.NIF_TIP
        self._nid.szTip = value
        Shell_NotifyIcon(con.NIM_MODIFY, byref(self._nid))

    @property
    def icon(self): return self._iconpath

    @icon.setter
    def icon(self, value):
        self._iconpath = value
        self._hTrayIcon =  (LoadImage(None, value, con.IMAGE_ICON, 
                                      0, 0, LIMG_FLAG) or         
                            LoadIcon(None, LPCWSTR(con.IDI_INFO)))        
        self._nid.uFlags = con.NIF_ICON|con.NIF_MESSAGE|con.NIF_TIP
        self._nid.hIcon = self._hTrayIcon
        Shell_NotifyIcon(con.NIM_MODIFY, byref(self._nid))

    @property
    def contextMenu(self): return self._cmenu

    @contextMenu.setter
    def contextMenu(self, value):
        self._cmenu = value
        self._cmenu._formHwnd = self._msgHwnd
        self._menuTrigger = TrayMenuTrigger.RIGHT_CLICK


    def finalize(self):
        Shell_NotifyIcon(con.NIM_DELETE, byref(self._nid))
        if self._hTrayIcon: DestroyIcon(self._hTrayIcon)


def trayBalloon(title, message, timeout, noSound=False, 
                    icon = BalloonIcon.INFO, iconpath=""):
    """
    Shows a balloon notification on system tray. The tray icon will be...
        created aytomatically.
    Parameters:
        title(str)   : Title of the balloon.
        message(str) : Message to be shown in balloon.
        timeout(int) : The time in milliseconds to display the balloon notification.
        noSound(bool): If True, the system default notification sound will be **suppressed**.
                        If False, the system will play its default sound when the balloon appears.
        icon(BalloonIcon enum): The icon to be shown in balloon. Possible
                                values are, NONE, INFO, WARNING, ERROR, CUSTOM.
                                Default is **INFO**. If you choose **CUSTOM**, 
                                you must provide a valid icon file path in 'iconpath'.
        iconpath(str): File path to an icon, this works only if user choose
                        BalloonIcon.CUSTOM for parameter 'icon'. 
    """
    ti = TrayIcon("PyForms Tray Balloon", iconpath)
    ti.onBalloonClose = lambda x, y: x._destroyMsgWindow()
    ti.showBalloon(title, message, timeout, noSound, icon, iconpath)
    