
# treeview module - Created on 15-Jan-2023 04:59:20
from ctypes.wintypes import HWND, UINT, HDC
from ctypes import byref, cast, addressof, create_unicode_buffer, c_wchar_p
import ctypes as ctp

from .control import Control
from . import constants as con
from .commons import MyMessages
from .enums import ControlType, NodeOp
# from .events import EventArgs
from . import apis as api
from .apis import LRESULT, UINT_PTR, DWORD_PTR, WPARAM, LPARAM, HTREEITEM, LPNMHDR, LPNMCUSTOMDRAW, SUBCLASSPROC
from .colors import Color

from horology import Timing
# from .winmsgs import log_msg

tv_dict = {}
nump_tb_dict = {}
tv_style = con.WS_VISIBLE|con.WS_CHILD|con.TVS_HASLINES|con.TVS_HASBUTTONS|con.TVS_LINESATROOT|con.TVS_DISABLEDRAGDROP|con.WS_BORDER
# txtFlag = con.DT_SINGLELINE | con.DT_VCENTER | con.DT_CENTER | con.DT_NOPREFIX



class TreeView(Control):

    """TreeView class.
    """
    Control.icc.init_comm_ctls(con.ICC_TREEVIEW_CLASSES)
    _count = 1
    __slots__ = ( "_no_lines", "_no_buttons", "_has_checkboxes", "_full_row_sel", "_editable", "_node_clr_change",
    			 "_show_sel", "_hot_track", "_line_color", "_sel_node", "_nodes", "_node_count",
                 "_nxt_node_hwnd", "_uniq_node_id", "_node_dict")

    def __init__(self, parent, xpos: int = 10, ypos: int = 10, width: int = 80, height: int = 24 ) -> None:
        super().__init__()
        self._cls_name = "SysTreeView32"
        self.name = f"TreeView_{TreeView._count}"
        # self._text = self.name if txt == "" else txt
        self._ctl_type = ControlType.TREE_VIEW
        self._parent = parent
        self._bg_color = Color(0xFFFFFF)
        self._font = parent._font
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        # self._is_textable = True
        self._style = tv_style
        self._ex_style = 0x00000000

        self._no_lines = False
        self._line_color = Color(0x00FF0000)
        self._no_buttons = False
        self._has_checkboxes = True
        self._full_row_sel = True
        self._editable = False
        self._show_sel = True
        self._hot_track = False
        self._nodes = [] # This list will hold the top level nodes only
        self._node_clr_change = False
        self._node_count = 0
        self._nxt_node_hwnd = 0
        self._uniq_node_id = 100
        self._node_dict = {} # This dict will hold all the nodes.


        #Events
        # self.on_value_changed = 0

        TreeView._count += 1


    # -region Public funcs
    def create_handle(self):
        self._tv_set_styles()
        self._create_control()
        if self._hwnd:
            # print("treeview hwnd ", self._hwnd)
            tv_dict[self._hwnd] = self
            # self._set_subclass(tv_wnd_proc)
            api.SetWindowSubclass(self._hwnd, tv_wnd_proc, Control._subclass_id, id(self))
            Control._subclass_id += 1

            self._set_font_internal()

            if self._bg_color.value != 0xFFFFFF: # Change back color
                api.SendMessage(self._hwnd, con.TVM_SETBKCOLOR, 0, self._bg_color.ref)

            if self._fg_color.value != 0x00000000: # change fore color
                api.SendMessage(self._hwnd, con.TVM_SETTEXTCOLOR, 0, self._fg_color.ref)

            if self._line_color.value != 0x00000000 and not self._no_lines: # Change line color
                api.SendMessage(self._hwnd, con.TVM_SETLINECOLOR, 0, self._line_color.ref)

    #End of create function----------------------------------------------------------------->


    def add_node(self, node):
        self._manage_node_operation(NodeOp.ADD_NODE, node)

    def add_nodes(self, *nodes):
        for node in nodes:
            self._manage_node_operation(NodeOp.ADD_NODE, node)

    def insert_node(self, node, pos: int):
        self._manage_node_operation(NodeOp.INSERT_NODE, node, pos)

    def add_child_node(self, node, parent):
        self._manage_node_operation(NodeOp.ADD_CHILD, node, pnode=parent)

    def add_child_nodes(self, parent, *nodes):
        for node in nodes:
            self._manage_node_operation(NodeOp.ADD_CHILD, node, pnode=parent)

    def insert_child_node(self, node, parent, pos):
        self._manage_node_operation(NodeOp.INSERT_CHILD, node, pos, parent)




    # def add_child_node(self, txt: str, parent_node, )

    # -endregion Public funcs

    # -region Private funcs
    def _tv_set_styles(self):
        if self._no_lines: self._style ^= con.TVS_HASLINES
        if self._no_buttons: self._style ^= con.TVS_HASBUTTONS
        if self._has_checkboxes: self._style |= con.TVS_CHECKBOXES
        if self._full_row_sel: self._style |= con.TVS_FULLROWSELECT
        if self._editable: self._style |= con.TVS_EDITLABELS
        if self._show_sel: self._style |= con.TVS_SHOWSELALWAYS
        if self._hot_track: self._style |= con.TVS_TRACKSELECT
        if self._no_buttons and self._no_lines: self._style ^= con.TVS_LINESATROOT
        # print("size of ulongptr ", ctp.sizeof(api.ULONG_PTR))
        # print("ulong max ", 1 << 64)


    def _manage_node_operation(self, op: NodeOp, node, pos = -1, pnode = None):
        if not self._is_created: raise Exception("TreeView's handle is not created")
        node._is_created = True
        node._notify_handler = self.notify_parent
        node._tree_hwnd = self._hwnd
        node._index = self._node_count
        node._node_id = self._uniq_node_id # We can identify any node with this
        is_main_node = False
        err_msg = "Can't Add"
        tvi = self._make_tvitem(node)
        tis = api.TVINSERTSTRUCT()
        tis.itemEx = tvi
        tis.itemEx.lParam = id(node)  #node._node_id
        match op:
            case NodeOp.ADD_NODE:
                tis.hParent = con.TVI_ROOT
                tis.hInsertAfter = self._nodes[self._node_count - 1]._hwnd if self._node_count > 0 else con.TVI_FIRST
                is_main_node = True

            case NodeOp.INSERT_NODE:
                tis.hParent = con.TVI_ROOT
                tis.hInsertAfter = con.TVI_FIRST if pos == 0 else self._nodes[pos - 1]._hwnd
                is_main_node = True
                err_msg = "Can't Insert"

            case NodeOp.ADD_CHILD:
                tis.hInsertAfter = con.TVI_LAST
                tis.hParent = pnode._hwnd
                node._parent_node = pnode
                pnode._nodes.append(node)
                pnode._node_count += 1
                err_msg = "Can't Add Child"

            case NodeOp.INSERT_CHILD:
                tis.hParent = pnode._hwnd
                tis.hInsertAfter = con.TVI_FIRST if pos == 0 else pnode._nodes[pos - 1]._hwnd
                node._parent_node = pnode
                pnode._nodes.append(node)
                pnode._node_count += 1
                err_msg = "Can't Insert Child"

        # self._node_dict[node._node_id] = node # Advances dict entry, because we just want to avoid KeyError
        hItem =  HTREEITEM(api.SendMessage(self._hwnd, con.TVM_INSERTITEMW, 0, addressof(tis)))
        if hItem:
            node._hwnd = hItem
            self._uniq_node_id += 1

        else:
            raise Exception(f"{err_msg} node!, Error - {api.GetLastError()}")

        if is_main_node:
            self._nodes.append(node)
            self._node_count += 1
    #End of function---------------------------------------------------------------------------->



    def _make_tvitem(self, node) -> api.TVITEMEXW:
        # Initialize a TVITEMEX struct with necessary values from given TreeNode class.
        tvi = api.TVITEMEXW()
        tvi.mask = con.TVIF_TEXT | con.TVIF_PARAM
        tvi.pszText = cast(create_unicode_buffer(node._text), c_wchar_p)
        tvi.cchTextMax = len(node._text)
        tvi.iImage = node._img_index
        tvi.iSelectedImage = node._sel_img_index
        tvi.stateMask = con.TVIS_USERMASK
        # tvi.lParam = node._node_id
        if node._img_index > -1: tvi.mask |= con.TVIF_IMAGE
        if node._sel_img_index > -1: tvi.mask |= con.TVIF_SELECTEDIMAGE
        if node._fg_color.value != 0x000000: self._node_clr_change = True
        return tvi


    def _change_tvitem_props(self, prop, value):
        tvi = api.TVITEMEXW()
        if prop == 1:
            tvi.mask = con.TVIF_TEXT
            tvi.pszText = cast(create_unicode_buffer(value), c_wchar_p)
            tvi.cchTextMax = len(value)



    def notify_parent(self, node, property: str, data):
        # print(f"Hi this parent named {self.name} is notified with this data {data}")
        match property:
            case "fore_color":pass
                # Change treeview item fore color
            case "back_color":pass
                # Change treeview item back color
            case "text": pass
                # Change item text


    # def _change_tree_item_forecolor(self, node, clr):
    #     s


    # -endregion Private funcs

    # -region Properties

    # @property
    # def auto_size(self): return self._auto_size

    # @Control.back_color.setter
    # def back_color(self, value : int):
    #     self._bg_color.update_color(value)
    #     if not self._draw_flag & (1 << 1): self._draw_flag += 2
    #     self._manage_redraw()

    # @property
    # def decimal_points(self): return self._deci_precis

    # @decimal_points.setter
    # def decimal_points(self, value: int): self._deci_precis = value
    #-----------------------------------------------------------------------[1]


    # -endregion Properties
    x = 100 # dummy

#End TreeView

class TreeNode:

    __slots__ = ("_hwnd", "_parent_node", "_nodes", "_img_index", "_sel_img_index", "_node_count", "_fg_color",
                 "_bg_color", "_checked", "_text", "_index", "_node_id", "_tree_hwnd", "_is_created", "_notify_handler" )

    def __init__(self, text: str) -> None:
        self._nodes = []
        self._img_index = -1
        self._sel_img_index = -1
        self._node_count = 0
        self._fg_color = Color(0x000000)
        self._bg_color = Color(0xFFFFFF)
        self._checked = False
        self._text = text
        self._index = -1
        self._node_id = 0
        self._tree_hwnd = 0
        self._is_created = False
        self._notify_handler = 0

    @property
    def image_index(self): return self._img_index

    @image_index.setter
    def image_index(self, value: int):self._img_index = value

    @property
    def selected_image_index(self): return self._sel_img_index

    @selected_image_index.setter
    def selected_image_index(self, value: int):self._sel_img_index = value

    @property
    def fore_color(self): return self._fg_color

    @fore_color.setter
    def fore_color(self, value: int):
        self._fg_color = Color(value)
        if self._is_created: self._notify_handler(self, "fore_color", value)


    @property
    def back_color(self): return self._bg_color

    @back_color.setter
    def back_color(self, value: int):
        self._bg_color = Color(value)
        if self._is_created: self._notify_handler(self, "back_color", value)

    @property
    def text(self): return self._text

    @text.setter
    def text(self, value: int):
        self._text = Color(value)
        if self._is_created: self._notify_handler(self, "text", value)



# @WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR)
@SUBCLASSPROC
def tv_wnd_proc(hw, msg, wp, lp, scID, refData) -> LRESULT:
    # log_msg(msg)
    # with Timing("py obj time : "):
    tv = tv_dict[hw]
        # tv = cast(refData, ctp.py_object).value
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, tv_wnd_proc, scID)
            print("remove subclass for - ", tv.name)

        case MyMessages.CTRL_NOTIFY:
            nmh = cast(lp, LPNMHDR).contents
            match nmh.code:
                case con.NM_CUSTOMDRAW:
                    nmcd = cast(lp, LPNMCUSTOMDRAW).contents
                    match nmcd.dwDrawStage:
                        case con.CDDS_PREPAINT: return con.CDRF_NOTIFYITEMDRAW
                        case con.CDDS_ITEMPREPAINT:
                            if nmcd.lItemParam:
                                # node = tv._node_dict[nmcd.lItemParam]
                                # node = ctp.py_object.from_param(nmcd.lItemParam)
                                # with Timing("node time : "):
                                    # node = tv._node_dict.get(nmcd.lItemParam, 0)
                                node = cast(nmcd.lItemParam, ctp.py_object).value
                                # print(f"{nmcd.dwItemSpec = }, {nmcd.lItemParam = }, {node._text = }")
                                return con.CDRF_DODEFAULT

        #     if nm.hdr.code == con.UDN_DELTAPOS:
        #         tv._value = float(tv._get_ctrl_text_ex(tv._buddy_hwnd))
        #         tv._set_numpick_value(nm.iDelta)
        #         tv._display_value()
        #         if tv.on_value_changed: tv.on_value_changed(np, EventArgs())

        # case con.WM_SETFOCUS: tv._got_focus_handler()
        # case con.WM_KILLFOCUS: tv._lost_focus_handler()
        # case con.WM_LBUTTONDOWN: tv._left_mouse_down_handler(msg, wp, lp)
        # case con.WM_LBUTTONUP: tv._left_mouse_up_handler(msg, wp, lp)
        # case MyMessages.MOUSE_CLICK: tv._mouse_click_handler()
        # case con.WM_RBUTTONDOWN: tv._right_mouse_down_handler(msg, wp, lp)
        # case con.WM_RBUTTONUP: tv._right_mouse_up_handler(msg, wp, lp)
        # case MyMessages.RIGHT_CLICK: tv._right_mouse_click_handler()
        # case con.WM_MOUSEWHEEL: tv._mouse_wheel_handler(msg, wp, lp)
        # case con.WM_MOUSEMOVE: tv._mouse_move_handler(msg, wp, lp)
        # case con.WM_MOUSELEAVE:
        #     if tv._track_mouse_leave:
        #         if not tv._is_mouse_upon_me():
        #             tv._is_mouse_entered = False
        #             if tv.on_mouse_leave: tv.on_mouse_leave(np, EventArgs())

    return api.DefSubclassProc(hw, msg, wp, lp)



