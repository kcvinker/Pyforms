
# menubar module - Created on 21-02-2023 12:48 AM

from enum import Enum
from ctypes import create_unicode_buffer, sizeof, byref
from .apis import CreateMenu, AppendMenu, SetMenu, SetMenuInfo, SendMessage, MENUINFO
from .control import MenuEventData
from .commons import MyMessages


# Constants
MF_POPUP = 0x00000010
MF_STRING = 0x00000000
MF_SEPARATOR = 0x00000800
MF_CHECKED = 0x00000008
MNS_NOTIFYBYPOS = 0x08000000
MIM_STYLE = 0x00000010

# To hold static data for menu item and menu bar
class MenuData:
	static_menu_id = 100

# Differentiate various menu types
class MenuType(Enum):
	BASE_MENU = 0
	MENU_ITEM = 1
	POP_UP = 2
	SEPARATOR = 3
	MENU_BAR = 4

class MenuEvents(Enum):
	MENU_CLICK = 0



class MenuBar:
	"""MenuBar class is the container of all menus"""

	__slots__ = ("_hwnd", "menus", "_parent", "_type")

	def __init__(self, parent) -> None:
		self._hwnd = CreateMenu()
		self._parent = parent
		self._type = MenuType.MENU_BAR
		self.menus = {}

	def add_menu(self, txt: str):
		mi = MenuItem(txt, MenuType.BASE_MENU, self)
		self.menus[txt] = mi
		return mi

	def create(self):
		if len(self.menus):
			for menu in self.menus.values(): menu.create()

		SetMenu(self._parent._hwnd, self._hwnd)
		# mi = MENUINFO()
		# mi.cbSize = sizeof(MENUINFO)
		# mi.fMask = MIM_STYLE
		# mi.dwStyle = MNS_NOTIFYBYPOS
		# SetMenuInfo(self._hwnd, byref(mi))





class MenuItem:
	"""MenuItem represents a simple menu or dropdown menu or a separator"""
	__slots__ = ("_hwnd", "_parent", "_id", "_level", "_text", "_type", "menus", "_flags", "_form_hwnd", "_click")

	def __init__(self, txt: str, typ: MenuType, parent) -> None:
		self._hwnd = CreateMenu()
		self._id = MenuData.static_menu_id
		self._text = f"{self._id}" if txt == "" else txt
		self._type = typ
		self._parent = parent
		self.menus = {}
		self._flags = 0
		MenuData.static_menu_id += 1
		match typ:
			case MenuType.BASE_MENU:
				self._flags |= MF_POPUP
				self._form_hwnd = parent._parent._hwnd
			case MenuType.POP_UP:
				self._flags |= MF_POPUP
				self._form_hwnd = parent._form_hwnd
			case MenuType.MENU_ITEM :
				self._flags |= MF_STRING
				self._form_hwnd = parent._form_hwnd
			case MenuType.SEPARATOR:
				self._flags |= MF_SEPARATOR
				self._form_hwnd = parent._form_hwnd

	def add_menu(self, txt: str):
		mi = MenuItem(txt, MenuType.MENU_ITEM, self)
		self.menus[txt] = mi
		return mi

	def add_popup_menu(self, txt: str):
		mi = MenuItem(txt, MenuType.POP_UP, self)
		self.menus[txt] = mi
		return mi

	def add_seperator(self):
		mi = MenuItem("", MenuType.SEPARATOR, self)
		self.menus[mi._text] = mi
		return mi


	def create(self):
		match self._type:
			case MenuType.BASE_MENU | MenuType.POP_UP:
				if len(self.menus):
					for menu in self.menus.values(): menu.create()
					AppendMenu(self._parent._hwnd, self._flags, self._hwnd, create_unicode_buffer(self._text))
				else:
					# It will act like a normal menu item.
					self._flags ^= MF_POPUP
					self._flags |= MF_STRING
					AppendMenu(self._parent._hwnd, self._flags, self._id, create_unicode_buffer(self._text))
			case MenuType.MENU_ITEM:
				AppendMenu(self._parent._hwnd, self._flags, self._id, create_unicode_buffer(self._text))
			case MenuType.SEPARATOR:
				AppendMenu(self._parent._hwnd, self._flags, 0, None)


	@property
	def on_click(self) : return self._click

	@on_click.setter
	def on_click(self, value) :
		self._click = value
		SendMessage(self._form_hwnd, MyMessages.MENU_EVENT_SET, 0, id(self)) # Inform our parent window.







