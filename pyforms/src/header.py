#Header module - Created on 17-Apr-2023 18:17:00

from ctypes import byref, create_unicode_buffer, cast, c_wchar_p, addressof
from pyforms.src.control import Control
import pyforms.src.constants as con
from pyforms.src.commons import MyMessages, Font
from pyforms.src.enums import ControlType, TextAlignment, HeaderStyle
from pyforms.src.events import EventArgs, HeaderEventArgs
from pyforms.src.apis import SUBCLASSPROC, LPNMCUSTOMDRAW, LPRECT, LPWINDOWPOS
import pyforms.src.apis as api
from pyforms.src.colors import Color

from pyforms.src.winmsgs import log_msg

hdrDict = {}
hdrStyle = con.WS_VISIBLE | con.WS_CHILD | con.HDS_BUTTONS | con.HDS_HORZ #| con.WS_BORDER
defItems = ["Item1", "Item2", "Item3"]

class CurveInfo:
    def __init__(self, bgc) -> None:
        lum = bgc.luminance()
        tbAdj = 0
        dhAdj = 1.2
        if lum > 200: tbAdj = 0.9
        elif lum > 150 and lum < 201: tbAdj = 0.8
        elif lum > 100 and lum < 151: tbAdj = 0.7
        elif lum > 50 and lum < 101: tbAdj = 0.6
        elif lum > 0 and lum < 51: tbAdj = 0.5

        if lum > 200: dhAdj = 1.25
        if lum < 100: dhAdj = 0.8

        self.topDefColor = bgc
        self.botDefColor = bgc.getShadedColor(tbAdj)

        self.topHotColor = bgc.getShadedColor(dhAdj)
        self.botHotColor = self.topHotColor.getShadedColor(tbAdj)

        self.topDefBrush = self.topDefColor.createHBrush()
        self.botDefBrush = self.botDefColor.createHBrush()
        self.topHotBrush = self.topHotColor.createHBrush()
        self.botHotBrush = self.botHotColor.createHBrush()

        self.topRect = api.RECT()
        self.botRect = api.RECT()



class HeaderItem:
    __slots__ = ("text", "index", "width", "bgColor", "fgColor", "_defBrush", "_hotBrush", "_divPen", "_bgcChanged", "_borderBrush",
                "_curveInfo", "onClick")
    def __init__(self, txt, indx, wdth, bgc = 0xe9d8a6, fgc = 0x000000) -> None:
        self.text = txt
        self.index = indx
        self.width = wdth
        self.bgColor = Color(bgc)
        self.fgColor = Color(fgc)
        self._bgcChanged = False
        self._defBrush = self.bgColor.createHBrush()
        self._hotBrush = self.bgColor.createHBrush(1.1)
        self._borderBrush = self.bgColor.createHBrush(0.6)
        self._curveInfo = None
        #Events
        self.onClick = None


    def _getTwoRects(self, rc):
        # We need to get two rect from given rc.
        tBottom = (rc.bottom - rc.top ) // 2
        # bTop = (rc.bottom - rc.top) //
        self._curveInfo.topRect = api.RECT(rc.left, rc.top, rc.right, tBottom)
        self._curveInfo.botRect = api.RECT(rc.left, tBottom, rc.right, rc.bottom)




class Header(Control):

    _count = 1
    __slots__ = ("_noSizing", "_flatHdr", "_hotTrack", "_hasCB", "_txtAlign", "_items", "_hotIndex", "_hotBrush", "_txtFlag", "cnt",
                "_hdrStyle", "_cdSet", "_itemIndex", "onDrag", "_drawFunc")
    def __init__(self, parent, xpos: int = 10, ypos: int = 10, width: int = 0, height: int = 25 ) -> None:
        super().__init__()
        self._clsName = "SysHeader32"
        self.name = f"Header_{Header._count}"
        self._ctlType = ControlType.HEADER
        self._parent = parent
        self._bgColor = Color(0xe9d8a6) # foreColor is setting in Control's init
        self._font = parent._font
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._isTextable = True
        self._style = hdrStyle
        self._exStyle = 0x00000000
        self._noSizing = False
        self._flatHdr = False
        self._hotTrack = True
        self._hasCB = False
        self._txtAlign = TextAlignment.CENTER
        self._items = []
        self._hasBrush = True
        self._hotIndex = -1
        self._hotBrush = None
        self._cdSet = False
        self._hdrStyle = HeaderStyle.FLAT
        self._txtFlag = con.DT_SINGLELINE | con.DT_VCENTER | con.DT_CENTER | con.DT_NOPREFIX
        self._drawFunc = self._drawFlatHeader
        # self._dividerPen = self._bgColor.createHPen(0.5)
        self.cnt = 1
        self._itemIndex = 0
        # Events
        self.onDrag = None
        self._hwnd = None
        parent._controls.append(self)
        Header._count += 1


    # -region Public funcs
    def createHandle(self):
        """Create handle for this Header"""
        self._setStyles()
        self._createControl()
        if self._hwnd:
            hdrDict[self._hwnd] = self
            self._setSubclass(hdrWndProc)
            self._setFontInternal()
            self._insertItemsInternal()
            self._checkCurveData()


    def addItem(self, itemTxt, width, bgc = None, fgc = 0x000000):
        if bgc == None: bgc = self._bgColor.value
        hItem = HeaderItem(itemTxt, self._itemIndex, width, bgc, fgc)
        if bgc != None and bgc != self._bgColor.value: hItem._bgcChanged = True
        if self._isCreated: self._insertItemInternal(hItem)
        self._items.append(hItem)
        self._itemIndex += 1
        self._width += width

    # -endregion Public funcs
    # -region Private funcs

    # Set the styles this Header
    def _setStyles(self):
        if self._noSizing: self._style |= con.HDS_NOSIZING
        if self._flatHdr: self._style |= con.HDS_FLAT
        if self._hotTrack: self._style |= con.HDS_HOTTRACK
        if self._hasCB: self._style |= con.HDS_CHECKBOXES
        self._bkgBrush = api.CreateSolidBrush(self._bgColor.ref)
        self._hotBrush = self._bgColor.createHBrush(1.3)


    def _checkCurveData(self):
        # If user wants to use curved header, we need to set the info for drawing curved header
        if self._hdrStyle == HeaderStyle.CURVED and not self._cdSet:
            for item in self._items:
                item._curveInfo = CurveInfo(item.bgColor)
            self._cdSet = True
        if self._hdrStyle == HeaderStyle.CURVED: self._drawFunc = self._drawCurvedHeader


    def _insertItemsInternal(self):
        if len(self._items):
            for item in self._items:
                hdi = api.HDITEM()
                hdi.cxy = item.width
                hdi.mask = con.HDI_TEXT | con.HDI_FORMAT | con.HDI_WIDTH
                hdi.pszText = cast(item.text, c_wchar_p)
                hdi.cchTextMax = len(item.text)
                hdi.fmt = con.HDF_LEFT | con.HDF_STRING
                api.SendMessage(self._hwnd, con.HDM_INSERTITEMW, item.index, addressof(hdi))


    def _insertItemInternal(self, item: HeaderItem):
        hdi = api.HDITEM()
        hdi.cxy = item.width
        hdi.mask = con.HDI_TEXT | con.HDI_FORMAT | con.HDI_WIDTH
        hdi.pszText = cast(item.text, c_wchar_p)
        hdi.cchTextMax = len(item.text)
        hdi.fmt = con.HDF_LEFT | con.HDF_STRING
        api.SendMessage(self._hwnd, con.HDM_INSERTITEMW, item.index, addressof(hdi))



    def _drawFlatHeader(self, nmcd: LPNMCUSTOMDRAW) -> int:
        self.findHotItem()
        item = self._items[nmcd.dwItemSpec] # Get our item
        if nmcd.uItemState & con.CDIS_SELECTED:
            nmcd.rc.left += 1
            nmcd.rc.top += 1
            api.FillRect(nmcd.hdc, byref(nmcd.rc), item._defBrush)
            api.FrameRect(nmcd.hdc, byref(nmcd.rc), item._borderBrush)

        else:
            if nmcd.dwItemSpec == self._hotIndex: # Mouse over
                api.FillRect(nmcd.hdc, byref(nmcd.rc), item._hotBrush)
                api.FrameRect(nmcd.hdc, byref(nmcd.rc), item._borderBrush)
            else: # Default color
                api.FillRect(nmcd.hdc, byref(nmcd.rc), item._defBrush)
                api.DrawEdge(nmcd.hdc, byref(nmcd.rc), con.BDR_RAISEDINNER, con.BF_BOTTOMRIGHT)

        api.SetBkMode(nmcd.hdc, con.TRANSPARENT)
        api.SelectObject(nmcd.hdc, self._font._hwnd)
        api.SetTextColor(nmcd.hdc, self._fgColor.ref)
        api.DrawText(nmcd.hdc, item.text, -1, byref(nmcd.rc), self._txtFlag )

    def _drawCurvedHeader(self, nmcd: LPNMCUSTOMDRAW) -> int:
        self.findHotItem()
        item = self._items[nmcd.dwItemSpec] # Get our item
        item._getTwoRects(nmcd.rc)
        if nmcd.uItemState & con.CDIS_SELECTED:
            nmcd.rc.left += 1
            nmcd.rc.top += 1
            item._curveInfo.topRect.left += 1
            item._curveInfo.botRect.left += 1
            item._curveInfo.topRect.top += 1

            api.FillRect(nmcd.hdc, byref(item._curveInfo.topRect), item._curveInfo.topDefBrush)
            api.FillRect(nmcd.hdc, byref(item._curveInfo.botRect), item._curveInfo.botDefBrush)
            api.FrameRect(nmcd.hdc, byref(nmcd.rc), item._borderBrush)

        else:
            if nmcd.dwItemSpec == self._hotIndex: # Mouse over
                # api.FillRect(nmcd.hdc, byref(nmcd.rc), item._hotBrush)
                api.FillRect(nmcd.hdc, byref(item._curveInfo.topRect), item._curveInfo.topHotBrush)
                api.FillRect(nmcd.hdc, byref(item._curveInfo.botRect), item._curveInfo.botHotBrush)
                api.FrameRect(nmcd.hdc, byref(nmcd.rc), item._borderBrush)
            else: # Default color
                # api.FillRect(nmcd.hdc, byref(nmcd.rc), item._defBrush)
                api.FillRect(nmcd.hdc, byref(item._curveInfo.topRect), item._curveInfo.topDefBrush)
                api.FillRect(nmcd.hdc, byref(item._curveInfo.botRect), item._curveInfo.botDefBrush)
                api.FrameRect(nmcd.hdc, byref(nmcd.rc), item._borderBrush)
                # api.DrawEdge(nmcd.hdc, byref(nmcd.rc), con.BDR_RAISEDINNER, con.BF_BOTTOMRIGHT)

        api.SetBkMode(nmcd.hdc, con.TRANSPARENT)
        api.SelectObject(nmcd.hdc, self._font._hwnd)
        api.SetTextColor(nmcd.hdc, self._fgColor.ref)
        api.DrawText(nmcd.hdc, item.text, -1, byref(nmcd.rc), self._txtFlag )



    # Reset the back gound brush for this Header
    def resetBrush(self): self._bkgBrush = self._bgColor.createHBrush()

    def findHotItem(self):
        pt = api.POINT()
        api.GetCursorPos(byref(pt))
        api.ScreenToClient(self._hwnd, byref(pt))
        hit = api.HDHITTESTINFO(pt) # Passing it to this struct
        self._hotIndex = api.SendMessage(self._hwnd, con.HDM_HITTEST, 0, addressof(hit) )

    # -endregion Private funcs
    # -region Properties

    @property
    def items(self):
        """Returns true if auto size is set"""
        return self._items

    # @autoSize.setter
    # def autoSize(self, value: bool):
    #     """Set true if auto size set"""
    #     self._autoSize = value

    @property
    def style(self):
        """Returns the drawing style"""
        return self._hdrStyle

    @style.setter
    def style(self, value: HeaderStyle):
        """Set the drawing style"""
        self._hdrStyle = value
        if value == HeaderStyle.CURVED:
            if len(self._items):
                for item in self._items:
                    item._curveInfo = CurveInfo(item._bgColor)
                self._cdSet = True


    # @property
    # def textAlign(self):
    #     """Returns the text alignment mode. Check for TextAlignment enum"""
    #     return self._txtAlign

    # @textAlign.setter
    # def textAlign(self, value: TextAlignment):
    #     """Set the text alignment mode. Check for TextAlignment enum"""
    #     self._txtAlign = value

    # @property
    # def borderStyle(self):
    #     """Returns the border style. Check for HeaderBorder enum"""
    #     return self._borderStyle

    # @borderStyle.setter
    # def borderStyle(self, value: HeaderBorder):
    #     """set the border style. Check for HeaderBorder enum"""
    #     self._borderStyle = value

    # -endregion Properties

#End Header


@SUBCLASSPROC
def hdrWndProc(hw, msg, wp, lp, scID, refData):
    # log_msg(msg)
    this = hdrDict[hw]
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, hdrWndProc, scID)
            del hdrDict[hw]

        case con.WM_SETFOCUS: this._gotFocusHandler()
        case con.WM_KILLFOCUS: this._lostFocusHandler()
        # case con.WM_LBUTTONDOWN: this._leftMouseDownHandler(msg, wp, lp)
        # case con.WM_LBUTTONUP: this._leftMouseUpHandler(msg, wp, lp)
        # case con.WM_RBUTTONDOWN: this._rightMouseDownHandler(msg, wp, lp)
        # case con.WM_RBUTTONUP: this._rightMouseUpHandler(msg, wp, lp)
        case con.WM_MOUSEWHEEL: this._mouseWheenHandler(msg, wp, lp)
        case con.WM_MOUSEMOVE: this._mouseMoveHandler(msg, wp, lp)
        case con.WM_MOUSELEAVE: this._mouseLeaveHandler()

        case MyMessages.CTRL_NOTIFY:
            nmh = cast(lp, api.LPNMHDR).contents
            match nmh.code:
                case con.NM_CUSTOMDRAW:
                    nmcd = cast(lp, api.LPNMCUSTOMDRAW).contents
                    match nmcd.dwDrawStage:
                        case con.CDDS_PREPAINT: return con.CDRF_NOTIFYITEMDRAW
                        case con.CDDS_ITEMPREPAINT:
                            # this._drawFlatHeader(nmcd)
                            this._drawFunc(nmcd)
                            return con.CDRF_SKIPDEFAULT
                case con.HDN_ITEMCLICKW:
                    hdr = cast(lp, api.LPNMHEADER).contents
                    item = this._items[hdr.iItem]
                    if item.onClick: item.onClick(this, EventArgs())
                case con.HDN_ITEMDBLCLICKW:
                    if this.onDoubleClick: this.onDoubleClick(this, EventArgs())
                case con.HDN_TRACKW:
                    if this.onDrag: this.onDrag(this, HeaderEventArgs(lp))
                case con.NM_RCLICK:
                    if this.onRightClick: this.onRightClick(this, HeaderEventArgs(lp))

    return api.DefSubclassProc(hw, msg, wp, lp)

