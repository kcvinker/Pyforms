
# calendarbox module - Created on 30-Nov-2022 00:37:20

from ctypes.wintypes import HWND, UINT, LPCWSTR
from ctypes import addressof, cast
import sys

from pyforms.src.control import Control
import pyforms.src.constants as con
from pyforms.src.commons import MyMessages
from pyforms.src.enums import ControlType, ViewMode
from pyforms.src.events import EventArgs
from pyforms.src.apis import RECT, LPNMHDR, LPNMSELCHANGE, LPNMVIEWCHANGE, SUBCLASSPROC
import pyforms.src.apis as api
from pyforms.src.colors import Color
from datetime import datetime
# from horology import Timing

calDict = {}
calStyle = con.WS_CHILD | con.WS_VISIBLE


class CalendarBox(Control):

    """Represents MonthCalendar control """

    Control.icc.initCommCtls(con.ICC_DATE_CLASSES)
    _count = 1
    __slots__ = ( "_showWeekNum", "_noTodayCircle", "_noToday", "_noTrailDates", "_shortDateNames",
                    "_fgColor", "_bgColor", "onSelectionCommitted", "onListClosed", "_value", "_viewMode", "_oldView",
                     "onViewChanged", "onSelectionChanged", "onValueChanged"  )

    def __init__(self, parent, xpos: int = 10, ypos: int = 10, auto = False) -> None:
        super().__init__()

        self._clsName = "SysMonthCal32"
        self.name = f"CalendarBox_{CalendarBox._count}"
        self._ctlType = ControlType.CALENDAR_BOX
        self._parent = parent
        self._bgColor = Color(parent._bgColor)
        self._font = parent._font
        self._width = 0
        self._height = 0
        self._xpos = xpos
        self._ypos = ypos
        self._style = calStyle
        self._exStyle = 0
        self._showWeekNum = False
        self._noTodayCircle = False
        self._noToday = False
        self._noTrailDates = False
        self._shortDateNames = False
        self._value = 0
        self._viewMode = ViewMode.MONTH_VIEW
        self._oldView = 0

        # Events
        self.onValueChanged = 0
        self.onViewChanged = 0
        self.onSelectionChanged = 0
        self._hwnd = None
        parent._controls.append(self)

        CalendarBox._count += 1
        if auto: self.createHandle()


    # Create's combo box handle
    def createHandle(self):

        """Create's calendar handle"""

        self._setStyles()
        self._createControl()
        if self._hwnd:
            calDict[self._hwnd] = self
            self._setSubclass(calWndProc)

            # Set the size for CalendarBox, because it is created with zero size
            rc = RECT()
            api.SendMessage(self._hwnd, con.MCM_GETMINREQRECT, 0, addressof(rc))
            self._width = rc.right
            self._height = rc.bottom
            api.SetWindowPos(self._hwnd, None, self._xpos, self._ypos, rc.right, rc.bottom, con.SWP_NOZORDER)

            # Get current selection from Calendar
            st = api.SYSTEMTIME()
            api.SendMessage(self._hwnd, con.MCM_GETCURSEL, 0, addressof(st))
            self._setValue(st)


    # -region private_funcs

    def _setStyles(self):
        if self._showWeekNum: self._styles |= con.MCS_WEEKNUMBERS
        if self._noTodayCircle: self._styles |= con.MCS_NOTODAYCIRCLE
        if self._noToday: self._styles  |= con.MCS_NOTODAY
        if self._noTrailDates: self._styles |= con.MCS_NOTRAILINGDATES
        if self._shortDateNames: self._styles |= con.MCS_SHORTDAYSOFWEEK

    def _setValue(self, st):
        self._value = datetime(st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond, st.wMilliseconds)

    # -endregion Private funcs

    # -region Properties

    @property
    def value(self)-> datetime: return self._value

    @value.setter
    def value(self, value: datetime):
        self._value = value
        st = self._makeSysTime(value)
        if self._isCreated: api.SendMessage(self._hwnd, con.MCM_SETCURSEL, 0, addressof(st))
    #----------------------------------------------------1

    @property
    def viewMode(self)-> ViewMode: return self._viewMode

    @viewMode.setter
    def viewMode(self, value: ViewMode):
        self._viewMode = value
        if self._isCreated: api.SendMessage(self._hwnd, con.MCM_SETCURRENTVIEW, 0, self._viewMode.value)
    #----------------------------------------------------2

    @property
    def oldViewMode(self) -> ViewMode: return self._oldView
    #----------------------------------------------------3

    @property
    def showWeekNumber(self)-> bool: return self._showWeekNum

    @showWeekNumber.setter
    def showWeekNumber(self, value): self._showWeekNum = value
    #----------------------------------------------------4

    @property
    def noTodayCircle(self)-> bool: return self._noTodayCircle

    @noTodayCircle.setter
    def noTodayCircle(self, value): self._noTodayCircle = value
    #----------------------------------------------------5

    @property
    def noToday(self)-> bool: return self._noToday

    @noToday.setter
    def noToday(self, value): self._noToday = value
    #----------------------------------------------------6

    @property
    def noTrailingDates(self)-> bool: return self._noTrailDates

    @noTrailingDates.setter
    def noTrailingDates(self, value): self._noTrailDates = value
    #----------------------------------------------------7

    @property
    def shortDateNames(self)-> bool: return self._shortDateNames

    @shortDateNames.setter
    def shortDateNames(self, value): self._shortDateNames = value
    #----------------------------------------------------8

    # -endregion Properties

    #dummy line


# End CalendarBox

# @WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR)
@SUBCLASSPROC
def calWndProc(hw, msg, wp, lp, scID, refData):
    # printWinMsg(msg)
    cal = calDict[hw]
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, calWndProc, scID)
            del calDict[hw]

        case MyMessages.CTRL_NOTIFY:
            nm = cast(lp, LPNMHDR).contents
            match nm.code:
                case con.MCN_SELECT: # 4294966550
                    nms = cast(lp, LPNMSELCHANGE).contents
                    cal._setValue(nms.stSelStart)
                    if cal.onValueChanged: cal.onValueChanged(cal, EventArgs())
                case con.MCN_SELCHANGE:
                    nms = cast(lp, LPNMSELCHANGE).contents
                    cal._setValue(nms.stSelStart)
                    if cal.onSelectionChanged: cal.onSelectionChanged(cal, EventArgs())

                case con.MCN_VIEWCHANGE:
                    nmv = cast(lp, LPNMVIEWCHANGE).contents
                    cal._viewMode = ViewMode(nmv.dwNewView)
                    cal._oldView = ViewMode(nmv.dwOldView)
                    if cal.onViewChanged: cal.onViewChanged(cal, EventArgs())

        case con.WM_SETFOCUS: cal._gotFocusHandler()
        case con.WM_KILLFOCUS: cal._lostFocusHandler()
        case con.WM_LBUTTONDOWN: cal._leftMouseDownHandler(msg, wp, lp)
        case con.WM_LBUTTONUP: cal._leftMouseUpHandler(msg, wp, lp)
        case con.WM_RBUTTONDOWN: cal._rightMouseDownHandler(msg, wp, lp)
        case con.WM_RBUTTONUP: cal._rightMouseUpHandler(msg, wp, lp)
        case con.WM_MOUSEWHEEL: cal._mouseWheenHandler(msg, wp, lp)
        case con.WM_MOUSEMOVE: cal._mouseMoveHandler(msg, wp, lp)
        case con.WM_MOUSELEAVE: cal._mouseLeaveHandler()

    return api.DefSubclassProc(hw, msg, wp, lp)
