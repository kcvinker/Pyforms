# trackbar module - Created on 21-Dec-2022 01:22:20

from ctypes import byref, addressof, cast
# import ctypes as ctp
from pyforms.src.control import Control
import pyforms.src.constants as con
from pyforms.src.commons import MyMessages
from pyforms.src.enums import ControlType, TickPosition, ChannelStyle, TrackChange
from pyforms.src.events import GEA
from pyforms.src.apis import LRESULT, RECT, LPNMCUSTOMDRAW, SUBCLASSPROC
import pyforms.src.apis as api
from pyforms.src.colors import Color
from pyforms.src.winmsgs import log_msg

trkDict = {}
trkStyle = con.WS_CHILD | con.WS_VISIBLE | con.TBS_AUTOTICKS | con.WS_CLIPCHILDREN

# If reversed style is applied, trackbar returns a minus value. This is because, we use minus value range...
# in order to make it work. Otherwise, there is no way to achieve desired result.
# So, in such cases, we need to subtract the value from u16 max.
U16_MAX = 1 << 16


class TrackBar(Control):

    """TrackBar control """
    Control.icc.initCommCtls(con.ICC_BAR_CLASSES)
    _count = 1
    __slots__ = ( "_vertical", "_reversed", "_noTics", "_selRange", "_defTics", "_ticColor", "_chanColor",
                    "_ticWidth",  "_minRange", "_maxRange", "_frequency", "_value", "_ticPos", "_pageSize",
                    "_lineSIze", "_noThumb", "_tooltip", "_chanPen", "_chanStyle", "_chanRc",
                    "_thumbRc", "_drawTic", "_ticPen", "_myRect", "_ticLen", "_custDraw", "_mouseOver", "_freeMove",
                    "_thumbHalf", "_range", "_selColor", "_selBrush", "onValueChanged", "onDragging",
                    "onDragged", "_trackChange", "_lbDown", "_ticList", "_point1", "_point2" )

    def __init__(self, parent, xpos: int = 10, ypos: int = 10, 
                 width: int = 150, height: int = 25) -> None:
        super().__init__()

        self._clsName = "msctls_trackbar32"
        self.name = f"TrackBar_{TrackBar._count}"
        self._ctlType = ControlType.TRACK_BAR
        self._parent = parent
        self._bgColor = Color(parent._bgColor)
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._isTextable = False
        self._style = trkStyle
        self._exStyle = con.WS_EX_RIGHTSCROLLBAR |con.WS_EX_LTRREADING | con.WS_EX_LEFT
        self._text = "track_bar"
        self._ticPos = TickPosition.DOWN
        self._vertical = False
        self._reversed = False
        self._noTics = False
        self._selRange = False
        self._defTics = False
        self._noThumb = False
        self._tooltip = False
        self._value = 0
        self._frequency = 10
        self._ticWidth = 1
        self._minRange = 0
        self._maxRange = 100
        self._pageSize = self._frequency
        self._lineSIze = 1
        self._chanStyle = ChannelStyle.DEFAULT
        self._thumbRc = RECT()
        self._chanRc = RECT()
        self._myRect = RECT()
        self._drawTic = False
        self._ticLen = 4
        self._custDraw = False
        self._mouseOver = False
        self._freeMove = False
        self._thumbHalf = 0
        self._range = 0
        self._trackChange = TrackChange.NONE
        self._lbDown = False
        self._ticList = [] # List of TicData [index, pysical pos, logical pos]
        self._point1 = 0 # Needed for x or y point of tic.
        self._point2 = 0 # Needed for x or y point of tic only when TicPosition.BOTH flag on.
        self._selColor = Color(0x99ff33)
        self._chanColor = Color(0xd0d0e1) #(0xc2d6d6) #(0xc2c2d6)
        self._ticColor = Color(0x3385ff)
        self._bgColor = Color(parent._bgColor)
        self._selBrush = None
        self._ticPen = None
        self._chanPen = None
        self._hasBrush = True
        self._hwnd = None
        parent._controls.append(self)

        # Events
        self.onValueChanged = None
        self.onDragging = None
        self.onDragged = None
        TrackBar._count += 1
        if parent.createChilds: self.createHandle()

# -region Public functions

    def createHandle(self):
        """Create's TrackBar handle"""

        self._setTrackStyle()
        if self._custDraw: self._prepareCustDraw()
        self._createControl()
        if self._hwnd:
            trkDict[self._hwnd] = self
            self._setSubclass(trkWndProc)
            if self._custDraw: self._calcTics()
            if self._reversed:
                api.SendMessage(self._hwnd, con.TBM_SETRANGEMIN, 1, (self._maxRange * -1))
                api.SendMessage(self._hwnd, con.TBM_SETRANGEMAX, 1, self._minRange)
            else:
                api.SendMessage(self._hwnd, con.TBM_SETRANGEMIN, 1, self._minRange)
                api.SendMessage(self._hwnd, con.TBM_SETRANGEMAX, 1, self._maxRange)

            api.SendMessage(self._hwnd, con.TBM_SETTICFREQ, self._frequency, 0)
            api.SendMessage(self._hwnd, con.TBM_SETPAGESIZE, 0, self._pageSize)
            api.SendMessage(self._hwnd, con.TBM_SETLINESIZE, 0, self._lineSIze)

            if self._selRange: # We need to prepare a color and a brush
                self._selBrush = api.CreateSolidBrush(self._selColor.ref)


    def calsulateSize(self):
        """This function will show you how many points are
        needed to align all tics in perfect distance."""

        from .messagebox import msgbox
        thumb_width = (self._thumbRc.right - self._thumbRc.left)
        channel_width = (self._chanRc.right - self._chanRc.left)
        avail_channel = channel_width - thumb_width #(8 point padding in each side + 10 point thumb)
        _range = (self._maxRange - self._minRange)
        if _range % self._frequency != 0:
            msgbox(f"Frequency is not divisive with range. Diff is {_range % self._frequency}")
            return
        num_tics = _range // self._frequency
        extra = avail_channel % num_tics
        message = "Size is perfect now !!!"

        if extra:
            diff = num_tics - extra
            if self._vertical:
                message = f"Add '{diff}' points to height"
            else:
                message = f"Add '{diff}' points to width"

        msgbox(message)


    def setTicPos(self, pos:str):
        """A handy function to set the tic position. You can set it by passing a string.
        So, you don't need to import the TickPosition Enum.
        Accepted values are: {'both', 'up', 'down', 'left', 'right'}"""
        p = pos.upper()
        match p:
            case "BOTH": self._ticPos = TickPosition.BOTH
            case "UP": self._ticPos = TickPosition.UP
            case "DOWN": self._ticPos = TickPosition.DOWN
            case "LEFT": self._ticPos = TickPosition.LEFT
            case "RIGHT": self._ticPos = TickPosition.RIGHT

# -endregion Public functions


    # -region private_funcs

    def _setTrackStyle(self):
        # Setup different trackbar styles as per user's selection
        if self._vertical:
            self._style |= con.TBS_VERT
            match self._ticPos:
                case TickPosition.LEFT: self._style |= con.TBS_LEFT
                case TickPosition.RIGHT: self._style |= con.TBS_RIGHT
                case TickPosition.BOTH: self._style |= con.TBS_BOTH
        else:
            match self._ticPos:
                case TickPosition.DOWN: self._style |= con.TBS_BOTTOM
                case TickPosition.UP: self._style |= con.TBS_TOP
                case TickPosition.BOTH: self._style |= con.TBS_BOTH

        if self._selRange: self._style |= con.TBS_ENABLESELRANGE
        if self._reversed: self._style |= con.TBS_REVERSED
        if self._noTics: self._style |= con.TBS_NOTICKS
        if self._noThumb: self._style |= con.TBS_NOTHUMB
        if self._tooltip: self._style |= con.TBS_TOOLTIPS
        self._bkgBrush = self._bgColor.createHBrush()

    # Fill appropriate rects
    def _collectRects(self):
        # We need to keep the rects for different parts of this trackbar
        api.GetClientRect(self._hwnd, byref(self._myRect))
        api.SendMessage(self._hwnd, con.TBM_GETTHUMBRECT, 0, addressof(self._thumbRc)) # Get the thumb rect
        api.SendMessage(self._hwnd, con.TBM_GETCHANNELRECT, 0, addressof(self._chanRc)) # Get the channel rect

    # Calculate thumb's hanlf width / height
    def _calcThumbOffset(self):
        # half of the width of thumb. We need this to draw tics.
        if self._style & con.TBS_VERT:
            tw =  self._thumbRc.bottom - self._thumbRc.top
        else:
            tw =  self._thumbRc.right - self._thumbRc.left
        self._thumbHalf = int(tw/2)

    # Draw harizontal tics in down side
    def _drawHorizTics(self, hdc, px, py):
        api.MoveToEx(hdc, px, py, None)
        api.LineTo(hdc, px, py + self._ticLen)

    # Draw harizontal tics in up side
    def _drawHorizTicsUpper(self, hdc, px, py):
        api.MoveToEx(hdc, px, py, None)
        api.LineTo(hdc, px, py - self._ticLen)

    # Draw vertical tics
    def _drawVertTics(self, hdc, px, py):
        api.MoveToEx(hdc, px, py, None)
        api.LineTo(hdc, px + self._ticLen, py)

    # Get the rect for thumb
    def _getThumbRect(self): # Useless ?
        rc = RECT()
        api.SendMessage(self._hwnd, con.TBM_GETTHUMBRECT, 0, addressof(rc))
        return rc

    # Internal function for drawing tics
    def _drawTics(self, hdc):
        # This function get called inside the custom draw part.
        api.SelectObject(hdc, self._ticPen)
        if self._vertical:
            match self._ticPos:
                case TickPosition.RIGHT | TickPosition.LEFT:
                    for p in self._ticList:
                        self._drawVertTics(hdc, self._point1, p.phy_point)
                case TickPosition.BOTH:
                    for p in self._ticList:
                        self._drawVertTics(hdc, self._point1, p.phy_point)
                        self._drawVertTics(hdc, self._point2, p.phy_point)

        else:
            match self._ticPos:
                case TickPosition.UP | TickPosition.DOWN:
                    for p in self._ticList:
                        self._drawHorizTics(hdc, p.phy_point, self._point1)
                case TickPosition.BOTH:
                    for p in self._ticList:
                        self._drawHorizTics(hdc, p.phy_point, self._point1)
                        self._drawHorizTicsUpper(hdc, p.phy_point, self._point2)

    # Calculated the distants for drawing tics
    def _calcTics(self):
        # Calculating logical & physical positions for tics.
        self._collectRects()
        self._calcThumbOffset()
        self._range = self._maxRange - self._minRange
        api.SendMessage(self._hwnd, con.TBM_SETLINESIZE, 0, self._frequency)

        numtics = self._range // self._frequency
        if self._range % self._frequency == 0: numtics -= 1
        stpos = self._chanRc.left + self._thumbHalf
        enpos = self._chanRc.right - self._thumbHalf
        channel_len = enpos - stpos
        pfactor = channel_len / self._range

        tic = self._minRange + self._frequency
        self._ticList.append(TicData( stpos, 0))
        for i in range(numtics):
            # print(f"{tic * pfactor = }, {tic = }")
            self._ticList.append(TicData(int(tic * pfactor) + stpos, tic))
            tic += self._frequency

        self._ticList.append(TicData(enpos, self._range))
        # print("P factor ", pfactor)
        if self._vertical:
            match self._ticPos:
                case TickPosition.LEFT: self._point1 = self._thumbRc.left - 5
                case TickPosition.RIGHT: self._point1 = self._thumbRc.right + 2
                case TickPosition.BOTH:
                    self._point1 = self._thumbRc.right + 2
                    self._point2 = self._thumbRc.left - 5
        else:
            match self._ticPos:
                case TickPosition.DOWN: self._point1 = self._thumbRc.bottom + 1
                case TickPosition.UP: self._point1 = self._thumbRc.top - 4
                case TickPosition.BOTH:
                    self._point1 = self._thumbRc.bottom + 1
                    self._point2 = self._thumbRc.top - 3

    # Filling channel rect with selection color.
    def _fillChannelRect(self, nm, trc):
        # If showSelection property is enabled in this trackbar,
        # we need to show the area between thumb and channel starting in diff color.
        # But we need to check if the trackbar is reversed or not.
        result = False
        rc = RECT()

        if self._vertical:
            rc.left = nm.rc.left + 1
            rc.right = nm.rc.right - 1
            if self._reversed:
                rc.top = trc.bottom
                rc.bottom = nm.rc.bottom - 1
            else:
                rc.top = nm.rc.top
                rc.bottom = trc.top
        else:
            rc.top = nm.rc.top + 1
            rc.bottom = nm.rc.bottom - 1
            if self._reversed:
                rc.left = trc.right
                rc.right = nm.rc.right - 1
            else:
                rc.left = nm.rc.left + 1
                rc.right = trc.left

        result = api.FillRect(nm.hdc, byref(rc), self._selBrush)
        return result

    # Internal function for set value
    def _setValueInternal(self, val):
        self._value = (U16_MAX - val) if self._reversed else val


    # Preparing for custom draw
    def _prepareCustDraw(self):
        self._chanPen = self._chanColor.createHPen()
        self._ticPen = api.CreatePen(con.PS_SOLID, self._ticWidth, self._ticColor.ref)

    # Handling wm_notify message
    def _wmNotifyHandler(self, lp):
        nmh = cast(lp, api.LPNMHDR).contents
        match nmh.code:
            case con.NM_CUSTOMDRAW:
                if self._custDraw:
                    nmcd = cast(lp, LPNMCUSTOMDRAW).contents
                    match nmcd.dwDrawStage:
                        case con.CDDS_PREPAINT: return con.CDRF_NOTIFYITEMDRAW
                        case con.CDDS_ITEMPREPAINT:
                            # print(f"{nmcd.dwItemSpec = }, {con.TBCD_TICS = }, {con.TBCD_CHANNEL = }")
                            if nmcd.dwItemSpec == con.TBCD_TICS:
                                if not self._noTics: self._drawTics(nmcd.hdc)
                                # return con.CDRF_SKIPDEFAULT

                            elif nmcd.dwItemSpec == con.TBCD_CHANNEL:
                                if self._chanStyle == ChannelStyle.CLASSIC:
                                    api.DrawEdge(nmcd.hdc, byref(nmcd.rc), con.EDGE_SUNKEN, con.BF_RECT | con.BF_ADJUST) # 1 style
                                else:
                                    api.SelectObject(nmcd.hdc, self._chanPen)
                                    api.Rectangle(nmcd.hdc, nmcd.rc.left, nmcd.rc.top, nmcd.rc.right, nmcd.rc.bottom )

                                if self._selRange: # Fill the selection range
                                    rc = self._getThumbRect()
                                    if self._fillChannelRect(nmcd, rc):
                                        api.InvalidateRect(self._hwnd, byref(nmcd.rc), False)
                                return con.CDRF_SKIPDEFAULT
                            else:
                                return con.CDRF_DODEFAULT
                    return con.CDRF_DODEFAULT
                else:
                    return con.CDRF_DODEFAULT # We don't need to use custom draw
            case 4294967280: # con.TRBN_THUMBPOSCHANGING:
                self._trackChange = TrackChange.MOUSE_CLICK
                return con.CDRF_DODEFAULT


    # -endregion Private funcs

    # -region Properties

    @Control.backColor.setter
    def backColor(self, value):
        """Set the control's back color"""
        if isinstance(value, int):
            self._bgColor.updateColor(value)
        elif isinstance(value, Color):
            self._bgColor = value

        if self._drawFlag & 2 != 2: self._drawFlag += 2
        if self._isCreated: self._bkgBrush = self._bgColor.createHBrush()
        api.SendMessage(self._hwnd, con.TBM_SETRANGEMAX, 1, self._maxRange)
        self._manageRedraw()

    @property
    def trackChange(self)-> int:
        """Get the range beetween minimum & maximum values"""
        return self._range
    #------------------------------------------------------------- 1 TRACK RANGE

    @property
    def ticLength(self)-> int:
        """Returns the tic length"""
        return self._ticLen

    @ticLength.setter
    def ticLength(self, value: int):
        """Set the length of the tic marks"""
        self._ticLen = value
    # #------------------------------------------------------------------------2 TIC LENGTH

    @property
    def vertical(self)-> bool:
        """Returns true if vertical property is enabled"""
        return self._vertical

    @vertical.setter
    def vertical(self, value: bool):
        """If set to True, the Orientation of trackbar will be vertical"""
        self._vertical = value
        if self._ticPos == TickPosition.DOWN or self._ticPos == TickPosition.UP:
            self._ticPos = TickPosition.RIGHT
    # #------------------------------------------------------------------------3 VERTICAL

    @property
    def largeChange(self)-> int:
        """Returns true if large change enabled"""
        return self._pageSize

    @largeChange.setter
    def largeChange(self, value: int):
        """Determine how many logical points slider should move when pageup/pagedown keys or mouse button pressed.
        Note: Logical point is the single points in between minimum & maximum range.
        """
        self._pageSize = value
    # #------------------------------------------------------------------------4 LARGE CHANGE

    @property
    def smallChange(self)-> int:
        """Returns true if small change enabled"""
        return self._lineSIze

    @smallChange.setter
    def smallChange(self, value: int):
        """Determine how many logical points slider should move when arrow keys pressed.
        Note: Logical point is the single points in between minimum & maximum range.
        """
        self._lineSIze = value
    # #------------------------------------------------------------------------5 SMALL CHANGE

    @property
    def showSelection(self)-> bool:
        """Returns true if show selection enabled"""
        return self._selRange

    @showSelection.setter
    def showSelection(self, value: bool):
        """Get or set the behaviour for highlighting the selection in channel"""
        self._selRange = value
        if value and not self._custDraw:
            self._custDraw = True
            # self._prepareCustDraw()
    # #------------------------------------------------------------------------6 SHOW SELECTION

    @property
    def frequency(self)-> int:
        """Returns the frequency"""
        return self._frequency


    @frequency.setter
    def frequency(self, value: int):
        """Get or set the frequency of tics.
        If you set 8 as frequency, there will be 12 gaps in tics.
        Default is 10"""
        self._frequency = value
    # #------------------------------------------------------------------------7 FREQUENCY

    @property
    def minimum(self)-> int:
        """Returns the minimum value of track bar's range"""
        return self._minRange

    @minimum.setter
    def minimum(self, value: int):
        """Get or set the minimum of level of trackbar value range."""
        self._minRange = value
    # #------------------------------------------------------------------------8 MINIMUM

    @property
    def maximum(self)-> int:
        """Returns the maximum value of track bar's range"""
        return self._maxRange

    @maximum.setter
    def maximum(self, value: int):
        """Get or set the maximum of level of trackbar value range."""
        self._maxRange = value
    # #------------------------------------------------------------------------9 MAXIMUM

    @property
    def ticPosition(self)-> TickPosition:
        """Returns the tic position of track bar. Check TickPosition enum"""
        return self._ticPos

    @ticPosition.setter
    def ticPosition(self, value: TickPosition):
        """Get or set the tic position of trackbar. Check TickPosition enum"""
        self._ticPos = value
    # #------------------------------------------------------------------------10 TIC POS

    @property
    def tooltip(self)-> bool:
        """Returns true if tooltip is enabled"""
        return self._tooltip

    @tooltip.setter
    def tooltip(self, value: bool):
        """Get or set the tooltip for trackbar"""
        self._tooltip = value
    # #------------------------------------------------------------------------11 TOOLTIP

    @property
    def reverse(self)-> bool:
        """Returns true if reverse property enabled"""
        return self._reversed

    @reverse.setter
    def reverse(self, value: bool):
        """If set to True, the minimum & maximum points will be swapped"""
        self._reversed = value
    # #------------------------------------------------------------------------12 REVERSE

    @property
    def value(self)-> bool:
        """Returns the value of trackbar"""
        return self._value

    @value.setter
    def value(self, value: bool):
        """Set or get the value of trackbar"""
        self._value = value
        if self._isCreated: pass # TODO: Add code for this
    # #------------------------------------------------------------------------13 VALUE

    @property
    def selectionColor(self)-> Color:
        """Returns the selection color"""
        return self._selColor

    @selectionColor.setter
    def selectionColor(self, value: int):
        """Set or get the color for selection range of trackbar"""
        self._selColor = Color(value)
    # #------------------------------------------------------------------------14 VALUE

    @property
    def ticColor(self)-> Color:
        """Returns the tic color"""
        return self._ticColor

    @ticColor.setter
    def ticColor(self, value: int):
        """Set or get the color for tic marks of trackbar"""
        self._ticColor = Color(value)
        if value and not self._custDraw:
            self._custDraw = True
    # #------------------------------------------------------------------------15 TIC COLOR

    @property
    def channelColor(self)-> Color:
        """Returns the channel color"""
        return self._chanColor

    @channelColor.setter
    def channelColor(self, value: int):
        """Set or get the color for channel of trackbar"""
        self._chanColor = Color(value)
    # #------------------------------------------------------------------------16 CHANNEL COLOR

    @property
    def freeMove(self)-> bool:
        """Returns true if free move property enabled"""
        return self._freeMove

    @freeMove.setter
    def freeMove(self, value: bool):
        """If set to True, thumb can be dragged freely. Default is False"""
        self._freeMove = value
    # #------------------------------------------------------------------------17 FREE MOVE

    @property
    def ticWidth(self)-> bool:
        """Returns tic width"""
        return self._ticWidth

    @ticWidth.setter
    def ticWidth(self, value: bool):
        """Set or get the tic width"""
        self._ticWidth = value
    # #------------------------------------------------------------------------18 TIC WIDTH

    @property
    def noTics(self)-> bool:
        """Returns true if no tics property enabled"""
        return self._noTics

    @noTics.setter
    def noTics(self, value: bool):
        """If set to True there would be no tic marks. Default is False"""
        self._noTics = value
    # #------------------------------------------------------------------------19 NO TICs

    @property
    def channelStyle(self)-> bool:
        """Returns the channel style. Check ChannelStyle enum"""
        return self._chanStyle

    @channelStyle.setter
    def channelStyle(self, value: ChannelStyle):
        """Set or get the channel style. Possible styles are classic & outline. Default is classic"""
        self._chanStyle = value
    # #------------------------------------------------------------------------19 NO TICs


    @property
    def customDraw(self)-> int:
        """Returns true if custom draw enabled"""
        return self._custDraw # Fixme: Do we need this getter ?

    @customDraw.setter
    def customDraw(self, value: int):
        """Enable custom draw for this TrackBar.
        This will allow you to set the tic & channel colors, tic width & length etc. """
        self._custDraw = value
        # if value: self._prepareCustDraw()

    # #---------------------------------------------------------------------------------- CUSTOM DRAW

    # -endregion Properties

# End TrackBar


class TicData:
    """Only for internal use.
    This class is a helper class to hold the
    tic logical positions and physical positions.
    """
    num = 0
    def __init__(self, phyPoint: int, logPoint: int) -> None:
        self.index = TicData.num
        self.phy_point = phyPoint
        self.log_point = logPoint
        TicData.num += 1

    def __str__(self) -> str:
        return f"{self.index = }, {self.phy_point = }, {self.log_point = }"



@SUBCLASSPROC # This decorator is essential.
def trkWndProc(hw, msg, wp, lp, scID, refData) -> LRESULT:
    # log_msg(msg)
    trk = trkDict[hw]

    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, trkWndProc, scID)
            del trkDict[hw]

        case MyMessages.HORI_SCROLL | MyMessages.VERT_SCROLL:
            lwp = api.LOWORD(wp)
            match lwp:
                case con.TB_THUMBPOSITION:
                    # Thumb dragging finished. Let's collect the value
                    trk._setValueInternal(api.HIWORD(wp))

                    # if freeMove property is false, we need to adjust the thumb on nearest tic.
                    if not trk._freeMove: #Improve
                        pos = trk._value
                        half = trk._frequency // 2
                        diff = trk._value % trk._frequency
                        if diff >= half:
                            pos = (trk._frequency - diff) + trk._value
                        elif diff < half:
                            pos =  trk._value - diff
                        if trk._reversed:
                            api.SendMessage(trk._hwnd, con.TBM_SETPOS, True, (pos * -1))
                        else:
                            api.SendMessage(trk._hwnd, con.TBM_SETPOS, True, pos)

                        trk._value = pos

                    # We need to refresh Trackbar in order to display our new drawings.
                    api.InvalidateRect(hw, byref(trk._chanRc), False)

                    trk._trackChange = TrackChange.MOUSE_DRAG
                    if trk.onDragged: trk.onDragged(trk, GEA)
                    if trk.onValueChanged: trk.onValueChanged(trk, GEA)

                case  con.THUMB_LINE_HIGH:
                    trk._setValueInternal(api.SendMessage(hw, con.TBM_GETPOS, 0, 0))
                    trk._trackChange = TrackChange.ARROW_HIGH
                    # print(trk._trackChange)
                    if trk.onValueChanged:
                        trk.onValueChanged(trk, GEA)

                case con.THUMB_LINE_LOW:
                    trk._setValueInternal(api.SendMessage(hw, con.TBM_GETPOS, 0, 0))
                    trk._trackChange = TrackChange.ARROW_LOW
                    # print(trk._trackChange)
                    if trk.onValueChanged:
                        trk.onValueChanged(trk, GEA)

                case con.THUMB_PAGE_HIGH:
                    trk._setValueInternal(api.SendMessage(hw, con.TBM_GETPOS, 0, 0))
                    # print("value ", trk._value)
                    if not trk._lbDown:
                        trk._trackChange = TrackChange.PAGE_HIGH
                        # print(trk._trackChange, " 458 ")

                    if trk.onValueChanged:
                        trk.onValueChanged(trk, GEA)

                case con.THUMB_PAGE_LOW:
                    trk._setValueInternal(api.SendMessage(hw, con.TBM_GETPOS, 0, 0))
                    trk._trackChange = TrackChange.PAGE_LOW
                    # print(trk._trackChange)
                    if trk.onValueChanged:
                        trk.onValueChanged(trk, GEA)

                case con.TB_THUMBTRACK: # User dragging thumb.
                    trk._setValueInternal(api.HIWORD(wp))
                    # api.InvalidateRect(hw, byref(trk._chanRc), False)
                    if trk.onDragging: trk.onDragging(trk, GEA)

        case MyMessages.LABEL_COLOR:
            # api.SetBkColor(wp, trk._bgColor.ref)
            return trk._bkgBrush

        case MyMessages.CTRL_NOTIFY:
            nmh = cast(lp, api.LPNMHDR)[0]
            match nmh.code:
                case con.NM_CUSTOMDRAW:
                    if trk._custDraw:
                        nmcd = cast(lp, LPNMCUSTOMDRAW)[0]
                        match nmcd.dwDrawStage:
                            case con.CDDS_PREPAINT: return con.CDRF_NOTIFYITEMDRAW
                            case con.CDDS_ITEMPREPAINT:
                                # print(f"{nmcd.dwItemSpec = }, {con.TBCD_TICS = }, {con.TBCD_CHANNEL = }")
                                if nmcd.dwItemSpec == con.TBCD_CHANNEL:
                                    if trk._chanStyle == ChannelStyle.CLASSIC:
                                        api.DrawEdge(nmcd.hdc, byref(nmcd.rc), con.EDGE_SUNKEN, con.BF_RECT | con.BF_ADJUST) # 1 style
                                    elif trk._chanStyle == ChannelStyle.OUTLINE:
                                        api.SelectObject(nmcd.hdc, trk._chanPen)
                                        api.Rectangle(nmcd.hdc, nmcd.rc.left, nmcd.rc.top, nmcd.rc.right, nmcd.rc.bottom )
                                    else:
                                        return con.CDRF_DODEFAULT

                                    if trk._selRange: # Fill the selection range
                                        rc = trk._getThumbRect()
                                        if trk._fillChannelRect(nmcd, rc):
                                            api.InvalidateRect(hw, byref(nmcd.rc), False)
                                    return con.CDRF_SKIPDEFAULT

                                if nmcd.dwItemSpec == con.TBCD_TICS:

                                    if not trk._noTics:
                                        trk._drawTics(nmcd.hdc)
                                        return con.CDRF_SKIPDEFAULT
                                    else: con.CDRF_DODEFAULT

                        return con.CDRF_DODEFAULT

                case 4294967280: # con.TRBN_THUMBPOSCHANGING:
                    trk._trackChange = TrackChange.MOUSE_CLICK
                    return con.CDRF_DODEFAULT
            return 0 #api.DefSubclassProc(hw, msg, wp, lp)

        case con.WM_SETFOCUS: trk._gotFocusHandler()
        case con.WM_KILLFOCUS: trk._lostFocusHandler()
        case con.WM_LBUTTONDOWN:
            trk._lbDown = True
            trk._leftMouseDownHandler(msg, wp, lp)
        case con.WM_LBUTTONUP:
            trk._lbDown = False
            trk._leftMouseUpHandler(msg, wp, lp)
        case con.WM_RBUTTONDOWN: trk._rightMouseDownHandler(msg, wp, lp)
        case con.WM_RBUTTONUP: trk._rightMouseUpHandler(msg, wp, lp)
        case con.WM_MOUSEWHEEL: trk._mouseWheenHandler(msg, wp, lp)
        case con.WM_MOUSEMOVE: trk._mouseMoveHandler(msg, wp, lp)
        case con.WM_MOUSELEAVE: trk._mouseLeaveHandler()

    return api.DefSubclassProc(hw, msg, wp, lp)


