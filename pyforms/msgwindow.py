
# Created on 14-Jun-2025 12:28
# This script provide a class for msg-only window.

from pyforms.commons import StaticData, MyMessages
from pyforms.trayicon import TrayIcon
from pyforms.forms import Timer
from pyforms.events import GEA
import pyforms.constants as con
from pyforms.enums import Keys
from pyforms.apis import (
    GetModuleHandle, LPCWSTR, WNDPROC, WPARAM, LPARAM, CreateWindowEx,
    LPCWSTR, WNDCLASSEX, RegisterClassEx, GetWindowLongPtr,
    DefWindowProc, DestroyWindow, SetWindowLongPtr, MSG,
    GetMessage, TranslateMessage, DispatchMessage, PostQuitMessage,
    RegisterHotKey, UnregisterHotKey, GetLastError, SendMessage
    )
from ctypes import py_object, cast, byref, sizeof
import threading

hfClassName = "PyForms_MsgOnly_Window"

def regHiddenFormClass(proc):    
    wc = WNDCLASSEX()
    wc.cbSize = sizeof(WNDCLASSEX)
    wc.lpfnWndProc = proc 
    wc.hInstance = StaticData.hInstance
    wc.lpszClassName = hfClassName
    RegisterClassEx(byref(wc))

globalMsgList = []


@WNDPROC
def hfWndProc(hwnd, umsg, wpm, lpm):
    # print(f"msg-only window: {umsg}")
    if umsg in globalMsgList:
        this = cast(GetWindowLongPtr(hwnd, con.GWLP_USERDATA), py_object).value
        return this.msgHandler(this, umsg, wpm, lpm)
    
    elif umsg == con.WM_DESTROY:
        # print("Hidden Form msg-only window destroying")
        PostQuitMessage(0)
        return 0
    
    elif umsg == con.WM_HOTKEY:   
        # print("wm hotkey handler")     
        this = cast(GetWindowLongPtr(hwnd, con.GWLP_USERDATA), py_object).value
        func = this._hotkeyDict.get(wpm)
        if func: 
            # print("func is ready")
            func(this, GEA)
        return 0
        
    elif umsg == con.WM_TIMER:
        this = cast(GetWindowLongPtr(hwnd, con.GWLP_USERDATA), py_object).value
        timer = this._timerDict.get(wpm, None)
        if not timer is None and timer.onTick:
            timer.onTick(this, GEA)

    elif umsg == MyMessages.MM_TIMER_DESTROY:
        # print("Timer destroy message")
        this = cast(GetWindowLongPtr(hwnd, con.GWLP_USERDATA), py_object).value
        if wpm in this._timerDict:
            del this._timerDict[wpm]

        return 0

    else:
        # If the message is not handled by the user, we pass it to the default window procedure.
        return DefWindowProc(hwnd, umsg, wpm, lpm)

    return DefWindowProc(hwnd, umsg, wpm, lpm)
       

class HiddenForm:
    _isClassReg = False

    __slots__ = ("_tray", "_isActive", "msgHandler", "_hwnd",
                 "_noTray", "_hotkeyDict", "_timerDict" )
    def __init__(self, func, autoc=True, noIcon=False, 
                    trayTip="Pyforms MsgWindow", iconpath=None,
                    noCmenu=False):

        self.msgHandler = func
        self._hwnd = None
        self._noTray = noIcon
        self._hotkeyDict = {}
        self._timerDict = {}

        if StaticData.hInstance is None:
            StaticData.hInstance = GetModuleHandle(LPCWSTR(0))

        self._isActive = True

        if not self._noTray:
            self._tray = TrayIcon(trayTip, iconpath)
            if not noCmenu:
                self._tray.addContextMenu(["Quit"])
                self._tray.contextMenu.addHandler("Quit", self.onTrayQuit)

        if not HiddenForm._isClassReg:
            regHiddenFormClass(hfWndProc)
            HiddenForm._isClassReg = True

        if autoc: self.createHandle()


    def createHandle(self):
        self._hwnd = CreateWindowEx(0, hfClassName, None, 0, 0, 0, 0, 0, 
                                    con.HWND_MESSAGE, None, 
                                    StaticData.hInstance, None)
        if self._hwnd:
            SetWindowLongPtr(self._hwnd, con.GWLP_USERDATA, id(self))


    def startListening(self, *messages):
        """Start the message loop for the hidden form."""
        for msg in messages:
            if msg not in globalMsgList:
                globalMsgList.append(msg)
                
        pMsg = MSG()
        while GetMessage(byref(pMsg), None, 0, 0) > 0:
            TranslateMessage(byref(pMsg))
            DispatchMessage(byref(pMsg))

        # Right after we exit from the loop, starting housekeeping.
        self.finalize() 
                
    def close(self):
        if self._hwnd:
            DestroyWindow(self._hwnd)


    def sendMsg(self, hwnd, msg, wpm, lpm):
        return SendMessage(hwnd, msg, WPARAM(wpm), LPARAM(lpm))
    

    def startFormThread(self, func, *args, **kwargs):
        """Start a Form in a separate thread."""
        t = threading.Thread(target=lambda: func(*args, **kwargs), name="HiddenFormThread")
        t.daemon = True
        t.start()
        return t
    
    
    def addTimer(self, tickInterval = 100, tickHandler = None):
        timer = Timer(self._hwnd, tickInterval, tickHandler)
        self._timerDict[timer._idNum] = timer
        return timer
    
    # def removeTimer(self, timer):
    #     if timer._idNum in self._timerDict:
    #         timer._destructor()
    #         del self._timerDict[timer._idNum]
    #         HiddenForm._timerCount -= 1


    def setHotKey(self, keyList, callback=None, noRepeat=True):
        # print(keyList)
        result = -1
        if self._hwnd:
            fmod = 0
            vkey = None
            for k in keyList:
                if k == Keys.CTRL:
                    fmod |= 0x0002
                elif k == Keys.ALT or k == Keys.LEFT_MENU or k == Keys.RIGHT_MENU:
                    fmod |= 0x0001
                elif k == Keys.SHIFT:
                    fmod |= 0x0004
                elif k == Keys.LEFT_WIN or k == Keys.RIGHT_WIN:
                    fmod |= 0x0008
                elif k.value < 256:  # assuming key codes are < 256
                    vkey = int(k)
            if noRepeat: fmod |= 0x4000
            StaticData.gHkeyID += 1
            fres = RegisterHotKey(self._hwnd, StaticData.gHkeyID, fmod, vkey)
            if fres:
                self._hotkeyDict[StaticData.gHkeyID] = callback 
                result = StaticData.gHkeyID                
                # print(f"Hotkey : {fres}")
                return result
            else:
                print(f"Reg Hot Key [{keyList}] Error: {GetLastError()}")
            
        else:
            print("Set Hotkey Error: Hwnd is not valid.")
        return result


    def removeHotKey(self, hotkeyId):
        if hotkeyId in self._hotkeyDict:
            x = UnregisterHotKey(self._hwnd, hotkeyId)
            # if x:
            #     HiddenForm._hkeyNum -= 1

            del self._hotkeyDict[hotkeyId]

        
    def removeHotKeys(self, *keyids):
        for kid in keyids:
            if kid in self._hotkeyDict:
                x = UnregisterHotKey(self._hwnd, kid)
                del self._hotkeyDict[kid]


    def addContextMenuItem(self, menuText, callback):
        self._tray.contextMenu.addMenuItem(menuText, callback)

    def finalize(self):
        if self._isActive:
            if not self._noTray:
                self._tray.finalize()
                if not self._tray._hTrayIcon:
                    self._isActive = False

            if self._hotkeyDict:
                for hkid in self._hotkeyDict:
                    x = UnregisterHotKey(self._hwnd, hkid)
                    # if x: HiddenForm._hkeyNum -= 1
                    print(f"unreg hot key res: {x}")

            if self._timerDict:
                for timer in self._timerDict.values():
                    timer.destroy()

            self._hotkeyDict.clear()            
            StaticData.finalize()


    # def __del__(self):
    #     if self._isActive:
    #         self.finalize()    


    def onTrayQuit(self, c, e):
        """This function get called when user selects the 'Quit' menu on tray."""
        DestroyWindow(self._hwnd)


    @property
    def trayicon(self): return self._tray
    
    @property
    def handle(self): return self._hwnd

    @property
    def quitMenuHandler(self):
        raise AttributeError("This property is write-only")

    @quitMenuHandler.setter
    def quitMenuHandler(self, func):
        """Overriding Quit menu onClick event handler."""
        self._tray.contextMenu.addHandler("Quit", func)