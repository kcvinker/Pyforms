# listview module - Created on 02-Jan-2023 21:21:20

import typing
from enum import Enum
from ctypes.wintypes import HWND, UINT
from ctypes import WINFUNCTYPE, byref, addressof, cast, create_unicode_buffer, c_wchar_p
from pyforms.src.control import Control

import pyforms.src.constants as con
from pyforms.src.commons import Font, MyMessages, getMousePoints
from pyforms.src.enums import ControlType, TextAlignment, ListViewStyle
from pyforms.src.apis import LRESULT, UINT_PTR, DWORD_PTR, RECT, LPNMCUSTOMDRAW, LVCOLUMNW, WPARAM, LPARAM, SUBCLASSPROC
import pyforms.src.apis as api
from pyforms.src.colors import Color
from pyforms.src.winmsgs import log_msg
# from horology import Timing

lvDict = {}
hdrDict = {}
lvStyle = con.WS_CHILD | con.WS_VISIBLE | con.LVS_ALIGNLEFT| con.LVS_EDITLABELS | con.WS_BORDER
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
    Control.icc.initCommCtls(con.ICC_LISTVIEW_CLASSES)
    _count = 1
    __slots__ = ("_selIndex", "_selItem", "_editLabel", "_lblHwnd", "_hdrHwnd", "_itemTopAlign",
					"_hideSel", "_multiSel", "_checkBox", "_fullRowSel", "_showGrid", "_oneClickAct", "_hotTrackSel",
					"_noHdr", "_changeHdrHeight", "_hdrDrawFont", "_setCBLast", "_cbIsLast", "_cbChecked",
					"_hdrFont", "_colAlign", "_viewStyle", "_columns", "_items", "_colIndList", "_colIndex",
                    "_hdrHeight", "_selItemIndex", "_selSubIndex", "_imgList", "_hdrItemDict", "_hdrPts", "_mouseOnHdr",
                    "_hdrBgColor", "_hdrFgColor", "_hdrBkBrush", "_hdrOwnDraw", "_hotHdr", "_colIndex",
                    "_hdrHotBrush", "_hdrClickable", "_selectable", "_itemIndex", "_itemDrawn", "_destroyCount", "_layCount" )

    def __init__(self, parent, xpos: int = 10, ypos: int = 10, width: int = 250, height: int = 200, auto = False, cols = None) -> None:
        super().__init__()

        self._clsName = "SysListView32"
        self.name = f"ListView_{ListView._count}"
        self._ctlType = ControlType.LIST_VIEW
        self._parent = parent
        self._bgColor = Color(0xFFFFFF)
        # self._fgColor = Color(0x000000) # Control class is taking care of this
        self._font = parent._font
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._isTextable = False
        self._style = lvStyle
        self._exStyle = 0
        self._text = ""

        self._columns = []
        self._items = []
        self._colIndList = []
        self._viewStyle = ListViewStyle.REPORT_VIEW # Ideal for most common use cases
        self._showGrid = True
        self._fullRowSel = True
        self._editLabel = False
        self._hideSel = True
        self._noHdr = False
        self._multiSel = False
        self._checkBox = False
        self._oneClickAct = True
        self._hotTrackSel = False
        self._cbIsLast = False
        self._hdrPts = api.POINT()
        self._mouseOnHdr = False
        self._hdrBgColor = Color(0xb3cccc)
        self._hdrFgColor = Color(0x000000)
        self._hdrClickable = True
        self._hdrFont = parent._font # Font("Tahoma", 11, FontWeight.BOLD)
        self._selectable = False
        self._itemIndex = -1
        self._itemDrawn = -1
        self._hdrOwnDraw = False
        self._changeHdrHeight = True
        self._hdrHeight = 25
        self._hotHdr = -1
        self._colIndex = 0
        self._destroyCount = 0
        self._layCount = 0
        self._hwnd = None
        parent._controls.append(self)
        # Events

        ListView._count += 1
        if auto: self.createHandle()
        if isinstance(cols, list): self.addColumnsEx(*cols)



# -region Public functions

    def createHandle(self):
        """Create's ListView handle"""
        # self._parent.lv_func = self._lvWmNotifyHandler
        self._setLVStyles()
        self._createControl()
        if self._hwnd:
            # self._parent.lv_hwnd = self._hwnd
            self._setLVExStyles()
            lvDict[self._hwnd] = self
            self._setSubclass(lvWndProc)
            self._setFontInternal()

            if self._columns:
                for col in self._columns:
                    api.SendMessage(self._hwnd, con.LVM_INSERTCOLUMNW, col.index, addressof(col.lvc))

            self._hdrHwnd = api.SendMessage(self._hwnd, con.LVM_GETHEADER, 0, 0)
            # hdrDict[self._hdrHwnd] = self # Put ourself inside this dict so that we can appear in hdrWndProc
            if not self._hdrFont.handle: self._hdrFont.createHandle(self._hdrHwnd)# Making sure header font is ready.
            #
            # We are going to send the list view hwnd with this function. So, we can grab it inside
            # header's wndproc function.
            api.SetWindowSubclass(self._hdrHwnd, hdrWndProc, ListView._count, self._hwnd)
            if self._bgColor != self._parent._bgColor:
                api.SendMessage(self._hwnd, con.LVM_SETBKCOLOR, 0, self._bgColor.ref)

            if self._cbIsLast:
                ord_list = self._changeColOrder()
                api.SendMessage(self._hwnd, con.LVM_SETCOLUMNORDERARRAY, len(ord_list), addressof(ord_list))
                self._cbIsLast = True

            # print("lv hwnd ", self._hwnd)
            # print("frm hwnd ", self._parent._hwnd)


    #End of Create function-----------------------------------------------

    def addColumnEx(self, lvc):
        self._addColInternal(lvc)


    def addColumn(self, txt: str, width: int = 100, image_index: int = -1):
        col = ListViewColumn(txt, width, image_index)
        self._addColInternal(col)


    def addColumns(self, col_names: list[str], col_widths: list[int]):
        if len(col_names) != len(col_widths):
            raise Exception("Length of column names & column widths are not equal")
        for (name, width) in zip(col_names, col_widths):
            col = ListViewColumn(name, width)
            self._addColInternal(col)

    def addColumnsEx(self, *colsAndWidths):
        cols = []
        wids = []
        for item in colsAndWidths:
            if isinstance(item, int): wids.append(item)
            if isinstance(item, str): cols.append(item)

        if len(cols) == len(wids):
            for (name, width) in zip(cols, wids):
                col = ListViewColumn(name, width)
                self._addColInternal(col)



    def addRow(self, *items):
        if self._viewStyle != ListViewStyle.REPORT_VIEW: raise Exception("Adding row is possible only in ListViewStyle.REPORT_VIEW")
        if not self._isCreated: raise Exception("Adding  row is possible only after ListView's handle created")
        if not items: raise Exception("items is not iterable")

        lvi = ListViewItem(items[0])
        self._addItemInternal(lvi)
        for i in range(1, len(items)):
            self._addSubItemInternal(items[i], lvi._index, i)


# -endregion Public functions


    # -region private_funcs

    def _setLVStyles(self):
        # Setup different listview styles as per user's selection
        match self._viewStyle:
            case ListViewStyle.LARGE_ICON: self._style |= con.LVS_ICON
            case ListViewStyle.REPORT_VIEW: self._style |= con.LVS_REPORT
            case ListViewStyle.SMALL_ICON: self._style |= con.LVS_SMALLICON
            case ListViewStyle.LIST_VIEW: self._style |= con.LVS_LIST
        # print(self._viewStyle, " self._viewStyle")

        # Set some more styles...
        if self._editLabel: self._style |= con.LVS_EDITLABELS
        if self._hideSel: self._style ^= con.LVS_SHOWSELALWAYS
        if self._noHdr: self._style |= con.LVS_NOCOLUMNHEADER
        if self._multiSel: self._style ^= con.LVS_SINGLESEL

        # Set some brushes
        self._hdrBkBrush = self._hdrBgColor.createHBrush()
        self._hdrHotBrush = self._hdrBgColor.createHBrush(1.09)


    def _setLVExStyles(self):
        # Setup the different ex styles for this list view
        lv_ex_style = 0x0000
        if self._showGrid: lv_ex_style |= con.LVS_EX_GRIDLINES
        if self._checkBox: lv_ex_style |= con.LVS_EX_CHECKBOXES
        if self._fullRowSel: lv_ex_style |= con.LVS_EX_FULLROWSELECT
        if self._oneClickAct: lv_ex_style |= con.LVS_EX_ONECLICKACTIVATE
        if self._hotTrackSel: lv_ex_style |= con.LVS_EX_TRACKSELECT
        # if self._viewStyle == ListViewStyle.TILE_VIEW: api.SendMessage(self._hwnd, con.LVM_SETVIEW, 0x0004, 0)
        api.SendMessage(self._hwnd, con.LVM_SETEXTENDEDLISTVIEWSTYLE, 0 , lv_ex_style)


    def _lvWmNotifyHandler(self, lpm):
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
                        lvcd.clrTextBk = self._bgColor.ref
                        return con.CDRF_NEWFONT | con.CDRF_DODEFAULT

        return con.CDRF_DODEFAULT


    def _changeColOrder(self):
        # If user wants to swap the first and last columns, we can use this.
        indices = []
        for lc in self._columns:
            if lc.index > 0: indices.append(lc.index)
        indices.append(0)
        return indices


    def _addColInternal(self, lvcol):
        lvcol.index = self._colIndex
        lvc = LVCOLUMNW()
        lvc.mask = con.LVCF_TEXT  | con.LVCF_WIDTH | con.LVCF_FMT | con.LVCF_SUBITEM
        lvc.fmt = lvcol.textAlign.value
        lvc.cx = lvcol.width
        lvc.pszText = cast(create_unicode_buffer(lvcol.text), c_wchar_p)
        # lvc.iOrder = lvcol.index

        if lvcol.hasImage:
            lvc.mask |= con.LVCF_IMAGE
            lvc.fmt |= con.LVCFMT_COL_HAS_IMAGES | con.LVCFMT_IMAGE
            lvc.iImage = lvcol.imageIndex
            if lvcol.imageOnRight: lvc.fmt |= con.LVCFMT_BITMAP_ON_RIGHT

        lvcol.lvc = lvc
        if self._isCreated:
            api.SendMessage(self._hwnd, con.LVM_INSERTCOLUMNW, lvcol.index, addressof(lvc))


        self._columns.append(lvcol)
        self._colIndex += 1


    def _addItemInternal(self, item):
        lvi = api.LVITEMW()
        lvi.mask = con.LVIF_TEXT | con.LVIF_PARAM | con.LVIF_STATE
        if item._imgIndex != -1: lvi.mask |= con.LVIF_IMAGE
        lvi.state = 0
        lvi.stateMask = 0
        lvi.iItem = item._index
        lvi.iSubItem = 0
        lvi.iImage = item._imgIndex
        lvi.pszText = cast(create_unicode_buffer(item.text), c_wchar_p)
        lvi.cchTextMax = len(item._text) + 1
        # lvi.lParam = id(item)
        api.SendMessage(self._hwnd, con.LVM_INSERTITEMW, 0, addressof(lvi))
        self._items.append(item)


    def _addSubItemInternal(self, subitem: str, item_index: int, sub_index: int, imageIndex: int = -1):

        sitem = subitem if isinstance(subitem, str) else str(subitem)
        lvi = api.LVITEMW()
        # lvi.mask = con.LVIF_TEXT | con.LVIF_STATE
        # lvi.iItem = item_index
        lvi.iSubItem = sub_index
        lvi.pszText = cast(create_unicode_buffer(sitem), c_wchar_p)
        lvi.iImage = imageIndex
        api.SendMessage(self._hwnd, con.LVM_SETITEMTEXTW, item_index, addressof(lvi))
        self._items[item_index]._subitems.append(sitem) # Put the subitem in our item's bag.


    def _drawHeader(self, nmcd: LPNMCUSTOMDRAW) -> int:
        # Windows's own header drawing is white bkg color.
        # But listview itself is white bkg. We can't allow both hdr & listview in white.
        # So, we need to draw it on our own.
        if nmcd.dwItemSpec != 0: nmcd.rc.left += 1 # Give room for header divider.
        col = self._columns[nmcd.dwItemSpec] # Get our column class
        api.SetBkMode(nmcd.hdc, con.TRANSPARENT)

        if nmcd.uItemState & con.CDIS_SELECTED:
            api.FillRect(nmcd.hdc, byref(nmcd.rc), self._hdrBkBrush)
        else:
            # We will draw with a different color if mouse is over this hdr.
            if nmcd.dwItemSpec == self._hotHdr:
                api.FillRect(nmcd.hdc, byref(nmcd.rc), self._hdrHotBrush)
            else:
                api.FillRect(nmcd.hdc, byref(nmcd.rc), self._hdrBkBrush)

        api.SelectObject(nmcd.hdc, self._hdrFont.handle)
        api.SetTextColor(nmcd.hdc, self._hdrFgColor.ref)
        if self._hdrClickable and nmcd.uItemState & con.CDIS_SELECTED:
            # We are mimicing the dotnet listview header's nature here.
            # They did not resize the overall header item. They just reduce...
            # it for drawing text. That means, text is drawing in a small rect.
            # Thus, viewer thinks like header is pressed a little bit.
            nmcd.rc.left += 1
            nmcd.rc.top += 1
            nmcd.rc.right -= 1
            nmcd.rc.bottom += 1

        api.DrawText(nmcd.hdc, col.text, -1, byref(nmcd.rc), col._hdrTxtFlag )


    #------------------------------------------End
    # -endregion Private funcs

    # -region Properties

    @property
    def selectedIndex(self): return self._selIndex

    @property
    def selectedSubIndex(self): return self._selSubIndex

    @property
    def checked(self): return self._cbChecked

    @property
    def columns(self): return self._columns

    @property
    def items(self): return self._items

    @property
    def headerVisualStyle(self)-> int:
        """Get the range beetween minimum & maximum values"""
        return self._hdrOwnDraw

    @headerVisualStyle.setter
    def headerVisualStyle(self, value: int):
        """Set or get the header back color"""
        self._hdrOwnDraw = value
        if self._columns: self._make_hdr_owner_draw()

    #------------------------------------------------------------------------2 Header Back Color

    @property
    def headerHeight(self)-> int:
        """Get the header height."""
        return self._hdrHeight

    @headerHeight.setter
    def headerHeight(self, value: int):
        """Set the header height."""
        self._hdrHeight = value
    #------------------------------------------------------------------------2 Header Height

    @property
    def editLabel(self) : return self._editLabel

    @editLabel.setter
    def editLabel(self, value: bool) : self._editLabel = value

    @property
    def hideSelection(self) : return self._hideSel

    @hideSelection.setter
    def hideSelection(self, value: bool) : self._hideSel = value

    @property
    def multiSelection(self) : return self._multiSel

    @multiSelection.setter
    def multiSelection(self, value: bool): self._multiSel = value

    @property
    def hasCheckBox(self) : return self._hasCheckBox

    @hasCheckBox.setter
    def hasCheckBox(self, value: bool) : self._hasCheckBox = value

    @property
    def fullRowSelection(self) : return self._fullRowSel

    @fullRowSelection.setter
    def fullRowSelection(self, value: bool) : self._fullRowSel = value

    @property
    def showGrid(self) : return self._showGrid

    @showGrid.setter
    def showGrid(self, value: bool) : self._showGrid = value

    @property
    def oneClickActivate(self) : return self._oneClickActivate

    @oneClickActivate.setter
    def oneClickActivate(self, value: bool) : self._oneClickActivate = value

    @property
    def hotTrackSelection(self) : return self._hotTrackSel

    @hotTrackSelection.setter
    def hotTrackSelection(self, value: bool) : self._hotTrackSel = value

    @property
    def headerClickable(self) : return self._hdrClickable

    @headerClickable.setter
    def headerClickable(self, value: bool) : self._hdrClickable = value

    @property
    def checkBoxLast(self) : return self._checkBoxLast

    @checkBoxLast.setter
    def checkBoxLast(self, value: bool) : self._checkBoxLast = value

    @property
    def headerBackColor(self) : return self._hdrBgColor

    @headerBackColor.setter
    def headerBackColor(self, value) :
        if isinstance(value, int):
            self._hdrBgColor.updateColor(value)
        elif isinstance(value, Color):
            self._hdrBgColor = value

    @property
    def headerForeColor(self) : return self._hdrFgColor

    @headerForeColor.setter
    def headerForeColor(self, value) :
        if isinstance(value, int):
            self._hdrFgColor.updateColor(value)
        elif isinstance(value, Color):
            self._hdrFgColor = value

    @property
    def headerFont(self) : return self._hdrFont

    @headerFont.setter
    def headerFont(self, value: Font): self._hdrFont = value

    @property
    def selectedItem(self) : return self._selItem

    @selectedItem.setter
    def selectedItem(self, value): self._selItem = value

    @property
    def viewStyle(self) : return self._viewStyle

    @viewStyle.setter
    def viewStyle(self, value): self._viewStyle = value
    # -endregion Properties

# End ListView


class ColumnAlign(Enum):
    LEFT = 0
    RIGHT = 1
    CENTER = 2


class ListViewColumn:

    """Class for representing ListView Column"""

    __slots__ = ("_drawNeed", "_isHotItem", "text", "width", "index", "imageIndex", "_order", "_hdrTxtFlag",
                "_bgColor", "_fgColor", "imageOnRight", "textAlign", "_hdrTxtAlign", "lvc")

    def __init__(self, hdr_txt: str, width: int, img:int = -1, img_right: bool = False) -> None:
        self.text = hdr_txt
        self.width = width
        self.imageIndex = img
        self.imageOnRight = img_right
        self.textAlign = ColumnAlign.LEFT
        self.index = -1
        self._hdrTxtAlign = ColumnAlign.CENTER
        self._isHotItem = False
        self._hdrTxtFlag = con.DT_SINGLELINE | con.DT_VCENTER | con.DT_CENTER | con.DT_NOPREFIX


    # @property
    # def index(self): return self._index

    @property
    def hasImage(self): return self.imageIndex > -1

    @property
    def headerTextAlign(self): return self._hdrTxtAlign

    @headerTextAlign.setter
    def headerTextAlign(self, value: TextAlignment):
        self._hdrTxtAlign = value
        match value:
            case ColumnAlign.LEFT:
                self._hdrTxtFlag = con.DT_SINGLELINE | con.DT_VCENTER | con.DT_LEFT | con.DT_NOPREFIX
            case ColumnAlign.RIGHT:
                self._hdrTxtFlag = con.DT_SINGLELINE | con.DT_VCENTER | con.DT_RIGHT | con.DT_NOPREFIX
            case ColumnAlign.CENTER:
                self._hdrTxtFlag = con.DT_SINGLELINE | con.DT_VCENTER | con.DT_CENTER | con.DT_NOPREFIX

    @property
    def backColor(self) : return self._bgColor

    @backColor.setter
    def backColor(self, value) :
        if isinstance(value, int):
            self._bgColor.updateColor(value)
        elif isinstance(value, Color):
            self._bgColor = value

    @property
    def foreColor(self) : return self._fgColor

    @foreColor.setter
    def foreColor(self, value) :
        if isinstance(value, int):
            self._fgColor.updateColor(value)
        elif isinstance(value, Color):
            self._fgColor = value


# End of ListViewColumn class=====================================================

class ListViewItem:
    _slots_ = ("_text", "_bgColor", "_fgColor", "_imgIndex", "_index", "_font", "_subitems")
    _stindex = 0

    def __init__(self, txt: str, bg_color: int = 0xFFFFFF, fg_color: int = 0x000000, imageIndex: int = -1) -> None:
        self._text = str(txt)
        self._bgColor = bg_color
        self._fgColor = fg_color
        self._imgIndex = imageIndex
        self._font = Font() # Start with default font Tahoma, 11 point
        self._index = ListViewItem._stindex
        self._subitems = []
        ListViewItem._stindex += 1

    @property
    def index(self): return self._index

    @property
    def subItems(self): return self._subitems

    @property
    def text(self): return self._text

    @text.setter
    def text(self, value: str):
        self._text = value

    @property
    def backColor(self) : return self._bgColor

    @backColor.setter
    def backColor(self, value) :
        if isinstance(value, int):
            self._bgColor.updateColor(value)
        elif isinstance(value, Color):
            self._bgColor = value

    @property
    def foreColor(self) : return self._fgColor

    @foreColor.setter
    def foreColor(self, value) :
        if isinstance(value, int):
            self._fgColor.updateColor(value)
        elif isinstance(value, Color):
            self._fgColor = value

    @property
    def imageIndex(self): return self._imgIndex

    @imageIndex.setter
    def imageIndex(self, value: int): self._imgIndex = value

    @property
    def font(self): return self._font

    @font.setter
    def font(self, value: Font): self._font = value





#/////////////////////////////////////////////////////////////////////////////////////
#//             Window Procedure, All actions are happening here                    //
#/////////////////////////////////////////////////////////////////////////////////////
# @WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR)
@SUBCLASSPROC
def lvWndProc(hw, msg, wp, lp, scID, refData) -> LRESULT:
    # log_msg(msg)
    lv = lvDict[hw]
    match msg:
        case con.WM_DESTROY:
            if lv._contextMenu: lv._contextMenu.destroyContextMenu()
            api.RemoveWindowSubclass(hw, lvWndProc, scID)
            lv._destroyCount += 1
            if lv._destroyCount == 2: del lvDict[hw]

        case con.WM_MEASUREITEM:
            print("msr item lv")

        case con.WM_CONTEXTMENU: lv._wmContextMenuHandler(lp)

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
                    # lv._itemIndex = nia.iItem
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
                            lvcd.clrTextBk = lv._bgColor.ref
                            lvcd.clrText = lv._fgColor.ref
                            return con.CDRF_NEWFONT | con.CDRF_DODEFAULT



                        # case ITEM_POSTPAINT :
                        #     # print(lvcd.iSubItem)
                        #     return con.CDRF_DODEFAULT
                        #     print(f"{lvcd.iSubItem = }, {lvcd.dwItemType = }, {lvcd.iPartId = }, {lvcd.iStateId = }")
                        #     lv._itemDrawn += 1

                        #     if lv._selectable:
                        #         # print(f"{lv._itemDrawn = }, {lv._itemIndex = }")
                        #         if lv._itemDrawn == lv._itemIndex:
                        #             lv._selectable = False
                        #             lvcd.clrTextBk = 0x0066FF99
                        #         else:
                        #             lvcd.clrTextBk = lv._bgColor.ref
                        #     else:
                        #         lvcd.clrTextBk = lv._bgColor.ref
                        #     if lv._itemDrawn == len(lv._items) - 1: lv._itemDrawn = -1
                        #     return con.CDRF_NEWFONT | con.CDRF_DODEFAULT
                    return con.CDRF_DODEFAULT
                case pointInRect: return 0


        case con.WM_NOTIFY:
            nmh = cast(lp, api.LPNMHDR).contents
            if nmh.code == con.NM_CUSTOMDRAW:
                nmcd = cast(lp, api.LPNMCUSTOMDRAW).contents
                # print(f"{nmcd.dwDrawStage = }, {con.CDDS_ITEMPOSTERASE = }")
                match nmcd.dwDrawStage:
                    case con.CDDS_PREPAINT: return con.CDRF_NOTIFYITEMDRAW
                    case con.CDDS_ITEMPREPAINT:
    #                   # We are taking the opprtunity to draw the headers from Control
                        lv._drawHeader(nmcd)
                        return con.CDRF_SKIPDEFAULT

        case con.WM_SETFOCUS: lv._gotFocusHandler()
        case con.WM_KILLFOCUS: lv._lostFocusHandler()
        case con.WM_LBUTTONDOWN: lv._leftMouseDownHandler(msg, wp, lp)
        case con.WM_LBUTTONUP: lv._leftMouseUpHandler(msg, wp, lp)
        case con.WM_RBUTTONDOWN: return lv._rightMouseDownHandler(msg, wp, lp)

        case con.WM_RBUTTONUP: lv._rightMouseUpHandler(msg, wp, lp)
        case con.WM_MOUSEWHEEL: lv._mouseWheenHandler(msg, wp, lp)
        case con.WM_MOUSEMOVE: lv._mouseMoveHandler(msg, wp, lp)
        case con.WM_MOUSELEAVE: lv._mouseLeaveHandler()

        case con.WM_COMMAND:
            print("WM_COMMAND on LV")

    return api.DefSubclassProc(hw, msg, wp, lp)

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#||             Window Procedure for Header control.                   ||
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
@WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR)
def hdrWndProc(hw, msg, wp, lp, scID, refData) -> LRESULT:
    # log_msg(msg)
    lv = lvDict[refData]
    match msg:
        case con.WM_DESTROY:
            res = api.RemoveWindowSubclass(hw, hdrWndProc, scID)
            lv._destroyCount += 1
            if lv._destroyCount == 2: del lvDict[lv._hwnd]

        case con.HDM_LAYOUT:
            if lv._changeHdrHeight:
                phl = cast(lp, api.LPHDLAYOUT).contents
                # res = api.DefSubclassProc(hw, msg, wp, lp)
                pos = phl.pwpos.contents
                prc = phl.prc.contents
                pos.flags = con.SWP_FRAMECHANGED
                pos.hwnd = hw
                pos.y = 0
                pos.x = prc.left
                pos.cx = prc.right - prc.left
                pos.cy = lv._hdrHeight
                prc.top = lv._hdrHeight

                return -1

        case con.WM_MOUSEMOVE:
            pt = getMousePoints(lp) # Collecting mouse points
            hit = api.HDHITTESTINFO(pt) # Passing it to this struct

            # This message will return the header item index under the mouse
            # We can use this index when we draw the header back color.
            lv._hotHdr = api.SendMessage(hw, con.HDM_HITTEST, 0, addressof(hit) )

        # Make the hot index to -1, so that our headers are drawn with normal colors after this.
        case con.WM_MOUSELEAVE: lv._hotHdr = -1

        case con.WM_PAINT:
            # First, let the control to do it's necessary drawings.
            api.DefSubclassProc(hw, msg, wp, lp)

            # Now, we can draw the last part of the header.
            hrc = RECT()
            api.SendMessage(lv._hdrHwnd, con.HDM_GETITEMRECT, len(lv._columns) - 1, addressof(hrc))
            rc = RECT(hrc.right + 1, hrc.top, lv._width, hrc.bottom)
            hdc = api.GetDC(hw)
            api.FillRect(hdc, byref(rc), lv._hdrBkBrush)
            api.ReleaseDC(hw, hdc)
            return 0


    return api.DefSubclassProc(hw, msg, wp, lp)
