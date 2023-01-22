



# trackbar module - Created on 21-Dec-2022 01:22:20


from array import *
from ctypes.wintypes import HWND, UINT, DWORD
from ctypes import POINTER, Array, byref, addressof, cast
from .control import Control
import ctypes as ct

from . import constants as con
from .commons import MyMessages
from .enums import ControlType, TickPosition, ChannelStyle, TrackChange
from .events import EventArgs
from .apis import LRESULT, UINT_PTR, DWORD_PTR, RECT, LPNMCUSTOMDRAW, WPARAM, LPARAM, SUBCLASSPROC
from . import apis as api
from .colors import Color
from .winmsgs import log_msg
from horology import Timing

trk_dict = {}
trk_style = con.WS_CHILD | con.WS_VISIBLE | con.WS_CLIPCHILDREN | con.TBS_AUTOTICKS

# If reversed style is applied, trackbar returns a minus value. This is because, we use minus value range...
# in order to make it work. Otherwise, there is no way to achieve desired result.
# So, in such cases, we need to subtract the value from u16 max.
U16_MAX = 1 << 16


class TrackBar(Control):

    """TrackBar control """
    Control.icc.init_comm_ctls(con.ICC_BAR_CLASSES)
    _count = 1
    __slots__ = ( "_vertical", "_reversed", "_no_tics", "_sel_range", "_def_tics", "_tic_color", "_channel_color",
                    "_tic_width",  "_min_range", "_max_range", "_frequency", "_value", "_tic_pos", "_page_size",
                    "_line_size", "_no_thumb", "_tooltip", "_bkg_brush", "_channel_pen", "_channel_style", "_channel_rc",
                    "_thumb_rc", "_draw_tic", "_tic_pen", "_my_rect", "_tic_len", "_cust_draw", "_mouse_over", "_free_move",
                    "_thumb_half", "_range", "_sel_color", "_sel_brush", "on_value_changed", "on_dragging",
                    "on_dragged", "_track_change", "_lb_down", "_tics", "_point1", "_point2" )

    def __init__(self, parent, xpos: int = 10, ypos: int = 10, width: int = 150, height: int = 25) -> None:
        super().__init__()

        self._cls_name = "msctls_trackbar32"
        self.name = f"TrackBar{TrackBar._count}"
        self._ctl_type = ControlType.TRACK_BAR
        self._parent = parent
        self._bg_color = Color(parent._bg_color)
        # self._font = parent._font
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._is_textable = False
        self._style = trk_style
        self._ex_style = con.WS_EX_RIGHTSCROLLBAR |con.WS_EX_LTRREADING | con.WS_EX_LEFT
        self._text = "track_bar"
        self._tic_pos = TickPosition.DOWN
        self._vertical = False
        self._reversed = False
        self._no_tics = False
        self._sel_range = False
        self._def_tics = False
        self._no_thumb = False
        self._tooltip = False
        self._value = 0

        self._frequency = 10
        self._tic_width = 1
        self._min_range = 0
        self._max_range = 100
        self._page_size = self._frequency
        self._line_size = 1
        self._channel_style = ChannelStyle.DEFAULT
        self._thumb_rc = RECT()
        self._channel_rc = RECT()
        self._my_rect = RECT()
        self._draw_tic = False
        self._tic_len = 4
        self._cust_draw = False
        self._mouse_over = False
        self._free_move = False
        self._thumb_half = 0
        self._range = 0
        self._track_change = TrackChange.NONE
        self._lb_down = False
        self._tics = [] # List of TicData [index, pysical pos, logical pos]
        self._point1 = 0 # Needed for x or y point of tic.
        self._point2 = 0 # Needed for x or y point of tic only when TicPosition.BOTH flag on.
        self._sel_color = Color(0x99ff33)
        self._channel_color = Color(0xd0d0e1) #(0xc2d6d6) #(0xc2c2d6)
        self._tic_color = Color(0x3385ff)
        self._bg_color = Color(parent._bg_color)
        self._sel_brush = 0

        # Events
        self.on_value_changed = 0
        self.on_dragging = 0
        self.on_dragged = 0


        TrackBar._count += 1

# -region Public functions

    def create_handle(self):
        """Create's TrackBar handle"""

        self._set_trk_style()
        if self._cust_draw: self._prepare_for_custom_draw()
        self._create_control()
        if self._hwnd:
            print("Track hwnd ", self._hwnd)
            trk_dict[self._hwnd] = self
            self._set_subclass(trk_wnd_proc)
            if self._cust_draw: self._calc_tics()

            # self._set_font_internal()
            if self._reversed:
                api.SendMessage(self._hwnd, con.TBM_SETRANGEMIN, 1, (self._max_range * -1))
                api.SendMessage(self._hwnd, con.TBM_SETRANGEMAX, 1, self._min_range)
            else:
                api.SendMessage(self._hwnd, con.TBM_SETRANGEMIN, 1, self._min_range)
                api.SendMessage(self._hwnd, con.TBM_SETRANGEMAX, 1, self._max_range)

            api.SendMessage(self._hwnd, con.TBM_SETTICFREQ, self._frequency, 0)

            api.SendMessage(self._hwnd, con.TBM_SETPAGESIZE, 0, self._page_size)
            api.SendMessage(self._hwnd, con.TBM_SETLINESIZE, 0, self._line_size)

            if self._sel_range: # We need to prepare a color and a brush
                self._sel_brush = api.CreateSolidBrush(self._sel_color.ref)

            # api.SendMessage(self._hwnd, con.TBM_SETPOS, True, 1)

            # print(f" style bit {self._style & con.TBS_ENABLESELRANGE}, {con.TBS_ENABLESELRANGE = }")



    # def ptest(self):

    #     dwp = POINTER(ct.c_ulong)
    #     num_tics = api.SendMessage(self._hwnd, con.TBM_GETNUMTICS, 0, 0 ) - 2
    #     class P(ct.Structure):
    #         _fields_ = [("arr", POINTER(DWORD))]

    #     addr = api.SendMessage(self._hwnd, con.TBM_GETPTICS, 0, 0)
    #     at = POINTER(DWORD)

    #     # a = cast(addr, ct.c_void_p)
    #     arr = id(DWORD(addr))


    #     # arr = addr
    #     # a = ct.pointer(arr)
    #     print(type(arr), " type of arr")
    #     print(arr[0], " arr[0]")
    #     # for i in range(num_tics):
    #     #     print(arr[i])




    def calculate_size(self):
        """This function will show you how many points are
        needed to align all tics in perfect distance."""

        from .messagebox import msgbox
        thumb_width = (self._thumb_rc.right - self._thumb_rc.left)
        channel_width = (self._channel_rc.right - self._channel_rc.left)
        avail_channel = channel_width - thumb_width #(8 point padding in each side + 10 point thumb)
        _range = (self._max_range - self._min_range)
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

    def set_tic_pos(self, pos:str):
        """A handy function to set the tic position. You can set it by passing a string.
        So, you don't need to import the TickPosition Enum.
        Accepted values are: {'both', 'up', 'down', 'left', 'right'}"""
        p = pos.upper()
        match p:
            case "BOTH": self._tic_pos = TickPosition.BOTH
            case "UP": self._tic_pos = TickPosition.UP
            case "DOWN": self._tic_pos = TickPosition.DOWN
            case "LEFT": self._tic_pos = TickPosition.LEFT
            case "RIGHT": self._tic_pos = TickPosition.RIGHT

# -endregion Public functions


    # -region private_funcs

    def _set_trk_style(self):
        # Setup different trackbar styles as per user's selection
        if self._vertical:
            self._style |= con.TBS_VERT
            match self._tic_pos:
                case TickPosition.LEFT: self._style |= con.TBS_LEFT
                case TickPosition.RIGHT: self._style |= con.TBS_RIGHT
                case TickPosition.BOTH: self._style |= con.TBS_BOTH
        else:
            match self._tic_pos:
                case TickPosition.DOWN: self._style |= con.TBS_BOTTOM
                case TickPosition.UP: self._style |= con.TBS_TOP
                case TickPosition.BOTH: self._style |= con.TBS_BOTH

        if self._sel_range: self._style |= con.TBS_ENABLESELRANGE
        if self._reversed: self._style |= con.TBS_REVERSED
        if self._no_tics: self._style |= con.TBS_NOTICKS
        if self._no_thumb: self._style |= con.TBS_NOTHUMB
        if self._tooltip: self._style |= con.TBS_TOOLTIPS
        self._bkg_brush = api.CreateSolidBrush(self._bg_color.ref)

    def _collect_rects(self):
        # We need to keep the rects for different parts of this trackbar
        api.GetClientRect(self._hwnd, byref(self._my_rect))
        api.SendMessage(self._hwnd, con.TBM_GETTHUMBRECT, 0, addressof(self._thumb_rc)) # Get the thumb rect
        api.SendMessage(self._hwnd, con.TBM_GETCHANNELRECT, 0, addressof(self._channel_rc)) # Get the channel rect

    def _calc_thumb_offset(self):
        # half of the width of thumb. We need this to draw tics.
        if self._style & con.TBS_VERT:
            tw =  self._thumb_rc.bottom - self._thumb_rc.top
        else:
            tw =  self._thumb_rc.right - self._thumb_rc.left
        self._thumb_half = int(tw/2)

    def _draw_horiz_tics(self, hdc, px, py):
        api.MoveToEx(hdc, px, py, None)
        api.LineTo(hdc, px, py + self._tic_len)

    def _draw_horiz_tics_upper(self, hdc, px, py):
        api.MoveToEx(hdc, px, py, None)
        api.LineTo(hdc, px, py - self._tic_len)

    def _draw_vertical_tics(self, hdc, px, py):
        api.MoveToEx(hdc, px, py, None)
        api.LineTo(hdc, px + self._tic_len, py)

    def _get_thumb_rect(self): # Useless ?
        rc = RECT()
        api.SendMessage(self._hwnd, con.TBM_GETTHUMBRECT, 0, addressof(rc))
        return rc

    def _draw_tics(self, hdc):
        # This function get called inside the custom draw part.
        api.SelectObject(hdc, self._tic_pen)
        if self._vertical:
            match self._tic_pos:
                case TickPosition.RIGHT | TickPosition.LEFT:
                    for p in self._tics:
                        self._draw_vertical_tics(hdc, self._point1, p.phy_point)
                case TickPosition.BOTH:
                    for p in self._tics:
                        self._draw_vertical_tics(hdc, self._point1, p.phy_point)
                        self._draw_vertical_tics(hdc, self._point2, p.phy_point)

        else:
            match self._tic_pos:
                case TickPosition.UP | TickPosition.DOWN:
                    for p in self._tics:
                        self._draw_horiz_tics(hdc, p.phy_point, self._point1)
                case TickPosition.BOTH:
                    for p in self._tics:
                        self._draw_horiz_tics(hdc, p.phy_point, self._point1)
                        self._draw_horiz_tics_upper(hdc, p.phy_point, self._point2)


    def _calc_tics(self):
        # Calculating logical & physical positions for tics.
        self._collect_rects()
        self._calc_thumb_offset()
        self._range = self._max_range - self._min_range
        api.SendMessage(self._hwnd, con.TBM_SETLINESIZE, 0, self._frequency)

        numtics = self._range // self._frequency
        if self._range % self._frequency == 0: numtics -= 1
        stpos = self._channel_rc.left + self._thumb_half
        enpos = self._channel_rc.right - self._thumb_half
        channel_len = enpos - stpos
        pfactor = channel_len / self._range

        tic = self._min_range + self._frequency
        self._tics.append(TicData( stpos, 0))
        for i in range(numtics):
            # print(f"{tic * pfactor = }, {tic = }")
            self._tics.append(TicData(int(tic * pfactor) + stpos, tic))
            tic += self._frequency

        self._tics.append(TicData(enpos, self._range))
        # print("P factor ", pfactor)
        if self._vertical:
            match self._tic_pos:
                case TickPosition.LEFT: self._point1 = self._thumb_rc.left - 5
                case TickPosition.RIGHT: self._point1 = self._thumb_rc.right + 2
                case TickPosition.BOTH:
                    self._point1 = self._thumb_rc.right + 2
                    self._point2 = self._thumb_rc.left - 5
        else:
            match self._tic_pos:
                case TickPosition.DOWN: self._point1 = self._thumb_rc.bottom + 1
                case TickPosition.UP: self._point1 = self._thumb_rc.top - 4
                case TickPosition.BOTH:
                    self._point1 = self._thumb_rc.bottom + 1
                    self._point2 = self._thumb_rc.top - 3

    def fill_channel_rect(self, nm, trc):
        # If show_selection property is enabled in this trackbar,
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

        result = api.FillRect(nm.hdc, byref(rc), self._sel_brush)
        return result


    def _set_value_internal(self, val):
        if self._reversed:
            self._value = U16_MAX - val
        else:
            self._value = val

    def _prepare_for_custom_draw(self):
        self._channel_pen = api.CreatePen(con.PS_SOLID, 1, self._channel_color.ref)
        self._tic_pen = api.CreatePen(con.PS_SOLID, self._tic_width, self._tic_color.ref)

    def _wm_notify_handler(self, lp):
        nmh = cast(lp, api.LPNMHDR).contents
        match nmh.code:
            case con.NM_CUSTOMDRAW:
                if self._cust_draw:
                    nmcd = cast(lp, LPNMCUSTOMDRAW).contents
                    match nmcd.dwDrawStage:
                        case con.CDDS_PREPAINT: return con.CDRF_NOTIFYITEMDRAW
                        case con.CDDS_ITEMPREPAINT:
                            # print(f"{nmcd.dwItemSpec = }, {con.TBCD_TICS = }, {con.TBCD_CHANNEL = }")
                            if nmcd.dwItemSpec == con.TBCD_TICS:
                                if not self._no_tics: self._draw_tics(nmcd.hdc)
                                # return con.CDRF_SKIPDEFAULT

                            elif nmcd.dwItemSpec == con.TBCD_CHANNEL:
                                if self._channel_style == ChannelStyle.CLASSIC:
                                    api.DrawEdge(nmcd.hdc, byref(nmcd.rc), con.EDGE_SUNKEN, con.BF_RECT | con.BF_ADJUST) # 1 style
                                else:
                                    api.SelectObject(nmcd.hdc, self._channel_pen)
                                    api.Rectangle(nmcd.hdc, nmcd.rc.left, nmcd.rc.top, nmcd.rc.right, nmcd.rc.bottom )

                                if self._sel_range: # Fill the selection range
                                    rc = self._get_thumb_rect()
                                    if self.fill_channel_rect(nmcd, rc):
                                        api.InvalidateRect(self._hwnd, byref(nmcd.rc), False)
                                return con.CDRF_SKIPDEFAULT
                            else:
                                return con.CDRF_DODEFAULT
                    return con.CDRF_DODEFAULT
                else:
                    return con.CDRF_DODEFAULT # We don't need to use custom draw
            case 4294967280: # con.TRBN_THUMBPOSCHANGING:
                self._track_change = TrackChange.MOUSE_CLICK
                return con.CDRF_DODEFAULT


    # -endregion Private funcs

    # -region Properties

    @property
    def track_range(self)-> int:
        """Get the range beetween minimum & maximum values"""
        return self._range
    #------------------------------------------------------------- 1 TRACK RANGE

    @property
    def tic_length(self)-> int: return self._tic_len

    @tic_length.setter
    def tic_length(self, value: int):
        """Set the length of the tic marks"""
        self._tic_len = value
    # #------------------------------------------------------------------------2 TIC LENGTH

    @property
    def vertical(self)-> bool: return self._vertical

    @vertical.setter
    def vertical(self, value: bool):
        """If set to True, the Orientation of trackbar will be vertical"""
        self._vertical = value
        if self._tic_pos == TickPosition.DOWN or self._tic_pos == TickPosition.UP:
            self._tic_pos = TickPosition.RIGHT
    # #------------------------------------------------------------------------3 VERTICAL

    @property
    def large_change(self)-> int: return self._page_size

    @large_change.setter
    def large_change(self, value: int):
        """Determine how many logical points slider should move when pageup/pagedown keys or mouse button pressed.
        Note: Logical point is the single points in between minimum & maximum range.
        """
        self._page_size = value
    # #------------------------------------------------------------------------4 LARGE CHANGE

    @property
    def small_change(self)-> int: return self._line_size

    @small_change.setter
    def small_change(self, value: int):
        """Determine how many logical points slider should move when arrow keys pressed.
        Note: Logical point is the single points in between minimum & maximum range.
        """
        self._line_size = value
    # #------------------------------------------------------------------------5 SMALL CHANGE

    @property
    def show_selection(self)-> bool: return self._sel_range

    @show_selection.setter
    def show_selection(self, value: bool):
        """Get or set the behaviour for highlighting the selection in channel"""
        self._sel_range = value
        if value and not self._cust_draw:
            self._cust_draw = True
            # self._prepare_for_custom_draw()
    # #------------------------------------------------------------------------6 SHOW SELECTION

    @property
    def frequency(self)-> int: return self._frequency


    @frequency.setter
    def frequency(self, value: int):
        """Get or set the frequency of tics.
        If you set 8 as frequency, there will be 12 gaps in tics.
        Default is 10"""
        self._frequency = value
    # #------------------------------------------------------------------------7 FREQUENCY

    @property
    def minimum(self)-> int: return self._min_range

    @minimum.setter
    def minimum(self, value: int):
        """Get or set the minimum of level of trackbar value range."""
        self._min_range = value
    # #------------------------------------------------------------------------8 MINIMUM

    @property
    def maximum(self)-> int: return self._max_range

    @maximum.setter
    def maximum(self, value: int):
        """Get or set the maximum of level of trackbar value range."""
        self._max_range = value
    # #------------------------------------------------------------------------9 MAXIMUM

    @property
    def tic_position(self)-> TickPosition: return self._tic_pos

    @tic_position.setter
    def tic_position(self, value: TickPosition):
        """Get or set the tic position of trackbar"""
        self._tic_pos = value
    # #------------------------------------------------------------------------10 TIC POS

    @property
    def tooltip(self)-> bool: return self._tooltip

    @tooltip.setter
    def tooltip(self, value: bool):
        """Get or set the tooltip for trackbar"""
        self._tooltip = value
    # #------------------------------------------------------------------------11 TOOLTIP

    @property
    def reverse(self)-> bool: return self._reversed

    @reverse.setter
    def reverse(self, value: bool):
        """If set to True, the minimum & maximum points will be swapped"""
        self._reversed = value
    # #------------------------------------------------------------------------12 REVERSE

    @property
    def value(self)-> bool: return self._value

    @value.setter
    def value(self, value: bool):
        """Set or get the value of trackbar"""
        self._value = value
        if self._is_created: pass # TODO: Add code for this
    # #------------------------------------------------------------------------13 VALUE

    @property
    def selection_color(self)-> Color: return self._sel_color

    @selection_color.setter
    def selection_color(self, value: int):
        """Set or get the color for selection range of trackbar"""
        self._sel_color = Color(value)
    # #------------------------------------------------------------------------14 VALUE

    @property
    def tic_color(self)-> Color: return self._tic_color

    @tic_color.setter
    def tic_color(self, value: int):
        """Set or get the color for tic marks of trackbar"""
        self._tic_color = Color(value)
        if value and not self._cust_draw:
            self._cust_draw = True
    # #------------------------------------------------------------------------15 TIC COLOR

    @property
    def channel_color(self)-> Color: return self._channel_color

    @channel_color.setter
    def channel_color(self, value: int):
        """Set or get the color for channel of trackbar"""
        self._channel_color = Color(value)
    # #------------------------------------------------------------------------16 CHANNEL COLOR

    @property
    def free_move(self)-> bool: return self._free_move

    @free_move.setter
    def free_move(self, value: bool):
        """If set to True, thumb can be dragged freely. Default is False"""
        self._free_move = value
    # #------------------------------------------------------------------------17 FREE MOVE

    @property
    def tic_width(self)-> bool: return self._tic_width

    @tic_width.setter
    def tic_width(self, value: bool):
        """Set or get the tic width"""
        self._tic_width = value
    # #------------------------------------------------------------------------18 TIC WIDTH

    @property
    def no_tics(self)-> bool: return self._no_tics

    @no_tics.setter
    def no_tics(self, value: bool):
        """If set to True there would be no tic marks. Default is False"""
        self._no_tics = value
    # #------------------------------------------------------------------------19 NO TICs

    @property
    def channel_style(self)-> bool: return self._channel_style

    @channel_style.setter
    def channel_style(self, value: ChannelStyle):
        """Set or get the channel style. Possible styles are classic & outline. Default is classic"""
        self._channel_style = value
    # #------------------------------------------------------------------------19 NO TICs


    @property
    def custom_draw(self)-> int: return self._cust_draw # Fixme: Do we need this getter ?

    @custom_draw.setter
    def custom_draw(self, value: int):
        """Enable custom draw for this TrackBar.
        This will allow you to set the tic & channel colors, tic width & length etc. """
        self._cust_draw = value
        # if value: self._prepare_for_custom_draw()


    # #---------------------------------------------------------------------------------- CUSTOM DRAW

    # -endregion Properties
    x = 100 # Dummy line


# End TrackBar


class TicData:
    """Only for internal use.
    This class is a helper class to hold the
    tic logical positions and physical positions.
    """
    num = 0
    def __init__(self, physical_point: int, logical_point: int) -> None:
        self.index = TicData.num
        self.phy_point = physical_point
        self.log_point = logical_point
        TicData.num += 1

    def __str__(self) -> str:
        return f"{self.index = }, {self.phy_point = }, {self.log_point = }"



@SUBCLASSPROC # This decorator is essential.
def trk_wnd_proc(hw, msg, wp, lp, scID, refData) -> LRESULT:
    trk = trk_dict[hw]
    # log_msg(msg)
    match msg:
        case con.WM_DESTROY:
            res = api.RemoveWindowSubclass(hw, trk_wnd_proc, scID)
            # print(f"remove subclass for {trk.name}, res - {res}")

        case MyMessages.HORI_SCROLL | MyMessages.VERT_SCROLL:
            lwp = api.LOWORD(wp)
            match lwp:
                case con.TB_THUMBPOSITION:
                    # Thumb dragging finished. Let's collect the value
                    trk._set_value_internal(api.HIWORD(wp))

                    # if free_move property is false, we need to adjust the thumb on nearest tic.
                    if not trk._free_move: #Improve
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
                    api.InvalidateRect(hw, byref(trk._channel_rc), False)

                    trk._track_change = TrackChange.MOUSE_DRAG
                    if trk.on_dragged: trk.on_dragged(trk, EventArgs())
                    if trk.on_value_changed: trk.on_value_changed(trk, EventArgs())

                case  con.THUMB_LINE_HIGH:
                    trk._set_value_internal(api.SendMessage(hw, con.TBM_GETPOS, 0, 0))
                    trk._track_change = TrackChange.ARROW_HIGH
                    # print(trk._track_change)
                    if trk.on_value_changed:
                        trk.on_value_changed(trk, EventArgs())

                case con.THUMB_LINE_LOW:
                    trk._set_value_internal(api.SendMessage(hw, con.TBM_GETPOS, 0, 0))
                    trk._track_change = TrackChange.ARROW_LOW
                    # print(trk._track_change)
                    if trk.on_value_changed:
                        trk.on_value_changed(trk, EventArgs())

                case con.THUMB_PAGE_HIGH:
                    trk._set_value_internal(api.SendMessage(hw, con.TBM_GETPOS, 0, 0))
                    # print("value ", trk._value)
                    if not trk._lb_down:
                        trk._track_change = TrackChange.PAGE_HIGH
                        # print(trk._track_change, " 458 ")

                    if trk.on_value_changed:
                        trk.on_value_changed(trk, EventArgs())

                case con.THUMB_PAGE_LOW:
                    trk._set_value_internal(api.SendMessage(hw, con.TBM_GETPOS, 0, 0))
                    trk._track_change = TrackChange.PAGE_LOW
                    # print(trk._track_change)
                    if trk.on_value_changed:
                        trk.on_value_changed(trk, EventArgs())

                case con.TB_THUMBTRACK: # User dragging thumb.
                    trk._set_value_internal(api.HIWORD(wp))
                    # api.InvalidateRect(hw, byref(trk._channel_rc), False)
                    if trk.on_dragging: trk.on_dragging(trk, EventArgs())


        case MyMessages.LABEL_COLOR:
            return trk._bkg_brush

        case MyMessages.CTRL_NOTIFY:
            nmh = cast(lp, api.LPNMHDR)[0]
            match nmh.code:
                case con.NM_CUSTOMDRAW:
                    if trk._cust_draw:
                        # with Timing("nmh time: "):
                        nmcd = cast(lp, LPNMCUSTOMDRAW)[0]
                        match nmcd.dwDrawStage:
                            case con.CDDS_PREPAINT: return con.CDRF_NOTIFYITEMDRAW
                            case con.CDDS_ITEMPREPAINT:
                                # print(f"{nmcd.dwItemSpec = }, {con.TBCD_TICS = }, {con.TBCD_CHANNEL = }")
                                if nmcd.dwItemSpec == con.TBCD_CHANNEL:
                                    if trk._channel_style == ChannelStyle.CLASSIC:
                                        api.DrawEdge(nmcd.hdc, byref(nmcd.rc), con.EDGE_SUNKEN, con.BF_RECT | con.BF_ADJUST) # 1 style
                                    elif trk._channel_style == ChannelStyle.OUTLINE:
                                        api.SelectObject(nmcd.hdc, trk._channel_pen)
                                        api.Rectangle(nmcd.hdc, nmcd.rc.left, nmcd.rc.top, nmcd.rc.right, nmcd.rc.bottom )
                                    else:
                                        return con.CDRF_DODEFAULT

                                    if trk._sel_range: # Fill the selection range
                                        rc = trk._get_thumb_rect()
                                        if trk.fill_channel_rect(nmcd, rc):
                                            api.InvalidateRect(hw, byref(nmcd.rc), False)
                                    return con.CDRF_SKIPDEFAULT

                                if nmcd.dwItemSpec == con.TBCD_TICS:
                                    if not trk._no_tics:
                                        trk._draw_tics(nmcd.hdc)
                                        return con.CDRF_SKIPDEFAULT
                                    else: con.CDRF_DODEFAULT

                                # else: return con.CDRF_DODEFAULT


                                # else:pass
                                    # print("else part")
                                # return con.CDRF_DODEFAULT
                        return con.CDRF_DODEFAULT
                    else:
                        return 0 # We don't need to use custom draw
                case 4294967280: # con.TRBN_THUMBPOSCHANGING:
                    trk._track_change = TrackChange.MOUSE_CLICK
                    return 0
            return api.DefSubclassProc(hw, msg, wp, lp)


        # case con.WM_PAINT:
        #     ps = api.PAINTSTRUCT()
        #     api.BeginPaint(hw, byref(ps))

        #     api.EndPaint(hw, byref(ps))
        #     return 0

        case con.WM_SETFOCUS: trk._got_focus_handler()
        case con.WM_KILLFOCUS: trk._lost_focus_handler()
        case con.WM_LBUTTONDOWN:
            trk._lb_down = True
            trk._left_mouse_down_handler(msg, wp, lp)
        case con.WM_LBUTTONUP:
            trk._lb_down = False
            trk._left_mouse_up_handler(msg, wp, lp)
        case MyMessages.MOUSE_CLICK: trk._mouse_click_handler()
        case con.WM_RBUTTONDOWN: trk._right_mouse_down_handler(msg, wp, lp)
        case con.WM_RBUTTONUP: trk._right_mouse_up_handler(msg, wp, lp)
        case MyMessages.RIGHT_CLICK: trk._right_mouse_click_handler()
        case con.WM_MOUSEWHEEL: trk._mouse_wheel_handler(msg, wp, lp)
        case con.WM_MOUSEMOVE: trk._mouse_move_handler(msg, wp, lp)
        case con.WM_MOUSELEAVE: trk._mouse_leave_handler()

    return api.DefSubclassProc(hw, msg, wp, lp)

        # Track Messages
# 1024		TBM_GETPOS
# 1025		TBM_GETRANGEMIN
# 1026		TBM_GETRANGEMAX
# 1027		TBM_GETTIC
# 1028		TBM_SETTIC
# 1029		TBM_SETPOS
# 1030		TBM_SETRANGE
# 1031		TBM_SETRANGEMIN
# 1032		TBM_SETRANGEMAX
# 1033		TBM_CLEARTICS
# 1034		TBM_SETSEL
# 1035		TBM_SETSELSTART
# 1036		TBM_SETSELEND
# 1038		TBM_GETPTICS
# 1039		TBM_GETTICPOS
# 1040		TBM_GETNUMTICS
# 1041		TBM_GETSELSTART
# 1042		TBM_GETSELEND
# 1043		TBM_CLEARSEL
# 1044		TBM_SETTICFREQ
# 1045		TBM_SETPAGESIZE
# 1046		TBM_GETPAGESIZE
# 1047		TBM_SETLINESIZE
# 1048		TBM_GETLINESIZE
# 1049		TBM_GETTHUMBRECT
# 1050		TBM_GETCHANNELRECT
# 1051		TBM_SETTHUMBLENGTH
# 1052		TBM_GETTHUMBLENGTH
# 1053		TBM_SETTOOLTIPS
# 1054		TBM_GETTOOLTIPS
# 1055		TBM_SETTIPSIDE
# 1056		TBM_SETBUDDY
# 1057		TBM_GETBUDDY
