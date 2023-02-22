# listbox module - Created on 11-Dec-2022 11:23:20

# from ctypes.wintypes import HWND, UINT, LPCWSTR
from ctypes import addressof, create_unicode_buffer, c_int
# from horology import Timing
from .control import Control
from . import constants as con
from .commons import MyMessages
from .enums import ControlType
from .events import EventArgs
from .apis import LRESULT, SUBCLASSPROC
from . import apis as api
from .colors import Color
# from datetime import datetime, date

lbx_dict = {}
lbx_style = con.WS_CHILD | con.WS_VISIBLE | con.WS_BORDER  | con.LBS_NOTIFY | con.LBS_HASSTRINGS


class ListBox(Control):

    """ListBox control """
    _count = 1
    __slots__ = ( "_has_sort", "_no_sel", "_multi_col", "_key_preview", "_use_vscroll", "_use_hscroll", "_multi_sel", "_sel_indices",
                    "_items",  "_dummy_index", "_sel_index", "on_selection_changed", "on_double_click"  )

    def __init__(self, parent, xpos: int = 10, ypos: int = 10, width: int = 150, height: int = 200) -> None:
        super().__init__()

        self._cls_name = "LISTBOX"
        self.name = f"ListBox_{ListBox._count}"
        self._ctl_type = ControlType.LIST_BOX
        self._parent = parent
        self._bg_color = Color(parent._bg_color)
        self._font = parent._font
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._is_textable = False
        self._style = lbx_style
        self._ex_style = 0
        self._has_sort = False
        self._no_sel = False
        self._multi_col = False
        self._key_preview = False
        self._use_hscroll = False
        self._use_vscroll = False
        self._multi_sel = False
        self._sel_indices = ()
        self._items = []
        self._dummy_index = -1
        self._sel_index = -1

        # Events
        self.on_selection_changed = 0
        self.on_double_click = 0

        ListBox._count += 1

# -region Public functions


    def create_handle(self):
        """Create's ListBox handle"""

        self._set_style()
        self._create_control()
        if self._hwnd:
            # print("list box hwnd ", self._hwnd)
            lbx_dict[self._hwnd] = self
            self._is_created = True
            self._set_subclass(lbx_wnd_proc)
            self._set_font_internal()

            if self._items:
                for item in self._items:
                    buff = create_unicode_buffer(item) if type(item) == str else create_unicode_buffer(str(item))
                    api.SendMessage(self._hwnd, con.LB_ADDSTRING, 0, addressof(buff))
                    if self._dummy_index > -1: api.SendMessage(self._hwnd, con.LB_SETCURSEL, self._dummy_index, 0)


    def select_all(self):
        """Select all the items in ListBox but only in multi selection mode"""
        if self._is_created and self._multi_sel:
            api.SendMessage(self._hwnd, con.LB_SETSEL, True, -1)


    def clear_selection(self):
        """Clear the selection from list box"""
        if self._is_created:
            if self._multi_sel:
                api.SendMessage(self._hwnd, con.LB_SETSEL, False, -1)
            else:
                api.SendMessage(self._hwnd, con.LB_SETCURSEL, -1, 0)


    def insert_item(self, item, index):
        """Insert an item to list box """
        if self._is_created:
            buff = create_unicode_buffer(str(item))
            api.SendMessage(self._hwnd, con.LB_INSERTSTRING, index, addressof(buff))

        if index == -1:
            self._items.append(item)
        else:
            self._items.insert(index, item)


    def remove_item(self, index):
        """Remove an item from list box"""
        if self._is_created:
            res = api.SendMessage(self._hwnd, con.LB_DELETESTRING, index, 0)
            if res != con.LB_ERR: del self._items[index]
        else:
            del self._items[index]


    def remove_all(self):
        """Remove all the items from list box"""
        if self._is_created:
            api.SendMessage(self._hwnd, con.LB_RESETCONTENT, 0, 0)
        self._items.clear()


# -endregion Public functions


    # -region private_funcs

    # Set list box styles
    def _set_style(self):
        if self._has_sort: self._style |= con.LBS_SORT
        if self._multi_sel: self._style |= con.LBS_EXTENDEDSEL | con.LBS_MULTIPLESEL
        if self._multi_col: self._style |= con.LBS_MULTICOLUMN
        if self._no_sel: self._style |= con.LBS_NOSEL
        if self._key_preview: self._style |= con.LBS_WANTKEYBOARDINPUT
        if self._use_hscroll: self._style |= con.WS_HSCROLL
        if self._use_vscroll: self._style |= con.WS_VSCROLL

    # Internal function to get an item from listbox
    def _get_item(self, index: int) -> str:
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
    def has_hscroll(self)-> bool:
        """Returns true if list box has horizontal scroll enabled"""
        return self._use_hscroll

    @has_hscroll.setter
    def has_hscroll(self, value: bool):
        """set true if list box has horizontal scroll enabled"""
        self._use_hscroll = value
    # #------------------------------------------------------------------------2

    @property
    def has_vscroll(self)-> bool:
        """Returns true if list box has vertical scroll enabled"""
        return self._use_vscroll

    @has_vscroll.setter
    def has_vscroll(self, value: bool):
        """Set true if list box has vertical scroll enabled"""
        self._use_vscroll = value
    # #------------------------------------------------------------------------3

    @property
    def selected_index(self)-> int:
        """Get the selected index from list box"""
        if self._is_created and not self._multi_sel:
            sel_ind = api.SendMessage(self._hwnd, con.LB_GETCURSEL, 0, 0)
            return sel_ind if sel_ind else -1
        return -1


    @selected_index.setter
    def selected_index(self, value: int):
        """Set the selected index of list box"""
        if self._is_created and not self._multi_sel:
            res = api.SendMessage(self._hwnd, con.LB_SETCURSEL, value, 0)
            if res != con.LB_ERR: self._sel_index = value # Fix this : We can avoid using _sel_index
        else:
            self._dummy_index = value
            self._sel_index = value
    # #------------------------------------------------------------------------4

    @property
    def selected_indices(self)-> tuple[int]:
        """Get the selected indices as a list from list box"""
        if self._multi_sel and self._is_created:
            sel_count = api.SendMessage(self._hwnd, con.LB_GETSELCOUNT, 0, 0)
            if sel_count:
                c_array = (c_int * sel_count )() # We create an array of int type
                api.SendMessage(self._hwnd, con.LB_GETSELITEMS, sel_count, addressof(c_array))
                # self._sel_indices = [item for item in c_array] # IMPROVE THIS
                self._sel_indices = tuple(c_array) # Seems better. 16 micro seconds. List's speed is 24 micro
            else:
                self._sel_indices = ()

        return self._sel_indices
    # #------------------------------------------------------------------------5

    @property
    def multi_selection(self)-> bool:
        """Returns true if this list box has multi selection enabled"""
        return self._multi_sel

    @multi_selection.setter
    def multi_selection(self, value: bool):
        """Set true if this list box has multi selection enabled"""
        self._multi_sel = value
    # #--------------------------------------------------------------------------------------------6

    @property
    def selected_item(self)-> str:
        """Returns the selected item from list box"""
        if self._is_created and not self._multi_sel:
            sel_ind = api.SendMessage(self._hwnd, con.LB_GETCURSEL, 0, 0)
            if sel_ind: return self._get_item(sel_ind)
        return ""

    @selected_item.setter
    def selected_item(self, value):
        """Set the given item as selected in list box"""
        if self._is_created and not self._multi_sel:
            api.SendMessage(self._hwnd, con.LB_SETCURSEL, value, 0)
    # #----------------------------------------------------------------------7

    @property
    def hot_index(self)-> int:
        """Returns the index of item under mouse pointer"""
        if self._is_created and self._multi_sel:
            return api.SendMessage(self._hwnd, con.LB_GETCARETINDEX, 0, 0)
    # #-------------------------------------------------------------------------8

    @property
    def selected_items(self)-> list[str]:
        """Returns the selected items as a list. Only work for multi selection list boxes"""
        if self._is_created and self._multi_sel:
            sel_count = api.SendMessage(self._hwnd, con.LB_GETSELCOUNT, 0, 0)
            if sel_count != con.LB_ERR:
                c_array = (c_int * sel_count)() # We create an array of int type
                api.SendMessage(self._hwnd, con.LB_GETSELITEMS, sel_count, addressof(c_array))
                return [self._get_item(index) for index in c_array]
        return None

    # #---------------------------------------------------------9

    @property
    def hot_item(self)-> str:
        """Returns the index of item under mouse pointer"""
        if self._is_created and self._multi_sel:
            indx = api.SendMessage(self._hwnd, con.LB_GETCARETINDEX, 0, 0)
            if indx: return self._get_item(indx)
        return ""

    # -endregion Properties

# End ListBox

@SUBCLASSPROC
def lbx_wnd_proc(hw, msg, wp, lp, scID, refData) -> LRESULT:
    # printWinMsg(msg)
    lbx = lbx_dict[hw]
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, lbx_wnd_proc, scID)
            del lbx_dict[hw]

        case MyMessages.LIST_COLOR:
            if lbx._draw_flag:
                api.SetBkMode(wp, 1)
                if lbx._draw_flag & 1: api.SetTextColor(wp, lbx._fg_color.ref)
                if lbx._draw_flag & 2:
                    return api.CreateSolidBrush(lbx._bg_color.ref)
                else:
                    return api.GetStockObject(con.DC_BRUSH)

        case MyMessages.CTL_COMMAND:
            ncode = api.HIWORD(wp)
            match ncode:
                case con.LBN_DBLCLK:
                    if lbx.on_double_click: lbx.on_double_click(lbx, EventArgs())
                case con.LBN_SELCHANGE:
                    if lbx.on_selection_changed: lbx.on_selection_changed(lbx, EventArgs())

        case con.WM_SETFOCUS: lbx._got_focus_handler()
        case con.WM_KILLFOCUS: lbx._lost_focus_handler()
        case con.WM_LBUTTONDOWN: lbx._left_mouse_down_handler(msg, wp, lp)
        case con.WM_LBUTTONUP: lbx._left_mouse_up_handler(msg, wp, lp)
        case MyMessages.MOUSE_CLICK: lbx._mouse_click_handler()
        case con.WM_RBUTTONDOWN: lbx._right_mouse_down_handler(msg, wp, lp)
        case con.WM_RBUTTONUP: lbx._right_mouse_up_handler(msg, wp, lp)
        case MyMessages.RIGHT_CLICK: lbx._right_mouse_click_handler()
        case con.WM_MOUSEWHEEL: lbx._mouse_wheel_handler(msg, wp, lp)
        case con.WM_MOUSEMOVE: lbx._mouse_move_handler(msg, wp, lp)
        case con.WM_MOUSELEAVE: lbx._mouse_leave_handler()

    return api.DefSubclassProc(hw, msg, wp, lp)