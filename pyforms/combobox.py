# Created on 24-Nov-2022 05:00:20

from ctypes.wintypes import HWND, UINT, HDC
from ctypes import WINFUNCTYPE, byref, sizeof, addressof, create_unicode_buffer
from .control import Control
from . import constants as con
from .commons import MyMessages, getMousePosOnMsg, point_in_rect
from .enums import ControlType
from .events import EventArgs
from .apis import LRESULT, UINT_PTR, DWORD_PTR, RECT, COMBOBOXINFO, WPARAM, LPARAM, SUBCLASSPROC
from . import apis as api
from .colors import Color
# from horology import Timing

cmb_dict = {}
cmb_tb_dict = {}
cmb_style = con.WS_CHILD | con.WS_VISIBLE

class ComboBox(Control):

    """Combo box control """
    _count = 1
    _tb_subcls_id = 4000
    __slots__ = ( "_onceCreated", "_items", "_visItemCount", "_selIndex", "_oldHwnd",
                    "_enableInput", "_recreated",
                    "onSelectionCommitted", "onListClosed", "onListOpened", "onTextUpdated", "onTextChanged",
                    "onSelectionChanged", "onSelectionCancelled" )

    def __init__(self, parent, xpos: int = 10, ypos: int = 10, width: int = 120, height: int = 30) -> None:
        super().__init__()
        self._clsName = "ComboBox"
        self.name = f"ComboBox_{ComboBox._count}"
        self._ctlType = ControlType.COMBO_BOX
        self._parent = parent
        self._bgColor = Color(parent._bgColor)
        self._font = parent._font
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._style = cmb_style
        self._exStyle = 0x00000200
        self._onceCreated = False
        self._items = []
        self._visItemCount = 0
        self._selIndex = -1
        self._oldHwnd = 0
        self._enableInput = False
        self._recreated = False

        # Events
        self.onSelectionCancelled = 0
        self.onSelectionChanged = 0
        self.onTextChanged = 0
        self.onTextUpdated = 0
        self.onListOpened = 0
        self.onListClosed = 0
        self.onSelectionCommitted = 0

        ComboBox._count += 1


    # Create's combo box handle
    def createHandle(self):

        """Create's combo box handle"""

        if self._recreated: # This is recreation.
            del cmb_dict[self._hwnd]
        else: # First time creation
            self._setCtlID()
            self._setStyles()

        self._hwnd = api.CreateWindowEx(self._exStyle,
                                        self._clsName,
                                        self._text,
                                        self._style,
                                        self._xpos,
                                        self._ypos,
                                        self._width,
                                        self._height,
                                        self._parent._hwnd,
                                        self._cid,
                                        self._parent.wnd_class.hInstance, None )
        if self._hwnd:
            cmb_dict[self._hwnd] = self
            if not self._isCreated:
                self._isCreated = True

            self._recreated = False # We need to allow user to recreate again and again.
            self._setSubclass(cmbWndProc)
            self._setFontInternal()
            self._getComboInfo()
            self._insertItems()
            if self._selIndex > -1: api.SendMessage(self._hwnd, con.CB_SETCURSEL, self._selIndex, 0)

    # -region private_funcs

    # Setting combo styles
    def _setStyles(self):
        if self._enableInput:
            self._style |= con.CBS_DROPDOWN
        else:
            self._style |= con.CBS_DROPDOWNLIST

    # Get the combo's internal info from OS
    def _getComboInfo(self):
        ci = COMBOBOXINFO()
        ci.cbSize = sizeof(COMBOBOXINFO)
        ciPtr = addressof(ci)
        api.SendMessage(self._hwnd, con.CB_GETCOMBOBOXINFO, 0, ciPtr)
        self.parent._combo_dict[ci.hwndList] = self._hwnd  # Putting list hwnd in form's special dict.
        api.SetWindowSubclass(ci.hwndItem, cmbEditWndProc, ComboBox._tb_subcls_id, self._hwnd)
        ComboBox._tb_subcls_id += 1


    # Helper function for inserting items to combo
    def _insertItems(self):
        if self._items:
            for item in self._items:
                sitem = item if isinstance(item, str) else str(item)
                buff = create_unicode_buffer(sitem)
                api.SendMessage(self._hwnd, con.CB_ADDSTRING, 0, addressof(buff))


    # Helper function for checking mouse lieaved from combo
    def _checkMouseLeave(self):
        rc = RECT()
        api.GetWindowRect(self._hwnd, byref(rc))
        p = getMousePosOnMsg()
        return point_in_rect(rc, p)

    # -endregion

    # -region Properties

    @property
    def items(self):
        """Get the items collection"""
        return self._items


    @property
    def itemCount(self):
        """Get the item count of this combo"""
        return len(self._items)

    @property
    def selectedIndex(self):
        """Get the selected index of this combo."""
        if self._isCreated: return api.SendMessage(self._hwnd, con.CB_GETCURSEL, 0, 0)
        return -1


    @selectedIndex.setter
    def selectedIndex(self, value):
        """Set the selected index of this combo"""
        self._selIndex = value
        if self._isCreated: api.SendMessage(self._hwnd, con.CB_SETCURSEL, value, 0)

    @property
    def enableInput(self):
        """Get the boolean value of enable text input for this combo. """
        return self._enableInput

    @enableInput.setter
    def enableInput(self, value: bool):
        """Enable text input for this combo"""
        if self._isCreated:
            if self._enableInput != value:
                if value:
                    self._style ^= con.CBS_DROPDOWNLIST
                    self._style |= con.CBS_DROPDOWN
                else:
                    self._style ^= con.CBS_DROPDOWN
                    self._style |= con.CBS_DROPDOWNLIST

                self._enableInput = value
                self._recreated = True
                api.DestroyWindow(self._hwnd) # Destroy this combo and create new one.
                self.createHandle()
        else:
            self._enableInput = value

    # -endregion props


    # -region public functions
    def addItem(self, item):
        """Add an item to this combo"""
        self._items.append(item)
        if self._isCreated:
            sitem = item if isinstance(item, str) else str(item)
            buff = create_unicode_buffer(sitem)
            api.SendMessage(self._hwnd, con.CB_ADDSTRING, 0, addressof(buff))


    def addItems(self, *args):
        """Add items to this combo"""
        self._items.extend(args)
        if self._isCreated:
            for item in args:
                sitem = item if isinstance(item, str) else str(item)
                buff = create_unicode_buffer(sitem)
                api.SendMessage(self._hwnd, con.CB_ADDSTRING, 0, addressof(buff))


    def removeItemAt(self, index):
        """Remove an item at the given index"""
        if index in range(len(self._items)):
            item = self._items[index]
            sitem = item if isinstance(item, str) else str(item)
            create_unicode_buffer(sitem)
            cIndex = api.SendMessage(self._hwnd, con.CB_FINDSTRING, -1, addressof(item))
            if cIndex > -1 :
                api.SendMessage(self._hwnd, con.CB_DELETESTRING, cIndex, 0)
                del self._items[index]


    def removeItem(self, item):
        """Remove the given item from combo"""
        if self._items.__contains__(item):
            sitem = item if isinstance(item, str) else str(item)
            buff = create_unicode_buffer(sitem)
            cIndex = api.SendMessage(self._hwnd, con.CB_FINDSTRING, -1, addressof(buff))
            if cIndex > -1 :
                api.SendMessage(self._hwnd, con.CB_DELETESTRING, cIndex, 0)
                self._items.remove(item)
        else:
            print("item is not in list")


    def removeItems(self, *args):
        """Remove the given items from this combo"""
        if(all(x in self._items for x in args)):
            for item in args:
                sitem = item if isinstance(item, str) else str(item)
                buff = create_unicode_buffer(sitem)
                cIndex = api.SendMessage(self._hwnd, con.CB_FINDSTRING, -1, addressof(buff))
                if cIndex > -1 :
                    api.SendMessage(self._hwnd, con.CB_DELETESTRING, cIndex, 0)
                    self._items.remove(item)
        else:
            print("Given items are not in list")


    def clearItems(self):
        """Delete all items from this combo"""
        if self._items:
            del self._items[:]
            api.SendMessage(self._hwnd, con.CB_DELETESTRING, 0, 0)


    # -endregion

    # def dumm(self): pass

#End ComboBox




@SUBCLASSPROC
def cmbWndProc(hw, msg, wp, lp, scID, refData):
    # printWinMsg(msg)
    cmb = cmb_dict[hw]
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, cmbWndProc, scID)
            if not cmb._recreated: del cmb_dict[hw] # Only remove if this is a natural end

        case MyMessages.LIST_COLOR:
            if cmb._drawFlag:
                hdc = HDC(wp)
                if cmb._drawFlag & 1: api.SetTextColor(hdc, cmb._fgColor.ref )
                api.SetBkColor(hdc, cmb._bgColor.ref)
                return api.CreateSolidBrush(cmb._bgColor.ref)

        case MyMessages.CTL_COMMAND:
            ncode = api.HIWORD(wp)
            match ncode:
                case con.CBN_SELCHANGE:
                    if cmb.onSelectionChanged: cmb.onSelectionChanged(cmb, EventArgs())
                case con.CBN_EDITCHANGE:
                    if cmb.onTextChanged: cmb.onTextChanged(cmb, EventArgs())
                case con.CBN_EDITUPDATE:
                    if cmb.onTextUpdated: cmb.onTextUpdated(cmb, EventArgs())
                case con.CBN_DROPDOWN:
                    if cmb.onListOpened: cmb.onListOpened(cmb, EventArgs())
                case con.CBN_CLOSEUP:
                    if cmb.onListClosed: cmb.onListClosed(cmb, EventArgs())
                case con.CBN_SELENDOK:
                    if cmb.onSelectionCommitted: cmb.onSelectionCommitted(cmb, EventArgs())
                case con.CBN_SELENDCANCEL:
                    if cmb.onSelectionCancelled: cmb.onSelectionCancelled(cmb, EventArgs())

        case con.WM_SETFOCUS: cmb._gotFocusHandler()
        case con.WM_KILLFOCUS: cmb._lostFocusHandler()
        case con.WM_LBUTTONDOWN: cmb._leftMouseDownHandler(msg, wp, lp)
        case con.WM_LBUTTONUP: cmb._leftMouseUpHandler(msg, wp, lp)
        case MyMessages.MOUSE_CLICK: cmb._mouse_click_handler()
        case con.WM_RBUTTONDOWN: cmb._rightMouseDownHandler(msg, wp, lp)
        case con.WM_RBUTTONUP: cmb._rightMouseUpHandler(msg, wp, lp)
        case MyMessages.RIGHT_CLICK: cmb._right_mouse_click_handler()
        case con.WM_MOUSEWHEEL: cmb._mouseWheenHandler(msg, wp, lp)
        case con.WM_MOUSEMOVE: cmb._mouseMoveHandler(msg, wp, lp)
        case con.WM_MOUSELEAVE:
            # Here, we need to do a trick. Actually, in a Combobox, when it's
            # text input mode enabled, we get two mouse leave msg & two mouse move msg
            # Because, combo's text area is an edit control. It is surrounded by the combo.
            # So, when mouse enters the combo's rect, we get a mouse move msg.
            # But when mouse enters into text box's rect, we get a mouse leave from
            # combo and mouse move from textbox. So here we are checking the mouse is
            # in combo's rect or not. If it is stil inside, we suppress the mouse leave
            # and continue receiving the mouse move msgs from text are.
            if cmb._enableInput:
                if cmb._checkMouseLeave():
                    return 1
                else:
                    cmb._mouseLeaveHandler()
            else:
                cmb._mouseLeaveHandler()

    return api.DefSubclassProc(hw, msg, wp, lp)


# Wndproc for edit control of this combo
@WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR)
def cmbEditWndProc(hw, msg, wp, lp, scID, refData):
    cmb = cmb_dict[refData]
    match msg:
        case con.WM_NCDESTROY:
            api.RemoveWindowSubclass(hw, cmbEditWndProc, scID)

        case MyMessages.EDIT_COLOR:
            if cmb._drawFlag:
                hdc = HDC(wp)
                if cmb._drawFlag & (1 << 0): api.SetTextColor(hdc, cmb._fgColor.ref )
                api.SetBkColor(hdc, cmb._bgColor.ref)
                return api.CreateSolidBrush(cmb._bgColor.ref)

        case MyMessages.LABEL_COLOR: # Not Working
            if cmb._drawFlag:
                hdc = HDC(wp)
                if cmb._drawFlag & (1 << 0): api.SetTextColor(hdc, cmb._fgColor.ref )
                api.SetBkColor(hdc, cmb._bgColor.ref)
                return api.CreateSolidBrush(cmb._bgColor.ref)


        case con.WM_KEYDOWN: cmb._keyDownHandler(wp)
        case con.WM_KEYUP: cmb._keyUpHandler(wp)
        case con.WM_CHAR: cmb._keyPressHandler(wp)
        case con.WM_LBUTTONDOWN: cmb._leftMouseDownHandler(msg, wp, lp)
        case con.WM_LBUTTONUP: cmb._leftMouseUpHandler(msg, wp, lp)
        case MyMessages.MOUSE_CLICK: cmb._mouse_click_handler()
        case con.WM_RBUTTONDOWN: cmb._mouse_click_handler(msg, wp, lp)
        case con.WM_RBUTTONUP: cmb._mouse_click_handler(msg, wp, lp)
        case MyMessages.RIGHT_CLICK: cmb._mouse_click_handler()
        case con.WM_MOUSEMOVE:
            # When mouse pointer moves from combo's rect boundary and get into edit's rect
            # we will continue the mouse move message handling.
            cmb._mouseMoveHandler(msg, wp, lp)

    return api.DefSubclassProc(hw, msg, wp, lp)
