# treeview module - Created on 15-Jan-2023 04:59:20
from ctypes.wintypes import HWND, UINT, HDC
from ctypes import cast, addressof, create_unicode_buffer, c_wchar_p
import ctypes as ctp
from pyforms.src.control import Control
import pyforms.src.constants as con
from pyforms.src.commons import MyMessages
from pyforms.src.enums import ControlType, NodeOp
import pyforms.src.apis as api
from pyforms.src.apis import LRESULT, HTREEITEM, LPNMHDR, LPNMCUSTOMDRAW, SUBCLASSPROC
from pyforms.src.colors import Color
# from horology import Timing
# from .winmsgs import log_msg

tvDict = {}
tvStyle = con.WS_VISIBLE|con.WS_CHILD|con.TVS_HASLINES|con.TVS_HASBUTTONS|con.TVS_LINESATROOT|con.TVS_DISABLEDRAGDROP|con.WS_BORDER


class TreeView(Control):

    """TreeView class.
    """
    Control.icc.initCommCtls(con.ICC_TREEVIEW_CLASSES)
    _count = 1
    __slots__ = ( "_noLines", "_noButtons", "_hasCheckBox", "_fullRowSel", "_editable", "_nodeClrChange",
    			 "_showSel", "_hotTrack", "_lineColor", "_selNode", "_nodes", "_nodeCount",
                 "_nxtNodeHwnd", "_uniqNodeID", "_nodeDict")

    def __init__(self, parent, xpos: int = 10, ypos: int = 10, 
                 width: int = 80, height: int = 24 ) -> None:
        super().__init__()
        self._clsName = "SysTreeView32"
        self.name = f"TreeView_{TreeView._count}"
        self._ctlType = ControlType.TREE_VIEW
        self._parent = parent
        self._bgColor = Color(0xFFFFFF)
        self._font.colneFrom(parent._font)
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._style = tvStyle
        self._exStyle = 0x00000000
        self._noLines = False
        self._lineColor = Color(0x00FF0000)
        self._noButtons = False
        self._hasCheckBox = True
        self._fullRowSel = True
        self._editable = False
        self._showSel = True
        self._hotTrack = False
        self._nodes = [] # This list will hold the top level nodes only
        self._nodeClrChange = False
        self._nodeCount = 0
        self._nxtNodeHwnd = 0
        self._uniqNodeID = 100
        self._nodeDict = {} # This dict will hold all the nodes.
        self._hwnd = None
        parent._controls.append(self)
        #Events

        TreeView._count += 1
        if parent.createChilds: self.createHandle()


    # -region Public funcs
    def createHandle(self):
        self._setStyles()
        self._createControl()
        if self._hwnd:
            # print("treeview hwnd ", self._hwnd)
            tvDict[self._hwnd] = self
            # self._setSubclass(tvWndProc)
            api.SetWindowSubclass(self._hwnd, tvWndProc, Control._subclass_id, id(self))
            Control._subclass_id += 1

            self._setFontInternal()

            if self._bgColor.value != 0xFFFFFF: # Change back color
                api.SendMessage(self._hwnd, con.TVM_SETBKCOLOR, 0, self._bgColor.ref)

            if self._fgColor.value != 0x00000000: # change fore color
                api.SendMessage(self._hwnd, con.TVM_SETTEXTCOLOR, 0, self._fgColor.ref)

            if self._lineColor.value != 0x00000000 and not self._noLines: # Change line color
                api.SendMessage(self._hwnd, con.TVM_SETLINECOLOR, 0, self._lineColor.ref)

    #End of create function----------------------------------------------------------------->


    def addNode(self, node):
        self._manageNodeOps(NodeOp.ADD_NODE, node)

    def addNodes(self, *nodes):
        for node in nodes:
            self._manageNodeOps(NodeOp.ADD_NODE, node)

    def insertNode(self, node, pos: int):
        self._manageNodeOps(NodeOp.INSERT_NODE, node, pos)

    def addChildNode(self, node, parent):
        self._manageNodeOps(NodeOp.ADD_CHILD, node, pnode=parent)

    def addChildNodes(self, parent, *nodes):
        for node in nodes:
            self._manageNodeOps(NodeOp.ADD_CHILD, node, pnode=parent)

    def insertChildNode(self, node, parent, pos):
        self._manageNodeOps(NodeOp.INSERT_CHILD, node, pos, parent)

    def addNodeWithChilds(self, nodeTxt, *childTxts):
        pnode = TreeNode(nodeTxt)
        self._manageNodeOps(NodeOp.ADD_NODE, pnode)
        for txt in childTxts:
            cnode = TreeNode(txt)
            self._manageNodeOps(NodeOp.ADD_CHILD, cnode, pnode=pnode)





    # def addChildNode(self, txt: str, parent_node, )

    # -endregion Public funcs

    # -region Private funcs
    def _setStyles(self):
        if self._noLines: self._style ^= con.TVS_HASLINES
        if self._noButtons: self._style ^= con.TVS_HASBUTTONS
        if self._hasCheckBox: self._style |= con.TVS_CHECKBOXES
        if self._fullRowSel: self._style |= con.TVS_FULLROWSELECT
        if self._editable: self._style |= con.TVS_EDITLABELS
        if self._showSel: self._style |= con.TVS_SHOWSELALWAYS
        if self._hotTrack: self._style |= con.TVS_TRACKSELECT
        if self._noButtons and self._noLines: self._style ^= con.TVS_LINESATROOT
        # print("size of ulongptr ", ctp.sizeof(api.ULONG_PTR))
        # print("ulong max ", 1 << 64)


    def _manageNodeOps(self, op: NodeOp, node, pos = -1, pnode = None):
        if not self._isCreated: raise Exception("TreeView's handle is not created")
        node._isCreated = True
        node._notifyHandler = self.notifyParent
        node._treeHwnd = self._hwnd
        node._index = self._nodeCount
        node._nodeID = self._uniqNodeID # We can identify any node with this
        is_main_node = False
        err_msg = "Can't Add"
        tvi = self._makeTVItem(node)
        tis = api.TVINSERTSTRUCT()
        tis.itemEx = tvi
        tis.itemEx.lParam = id(node)  #node._nodeID
        match op:
            case NodeOp.ADD_NODE:
                tis.hParent = con.TVI_ROOT
                tis.hInsertAfter = self._nodes[self._nodeCount - 1]._hwnd if self._nodeCount > 0 else con.TVI_FIRST
                is_main_node = True

            case NodeOp.INSERT_NODE:
                tis.hParent = con.TVI_ROOT
                tis.hInsertAfter = con.TVI_FIRST if pos == 0 else self._nodes[pos - 1]._hwnd
                is_main_node = True
                err_msg = "Can't Insert"

            case NodeOp.ADD_CHILD:
                tis.hInsertAfter = con.TVI_LAST
                tis.hParent = pnode._hwnd
                node._parentNode = pnode
                pnode._nodes.append(node)
                pnode._nodeCount += 1
                err_msg = "Can't Add Child"

            case NodeOp.INSERT_CHILD:
                tis.hParent = pnode._hwnd
                tis.hInsertAfter = con.TVI_FIRST if pos == 0 else pnode._nodes[pos - 1]._hwnd
                node._parentNode = pnode
                pnode._nodes.append(node)
                pnode._nodeCount += 1
                err_msg = "Can't Insert Child"

        # self._nodeDict[node._nodeID] = node # Advances dict entry, because we just want to avoid KeyError
        hItem =  HTREEITEM(api.SendMessage(self._hwnd, con.TVM_INSERTITEMW, 0, addressof(tis)))
        if hItem:
            node._hwnd = hItem
            self._uniqNodeID += 1

        else:
            raise Exception(f"{err_msg} node!, Error - {api.GetLastError()}")

        if is_main_node:
            self._nodes.append(node)
            self._nodeCount += 1
    #End of function---------------------------------------------------------------------------->



    def _makeTVItem(self, node) -> api.TVITEMEXW:
        # Initialize a TVITEMEX struct with necessary values from given TreeNode class.
        self._smBuffer.fillBuffer(node._text)
        tvi = api.TVITEMEXW()
        tvi.mask = con.TVIF_TEXT | con.TVIF_PARAM
        tvi.pszText = cast(self._smBuffer.addr, c_wchar_p)
        tvi.cchTextMax = len(node._text)
        tvi.iImage = node._imgIndex
        tvi.iSelectedImage = node._selImgIndex
        tvi.stateMask = con.TVIS_USERMASK
        # tvi.lParam = node._nodeID
        if node._imgIndex > -1: tvi.mask |= con.TVIF_IMAGE
        if node._selImgIndex > -1: tvi.mask |= con.TVIF_SELECTEDIMAGE
        if node._fgColor.value != 0x000000: self._nodeClrChange = True
        return tvi


    def _changeTVItemProps(self, prop, value):
        tvi = api.TVITEMEXW()
        if prop == 1:
            tvi.mask = con.TVIF_TEXT
            tvi.pszText = cast(create_unicode_buffer(value), c_wchar_p)
            tvi.cchTextMax = len(value)



    def notifyParent(self, node, property: str, data):
        # print(f"Hi this parent named {self.name} is notified with this data {data}")
        match property:
            case "foreColor":pass
                # Change treeview item fore color
            case "backColor":pass
                # Change treeview item back color
            case "text": pass
                # Change item text


    # def _change_tree_item_forecolor(self, node, clr):
    #     s


    # -endregion Private funcs

    # -region Properties

    @property
    def nodes(self) : return self._nodes

    @property
    def selectedNode(self): return self._selNode


    @Control.foreColor.setter
    def foreColor(self, value):
        if isinstance(value, int):
            self._bgColor.updateColor(value)
        elif isinstance(value, Color):
            self._bgColor = value

        api.sendMessage(self._hwnd, con.TVM_SETTEXTCOLOR, 0, self._fgColor.ref)
        self.manageRedraw()

    @property
    def noLine(self): return self._noLine

    @noLine.setter
    def noLine(self, value: bool) : self._noLine = value


    @property
    def noButton(self): return self._noButton

    @noButton.setter
    def noButton(self, value: bool): self._noButton = value


    @property
    def hasCheckBox(self): return self._hasCheckBox

    @hasCheckBox.setter
    def hasCheckBox(self, value: bool): self._hasCheckBox = value


    @property
    def fullRowSelect(self): return self._fullRowSel

    @fullRowSelect.setter
    def fullRowSelect(self, value: bool): self._fullRowSel = value


    @property
    def isEditable(self): return self._editable

    @isEditable.setter
    def isEditable(self, value: bool): self._editable = value


    @property
    def showSelection(self): bool = self._showSel

    @showSelection.setter
    def showSelection(self, value: bool): self._showSel = value


    @property
    def hotTrack(self): return self._hotTrack

    @hotTrack.setter
    def hotTrack(self, value: bool): self._hotTrack = value


    @property
    def nodeCount(self): return self._nodeCount

    @nodeCount.setter
    def nodeCount(self, value: int): self._nodeCount = value


    @property
    def uniqNodeID(self): return self._uniqNodeID

    @uniqNodeID.setter
    def uniqNodeID(self, value: int): self._uniqNodeID = value


    @property
    def lineColor(self):return  self._lin

    @lineColor.setter
    def lineColor(self, value: int): self._lineColor =  Color(value)



    # -endregion Properties
    x = 100 # dummy

#End TreeView

class TreeNode:

    __slots__ = ("_hwnd", "_parentNode", "_nodes", "_imgIndex", "_selImgIndex", "_nodeCount", "_fgColor",
                 "_bgColor", "_checked", "_text", "_index", "_nodeID", "_treeHwnd", "_isCreated", "_notifyHandler" )

    def __init__(self, text: str) -> None:
        self._nodes = []
        self._imgIndex = -1
        self._selImgIndex = -1
        self._nodeCount = 0
        self._fgColor = Color(0x000000)
        self._bgColor = Color(0xFFFFFF)
        self._checked = False
        self._text = text
        self._index = -1
        self._nodeID = 0
        self._treeHwnd = 0
        self._isCreated = False
        self._notifyHandler = 0

    @property
    def imageIndex(self): return self._imgIndex

    @imageIndex.setter
    def imageIndex(self, value: int):self._imgIndex = value

    @property
    def selectedImageIndex(self): return self._selImgIndex

    @selectedImageIndex.setter
    def selectedImageIndex(self, value: int):self._selImgIndex = value

    @property
    def foreColor(self): return self._fgColor

    @foreColor.setter
    def foreColor(self, value: int):
        self._fgColor = Color(value)
        if self._isCreated: self._notifyHandler(self, "foreColor", value)


    @property
    def backColor(self): return self._bgColor

    @backColor.setter
    def backColor(self, value: int):
        self._bgColor = Color(value)
        if self._isCreated: self._notifyHandler(self, "backColor", value)

    @property
    def text(self): return self._text

    @text.setter
    def text(self, value: int):
        self._text = Color(value)
        if self._isCreated: self._notifyHandler(self, "text", value)



# @WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR)
@SUBCLASSPROC
def tvWndProc(hw, msg, wp, lp, scID, refData) -> LRESULT:
    # log_msg(msg)
    # with Timing("py obj time : "):
    tv = tvDict[hw]
        # tv = cast(refData, ctp.py_object).value
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, tvWndProc, scID)
            del tvDict[hw]

        case MyMessages.CTRL_NOTIFY:
            nmh = cast(lp, LPNMHDR).contents
            match nmh.code:
                case con.NM_CUSTOMDRAW:
                    nmcd = cast(lp, LPNMCUSTOMDRAW).contents
                    match nmcd.dwDrawStage:
                        case con.CDDS_PREPAINT: return con.CDRF_NOTIFYITEMDRAW
                        case con.CDDS_ITEMPREPAINT:
                            if nmcd.lItemParam:
                                # node = tv._nodeDict[nmcd.lItemParam]
                                # node = ctp.py_object.from_param(nmcd.lItemParam)
                                # with Timing("node time : "):
                                    # node = tv._nodeDict.get(nmcd.lItemParam, 0)
                                node = cast(nmcd.lItemParam, ctp.py_object).value
                                # print(f"{nmcd.dwItemSpec = }, {nmcd.lItemParam = }, {node._text = }")
                                return con.CDRF_DODEFAULT

        #     if nm.hdr.code == con.UDN_DELTAPOS:
        #         tv._value = float(tv._getCtrlTextEx(tv._buddy_hwnd))
        #         tv._set_numpick_value(nm.iDelta)
        #         tv._display_value()
        #         if tv.on_value_changed: tv.on_value_changed(np, EventArgs())

        case con.WM_SETFOCUS: tv._gotFocusHandler()
        case con.WM_KILLFOCUS: tv._lostFocusHandler()
        case con.WM_LBUTTONDOWN: tv._leftMouseDownHandler(msg, wp, lp)
        case con.WM_LBUTTONUP: tv._leftMouseUpHandler(msg, wp, lp)
        case con.WM_RBUTTONDOWN: tv._rightMouseDownHandler(msg, wp, lp)
        case con.WM_RBUTTONUP: tv._rightMouseUpHandler(msg, wp, lp)
        case con.WM_MOUSEWHEEL: tv._mouseWheenHandler(msg, wp, lp)
        case con.WM_MOUSEMOVE: tv._mouseMoveHandler(msg, wp, lp)
        # case con.WM_MOUSELEAVE:
        #     if tv._track_mouse_leave:
        #         if not tv._is_mouse_upon_me():
        #             tv._isMouseEntered = False
        #             if tv.on_mouse_leave: tv.on_mouse_leave(np, EventArgs())

    return api.DefSubclassProc(hw, msg, wp, lp)



