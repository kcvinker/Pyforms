# menubar module - Created on 21-02-2023 12:48 AM

from enum import Enum
import pyforms.src.apis as api
from ctypes import create_unicode_buffer, byref, cast, sizeof, c_wchar_p, py_object
from pyforms.src.apis import CreateMenu, AppendMenu, SetMenu, SendMessage, POINT, CreatePopupMenu, ClientToScreen, TrackPopupMenu, DestroyMenu
from pyforms.src.apis import SUBCLASSPROC, LRESULT, DefSubclassProc, CreateWindowEx, SetWindowSubclass, RemoveWindowSubclass, DestroyWindow
from pyforms.src.apis import LOWORD, HIWORD, DrawMenuBar, InsertMenuW, LPMEASUREITEMSTRUCT, LPDRAWITEMSTRUCT, MENUITEMINFO
from pyforms.src.apis import DrawText, InsertMenuItemW, SetBkMode, FillRect, CreateSolidBrush, ULONG_PTR, GetDC, ReleaseDC
from pyforms.src.commons import MyMessages, getMousePoints, getMouseXpoint, getMouseYpoint, getMousePosOnMsg, menuTxtFlag
from pyforms.src.control import Control
from pyforms.src.colors import Color
from pyforms.src.events import EventArgs
import pyforms.src.constants as con
from pyforms.src.winmsgs import log_msg

# region Constants
MF_POPUP = 0x00000010
MF_STRING = 0x00000000
MF_SEPARATOR = 0x00000800
MF_CHECKED = 0x00000008
MNS_NOTIFYBYPOS = 0x08000000
MIM_STYLE = 0x00000010
TPM_RIGHTBUTTON = 0x0002
MF_BYPOSITION = 0x400
MF_OWNERDRAW = 0x00000100

MIIM_STATE = 0x00000001
MIIM_ID = 0x00000002
MIIM_SUBMENU = 0x00000004
MIIM_CHECKMARKS = 0x00000008
MIIM_TYPE = 0x00000010
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

MF_BITMAP = 0x00000004

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
# endregion

calcRectFlag = con.DT_SINGLELINE | con.DT_LEFT | con.DT_VCENTER | con.DT_CALCRECT

# To hold static data for menu item and menu bar
class MenuData:
	staticMenuID = 100
	staticMenuIndex = 0


# Differentiate various menu types
class MenuType(Enum):
	BASE_MENU = 0
	MENU_ITEM = 1
	POP_UP = 2
	SEPARATOR = 3
	MENU_BAR = 4
	CONTEXT_MENU = 5
	CONTEXT_SEP = 6

class MenuEvents(Enum):
	MENU_CLICK = 0

class MenuState(Enum):
	ENABLED = 0
	GRAYED = 1
	DISABLED = 2


class MenuBar:
	"""MenuBar class is the container of all menus"""

	__slots__ = ("_hMenubar", "menus", "_parent", "_type", "_menuCount")

	def __init__(self, parent) -> None:
		self._hMenubar = CreateMenu()
		self._parent = parent
		self._type = MenuType.MENU_BAR
		self._menuCount = 0
		self.menus = {}

		# We need this brush & color ref for drawing a disabled menu.
		parent._menuGrayBrush = Color(0xced4da).createHBrush()
		parent._menuGrayCref = Color(0x979dac).ref
		# print("hmenubar ", self._hMenubar)
		# parent._menuBar = self

	def addMenu(self, txt: str):
		mi = MenuItem(txt, MenuType.BASE_MENU, self._hMenubar, self._menuCount)
		mi._formHwnd = self._parent._hwnd
		mi._formMenu = True
		self._menuCount += 1
		self.menus[txt] = mi
		self._parent._menuItemDict[mi._id] = mi
		return mi



	def create(self):
		self._parent._menuDefBgBrush = Color(0xe9ecef).createHBrush()
		self._parent._menuHotBgBrush = Color(0x90e0ef).createHBrush()
		self._parent._menuFrameBrush = Color(0x0077b6).createHBrush()
		self._parent._menuFont = self._parent._font
		if len(self.menus):
			for menu in self.menus.values(): menu.create()
		SetMenu(self._parent._hwnd, self._hMenubar)

	@property
	def handle(self): return self._hMenubar


# Removable candidates - _formHwnd


class MenuItem:
	"""MenuItem represents a simple menu or dropdown menu or a separator"""

	__slots__ = ("_index","_font", "_wTxt", "_wideText", "_bgColor", "_fgColor", "_hmenu", "_state",
	      			"_parentHmenu", "_id", "_level", "_text", "_type", "_menus", "_isCreated", "_isEnabled",
					"_formHwnd", "onClick", "onPopup", "onCloseup", "onFocus", "_childCount", "_popup", "_formMenu")

	def __init__(self, txt: str, typ: MenuType, parentHmenu, indexNum) -> None:
		self._popup = True if typ == MenuType.BASE_MENU or typ == MenuType.POP_UP else False
		self._hmenu = CreatePopupMenu() if self._popup else CreateMenu()
		self._index = indexNum
		self._id = MenuData.staticMenuID
		self._text = f"{self._id}" if txt == "" else txt
		self._wideText = create_unicode_buffer(self._text)
		self._wTxt = cast(self._wideText, c_wchar_p)
		self._type = typ
		self._parentHmenu = parentHmenu
		self._bgColor = Color(0xe9ecef)
		self._fgColor = Color(0x000000)
		self._menus = {}
		self.onClick = None
		self.onPopup = None
		self.onCloseup = None
		self.onFocus = None
		self._childCount = 0
		self._formMenu = False
		self._isCreated = False
		self._isEnabled = True
		self._state = MenuState.ENABLED
		MenuData.staticMenuID += 1

	def addMenu(self, txt: str):
		if self._type == MenuType.MENU_ITEM:
			self._hmenu = CreatePopupMenu()
			self._popup = True
		mi = MenuItem(txt, MenuType.MENU_ITEM, self._hmenu, self._childCount)
		mi._formHwnd = self._formHwnd
		mi._formMenu = self._formMenu
		if self._type != MenuType.BASE_MENU: self._type = MenuType.POP_UP
		self._childCount += 1
		self._menus[txt] = mi
		if mi._formMenu: api.SendMessage(mi._formHwnd, MyMessages.MENU_ADDED, mi._id, id(mi))
		return mi

	def addSeperator(self):
		mi = MenuItem("", MenuType.SEPARATOR, self._hmenu, self._childCount)
		self._childCount += 1
		self._menus[mi._text] = mi
		# return mi

	def _insertMenuInternal(self, parentHmenu):
		mii = MENUITEMINFO()
		mii.cbSize = sizeof(MENUITEMINFO)
		mii.fMask = MIIM_ID | MIIM_TYPE | MIIM_DATA | MIIM_SUBMENU | MIIM_STATE
		mii.fType = MF_OWNERDRAW
		mii.dwTypeData = self._wTxt
		mii.cch = len(self._text)
		mii.dwItemData = id(self)
		mii.wID = self._id
		mii.fState = self._state
		mii.hSubMenu = self._hmenu if self._popup else None
		InsertMenuItemW(parentHmenu, self._index, True, byref(mii))
		self._isCreated = True
		# print(f"{self._text = }, {self._state = }")


	def create(self):
		match self._type:
			case MenuType.BASE_MENU | MenuType.POP_UP:
				if len(self._menus):
					for menu in self._menus.values(): menu.create()
				self._insertMenuInternal(self._parentHmenu)

			case MenuType.MENU_ITEM:
				self._insertMenuInternal(self._parentHmenu)
			case MenuType.SEPARATOR:
				AppendMenu(self._parentHmenu, MF_SEPARATOR, 0, None)


	def getChildFromIndex(self, index):
		for menu in self._menus.values():
			# print("indexes ", menu._index)
			if menu._index == index:

				return menu
		return None


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

	# @property
	# def state(self): return self._state

	# @state.setter
	# def state(self, value: MenuState):
	# 	self._state = value
	# 	if self._isCreated:
	# 		if self._type == MenuType.BASE_MENU:
	# 			api.EnableMenuItem(self._hmenu, self._id, MF_BYCOMMAND | self._state )
	# 		elif self._type == MenuType.POP_UP:
	# 			api.EnableMenuItem(self._hmenu, self._id, MF_BYCOMMAND | self._state )
	# 		elif self._type == MenuType.MENU_ITEM:
	# 			api.EnableMenuItem(self._hmenu, self._index, MF_BYPOSITION | self._state )

	@property
	def enabled(self): return self._isEnabled

	@enabled.setter
	def enabled(self, value: bool):
		self._isEnabled = value
		if self._type == MenuType.BASE_MENU: api.InvalidateRect(self._hmenu, None, False)


	# @onClick.setter
	# def onClick(self, value) :
	# 	self._click = value
	# 	SendMessage(self._formHwnd, MyMessages.MENU_EVENT_SET, 0, id(self)) # Inform our parent window.





cmDict = {} # This will hold the context menu instances



@SUBCLASSPROC
def cmenuWndProc(hw, msg, wp, lp, scID, refData):
	# log_msg(msg)
	this = cmDict[refData]
	match msg:
		case con.WM_DESTROY:
			ret = RemoveWindowSubclass(hw, cmenuWndProc, scID)

		case con.WM_MEASUREITEM:
			pmi = cast(lp, LPMEASUREITEMSTRUCT).contents
			# mi = cast(pmi.itemData, py_object).value
			# hdc = GetDC(hw)
			# size = api.SIZE()
			# api.GetTextExtentPoint32(hdc, mi._wideText, len(mi._text), byref(size))
			# api.ReleaseDC(hw, hdc)
			pmi.itemWidth = this._width #size.cx + 10
			pmi.itemHeight = this._height #size.cy + 10
			return True

		case con.WM_DRAWITEM:
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
			DrawText(dis.hDC, mi._wideText, -1, byref(dis.rcItem), menuTxtFlag)
			return 0


		case con.WM_ENTERMENULOOP:
			if this.onMenuShown: this.onMenuShown(this, EventArgs())

		case con.WM_EXITMENULOOP:
			if this.onMenuClose: this.onMenuClose(this, EventArgs())

		case con.WM_MENUSELECT:
			# print(f"lpm : {lp}, loword WPM : {LOWORD(wp)}")
			idNum = LOWORD(wp)
			if lp and idNum:
				menu = this.getMenuItem(idNum)
				if menu and menu._isEnabled:
					if menu.onFocus: menu.onFocus(menu, EventArgs())

		case con.WM_COMMAND:
			idNum = LOWORD(wp)
			if idNum:
				menu = this.getMenuItem(idNum)
				if menu and menu._isEnabled:
					if menu.onClick: menu.onClick(menu, EventArgs())


	return DefSubclassProc(hw, msg, wp, lp)


def createDummy(hwndParent, hInst): # We need this dummy window to receive messages for context menu.
	dummyHwnd = CreateWindowEx(0, create_unicode_buffer("Button"), None, con.WS_CHILD, 0, 0, 0, 0, hwndParent, 0, hInst, None)
	SetWindowSubclass(dummyHwnd, cmenuWndProc, Control._subclass_id, MenuData.staticMenuID)
	MenuData.staticMenuID += 1
	Control._subclass_id += 1
	return dummyHwnd

#========= Context Menu======================================================

class ContextMenu:

	__slots__ = ("_menus", "_hMenu", "_font", "_width", "_height", "_dummyHwnd", "_defBgBrush", "_hotBgBrush", "_borderBrush",
	      		"_selTxtClr", "_grayCref", "_grayBrush", "_menuCount", "onMenuShown", "onMenuClose")

	def __init__(self, parent, *menuNames) -> None:
		self._menus = []
		self._hMenu = CreatePopupMenu()
		self._width = 120
		self._height = 25
		self.onMenuClose = None
		self.onMenuShown = None
		self._defBgBrush = Color(0xe9ecef).createHBrush()
		self._hotBgBrush = Color(0x90e0ef).createHBrush()
		self._borderBrush = Color(0x0077b6).createHBrush()
		self._selTxtClr = Color(0x000000)
		self._grayBrush = Color(0xced4da).createHBrush()
		self._grayCref = Color(0x979dac).ref
		self._menuCount = 0
		cmDict[MenuData.staticMenuID] = self
		self._dummyHwnd = createDummy(parent._hwnd, parent.wnd_class.hInstance)

		if len(menuNames):
			indx = 0
			for name in menuNames:
				mtyp = MenuType.CONTEXT_SEP if name == '_' else MenuType.CONTEXT_MENU
				mi = MenuItem(name, mtyp, parent, self._menuCount)
				self._menuCount += 1
				if mtyp == MenuType.CONTEXT_MENU:
					mi._insertMenuInternal(self._hMenu)
					self._menus.append(mi)
				elif mtyp == MenuType.CONTEXT_SEP:
					AppendMenu(self._hMenu, MF_SEPARATOR, 0, None)
				indx += 1


	def showContextMenu(self, lpm):
		xp = getMouseXpoint(lpm)
		yp = getMouseYpoint(lpm)
		if xp == -1 or yp == -1:
			# ContextMenu message generated by keybord shortcut.
			# So we need to find the mouse position.
			pt = getMousePosOnMsg()
			xp, yp = pt.x, pt.y
		TrackPopupMenu(self._hMenu, TPM_RIGHTBUTTON, xp, yp, 0, self._dummyHwnd, None)

	def getMenuItem(self, idNum):
		for menu in self._menus:
			if menu._id == idNum: return menu
		return None



	def destroyContextMenu(self):
		print("Destroying context menu")
		DestroyMenu(self._hMenu)



	@property
	def menus(self): return self._menus




	# def addMenu(self):
	# 	self._hMenu = CreatePopupMenu()
	# 	for name in

