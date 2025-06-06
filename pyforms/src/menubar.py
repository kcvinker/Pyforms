# menubar module - Created on 21-02-2023 12:48 AM

from enum import IntEnum
import pyforms.src.apis as api

from ctypes import (
    create_unicode_buffer, 
    byref, cast, sizeof, c_wchar_p, 
    py_object, addressof )

from pyforms.src.apis import (
    CreateMenu, AppendMenu, SetMenu, SendMessage, POINT, CreatePopupMenu,
    SIZE, ClientToScreen, TrackPopupMenu, DestroyMenu, 
    LRESULT, CreateWindowEx,  
    DestroyWindow, LOWORD, HIWORD, DrawMenuBar, 
    InsertMenuW, LPMEASUREITEMSTRUCT, LPDRAWITEMSTRUCT, MENUITEMINFO, 
    DrawText, InsertMenuItemW, SetBkMode, FillRect, CreateSolidBrush, 
    ULONG_PTR, GetDC, ReleaseDC, WNDPROC, DefWindowProc )

from pyforms.src.commons import (
    MyMessages, getMousePoints, getMouseXpoint, 
    getMouseYpoint, getMousePosOnMsg, menuTxtFlag,
     StaticData, Font )

from pyforms.src.control import Control
from pyforms.src.colors import Color
from pyforms.src.events import GEA
from pyforms.src.enums import ControlType, MenuStyle

import pyforms.src.constants as con
from pyforms.src.winmsgs import log_msg

# region Constants
MFT_BITMAP = 0x00000004
MF_POPUP = 0x00000010
MFT_STRING = 0x00000000
MFT_SEPARATOR = 0x00000800
MF_CHECKED = 0x00000008
MNS_NOTIFYBYPOS = 0x08000000
MIM_STYLE = 0x00000010
TPM_RIGHTBUTTON = 0x0002
MF_BYPOSITION = 0x400
MFT_OWNERDRAW = 0x00000100
MFT_RADIOCHECK = 0x00000200

MIIM_STATE = 0x00000001
MIIM_ID = 0x00000002
MIIM_SUBMENU = 0x00000004
MIIM_CHECKMARKS = 0x00000008
MIIM_DATA = 0x00000020
MIIM_STRING = 0x00000040
MIIM_BITMAP = 0x00000080
MIIM_FTYPE = 0x00000100
MIM_MENUDATA = 0x00000008

MF_INSERT = 0x00000000
MF_CHANGE = 0x00000080
MF_APPEND = 0x00000100
MF_DELETE = 0x00000200
MF_REMOVE = 0x00001000
MF_BYCOMMAND = 0x00000000
MF_BYPOSITION = 0x00000400
MF_ENABLED = 0x00000000
MF_GRAYED = 0x00000001
MF_DISABLED = 0x00000002
MF_UNCHECKED = 0x00000000

MF_USECHECKBITMAPS = 0x00000200



MF_MENUBARBREAK = 0x00000020
MF_MENUBREAK = 0x00000040
MF_UNHILITE = 0x00000000
MF_HILITE = 0x00000080
MF_DEFAULT = 0x00001000
MF_SYSMENU = 0x00002000
MF_HELP = 0x00004000
MF_RIGHTJUSTIFY = 0x00004000
MF_MOUSESELECT = 0x00008000
MF_END = 0x00000080

MFS_GRAYED = 0x00000003
MFS_DISABLED = MFS_GRAYED
MFS_CHECKED = MF_CHECKED
MFS_HILITE = MF_HILITE
MFS_ENABLED = MF_ENABLED
MFS_UNCHECKED = MF_UNCHECKED
MFS_UNHILITE = MF_UNHILITE
MFS_DEFAULT = MF_DEFAULT
TPM_RETURNCMD = 256
# endregion

calcRectFlag = con.DT_SINGLELINE | con.DT_LEFT | con.DT_VCENTER | con.DT_CALCRECT
# CM_DICT = {} # This will hold the context menu instances

# To hold static data for menu item and menu bar
class MenuData:
    staticMenuID = 100
    staticMenuIndex = 0


# Differentiate various menu types
class MenuType(IntEnum):
    BASE_MENU = 0
    MENU_ITEM = 1
    POP_UP = 2
    SEPARATOR = 3

class MenuEvents(IntEnum):
    MENU_CLICK = 0

class MenuState(IntEnum):
    ENABLED = 0
    DISABLED = 3
    CHECKED = 8
    HILITE = 128
    BOLD = 256

class MenuBase:
    __slots__ = ("_menus",  "_menuCount", "_handle", "_formHwnd", "_style"  )
    def __init__(self):
        self._menus = {}
        self._menuCount = 0
        self._handle = None
        self._formHwnd = None
        self._style = MenuStyle.SYSTEM

class MenuBar(MenuBase):
    """MenuBar class is the container of all menus"""

    __slots__ = ("_grayBrush", "_grayCref", "_defBgBrush", "_font", 
                  "_hotBgBrush", "_font", "_frameBrush", "_style",
                   "_isCreated" )

    def __init__(self, parent, style = MenuStyle.SYSTEM) -> None:
        super().__init__()
        self._handle = CreateMenu()
        self._formHwnd = parent._hwnd
        self._font = Font()
        self._font.colneFrom(parent._font)
        self._style = style
        self._isCreated = False
        parent._menubar = self

        # We need this brush & colorref for drawing a disabled menu.
        self._grayBrush = Color(0xced4da).createHBrush()
        self._grayCref = Color(0x979dac).ref
        self._defBgBrush = None
        self._hotBgBrush = None
        self._frameBrush = None
        

    def addMenu(self, txt: str):
        mi = MenuItem(txt, MenuType.BASE_MENU, self._handle, self._menuCount)
        mi._formHwnd = self._formHwnd
        mi._style = self._style
        mi._formMenu = True
        self._menuCount += 1
        self._menus[txt] = mi
        # self._parent._menuItemDict[mi._id] = mi
        return mi


    def create(self):
        self._defBgBrush = Color(0xe9ecef).createHBrush()
        self._hotBgBrush = Color(0x90e0ef).createHBrush()
        self._frameBrush = Color(0x0077b6).createHBrush()        
        if len(self.menus):
            hdc = None
            owner_draw = False
            if self._style == MenuStyle.CUSTOM:
                owner_draw = True
                hdc = GetDC(self._formHwnd)
                api.SelectObject(hdc, self._font._handle)
            for menu in self.menus.values(): 
                menu.insertInAPI(hdc, owner_draw)

            if hdc: api.ReleaseDC(self._formHwnd, hdc)
        SetMenu(self._formHwnd, self._handle)
        self._isCreated = True


    def finalize(self):
        if len(self._menus):
            for menu in self._menus.values(): menu.finalize()

        if self._handle: 
            api.DestroyMenu(self._handle)
            # print("Bar: destroyed for MenuBar")


    @property
    def handle(self): return self._handle

    @property
    def style(self):
        return self._style
    
    @style.setter
    def style(self, value):
        self._style = value

    @property
    def menus(self):
        return self._menus


# Removable candidates - _formHwnd


class MenuItem(MenuBase):
    """MenuItem represents a simple menu or dropdown menu or a separator"""

    __slots__ = ("_index","_bgColor", "_fgColor", "_isCmenu", 
                 "_state", "_parentHmenu", "_id", 
                 "_level", "_text", "_type", "_typeFlag",  
                "_isCreated", "_isEnabled", "onClick", 
                "onPopup", "onCloseup", "onFocus", "_childCount", 
                "_popup", "_formMenu", "_getTxtSize", "_txtSize")

    def __init__(self, txt: str, typ: MenuType, parentHmenu, indexNum) -> None:
        super().__init__()
        self._popup = True if typ == MenuType.BASE_MENU or typ == MenuType.POP_UP else False
        self._handle = CreatePopupMenu() if self._popup else CreateMenu()
        self._index = indexNum
        self._id = MenuData.staticMenuID
        self._text = f"{self._id}" if txt == "" else txt
        self._type = typ
        self._typeFlag = MFT_STRING
        self._parentHmenu = parentHmenu
        self._bgColor = Color(0xe9ecef)
        self._fgColor = Color(0x000000)
        self.onClick = None
        self.onPopup = None
        self.onCloseup = None
        self.onFocus = None
        self._childCount = 0
        self._formMenu = False
        self._isCreated = False
        self._getTxtSize = False
        self._isCmenu = False
        self._isEnabled = True
        self._txtSize = SIZE()
        self._state = MenuState.ENABLED
        
        MenuData.staticMenuID += 1

    
    def addMenu(self, txt: str):
        if self._type == MenuType.MENU_ITEM:
            self._handle = CreatePopupMenu()
            self._popup = True

        mi = MenuItem(txt, MenuType.MENU_ITEM, self._handle, self._childCount)
        mi._formHwnd = self._formHwnd
        mi._formMenu = self._formMenu
        mi._style = self._style
        if self._type != MenuType.BASE_MENU: self._type = MenuType.POP_UP
        self._childCount += 1
        self._menus[txt] = mi
        if mi._formMenu: api.SendMessage(mi._formHwnd, 
                                         MyMessages.MENU_ADDED, mi._id, id(mi))
        return mi

    
    def addSeperator(self):
        mi = MenuItem("", MenuType.SEPARATOR, self._handle, self._childCount)
        self._childCount += 1
        self._menus[mi._text] = mi
        # return mi

    
    def _insertMenuInternal(self, parentHmenu, owndraw = False):
        mii = MENUITEMINFO()
        mii.cbSize = sizeof(MENUITEMINFO)
        mii.fMask = MIIM_ID|MIIM_FTYPE|MIIM_DATA|MIIM_SUBMENU|MIIM_STATE|MIIM_STRING
        if owndraw: self._typeFlag = MFT_OWNERDRAW
        mii.fType = self._typeFlag
        mii.dwTypeData = self._text
        mii.cch = len(self._text)
        mii.dwItemData = id(self)
        mii.wID = self._id
        mii.fState = self._state
        mii.hSubMenu = self._handle if self._popup else None
        x = InsertMenuItemW(parentHmenu, self._id, False, byref(mii))
        self._isCreated = True


    def insertInAPI(self, hdc, owner_draw):
        if owner_draw:
            api.GetTextExtentPoint32(hdc, self._text, len(self._text), 
                                            byref(self._txtSize))
            if self._type != MenuType.BASE_MENU:
                if self._txtSize.cx < 100:
                    self._txtSize.cx = 100
                else:
                    self._txtSize.cx += 20
                # self._txtSize.cy += 5

        match self._type:
            case MenuType.BASE_MENU | MenuType.POP_UP:
                if len(self._menus):
                    for menu in self._menus.values(): 
                        menu.insertInAPI(hdc, owner_draw)

                self._insertMenuInternal(self._parentHmenu, owner_draw)
            case MenuType.MENU_ITEM:
                self._insertMenuInternal(self._parentHmenu, owner_draw)
            case MenuType.SEPARATOR:
                AppendMenu(self._parentHmenu, MFT_SEPARATOR, 0, None)

        
    def menuItem(self, txt):
        if len(self._menus):
            for menu in self._menus.values():
                if menu._text == txt: return menu
        return None

    
    def finalize(self):
        if len(self._menus):
            for menu in self._menus.values():
                menu.finalize()

        if self._handle: 
            api.DestroyMenu(self._handle)
            # print(f"Item: HMENU destroyed for {self._text}")

    
    def getChildFromIndex(self, index):
        for menu in self._menus.values():
            # print("indexes ", menu._index)
            if menu._index == index:

                return menu
        return None

    
    def _handleWMMeasureItem(self, pmi):
        # if not self._txtSizeReady: self._getTextSize(hw)
        if self._type == MenuType.BASE_MENU:        
            pmi.itemWidth = self._txtSize.cx #+ 10
            pmi.itemHeight = self._txtSize.cy
        else:
            pmi.itemWidth = 140 #size.cx #+ 10
            pmi.itemHeight = 25
        return 1

    def _changeMenuState(self):
        api.ModifyMenu(self._handle, self._id, 0x0, self._state, self._id, None)
        if self._formMenu: api.DrawMenuBar(self._formHwnd)

    @property
    def handle(self): return self._hmenu

    @property
    def foreColor(self) : return self._fgColor

    @foreColor.setter
    def foreColor(self, value):
        if isinstance(value, int):
            self._fgColor.updateColor(value)
        elif isinstance(value, Color):
            self._fgColor = value
        if self._type == MenuType.BASE_MENU: api.InvalidateRect(self._hmenu, None, False)

    @property
    def state(self): return self._state

    @state.setter
    def state(self, value: MenuState):
        self._state = value
        if self._isCreated:
            self._changeMenuState()
            # if self._type == MenuType.BASE_MENU:
            #     api.EnableMenuItem(self._hmenu, self._id, MF_BYCOMMAND | self._state )
            # elif self._type == MenuType.POP_UP:
            #     api.EnableMenuItem(self._hmenu, self._id, MF_BYCOMMAND | self._state )
            # elif self._type == MenuType.MENU_ITEM:
            #     api.EnableMenuItem(self._hmenu, self._index, MF_BYPOSITION | self._state )

    @property
    def enabled(self): return self._isEnabled

    @enabled.setter
    def enabled(self, value: bool):
        self._isEnabled = value
        if not value:
            self._state = MenuState.DISABLED
        else:
            self._state = MenuState.ENABLED
        if self._isCreated:
            self._changeMenuState()



    # @onClick.setter
    # def onClick(self, value) :
    #     self._click = value
    #     SendMessage(self._formHwnd, MyMessages.MENU_EVENT_SET, 0, id(self)) # Inform our parent window.





@WNDPROC
def cmenuWndProc(hw, msg, wp, lp):
    # log_msg(msg)
    match msg:
        case con.WM_DESTROY:
            
            print("Context Menu Msg Only Window destroyed")

        case con.WM_MEASUREITEM:
            pmi = cast(lp, LPMEASUREITEMSTRUCT).contents
            mi = cast(pmi.itemData, py_object).value
            pmi.itemWidth = mi._txtSize.cx + 20
            pmi.itemHeight = mi._txtSize.cy + 10
            # print("wm measure item")
            return True

        case con.WM_DRAWITEM:
            this = cast(api.GetWindowLongPtr(hw, con.GWLP_USERDATA), py_object).value
            dis = cast(lp, LPDRAWITEMSTRUCT).contents
            mi = cast(dis.itemData, py_object).value
            txtClrRef = mi._fgColor.ref
        
            if dis.itemState == 257:
                rc = api.RECT(dis.rcItem.left + 4, dis.rcItem.top + 2, dis.rcItem.right, dis.rcItem.bottom - 2)
                if mi._isEnabled:
                    FillRect(dis.hDC, byref(rc), this._hotBgBrush)
                    api.FrameRect(dis.hDC, byref(rc), this._borderBrush)
                    txtClrRef = 0x00000000
                else:
                    FillRect(dis.hDC, byref(rc), this._grayBrush)
                    # api.FrameRect(dis.hDC, byref(rc), this._borderBrush)
                    txtClrRef = this._grayCref

            else:
                FillRect(dis.hDC, byref(dis.rcItem), this._defBgBrush)
                if not mi._isEnabled: txtClrRef = this._grayCref

            SetBkMode(dis.hDC, con.TRANSPARENT)
            dis.rcItem.left += 20
            api.SetTextColor(dis.hDC, txtClrRef)
            api.SelectObject(dis.hDC, this._font.handle)
            DrawText(dis.hDC, mi._text, len(mi._text), byref(dis.rcItem), menuTxtFlag)
            return 0


        case con.WM_ENTERMENULOOP:
            this = cast(api.GetWindowLongPtr(hw, con.GWLP_USERDATA), py_object).value
            if this.onMenuShown: this.onMenuShown(this, GEA)

        case con.WM_EXITMENULOOP:
            this = cast(api.GetWindowLongPtr(hw, con.GWLP_USERDATA), py_object).value
            if this.onMenuClose: this.onMenuClose(this, GEA)

        case con.WM_MENUSELECT:
            this = cast(api.GetWindowLongPtr(hw, con.GWLP_USERDATA), py_object).value
            # print(f"lpm : {lp}, loword WPM : {LOWORD(wp)}")
            idNum = LOWORD(wp)
            if lp and idNum:
                menu = this._menus[idNum]
                if menu and menu._isEnabled:
                    if menu.onFocus: menu.onFocus(menu, GEA)

        case con.WM_COMMAND:
            this = cast(api.GetWindowLongPtr(hw, con.GWLP_USERDATA), py_object).value
            idNum = LOWORD(wp)
            if idNum:
                menu = this._menus[idNum]
                if menu and menu._isEnabled:
                    if menu.onClick: menu.onClick(menu, GEA)


    return DefWindowProc(hw, msg, wp, lp)



#========= Context Menu======================================================

CMMW_CLS = "PyFormsCmenuMsgWin" # ContextMenu Message Window Class

class ContextMenu(MenuBase):
    _isWinClassReg = False
    __slots__ = ("_font", "_width", "_height", "_msgWinHwnd", 
                 "_defBgBrush", "_hotBgBrush", "_borderBrush", 
                 "_selTxtClr", "_grayCref", "_grayBrush", "_style", 
                 "_menuInserted", "onMenuShown", "onMenuClose")

    def __init__(self, *menuNames) -> None:
        # parent = Control class object. Might be a Form or any controls.
        super().__init__()
        self._handle = CreatePopupMenu()
        self._width = 120
        self._height = 25
        self._font = Font()
        self.onMenuClose = None
        self.onMenuShown = None
        self._defBgBrush = Color(0xe9ecef).createHBrush()
        self._hotBgBrush = Color(0x90e0ef).createHBrush()
        self._borderBrush = Color(0x0077b6).createHBrush()
        self._selTxtClr = Color(0x000000)
        self._grayBrush = Color(0xced4da).createHBrush()
        self._grayCref = Color(0x979dac).ref 
        self._style = MenuStyle.SYSTEM      
        self._menuInserted = False
        if len(menuNames):
            indx = 0
            for name in menuNames:
                mtyp = MenuType.SEPARATOR if name == '_' else MenuType.MENU_ITEM
                mi = MenuItem(name, mtyp, self._handle, self._menuCount)
                mi._isCmenu = True
                self._menuCount += 1
                self._menus[mi._id] = mi
                indx += 1


    def showContextMenu(self, lpm):
        try:
            self._createMsgWindow()
            if not self._menuInserted: self._cmenuCreateHandle()
            xp = getMouseXpoint(lpm)
            yp = getMouseYpoint(lpm)
            if xp == -1 or yp == -1:
                # ContextMenu message generated by keybord shortcut.
                # So we need to find the mouse position.
                pt = getMousePosOnMsg()
                xp, yp = pt.x, pt.y

            mid = TrackPopupMenu(self._handle, TPM_RETURNCMD, xp, yp, 
                                            0, self._msgWinHwnd, None)
            if mid > 0:
                thismenu = self._menus[mid]
                if thismenu and thismenu._isEnabled:
                    if thismenu.onClick: 
                        thismenu.onClick(thismenu, GEA) 
        finally:
            if self._msgWinHwnd: DestroyWindow(self._msgWinHwnd)

    def getMenuItem(self, idNum):
        for menu in self._menus.values():
            if menu._id == idNum: return menu
        return None

    def _cmenuCreateHandle(self):
        if len(self._menus) > 0:
            hdc = None
            owner_draw = False
            if self._style == MenuStyle.CUSTOM:
                hdc = GetDC(self._formHwnd)
                api.SelectObject(hdc, self._font._handle)
                owner_draw = True
            for menu in self._menus.values():
                menu.insertInAPI(hdc, owner_draw)

            if hdc: api.ReleaseDC(self._formHwnd, hdc)
        self._menuInserted = True

    def _createMsgWindow(self): 
        # This hidden window will receive messages for context menu.

        if not ContextMenu._isWinClassReg:
            StaticData.registerMsgWinClass(CMMW_CLS, cmenuWndProc)
            ContextMenu._isWinClassReg = True

        self._msgWinHwnd = CreateWindowEx(0, CMMW_CLS, None, 0, 0, 0, 0, 0, 
                                          con.HWND_MESSAGE, None, StaticData.hInstance, None)
        if self._msgWinHwnd:
            # Storing the handle in global list so that we can destroy the window later.
            # CM_DICT[self._msgWinHwnd] = self
            api.SetWindowLongPtr(self._msgWinHwnd, con.GWLP_USERDATA, id(self))
            


    def finalize(self):
        if len(self._menus) > 0:
            for menu in self._menus.values():
                menu.finalize()

        api.DeleteObject(self._defBgBrush)
        api.DeleteObject(self._hotBgBrush)
        api.DeleteObject(self._borderBrush)
        api.DeleteObject(self._grayBrush)

        print("Destroying context menu")
        DestroyMenu(self._handle)



    @property
    def menus(self): return self._menus

    @property
    def style(self):
        return self._style
    
    @style.setter
    def style(self, value):
        self._style = value

    
    def menuItem(self, txt):
        for menu in self._menus.values():
            if menu._text == txt: return menu
        return None



    # def addMenu(self):
    #     self._hMenu = CreatePopupMenu()
    #     for name in

