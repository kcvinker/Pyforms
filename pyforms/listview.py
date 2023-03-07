

# listview module - Created on 02-Jan-2023 21:21:20

import typing
from enum import Enum
from ctypes.wintypes import HWND, UINT, DWORD
from ctypes import POINTER, WINFUNCTYPE, byref, addressof, cast, create_unicode_buffer, c_wchar_p, pointer
from .control import Control

from . import constants as con
from .commons import Font, MyMessages, getMousePoints
from .enums import ControlType, TextAlignment, ListViewStyle
from .events import EventArgs
from .apis import LRESULT, UINT_PTR, DWORD_PTR, RECT, LPNMCUSTOMDRAW, LVCOLUMNW, LPLVCOLUMNW, WPARAM, LPARAM, SUBCLASSPROC
from . import apis as api
from .colors import Color
from .winmsgs import log_msg
from horology import Timing

lv_dict = {}
hdr_dict = {}
lv_style = con.WS_CHILD | con.WS_VISIBLE | con.LVS_ALIGNLEFT| con.LVS_EDITLABELS | con.WS_BORDER
LV_VIEW_ICON            = 0x0000
LV_VIEW_DETAILS         = 0x0001
LV_VIEW_SMALLICON       = 0x0002
LV_VIEW_LIST            = 0x0003
LV_VIEW_TILE            = 0x0004
LV_VIEW_MAX             = 0x0004
HDI_FORMAT = 0x0004
HDF_OWNERDRAW = 0x8000
ITEM_POSTPAINT = (con.CDDS_SUBITEM | con.CDDS_ITEMPOSTPAINT) - 1

# ListViewColumn = typing.TypeVar("ListViewColumn")
# ListViewItem = typing.TypeVar("ListViewItem")
# Form = typing.TypeVar("Form")
SKIPDEFAULT_DRAW = typing.TypeVar("SKIPDEFAULT_DRAW")
HDR_CUST_DRAW = 7500
class ColAndIndex:
    def __init__(self, indx: int, col: LVCOLUMNW) -> None:
        self.index = indx
        self.lvc = col

class ListView(Control):

    """ListView control """
    Control.icc.init_comm_ctls(con.ICC_LISTVIEW_CLASSES)
    _count = 1
    __slots__ = ("_sel_index", "_sel_item", "_edit_label", "_lbl_hwnd", "_hdr_hwnd", "_item_top_align",
					"_hide_sel", "_multi_sel", "_check_box", "_full_row_sel", "_show_grid", "_one_click_act", "_hot_track_sel",
					"_no_hdr", "_change_hdr_height", "_hdr_draw_font", "_set_cb_last", "_cb_is_last", "_cb_checked",
					"_hdr_font", "_col_align", "_view_style", "_columns", "_items", "_col_ind_list", "_col_index",
                    "_hdr_height", "_sel_item_index", "sel_sub_index", "_img_list", "_hdr_item_dict", "_hdr_pts", "_mouse_on_hdr",
                    "_hdr_bg_color", "_hdr_fg_color", "_hdr_bk_brush", "_hdr_odraw", "_hot_hdr", "_col_index",
                    "_hdr_hot_brush", "_hdr_clickable", "_selectable", "_item_index", "_item_drawn", "_destroyCount", "_layCount" )

    def __init__(self, parent, xpos: int = 10, ypos: int = 10, width: int = 250, height: int = 200) -> None:
        super().__init__()

        self._cls_name = "SysListView32"
        self.name = f"ListView_{ListView._count}"
        self._ctl_type = ControlType.LIST_VIEW
        self._parent = parent
        self._bg_color = Color(0xFFFFFF)
        self._fg_color = Color(0x000000)
        self._font = parent._font
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._is_textable = False
        self._style = lv_style
        self._ex_style = 0
        self._text = ""

        self._columns = []
        self._items = []
        self._col_ind_list = []
        self._view_style = ListViewStyle.REPORT_VIEW # Ideal for most common use cases
        self._show_grid = True
        self._full_row_sel = True
        self._edit_label = False
        self._hide_sel = True
        self._no_hdr = False
        self._multi_sel = False
        self._check_box = False
        self._one_click_act = True
        self._hot_track_sel = False
        self._cb_is_last = False
        self._hdr_pts = api.POINT()
        self._mouse_on_hdr = False
        self._hdr_bg_color = Color(0xb3cccc)
        self._hdr_fg_color = Color(0x000000)
        self._hdr_clickable = True
        self._hdr_font = parent._font # Font("Tahoma", 11, FontWeight.BOLD)
        self._selectable = False
        self._item_index = -1
        self._item_drawn = -1
        self._hdr_odraw = False
        self._change_hdr_height = True
        self._hdr_height = 25
        self._hot_hdr = -1
        self._col_index = 0
        self._destroyCount = 0
        self._layCount = 0

        # Events
        # self.on_value_changed = 0
        # self.on_dragging = 0
        # self.on_dragged = 0


        ListView._count += 1


# -region Public functions

    def create_handle(self):
        """Create's ListView handle"""
        # self._parent.lv_func = self.lv_wmnotify_handler
        self._set_lv_style()
        self._create_control()
        if self._hwnd:
            # self._parent.lv_hwnd = self._hwnd
            self._set_lv_exstyle()
            lv_dict[self._hwnd] = self
            self._set_subclass(lv_wnd_proc)
            self._set_font_internal()

            if self._columns:
                for col in self._columns:
                    api.SendMessage(self._hwnd, con.LVM_INSERTCOLUMNW, col.index, addressof(col.lvc))

            self._hdr_hwnd = api.SendMessage(self._hwnd, con.LVM_GETHEADER, 0, 0)
            # hdr_dict[self._hdr_hwnd] = self # Put ourself inside this dict so that we can appear in hdr_wnd_proc
            if not self._hdr_font.handle: self._hdr_font.create_handle(self._hdr_hwnd)# Making sure header font is ready.
            #
            # We are going to send the list view hwnd with this function. So, we can grab it inside
            # header's wndproc function.
            api.SetWindowSubclass(self._hdr_hwnd, hdr_wnd_proc, ListView._count, self._hwnd)
            if self._bg_color != self._parent._bg_color:
                api.SendMessage(self._hwnd, con.LVM_SETBKCOLOR, 0, self._bg_color.ref)

            if self._cb_is_last:
                ord_list = self._change_column_order()
                api.SendMessage(self._hwnd, con.LVM_SETCOLUMNORDERARRAY, len(ord_list), addressof(ord_list))
                self._cb_is_last = True


    #End of Create function-----------------------------------------------




    def add_column_ex(self, lvc):
        self._add_column_internal(lvc)


    def add_column(self, txt: str, width: int = 100, image_index: int = -1):
        col = ListViewColumn(txt, width, image_index)
        self._add_column_internal(col)


    def add_columns(self, col_names: list[str], col_widths: list[int]):
        if len(col_names) != len(col_widths):
            raise Exception("Length of column names & column widths are not equal")
        for (name, width) in zip(col_names, col_widths):
            col = ListViewColumn(name, width)
            self._add_column_internal(col)


    def add_row(self, *items):
        if self._view_style != ListViewStyle.REPORT_VIEW: raise Exception("Adding row is possible only in ListViewStyle.REPORT_VIEW")
        if not self._is_created: raise Exception("Adding  row is possible only after ListView's handle created")
        if not items: raise Exception("items is not iterable")

        lvi = ListViewItem(items[0])
        self._add_item_internal(lvi)
        for i in range(1, len(items)):
            self._add_subitem_internal(items[i], lvi._index, i)










# -endregion Public functions


    # -region private_funcs

    def _set_lv_style(self):
        # Setup different listview styles as per user's selection
        match self._view_style:
            case ListViewStyle.LARGE_ICON: self._style |= con.LVS_ICON
            case ListViewStyle.REPORT_VIEW: self._style |= con.LVS_REPORT
            case ListViewStyle.SMALL_ICON: self._style |= con.LVS_SMALLICON
            case ListViewStyle.LIST_VIEW: self._style |= con.LVS_LIST
        # print(self._view_style, " self._view_style")

        # Set some more styles...
        if self._edit_label: self._style |= con.LVS_EDITLABELS
        if self._hide_sel: self._style ^= con.LVS_SHOWSELALWAYS
        if self._no_hdr: self._style |= con.LVS_NOCOLUMNHEADER
        if self._multi_sel: self._style ^= con.LVS_SINGLESEL

        # Set some brushes
        self._hdr_bk_brush = api.CreateSolidBrush(self._hdr_bg_color.ref)
        self._hdr_hot_brush = self._hdr_bg_color.get_hot_brush(1.5)


    def _set_lv_exstyle(self):
        # Setup the different ex styles for this list view
        lv_ex_style = 0x0000
        if self._show_grid: lv_ex_style |= con.LVS_EX_GRIDLINES
        if self._check_box: lv_ex_style |= con.LVS_EX_CHECKBOXES
        if self._full_row_sel: lv_ex_style |= con.LVS_EX_FULLROWSELECT
        if self._one_click_act: lv_ex_style |= con.LVS_EX_ONECLICKACTIVATE
        if self._hot_track_sel: lv_ex_style |= con.LVS_EX_TRACKSELECT
        # if self._view_style == ListViewStyle.TILE_VIEW: api.SendMessage(self._hwnd, con.LVM_SETVIEW, 0x0004, 0)
        api.SendMessage(self._hwnd, con.LVM_SETEXTENDEDLISTVIEWSTYLE, 0 , lv_ex_style)


    def lv_wmnotify_handler(self, lpm):
        nmh = cast(lpm, api.LPNMHDR).contents
        # print(nmh.code, " LV notify ", con.NM_CUSTOMDRAW )
        match nmh.code:
            case con.NM_CUSTOMDRAW:
                # if lv._cust_draw:
                lvcd = cast(lpm, api.LPNMLVCUSTOMDRAW).contents
                # print(f"{lvcd.nmcd.dwDrawStage & con.CDDS_ITEMPREPAINT = }, {con.CDDS_ITEMPREPAINT = }")
                match lvcd.nmcd.dwDrawStage:
                    case con.CDDS_PREPAINT:
                        return con.CDRF_NOTIFYITEMDRAW

                    case con.CDDS_ITEMPREPAINT:
                        # print("prepaint")
                        lvcd.clrTextBk = self._bg_color.ref
                        return con.CDRF_NEWFONT | con.CDRF_DODEFAULT

        return con.CDRF_DODEFAULT


    def _change_column_order(self):
        # If user wants to swap the first and last columns, we can use this.
        indices = []
        for lc in self._columns:
            if lc.index > 0: indices.append(lc.index)
        indices.append(0)
        return indices


    def _add_column_internal(self, lvcol):
        lvcol.index = self._col_index
        lvc = LVCOLUMNW()
        lvc.mask = con.LVCF_TEXT  | con.LVCF_WIDTH | con.LVCF_FMT | con.LVCF_SUBITEM
        lvc.fmt = lvcol.text_align.value
        lvc.cx = lvcol.width
        lvc.pszText = cast(create_unicode_buffer(lvcol.text), c_wchar_p)
        # lvc.iOrder = lvcol.index

        if lvcol.has_image:
            lvc.mask |= con.LVCF_IMAGE
            lvc.fmt |= con.LVCFMT_COL_HAS_IMAGES | con.LVCFMT_IMAGE
            lvc.iImage = lvcol.img_index
            if lvcol.img_on_right: lvc.fmt |= con.LVCFMT_BITMAP_ON_RIGHT

        lvcol.lvc = lvc
        if self._is_created:
            api.SendMessage(self._hwnd, con.LVM_INSERTCOLUMNW, lvcol.index, addressof(lvc))


        self._columns.append(lvcol)
        self._col_index += 1


    def _add_item_internal(self, item):
        lvi = api.LVITEMW()
        lvi.mask = con.LVIF_TEXT | con.LVIF_PARAM | con.LVIF_STATE
        if item._img_index != -1: lvi.mask |= con.LVIF_IMAGE
        lvi.state = 0
        lvi.stateMask = 0
        lvi.iItem = item._index
        lvi.iSubItem = 0
        lvi.iImage = item._img_index
        lvi.pszText = cast(create_unicode_buffer(item.text), c_wchar_p)
        lvi.cchTextMax = len(item._text) + 1
        # lvi.lParam = id(item)
        api.SendMessage(self._hwnd, con.LVM_INSERTITEMW, 0, addressof(lvi))
        self._items.append(item)


    def _add_subitem_internal(self, subitem: str, item_index: int, sub_index: int, img_index: int = -1):

        sitem = subitem if isinstance(subitem, str) else str(subitem)
        lvi = api.LVITEMW()
        # lvi.mask = con.LVIF_TEXT | con.LVIF_STATE
        # lvi.iItem = item_index
        lvi.iSubItem = sub_index
        lvi.pszText = cast(create_unicode_buffer(sitem), c_wchar_p)
        lvi.iImage = img_index
        api.SendMessage(self._hwnd, con.LVM_SETITEMTEXTW, item_index, addressof(lvi))
        self._items[item_index]._subitems.append(sitem) # Put the subitem in our item's bag.


    def _draw_headers(self, nmcd: LPNMCUSTOMDRAW) -> int:
        # Windows's own header drawing is white bkg color.
        # But listview itself is white bkg. We can't allow both hdr & listview in white.
        # So, we need to draw it on our own.
        if nmcd.dwItemSpec != 0: nmcd.rc.left += 1 # Give room for header divider.
        col = self._columns[nmcd.dwItemSpec] # Get our column class
        api.SetBkMode(nmcd.hdc, con.TRANSPARENT)

        if nmcd.uItemState & con.CDIS_SELECTED:
            api.FillRect(nmcd.hdc, byref(nmcd.rc), self._hdr_bk_brush)
        else:
            # We will draw with a different color if mouse is over this hdr.
            if nmcd.dwItemSpec == self._hot_hdr:
                api.FillRect(nmcd.hdc, byref(nmcd.rc), self._hdr_hot_brush)
            else:
                api.FillRect(nmcd.hdc, byref(nmcd.rc), self._hdr_bk_brush)

        api.SelectObject(nmcd.hdc, self._hdr_font.handle)
        api.SetTextColor(nmcd.hdc, self._hdr_fg_color.ref)
        if self._hdr_clickable and nmcd.uItemState & con.CDIS_SELECTED:
            # We are mimicing the dotnet listview header's nature here.
            # They did not resize the overall header item. They just reduce...
            # it for drawing text. That means, text is drawing in a small rect.
            # Thus, viewer thinks like header is pressed a little bit.
            nmcd.rc.left += 2
            nmcd.rc.top += 2

        api.DrawText(nmcd.hdc, col.text, -1, byref(nmcd.rc), col._hdr_txt_flag )


    #------------------------------------------End

    # def _draw_hdrs_last_part(self):

    #     hrc = RECT()
    #     api.SendMessage(self._hdr_hwnd, con.HDM_GETITEMRECT, len(self._columns) - 1, addressof(hrc))
    #     rc = RECT(hrc.right + 1, hrc.top, self.width, hrc.bottom)
    #     hdc = api.GetDC(self._hwnd)
    #     api.FillRect(hdc, byref(rc), self._hdr_bk_brush)
    #     api.ReleaseDC(self._hwnd, hdc)


    # def _is_mouse_on_hdr(self, rc): Useless
    #     pt = api.POINT()
    #     api.GetCursorPos(byref(pt))
    #     api.ScreenToClient(self._parent._hwnd, byref(pt))
    #     rc = rECT(self._xpos + rc.left, self._ypos + rc.top,
    #                     rc.right + self._xpos, rc.bottom + self._ypos)
    #     return api.PtInRect(byref(rc), pt)



    # -endregion Private funcs

    # -region Properties

    @property
    def header_visual_style(self)-> int:
        """Get the range beetween minimum & maximum values"""
        return self._hdr_odraw

    @header_visual_style.setter
    def header_visual_style(self, value: int):
        """Set or get the header back color"""
        self._hdr_odraw = value
        if self._columns: self._make_hdr_owner_draw()

    #------------------------------------------------------------------------2 Header Back Color


    @property
    def header_height(self)-> int:
        """Get the header height."""
        return self._hdr_height

    @header_height.setter
    def header_height(self, value: int):
        """Set the header height."""
        self._hdr_height = value
    #------------------------------------------------------------------------2 Header Height





    # -endregion Properties
    x = 100 # Dummy line


# End ListView


class ColumnAlign(Enum):
    LEFT = 0
    RIGHT = 1
    CENTER = 2



class ListViewColumn:

    """Class for representing ListView Column"""

    __slots__ = ("_draw_need", "_is_hot_item", "text", "width", "index", "img_index", "_order", "_hdr_txt_flag",
                "_bg_color", "_fg_color", "img_on_right", "text_align", "_hdr_txt_align", "lvc")

    def __init__(self, hdr_txt: str, width: int, img:int = -1, img_right: bool = False) -> None:
        self.text = hdr_txt
        self.width = width
        self.img_index = img
        self.img_on_right = img_right
        self.text_align = ColumnAlign.LEFT
        self.index = -1
        self._hdr_txt_align = ColumnAlign.CENTER
        self._is_hot_item = False
        self._hdr_txt_flag = con.DT_SINGLELINE | con.DT_VCENTER | con.DT_CENTER | con.DT_NOPREFIX


    # @property
    # def index(self): return self._index

    @property
    def has_image(self): return self.img_index > -1

    @property
    def header_text_align(self): return self._hdr_txt_align

    @header_text_align.setter
    def header_text_align(self, value: TextAlignment):
        self._hdr_txt_align = value
        match value:
            case ColumnAlign.LEFT:
                self._hdr_txt_flag = con.DT_SINGLELINE | con.DT_VCENTER | con.DT_LEFT | con.DT_NOPREFIX
            case ColumnAlign.RIGHT:
                self._hdr_txt_flag = con.DT_SINGLELINE | con.DT_VCENTER | con.DT_RIGHT | con.DT_NOPREFIX
            case ColumnAlign.CENTER:
                self._hdr_txt_flag = con.DT_SINGLELINE | con.DT_VCENTER | con.DT_CENTER | con.DT_NOPREFIX


# End of ListViewColumn class=====================================================

class ListViewItem:
    _slots_ = ("_text", "_bg_color", "_fg_color", "_img_index", "_index", "_font", "_subitems")
    _stindex = 0

    def __init__(self, txt: str, bg_color: int = 0xFFFFFF, fg_color: int = 0x000000, img_index: int = -1) -> None:
        self._text = str(txt)
        self._bg_color = bg_color
        self._fg_color = fg_color
        self._img_index = img_index
        self._font = Font() # Start with default font Tahoma, 11 point
        self._index = ListViewItem._stindex
        self._subitems = []
        ListViewItem._stindex += 1

    @property
    def text(self): return self._text

    @text.setter
    def text(self, value: str):
        self._text = value





#/////////////////////////////////////////////////////////////////////////////////////
#//             Window Procedure, All actions are happening here                    //
#/////////////////////////////////////////////////////////////////////////////////////
# @WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR)
@SUBCLASSPROC
def lv_wnd_proc(hw, msg, wp, lp, scID, refData) -> LRESULT:
    # log_msg(msg)
    lv = lv_dict[hw]
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, lv_wnd_proc, scID)
            lv._destroyCount += 1
            if lv._destroyCount == 2: del lv_dict[hw]


        case MyMessages.CTRL_NOTIFY:
            nmh = cast(lp, api.LPNMHDR).contents
        #     print(nmh.code, " LV notify ", con.NM_CUSTOMDRAW )
            match nmh.code:
        # #         # case con.LVN_ITEMCHANGED:
        # #         #     print("LVN_ITEMCHANGED ", con.LVN_ITEMCHANGED)
        # #         # case 4294967195:
        # #         #     print("actual")

                case con.NM_CLICK:pass
                    # print("nm click ", con.LVN_ITEMCHANGING)
                    # nia = cast(lp, api.LPNMITEMACTIVATE).contents
                    # # print(nia, " on nm click")
                    # lv._item_index = nia.iItem
                    # lv._selectable = True
                    # api.InvalidateRect(hw, None, False)
                    # api.SendMessage(hw, con.LVM_SETSELECTIONMARK, 0, nia.iItem)
                case con.NM_SETFOCUS:pass
                    # print("NM_SETFOCUS = NM_FIRST - 7")

                case con.NM_CUSTOMDRAW:
                    lvcd = cast(lp, api.LPNMLVCUSTOMDRAW).contents
                    # print(lvcd.nmcd.dwDrawStage, con.CDDS_SUBITEM | con.CDDS_ITEMPOSTPAINT)
                    match lvcd.nmcd.dwDrawStage:
                        case con.CDDS_PREPAINT:
                            return con.CDRF_NOTIFYITEMDRAW

                        case con.CDDS_ITEMPREPAINT:
                            lvcd.clrTextBk = lv._bg_color.ref
                            lvcd.clrText = lv._fg_color.ref
                            return con.CDRF_NEWFONT | con.CDRF_DODEFAULT



                        # case ITEM_POSTPAINT :
                        #     # print(lvcd.iSubItem)
                        #     return con.CDRF_DODEFAULT
                        #     print(f"{lvcd.iSubItem = }, {lvcd.dwItemType = }, {lvcd.iPartId = }, {lvcd.iStateId = }")
                        #     lv._item_drawn += 1

                        #     if lv._selectable:
                        #         # print(f"{lv._item_drawn = }, {lv._item_index = }")
                        #         if lv._item_drawn == lv._item_index:
                        #             lv._selectable = False
                        #             lvcd.clrTextBk = 0x0066FF99
                        #         else:
                        #             lvcd.clrTextBk = lv._bg_color.ref
                        #     else:
                        #         lvcd.clrTextBk = lv._bg_color.ref
                        #     if lv._item_drawn == len(lv._items) - 1: lv._item_drawn = -1
                        #     return con.CDRF_NEWFONT | con.CDRF_DODEFAULT
                    return con.CDRF_DODEFAULT
                case _: return 0


        case con.WM_NOTIFY:
            nmh = cast(lp, api.LPNMHDR).contents
            if nmh.code == con.NM_CUSTOMDRAW:
                nmcd = cast(lp, api.LPNMCUSTOMDRAW).contents
                # print(f"{nmcd.dwDrawStage = }, {con.CDDS_ITEMPOSTERASE = }")
                match nmcd.dwDrawStage:
                    case con.CDDS_PREPAINT: return con.CDRF_NOTIFYITEMDRAW
                    case con.CDDS_ITEMPREPAINT:
    #                   # We are taking the opprtunity to draw the headers from Control
                        lv._draw_headers(nmcd)
                        return con.CDRF_SKIPDEFAULT

        case con.WM_SETFOCUS: lv._got_focus_handler()
        case con.WM_KILLFOCUS: lv._lost_focus_handler()
        case con.WM_LBUTTONDOWN: lv._left_mouse_down_handler(msg, wp, lp)
        case con.WM_LBUTTONUP: lv._left_mouse_up_handler(msg, wp, lp)
        case MyMessages.MOUSE_CLICK: lv._mouse_click_handler()
        case con.WM_RBUTTONDOWN: lv._right_mouse_down_handler(msg, wp, lp)
        case con.WM_RBUTTONUP: lv._right_mouse_up_handler(msg, wp, lp)
        case MyMessages.RIGHT_CLICK: lv._right_mouse_click_handler()
        case con.WM_MOUSEWHEEL: lv._mouse_wheel_handler(msg, wp, lp)
        case con.WM_MOUSEMOVE: lv._mouse_move_handler(msg, wp, lp)
        case con.WM_MOUSELEAVE: lv._mouse_leave_handler()

    return api.DefSubclassProc(hw, msg, wp, lp)

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#||             Window Procedure for Header control.                   ||
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
@WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR)
def hdr_wnd_proc(hw, msg, wp, lp, scID, refData) -> LRESULT:
    # log_msg(msg)
    lv = lv_dict[refData]
    match msg:
        case con.WM_DESTROY:
            res = api.RemoveWindowSubclass(hw, hdr_wnd_proc, scID)
            lv._destroyCount += 1
            if lv._destroyCount == 2: del lv_dict[lv._hwnd]

        case con.HDM_LAYOUT:
            if lv._change_hdr_height:
                phl = cast(lp, api.LPHDLAYOUT).contents
                # res = api.DefSubclassProc(hw, msg, wp, lp)
                pos = phl.pwpos.contents
                prc = phl.prc.contents
                pos.flags = con.SWP_FRAMECHANGED
                pos.hwnd = hw
                pos.y = 0
                pos.x = prc.left
                pos.cx = prc.right - prc.left
                pos.cy = lv._hdr_height
                prc.top = lv._hdr_height

                return -1

        case con.WM_MOUSEMOVE:
            pt = getMousePoints(lp) # Collecting mouse points
            hit = api.HDHITTESTINFO(pt) # Passing it to this struct

            # This message will return the header item index under the mouse
            # We can use this index when we draw the header back color.
            lv._hot_hdr = api.SendMessage(hw, con.HDM_HITTEST, 0, addressof(hit) )

        # Make the hot index to -1, so that our headers are drawn with normal colors after this.
        case con.WM_MOUSELEAVE: lv._hot_hdr = -1

        case con.WM_PAINT:
            # First, let the control to do it's necessary drawings.
            api.DefSubclassProc(hw, msg, wp, lp)

            # Now, we can draw the last part of the header.
            hrc = RECT()
            api.SendMessage(lv._hdr_hwnd, con.HDM_GETITEMRECT, len(lv._columns) - 1, addressof(hrc))
            rc = RECT(hrc.right + 1, hrc.top, lv._width, hrc.bottom)
            hdc = api.GetDC(hw)
            api.FillRect(hdc, byref(rc), lv._hdr_bk_brush)
            api.ReleaseDC(hw, hdc)
            return 0


    return api.DefSubclassProc(hw, msg, wp, lp)