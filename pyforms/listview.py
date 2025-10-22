# listview module - Created on 02-Jan-2023 21:21:20

import typing
from enum import Enum
from ctypes.wintypes import HWND, UINT
from ctypes import WINFUNCTYPE, byref, addressof, cast, c_wchar_p
from pyforms.control import Control

import pyforms.constants as con
from pyforms.commons import (Font, MyMessages, getMousePoints, 
                                StaticData, log_cnt)
from pyforms.enums import ControlType, TextAlignment, ListViewStyle
from pyforms.apis import (LRESULT, UINT_PTR, DWORD_PTR, 
                            RECT, LPNMCUSTOMDRAW, LVCOLUMNW,
                            WPARAM, LPARAM, SUBCLASSPROC)
import pyforms.apis as api
from pyforms.events import GEA, LVSelChangedEventArgs, LVItemCheckEventArgs
from pyforms.colors import Color, COLOR_WHITE
from pyforms.winmsgs import log_msg
# from horology import timed
# from horology import Timing

lvDict = {}
hdrDict = {}
# lvStyle = con.LVS_ALIGNLEFT|con.LVS_EDITLABELS|con.WS_BORDER
LV_VIEW_ICON            = 0x0000
LV_VIEW_DETAILS         = 0x0001
LV_VIEW_SMALLICON       = 0x0002
LV_VIEW_LIST            = 0x0003
LV_VIEW_TILE            = 0x0004
LV_VIEW_MAX             = 0x0004
LVS_EX_DOUBLEBUFFER     = 0x00010000
HDI_FORMAT = 0x0004
HDF_OWNERDRAW = 0x8000
ITEM_POSTPAINT = (con.CDDS_SUBITEM | con.CDDS_ITEMPOSTPAINT) - 1

# ListViewColumn = typing.TypeVar("ListViewColumn")
# ListViewItem = typing.TypeVar("ListViewItem")
# Form = typing.TypeVar("Form")
SKIPDEFAULT_DRAW = typing.TypeVar("SKIPDEFAULT_DRAW")
HDR_CUST_DRAW = 7500
excep_repstyle = "Adding row is possible only in ListViewStyle.REPORT_VIEW"
excep_iscreate = "Adding  row is possible only after ListView's handle created"
excep_hasitems = "At least one item must be provided"
class ColAndIndex:
    def __init__(self, indx: int, col: LVCOLUMNW) -> None:
        self.index = indx
        self.lvc = col

class ListView(Control):

    """ListView control
    __init__ takes 'cols' and you can pass the column names &
    widths in single list. """
    Control.icc.initCommCtls(con.ICC_LISTVIEW_CLASSES)
    _count = 1
    __slots__ = ("_selIndex", "_selItem", "_selItems", "_editLabel", "_lblHwnd", 
                 "_hdrHwnd", "_itemTopAlign", "_hideSel",
                 "_multiSel", "_checkBox", "_fullRowSel", 
                 "_showGrid", "_oneClickAct", "_hotTrackSel",
				"_noHdr", "_changeHdrHeight", "_hdrDrawFont", 
                "_setCBLast", "_cbIsLast", "_cbChecked",
				"_hdrFont", "_colAlign", "_viewStyle", "_columns", 
                "_items", "_colIndList", "_colIndex", "_hdrHeight", 
                "_selItemIndex", "_selSubIndex", "_imgList", 
                "_hdrItemDict", "_hdrPts", "_mouseOnHdr",
                "_hdrBgColor", "_hdrFgColor", "_hdrBkBrush", 
                "_hdrOwnDraw", "_hotHdr", "_colIndex", "_hdrHotBrush", 
                "_hdrClickable", "_selectable", "_itemIndex", 
                "_itemDrawn", "_destroyCount", "_layCount",
                 "onItemActivate", "onSelectionChanged", "onItemCheckChanged",
                 "onItemClick", "onItemDoubleClick" )

    def __init__(self, parent, xpos: int = 10, ypos: int = 10, 
                 width: int = 250, height: int = 200, cols = None) -> None:
        super().__init__(parent, ControlType.LIST_VIEW, width, height)
        self.name = f"ListView_{ListView._count}"
        self._xpos = xpos
        self._ypos = ypos
        self._isTextable = False
        self._style |= con.LVS_ALIGNLEFT|con.LVS_EDITLABELS|con.WS_BORDER
        self._exStyle = 0
        self._text = None
        self._columns = []
        self._items = []
        self._colIndList = []
        self._selItems = None
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
        self._hdrFont = Font(StaticData.defHfont) 
        self._selectable = False
        self._itemIndex = 0
        self._itemDrawn = -1
        self._hdrOwnDraw = False
        self._changeHdrHeight = True
        self._hdrHeight = 25
        self._hotHdr = -1
        self._colIndex = 0
        self._destroyCount = 0
        self._layCount = 0
        self._selItem = None

        self.onItemActivate = None
        self.onSelectionChanged = None
        self.onItemCheckChanged = None
        self.onItemClick = None
        self.onItemDoubleClick = None
        parent._controls.append(self)
        # Events

        ListView._count += 1
        if parent.createChilds: self.createHandle()
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
                    api.SendMessage(self._hwnd, con.LVM_INSERTCOLUMNW, 
                                    col.index, addressof(col.lvc))

            self._hdrHwnd = api.SendMessage(self._hwnd, con.LVM_GETHEADER, 0, 0)
            if self._hdrFont._handle == 0: 
                self._hdrFont.createHandle()

            # We are going to send the list view hwnd with this function. So, we can grab it inside
            # header's wndproc function.
            api.SetWindowSubclass(self._hdrHwnd, hdrWndProc, ListView._count, self._hwnd)
            if self._bgColor.value != COLOR_WHITE.value:
                api.SendMessage(self._hwnd, con.LVM_SETBKCOLOR, 0, self._bgColor.ref)

            if self._cbIsLast:
                ord_list = self._changeColOrder()
                api.SendMessage(self._hwnd, con.LVM_SETCOLUMNORDERARRAY, 
                                len(ord_list), addressof(ord_list))
                self._cbIsLast = True

    def printCons(self):
        print(f"{con.NM_CLICK=}")
        print(f"{con.NM_DBLCLK=}")
        print(f"{con.LVN_ITEMCHANGED=}")
        print(f"{con.NM_CUSTOMDRAW=}")
        print(f"{con.NM_SETFOCUS=}")
        print(f"{con.LVN_ITEMACTIVATE=}")

    
    def newRowItem(self, *items, bgc=0xffffff, fgc=0x000000):
        if self._viewStyle != ListViewStyle.REPORT_VIEW: 
            raise Exception(excep_repstyle)
        
        if not self._isCreated: raise Exception(excep_iscreate)
        fitem = items[0] if isinstance(items[0], str) else str(items[0])
        lvitem = ListViewItem(fitem, bgc, fgc)
        lvitem._index = self._itemIndex
        lvitem._pHwnd = self._hwnd
        if bgc != 0xffffff: lvitem._bgdraw = True
        if fgc != 0x000000: lvitem._fgdraw = True
        self._itemIndex += 1
        self._addItemInternal(lvitem)
        for i in range(1, len(items)):
            self._addSubItemInternal(items[i], lvitem._index, i)

        return lvitem

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


    # def getRow(self, index):
    #     if self._viewStyle != ListViewStyle.REPORT_VIEW: 
    #         raise Exception(excep_repstyle)
    #     if not self._isCreated: raise Exception(excep_iscreate)
    #     if not items: raise Exception(excep_hasitems)
        
  



    def addRow(self, *items):
        if self._viewStyle != ListViewStyle.REPORT_VIEW: 
            raise Exception(excep_repstyle)
        if not self._isCreated: raise Exception(excep_iscreate)
        if not items: raise Exception(excep_hasitems)
        if not isinstance(items[0], str): 
            fitem = str(items[0])
        else:
            fitem    = items[0]
        lvi = ListViewItem(fitem)
        lvi._index = self._itemIndex
        lvi._pHwnd = self._hwnd
        self._itemIndex += 1
        self._addItemInternal(lvi)
        for i in range(1, len(items)):
            self._addSubItemInternal(items[i], lvi._index, i)


    def clear(self):
        """Deletes all items in list view"""
        if self._isCreated and len(self._items):
            x = self._sendMsg(con.LVM_DELETEALLITEMS, 0, 0)
            if x: 
                self._items.clear()
                self._itemIndex = 0
            return x
        return -1

    def setChecState(self, value, itemIndex = -1):
        if self._checkBox and len(self._items):
            if itemIndex > -1:
                # user wants to set the state of a specific item.
                self._items[itemIndex].checked = value
            else:
                # user wants to set the state for all items.
                # i=unchecked & 2=checked, so shift left 12 bits
                nstate = 2 << 12  if value else 1 << 12
                lvitem = api.LVITEMW()
                lvitem.mask = con.LVIF_STATE
                lvitem.stateMask = con.LVIS_STATEIMAGEMASK
                lvitem.state = nstate
                self._sendMsg(con.LVM_SETITEMSTATE, -1, addressof(lvitem))

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
        if self._noHdr: self._style |= con.LVS_NOCOLUMNHEADER
        if self._hideSel:
            self._style &= ~con.LVS_SHOWSELALWAYS   # Clear the bit
        else:
            self._style |= con.LVS_SHOWSELALWAYS    # Set the bit

        if self._multiSel:
            self._style &= ~con.LVS_SINGLESEL   # Clear the bit (enable multi-select)
            self._selItems = []
        else:
            self._style |= con.LVS_SINGLESEL    # Set the bit (disable multi-select)

        # Set some brushes
        self._hdrBkBrush = self._hdrBgColor.createHBrush()
        self._hdrHotBrush = self._hdrBgColor.createHBrush(1.09)


    def _setLVExStyles(self):
        # Setup the different ex styles for this list view
        lv_ex_style = LVS_EX_DOUBLEBUFFER # 0x0000
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
        Control._smBuffer.fillBuffer(lvcol.text)
        lvcol.index = self._colIndex
        lvc = LVCOLUMNW()
        lvc.mask = con.LVCF_TEXT  | con.LVCF_WIDTH | con.LVCF_FMT | con.LVCF_SUBITEM
        lvc.fmt = lvcol.textAlign.value
        lvc.cx = lvcol.width
        lvc.pszText = cast(Control._smBuffer.addr, c_wchar_p)
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
        Control._smBuffer.fillBuffer(item.text)
        lvi = api.LVITEMW()
        lvi.mask = con.LVIF_TEXT | con.LVIF_PARAM | con.LVIF_STATE
        if item._imgIndex != -1: lvi.mask |= con.LVIF_IMAGE
        lvi.state = 0
        lvi.stateMask = 0
        lvi.iItem = item._index
        lvi.iSubItem = 0
        lvi.iImage = item._imgIndex
        lvi.pszText = cast(Control._smBuffer.addr, c_wchar_p)
        lvi.cchTextMax = len(item._text) + 1
        lvi.lParam = id(item)

        # We need to fill our items list before sending the message.
        # Because, we will get LVN_ITEMCHANGED notification before,
        # SendMessage returns. So when we got the notification there,
        # we need our items list prepared. Otherwise nasty index errors will happen.
        self._items.append(item) 
        res = api.SendMessage(self._hwnd, con.LVM_INSERTITEMW, 0, addressof(lvi))
        if res == -1: self._items.pop()
        


    def _addSubItemInternal(self, subitem: str, item_index: int, sub_index: int, imageIndex: int = -1):
        # print(f"{item_index=}, {self._items}")
        sitem = subitem if isinstance(subitem, str) else str(subitem)
        Control._smBuffer.fillBuffer(sitem)
        lvi = api.LVITEMW()
        lvi.iSubItem = sub_index
        lvi.pszText = cast(Control._smBuffer.addr, c_wchar_p)
        lvi.iImage = imageIndex

        # Storing sitem in subitems list before sending the message is crucial.
        # Because we will get LVN_ITEMCHANGED notification before SendMessage return.
        self._items[item_index]._subitems.append(sitem)

        res = api.SendMessage(self._hwnd, con.LVM_SETITEMTEXTW, item_index, addressof(lvi))
        if res == 0: self._items[item_index]._subitems.pop()


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

        api.SelectObject(nmcd.hdc, self._hdrFont._handle)
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

        # api.DrawText(nmcd.hdc, col._wideText, -1, byref(nmcd.rc), col._hdrTxtFlag )
        api.DrawText(nmcd.hdc, col.text, len(col.text), byref(nmcd.rc), col._hdrTxtFlag )

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
    def hasCheckBox(self): return self._checkBox

    @hasCheckBox.setter
    def hasCheckBox(self, value): self._checkBox = value

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
    _slots_ = ("_text", "_bgColor", "_fgColor", "_imgIndex", 
                "_index", "_font", "_subitems", "_checked",
                "_pHwnd", "_bgdraw", "_fgdraw")
    

    def __init__(self, txt: str, bg_color: int = 0xFFFFFF, 
                 fg_color: int = 0x000000, imageIndex: int = -1) -> None:
        # Don't forget to set the _index & _pHwnd later.
        self._text = str(txt)
        self._bgColor = Color(bg_color)
        self._fgColor = Color(fg_color)
        self._imgIndex = imageIndex
        self._font = Font(StaticData.defHfont) # Start with default font Tahoma, 11 point
        self._index = -1
        self._checked = False
        self._pHwnd = None # Parent handle.
        self._subitems = []
        self._bgdraw = False
        self._fgdraw = False
        

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
        self._bgdraw = True
        

    @property
    def foreColor(self) : return self._fgColor

    @foreColor.setter
    def foreColor(self, value) :
        if isinstance(value, int):
            self._fgColor.updateColor(value)
        elif isinstance(value, Color):
            self._fgColor = value
        self._fgdraw = True

    @property
    def imageIndex(self): return self._imgIndex

    @imageIndex.setter
    def imageIndex(self, value: int): self._imgIndex = value

    @property
    def font(self): return self._font

    @font.setter
    def font(self, value: Font): 
        self._font = value
        self._setFontInternal()

    @property
    def checked(self): return self._checked

    @checked.setter
    def checked(self, value):
        item = api.LVITEMW()
        item.mask = con.LVIF_STATE
        item.iItem = self._index
        item.stateMask = con.LVIS_STATEIMAGEMASK
        item.state = (2 if value else 1) << 12  # 2 = checked, 1 = unchecked
        api.SendMessage(self._pHwnd, con.LVM_SETITEMSTATE, self._index, addressof(item))
        

    def __repr__(self):
        return self._text

notif_codes = {
    4294967196: "LVN_ITEMCHANGING",
    4294967194: "LVN_INSERTITEM",
    4294967294: "NM_CLICK",
    4294967293: "NM_DBLCLK",
    4294967195: "LVN_ITEMCHANGED",
    4294967284: "NM_CUSTOMDRAW",
    4294967289: "NM_SETFOCUS",
    4294967182: "LVN_ITEMACTIVATE"
}

#/////////////////////////////////////////////////////////////////////////////////////
#//             Window Procedure, All actions are happening here                    //
#/////////////////////////////////////////////////////////////////////////////////////
# @WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR)
@SUBCLASSPROC
def lvWndProc(hw, msg, wp, lp, scID, refData) -> LRESULT:
    # log_msg(msg)
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, lvWndProc, scID)
            lv = lvDict[hw]
            lv._destroyCount += 1
            if lv._destroyCount == 2: del lvDict[hw]

        # case con.WM_MEASUREITEM:
        #     print("msr item lv")

        case con.WM_CONTEXTMENU: 
            lv = lvDict[hw]
            lv._wmContextMenuHandler(lp)

        case MyMessages.CTRL_NOTIFY:
            lv = lvDict[hw]
            nmh = cast(lp, api.LPNMHDR).contents
            # if lv.name == "ListView_2":
            #     ncode = notif_codes.get(nmh.code, nmh.code)
                # log_cnt(f"{ncode=}")
            if nmh.code == con.NM_CLICK:                    
                if lv.onItemClick and len(lv._items): 
                    nmia = cast(lp, api.LPNMITEMACTIVATE).contents
                    sitem = lv._items[nmia.iItem]
                    lv.onItemClick(lv, sitem)
                    
            elif nmh.code == con.NM_DBLCLK:                    
                if lv.onItemDoubleClick and len(lv._items): 
                    nmia = cast(lp, api.LPNMITEMACTIVATE).contents
                    sitem = lv._items[nmia.iItem]
                    lv.onItemDoubleClick(lv, sitem)

            elif nmh.code == con.LVN_ITEMCHANGED:
                nmlv = cast(lp, api.LPNMLISTVIEW).contents
                # print(nmlv)
                if nmlv.uChanged & con.LVIF_STATE:
                    nowSelected = (nmlv.uNewState & con.LVIS_SELECTED)
                    wasSelected = (nmlv.uOldState & con.LVIS_SELECTED)
                    if nowSelected and not wasSelected:
                        sitem = lv._items[nmlv.iItem]
                        if lv._multiSel:
                            lv._selItems.append(sitem)
                        else:
                            lv._selItem = sitem
                        if lv.onSelectionChanged: 
                            lsea = LVSelChangedEventArgs(sitem, nmlv.iItem, nowSelected)
                            lv.onSelectionChanged(lv, lsea)
                                                    
                    elif not nowSelected and wasSelected:
                        sitem = lv._items[nmlv.iItem]
                        if lv._multiSel:
                            lv._selItems.remove(sitem)                                
                            if lv.onSelectionChanged: 
                                lsea = LVSelChangedEventArgs(sitem, nmlv.iItem, nowSelected)
                                lv.onSelectionChanged(lv, lsea)
                        
                    #end if---------------------------------------------
                    # ✅ Check for checkbox state change
                    state_index = (nmlv.uNewState & con.LVIS_STATEIMAGEMASK) >> 12
                    old_state_index = (nmlv.uOldState & con.LVIS_STATEIMAGEMASK) >> 12

                    if state_index != old_state_index: # Item checkbox changed
                        is_checked = (state_index == 2)  # 2 = checked, 1 = unchecked
                        # print(nmlv)
                        if len(lv._items):                               
                            sitem = lv._items[nmlv.iItem]
                            # if lv.name == "ListView_2":
                            #     print(f"P{lv._items=}, {sitem._subitems=}")
                            sitem._checked = is_checked  
                            if lv.onItemCheckChanged:
                                licea = LVItemCheckEventArgs(sitem, nmlv.iItem, is_checked)
                                lv.onItemCheckChanged(lv, licea)
                        # print(f"Item {nmlv.iItem} checkbox changed to: {is_checked}")
                    
            elif nmh.code == con.NM_SETFOCUS:pass
                # log_cnt("NM_SETFOCUS")
                # print("NM_SETFOCUS = NM_FIRST - 7")

            elif nmh.code == con.NM_CUSTOMDRAW:
                # log_cnt("NM_CUSTOMDRAW")
                lvcd = cast(lp, api.LPNMLVCUSTOMDRAW).contents
                # print(lvcd.nmcd.dwDrawStage, con.CDDS_SUBITEM | con.CDDS_ITEMPOSTPAINT)
                if lvcd.nmcd.dwDrawStage == con.CDDS_PREPAINT:
                    return con.CDRF_NOTIFYITEMDRAW # con.CDRF_NOTIFYITEMDRAW

                if lvcd.nmcd.dwDrawStage == con.CDDS_ITEMPREPAINT:
                    # print(f"{lvcd.nmcd.dwItemSpec=}")
                    lvitem = lvDict[hw]._items[lvcd.nmcd.dwItemSpec]
                    if lvitem._bgdraw: lvcd.clrTextBk = lvitem._bgColor.ref
                    if lvitem._fgdraw: lvcd.clrText = lvitem._fgColor.ref
                    return con.CDRF_NEWFONT #| con.CDRF_DODEFAULT                        

            elif nmh.code == con.LVN_ITEMACTIVATE:
                if lv.onItemActivate: lv.onItemActivate(lv, GEA)
                return con.CDRF_DODEFAULT
            
            # end wm_notify from parent--------------------------------------------


        case con.WM_NOTIFY:
            nmh = cast(lp, api.LPNMHDR).contents
            if nmh.code == con.NM_CUSTOMDRAW:
                nmcd = cast(lp, api.LPNMCUSTOMDRAW).contents
                # print(f"{nmcd.dwDrawStage = }, {con.CDDS_ITEMPOSTERASE = }")
                match nmcd.dwDrawStage:
                    case con.CDDS_PREPAINT: return con.CDRF_NOTIFYITEMDRAW
                    case con.CDDS_ITEMPREPAINT:
                        lv = lvDict[hw]
    #                   # We are taking the opprtunity to draw the headers from Control
                        lv._drawHeader(nmcd)
                        return con.CDRF_SKIPDEFAULT

        case con.WM_SETFOCUS: 
            lv = lvDict[hw]
            lv._gotFocusHandler()
        case con.WM_KILLFOCUS: 
            lv = lvDict[hw]
            lv._lostFocusHandler()
        case con.WM_LBUTTONDOWN: 
            lv = lvDict[hw]
            lv._leftMouseDownHandler(msg, wp, lp)
        case con.WM_LBUTTONUP: 
            lv = lvDict[hw]
            lv._leftMouseUpHandler(msg, wp, lp)
        case con.WM_RBUTTONDOWN: 
            lv = lvDict[hw]
            return lv._rightMouseDownHandler(msg, wp, lp)

        case con.WM_RBUTTONUP: 
            lv = lvDict[hw]
            lv._rightMouseUpHandler(msg, wp, lp)
        case con.WM_MOUSEWHEEL: 
            lv = lvDict[hw]
            lv._mouseWheenHandler(msg, wp, lp)
        case con.WM_MOUSEMOVE: 
            lv = lvDict[hw]
            lv._mouseMoveHandler(msg, wp, lp)
        case con.WM_MOUSELEAVE: 
            lv = lvDict[hw]
            lv._mouseLeaveHandler()

        # case con.WM_COMMAND:
        #     print("WM_COMMAND on LV")

    return api.DefSubclassProc(hw, msg, wp, lp)

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#||             Window Procedure for Header control.                   ||
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
@WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR)
def hdrWndProc(hw, msg, wp, lp, scID, refData) -> LRESULT:
    # log_msg(msg)
    match msg:
        case con.WM_DESTROY:
            lv = lvDict[refData]
            res = api.RemoveWindowSubclass(hw, hdrWndProc, scID)
            lv._destroyCount += 1
            if lv._destroyCount == 2: del lvDict[lv._hwnd]

        case con.HDM_LAYOUT:
            lv = lvDict[refData]
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
            lv = lvDict[refData]
            pt = getMousePoints(lp) # Collecting mouse points
            hit = api.HDHITTESTINFO(pt) # Passing it to this struct

            # This message will return the header item index under the mouse
            # We can use this index when we draw the header back color.
            lv._hotHdr = api.SendMessage(hw, con.HDM_HITTEST, 0, addressof(hit) )

        # Make the hot index to -1, so that our headers are drawn with normal colors after this.
        case con.WM_MOUSELEAVE: 
            lv = lvDict[refData]
            lv._hotHdr = -1

        case con.WM_PAINT:
            lv = lvDict[refData]
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
