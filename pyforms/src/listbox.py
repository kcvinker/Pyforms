# listbox module - Created on 11-Dec-2022 11:23:20

from ctypes import addressof, create_unicode_buffer, c_int
from pyforms.src.control import Control
import pyforms.src.constants as con
from pyforms.src.commons import MyMessages
from pyforms.src.enums import ControlType
from pyforms.src.events import EventArgs
from pyforms.src.apis import LRESULT, SUBCLASSPROC
import pyforms.src.apis as api
from pyforms.src.colors import Color

lbxDict = {}
lbxStyle = con.WS_CHILD | con.WS_VISIBLE | con.WS_BORDER  | con.LBS_NOTIFY | con.LBS_HASSTRINGS


class ListBox(Control):

    """ListBox control """
    _count = 1
    __slots__ = ( "_hasSort", "_noSel", "_multiCol", "_keyPreview", "_useVScroll", "_useHScroll", "_multiSel", "_selIndices",
                    "_items",  "_dummyIndex", "_selIndex", "onSelectionChanged", "onDoubleClick"  )

    def __init__(self, parent, xpos: int = 10, ypos: int = 10, width: int = 150, height: int = 200, bCreate = False) -> None:
        super().__init__()

        self._clsName = "LISTBOX"
        self.name = f"ListBox_{ListBox._count}"
        self._ctlType = ControlType.LIST_BOX
        self._parent = parent
        self._bgColor = Color(parent._bgColor)
        self._font = parent._font
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._isTextable = False
        self._style = lbxStyle
        self._exStyle = 0
        self._hasSort = False
        self._noSel = False
        self._multiCol = False
        self._keyPreview = False
        self._useHScroll = False
        self._useVScroll = False
        self._multiSel = False
        self._selIndices = ()
        self._items = []
        self._dummyIndex = -1
        self._selIndex = -1
        # print("listbox inited")
        # Events
        self.onSelectionChanged = None
        self.onDoubleClick = None

        ListBox._count += 1
        if bCreate: self.createHandle()

# -region Public functions


    def createHandle(self):
        """Create's ListBox handle"""

        self._setStyles()
        self._createControl()
        if self._hwnd:
            # print("list box hwnd ", self._hwnd)
            lbxDict[self._hwnd] = self
            self._isCreated = True
            self._setSubclass(lbxWndProc)
            self._setFontInternal()

            if self._items:
                for item in self._items:
                    buff = create_unicode_buffer(item) if type(item) == str else create_unicode_buffer(str(item))
                    api.SendMessage(self._hwnd, con.LB_ADDSTRING, 0, addressof(buff))
                    if self._dummyIndex > -1: api.SendMessage(self._hwnd, con.LB_SETCURSEL, self._dummyIndex, 0)

    def addItem(self, item):
        """Add an item to list box """
        if self._isCreated:
            buff = create_unicode_buffer(str(item))
            api.SendMessage(self._hwnd, con.LB_ADDSTRING, 0, addressof(buff))
        self._items.append(item)

    def addItems(self, *items):
        """Add an multiple items to list box """
        self._items.extend(items)
        if self._isCreated:
            for item in items:
                sitem = item if isinstance(item, str) else str(item)
                buff = create_unicode_buffer(sitem)
                api.SendMessage(self._hwnd, con.LB_ADDSTRING, 0, addressof(buff))
        else:
            for item in items:
                sitem = item if isinstance(item, str) else str(item)
                self._items.append(item)



    def selectAll(self):
        """Select all the items in ListBox but only in multi selection mode"""
        if self._isCreated and self._multiSel:
            api.SendMessage(self._hwnd, con.LB_SETSEL, True, -1)


    def clearSelection(self):
        """Clear the selection from list box"""
        if self._isCreated:
            if self._multiSel:
                api.SendMessage(self._hwnd, con.LB_SETSEL, False, -1)
            else:
                api.SendMessage(self._hwnd, con.LB_SETCURSEL, -1, 0)


    def insertItem(self, item, index):
        """Insert an item to list box """
        if self._isCreated:
            buff = create_unicode_buffer(str(item))
            api.SendMessage(self._hwnd, con.LB_INSERTSTRING, index, addressof(buff))

        if index == -1:
            self._items.append(item)
        else:
            self._items.insert(index, item)


    def removeItem(self, index):
        """Remove an item from list box"""
        if self._isCreated:
            res = api.SendMessage(self._hwnd, con.LB_DELETESTRING, index, 0)
            if res != con.LB_ERR: del self._items[index]
        else:
            del self._items[index]


    def removeAll(self):
        """Remove all the items from list box"""
        if self._isCreated:
            api.SendMessage(self._hwnd, con.LB_RESETCONTENT, 0, 0)
        self._items.clear()

# -endregion Public functions


    # -region private_funcs

    # Set list box styles
    def _setStyles(self):
        if self._hasSort: self._style |= con.LBS_SORT
        if self._multiSel: self._style |= con.LBS_EXTENDEDSEL | con.LBS_MULTIPLESEL
        if self._multiCol: self._style |= con.LBS_MULTICOLUMN
        if self._noSel: self._style |= con.LBS_NOSEL
        if self._keyPreview: self._style |= con.LBS_WANTKEYBOARDINPUT
        if self._useHScroll: self._style |= con.WS_HSCROLL
        if self._useVScroll: self._style |= con.WS_VSCROLL

    # Internal function to get an item from listbox
    def _getItem(self, index: int) -> str:
        # print("161")
        item_len = api.SendMessage(self._hwnd, con.LB_GETTEXTLEN, index, 0)
        if item_len != con.LB_ERR:
            buff = create_unicode_buffer(item_len)
            api.SendMessage(self._hwnd, con.LB_GETTEXT, index, addressof(buff))
            return buff.value
        else:
            return ""

    # -endregion Private funcs

    # -region Properties

    @property
    def items(self):
        """Returns the item collection"""
        return self._items
    #-----------------------------------------------------------------------------1

    @property
    def hasHScroll(self)-> bool:
        """Returns true if list box has horizontal scroll enabled"""
        return self._useHScroll

    @hasHScroll.setter
    def hasHScroll(self, value: bool):
        """set true if list box has horizontal scroll enabled"""
        self._useHScroll = value
    # #------------------------------------------------------------------------2

    @property
    def hasVScroll(self)-> bool:
        """Returns true if list box has vertical scroll enabled"""
        return self._useVScroll

    @hasVScroll.setter
    def hasVScroll(self, value: bool):
        """Set true if list box has vertical scroll enabled"""
        self._useVScroll = value
    # #------------------------------------------------------------------------3

    @property
    def selectedIndex(self)-> int:
        """Get the selected index from list box"""
        if self._isCreated and not self._multiSel:
            sel_ind = api.SendMessage(self._hwnd, con.LB_GETCURSEL, 0, 0)
            return sel_ind if sel_ind else -1
        return -1


    @selectedIndex.setter
    def selectedIndex(self, value: int):
        """Set the selected index of list box"""
        if self._isCreated and not self._multiSel:
            res = api.SendMessage(self._hwnd, con.LB_SETCURSEL, value, 0)
            if res != con.LB_ERR: self._selIndex = value # Fix this : We can avoid using _selIndex
        else:
            self._dummyIndex = value
            self._selIndex = value
    # #------------------------------------------------------------------------4

    @property
    def selectedIndices(self)-> tuple[int]:
        """Get the selected indices as a list from list box"""
        if self._multiSel and self._isCreated:
            sel_count = api.SendMessage(self._hwnd, con.LB_GETSELCOUNT, 0, 0)
            if sel_count:
                c_array = (c_int * sel_count )() # We create an array of int type
                api.SendMessage(self._hwnd, con.LB_GETSELITEMS, sel_count, addressof(c_array))
                # self._selIndices = [item for item in c_array] # IMPROVE THIS
                self._selIndices = tuple(c_array) # Seems better. 16 micro seconds. List's speed is 24 micro
            else:
                self._selIndices = ()

        return self._selIndices
    # #------------------------------------------------------------------------5

    @property
    def multiSelection(self)-> bool:
        """Returns true if this list box has multi selection enabled"""
        return self._multiSel

    @multiSelection.setter
    def multiSelection(self, value: bool):
        """Set true if this list box has multi selection enabled"""
        self._multiSel = value
    # #--------------------------------------------------------------------------------------------6

    @property
    def selectedItem(self)-> str:
        """Returns the selected item from list box"""
        if self._isCreated and not self._multiSel:
            sel_ind = api.SendMessage(self._hwnd, con.LB_GETCURSEL, 0, 0)
            # print(f"{sel_ind = }")
            if sel_ind >= 0: return self._getItem(sel_ind)
        return ""

    @selectedItem.setter
    def selectedItem(self, value):
        """Set the given item as selected in list box"""
        if self._isCreated and not self._multiSel:
            api.SendMessage(self._hwnd, con.LB_SETCURSEL, value, 0)
    # #----------------------------------------------------------------------7

    @property
    def hotIndex(self)-> int:
        """Returns the index of item under mouse pointer"""
        if self._isCreated and self._multiSel:
            return api.SendMessage(self._hwnd, con.LB_GETCARETINDEX, 0, 0)
    # #-------------------------------------------------------------------------8

    @property
    def selectedItems(self)-> list[str]:
        """Returns the selected items as a list. Only work for multi selection list boxes"""
        if self._isCreated and self._multiSel:
            sel_count = api.SendMessage(self._hwnd, con.LB_GETSELCOUNT, 0, 0)
            if sel_count != con.LB_ERR:
                c_array = (c_int * sel_count)() # We create an array of int type
                api.SendMessage(self._hwnd, con.LB_GETSELITEMS, sel_count, addressof(c_array))
                return [self._getItem(index) for index in c_array]
        return None

    # #---------------------------------------------------------9

    @property
    def hotItem(self)-> str:
        """Returns the index of item under mouse pointer"""
        if self._isCreated and self._multiSel:
            indx = api.SendMessage(self._hwnd, con.LB_GETCARETINDEX, 0, 0)
            if indx >= 0: return self._getItem(indx)
        return ""

    # -endregion Properties

# End ListBox

@SUBCLASSPROC
def lbxWndProc(hw, msg, wp, lp, scID, refData) -> LRESULT:
    # printWinMsg(msg)
    lbx = lbxDict[hw]
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, lbxWndProc, scID)
            del lbxDict[hw]

        case MyMessages.LIST_COLOR:
            if lbx._drawFlag:
                api.SetBkMode(wp, 1)

                if lbx._drawFlag & 1:
                    api.SetTextColor(wp, lbx._fgColor.ref)

                if lbx._drawFlag & 2:
                    return api.CreateSolidBrush(lbx._bgColor.ref)
                else:
                    return api.GetStockObject(con.DC_BRUSH)

        case MyMessages.CTL_COMMAND:
            ncode = api.HIWORD(wp)
            match ncode:
                case con.LBN_DBLCLK:
                    if lbx.onDoubleClick: lbx.onDoubleClick(lbx, EventArgs())
                case con.LBN_SELCHANGE:

                    if lbx.onSelectionChanged: lbx.onSelectionChanged(lbx, EventArgs())

        case con.WM_SETFOCUS: lbx._gotFocusHandler()
        case con.WM_KILLFOCUS: lbx._lostFocusHandler()
        case con.WM_LBUTTONDOWN: lbx._leftMouseDownHandler(msg, wp, lp)
        case con.WM_LBUTTONUP: lbx._leftMouseUpHandler(msg, wp, lp)
        case con.WM_RBUTTONDOWN: lbx._rightMouseDownHandler(msg, wp, lp)
        case con.WM_RBUTTONUP: lbx._rightMouseUpHandler(msg, wp, lp)
        case con.WM_MOUSEWHEEL: lbx._mouseWheenHandler(msg, wp, lp)
        case con.WM_MOUSEMOVE: lbx._mouseMoveHandler(msg, wp, lp)
        case con.WM_MOUSELEAVE: lbx._mouseLeaveHandler()

    return api.DefSubclassProc(hw, msg, wp, lp)
