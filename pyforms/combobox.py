
# Created on 24-Nov-2022 05:00:20

from ctypes.wintypes import HWND, UINT, HDC
from ctypes import WINFUNCTYPE, byref, sizeof, addressof, create_unicode_buffer
# import ctypes as ctp

from .control import Control
from . import constants as con
from .commons import MyMessages, get_mousepos_on_msg, point_in_rect
from .enums import ControlType
from .events import EventArgs
# from .apis import DefSubclassProc, RemoveWindowSubclass, COMBOBOXINFO, SetWindowSubclass, SendMessage
from .apis import LRESULT, UINT_PTR, DWORD_PTR, RECT, COMBOBOXINFO, WPARAM, LPARAM
# from .apis import LRESULT, SetBkColor, SetTextColor
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
    __slots__ = ( "_once_created", "_items", "_vis_tem_count", "_sel_index", "_recreate_enabled", "_old_hwnd",
                    "_enable_input", "_fg_color", "_bg_color",
                    "on_selection_committed", "on_list_closed", "on_list_opened", "on_text_updated", "on_text_changed",
                    "on_selection_changed", "on_selection_cancelled"  )

    def __init__(self, parent, xpos: int = 10, ypos: int = 10, width: int = 120, height: int = 30) -> None:
        super().__init__()
        self._cls_name = "ComboBox"
        self.name = f"ComboBox_{ComboBox._count}"
        self._ctl_type = ControlType.COMBO_BOX
        self._parent = parent
        self._bg_color = Color(parent._bg_color)
        self._font = parent._font
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        # self._is_textable = True
        self._style = cmb_style
        self._ex_style = 0x00000200
        self._once_created = False
        self._items = []
        self._vis_tem_count = 0
        self._sel_index = -1
        self._recreate_enabled = False
        self._old_hwnd = 0
        self._enable_input = False

        # Events
        self.on_selection_cancelled = 0
        self.on_selection_changed = 0
        self.on_text_changed = 0
        self.on_text_updated = 0
        self.on_list_opened = 0
        self.on_list_closed = 0
        self.on_selection_committed = 0

        ComboBox._count += 1
        # print("combo's init back color ref ", self._bg_color.ref)

    # Create's combo box handle
    def create_handle(self):

        """Create's combo box handle"""

        if not self._is_created:
            self._set_ctl_id()
            self._set_style()
        else:
            del cmb_dict[self._hwnd]

        self._hwnd = api.CreateWindowEx(  self._ex_style,
                                        self._cls_name,
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
            if not self._is_created:
                self._is_created = True

            self._set_subclass(cmb_wnd_proc)
            self._set_font_internal()
            self._get_combo_info()
            self._insert_items()
            if self._sel_index > -1: api.SendMessage(self._hwnd, con.CB_SETCURSEL, self._sel_index, 0)

    # -region private_funcs

    def _set_style(self):
        if self._enable_input:
            self._style |= con.CBS_DROPDOWN
        else:
            self._style |= con.CBS_DROPDOWNLIST

    def _get_combo_info(self):
        ci = COMBOBOXINFO()
        ci.cbSize = sizeof(COMBOBOXINFO)
        ciPtr = addressof(ci)
        api.SendMessage(self._hwnd, con.CB_GETCOMBOBOXINFO, 0, ciPtr)
        self.parent._combo_dict[ci.hwndList] = self._hwnd  # Putting list hwnd in form's special dict.
        # cmb_tb_dict[ci.hwndItem] = self
        api.SetWindowSubclass(ci.hwndItem, cmb_edit_wnd_proc, ComboBox._tb_subcls_id, self._hwnd)
        ComboBox._tb_subcls_id += 1
        # print("combo hwndItem - ", ci.hwndItem)

    def _insert_items(self):
        if self._items:
            for item in self._items:
                sitem = item if isinstance(item, str) else str(item)
                buff = create_unicode_buffer(sitem)
                api.SendMessage(self._hwnd, con.CB_ADDSTRING, 0, addressof(buff))

    def _checkMouseLeave(self):
        rc = RECT()
        api.GetWindowRect(self._hwnd, byref(rc))
        p = get_mousepos_on_msg()
        return point_in_rect(rc, p)


    # -endregion

    # -region Properties

    @property
    def items(self): return self._items

    @property
    def item_count(self): return len(self._items)

    @property
    def selected_index(self):
        if self._is_created: return api.SendMessage(self._hwnd, con.CB_GETCURSEL, 0, 0)
        return -1


    @selected_index.setter
    def selected_index(self, value):
        self._sel_index = value
        if self._is_created: api.SendMessage(self._hwnd, con.CB_SETCURSEL, value, 0)

    @property
    def enable_input(self): return self._enable_input

    @enable_input.setter
    def enable_input(self, value: bool):
        if self._is_created:
            if self._enable_input != value:
                if value:
                    self._style ^= con.CBS_DROPDOWNLIST
                    self._style |= con.CBS_DROPDOWN
                else:
                    self._style ^= con.CBS_DROPDOWN
                    self._style |= con.CBS_DROPDOWNLIST

                self._enable_input = value
                # del cmb_dict[self._hwnd] # We need to remove this combo from dict.
                api.DestroyWindow(self._hwnd) # Destroy this and create new one.
                self.create_handle()
        else:
            self._enable_input = value


    # -endregion props


    # -region pub_func
    def add_item(self, item):
        self._items.append(item)
        if self._is_created:
            sitem = item if isinstance(item, str) else str(item)
            buff = create_unicode_buffer(sitem)
            api.SendMessage(self._hwnd, con.CB_ADDSTRING, 0, addressof(buff))


    def add_items(self, *args):
        self._items.extend(args)
        if self._is_created:
            for item in args:
                sitem = item if isinstance(item, str) else str(item)
                buff = create_unicode_buffer(sitem)
                api.SendMessage(self._hwnd, con.CB_ADDSTRING, 0, addressof(buff))



    def remove_item_at(self, index):
        if index in range(len(self._items)):
            item = self._items[index]
            sitem = item if isinstance(item, str) else str(item)
            create_unicode_buffer(sitem)
            cIndex = api.SendMessage(self._hwnd, con.CB_FINDSTRING, -1, addressof(item))
            if cIndex > -1 :
                api.SendMessage(self._hwnd, con.CB_DELETESTRING, cIndex, 0)
                del self._items[index]


    def remove_item(self, item):
        if self._items.__contains__(item):
            sitem = item if isinstance(item, str) else str(item)
            buff = create_unicode_buffer(sitem)
            cIndex = api.SendMessage(self._hwnd, con.CB_FINDSTRING, -1, addressof(buff))
            if cIndex > -1 :
                api.SendMessage(self._hwnd, con.CB_DELETESTRING, cIndex, 0)
                self._items.remove(item)
        else:
            print("item is not in list")


    def remove_items(self, *args):
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

    def clear_items(self):
        if self._items:
            del self._items[:]
            api.SendMessage(self._hwnd, con.CB_DELETESTRING, 0, 0)


    # -endregion

    def dumm(self): pass

#End ComboBox




@WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR)
def cmb_wnd_proc(hw, msg, wp, lp, scID, refData):
    # printWinMsg(msg)
    cmb = cmb_dict[hw]
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, cmb_wnd_proc, scID)
            # print("remove subclass for - ", cmb.name)

        # case con.WM_CTLCOLOREDIT:
        #     print("combo ctl edit")

        # case con.CB_SHOWDROPDOWN:
        #     print("combo CB_SHOWDROPDOWN")

        case MyMessages.LIST_COLOR:
            if cmb._draw_flag:
                # print("combo list clr")
                hdc = HDC(wp)
                if cmb._draw_flag & 1: api.SetTextColor(hdc, cmb._fg_color.ref )
                api.SetBkColor(hdc, cmb._bg_color.ref)
                return api.CreateSolidBrush(cmb._bg_color.ref)

        case MyMessages.CTL_COMMAND:
            ncode = api.HIWORD(wp)
            match ncode:
                case con.CBN_SELCHANGE:
                    if cmb.on_selection_changed: cmb.on_selection_changed(cmb, EventArgs())
                case con.CBN_EDITCHANGE:
                    if cmb.on_text_changed: cmb.on_text_changed(cmb, EventArgs())
                case con.CBN_EDITUPDATE:
                    if cmb.on_text_updated: cmb.on_text_updated(cmb, EventArgs())
                case con.CBN_DROPDOWN:
                    if cmb.on_list_opened: cmb.on_list_opened(cmb, EventArgs())
                case con.CBN_CLOSEUP:
                    if cmb.on_list_closed: cmb.on_list_closed(cmb, EventArgs())
                case con.CBN_SELENDOK:
                    if cmb.on_selection_committed: cmb.on_selection_committed(cmb, EventArgs())
                case con.CBN_SELENDCANCEL:
                    if cmb.on_selection_cancelled: cmb.on_selection_cancelled(cmb, EventArgs())

        case con.WM_SETFOCUS: cmb._got_focus_handler()
        case con.WM_KILLFOCUS: cmb._lost_focus_handler()
        case con.WM_LBUTTONDOWN: cmb._left_mouse_down_handler(msg, wp, lp)
        case con.WM_LBUTTONUP: cmb._left_mouse_up_handler(msg, wp, lp)
        case MyMessages.MOUSE_CLICK: cmb._mouse_click_handler()
        case con.WM_RBUTTONDOWN: cmb._right_mouse_down_handler(msg, wp, lp)
        case con.WM_RBUTTONUP: cmb._right_mouse_up_handler(msg, wp, lp)
        case MyMessages.RIGHT_CLICK: cmb._right_mouse_click_handler()
        case con.WM_MOUSEWHEEL: cmb._mouse_wheel_handler(msg, wp, lp)
        case con.WM_MOUSEMOVE: cmb._mouse_move_handler(msg, wp, lp)
        case con.WM_MOUSELEAVE:
            # Here, we need to do a trick. Actually, in a Combobox, when it's
            # text input mode enabled, we get two mouse leave msg & two mouse move msg
            # Because, combo's text area is an edit control. It is surrounded by the combo.
            # So, when mouse enters the combo's rect, we get a mouse move msg.
            # But when mouse enters into text box's rect, we get a mouse leave from
            # combo and mouse move from textbox. So here we are checking the mouse is
            # in combo's rect or not. If it is stil inside, we suppress the mouse leave
            # and continue receiving the mouse move msgs from text are.
            if cmb._enable_input:
                if cmb._checkMouseLeave():
                    return 1
                else:
                    cmb._mouse_leave_handler()
            else:
                cmb._mouse_leave_handler()

    return api.DefSubclassProc(hw, msg, wp, lp)


@WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR)
def cmb_edit_wnd_proc(hw, msg, wp, lp, scID, refData):
    cmb = cmb_dict[refData]
    # printWinMsg(msg)
    match msg:
        case con.WM_NCDESTROY:
            api.RemoveWindowSubclass(hw, cmb_edit_wnd_proc, scID)
            print("remove subclass for ComboBox's text box -", hw)

        case MyMessages.EDIT_COLOR:
            if cmb._draw_flag:
                hdc = HDC(wp)
                if cmb._draw_flag & (1 << 0): api.SetTextColor(hdc, cmb._fg_color.ref )
                api.SetBkColor(hdc, cmb._bg_color.ref)
                return api.CreateSolidBrush(cmb._bg_color.ref)

        case MyMessages.LABEL_COLOR: # Not Working
            if cmb._draw_flag:
                # print("dra stsrt")
                # ret = api.DefSubclassProc(hw, msg, wp, lp)
                hdc = HDC(wp)
                if cmb._draw_flag & (1 << 0): api.SetTextColor(hdc, cmb._fg_color.ref )
                api.SetBkColor(hdc, cmb._bg_color.ref)
                return api.CreateSolidBrush(cmb._bg_color.ref)


        case con.WM_KEYDOWN: cmb._key_down_handler(wp)
        case con.WM_KEYUP: cmb._key_up_handler(wp)
        case con.WM_CHAR: cmb._key_press_handler(wp)
        case con.WM_LBUTTONDOWN: cmb._left_mouse_down_handler(msg, wp, lp)
        case con.WM_LBUTTONUP: cmb._left_mouse_up_handler(msg, wp, lp)
        case MyMessages.MOUSE_CLICK: cmb._mouse_click_handler()
        case con.WM_RBUTTONDOWN: cmb._mouse_click_handler(msg, wp, lp)
        case con.WM_RBUTTONUP: cmb._mouse_click_handler(msg, wp, lp)
        case MyMessages.RIGHT_CLICK: cmb._mouse_click_handler()
        case con.WM_MOUSEMOVE:
            # When mouse pointer moves from combo's rect boundary and get into edit's rect
            # we will continue the mouse move message handling.
            cmb._mouse_move_handler(msg, wp, lp)


    return api.DefSubclassProc(hw, msg, wp, lp)