# datetimepicker module - Created on 10-Dec-2022 17:45:20

from ctypes.wintypes import HWND, UINT
from ctypes import WINFUNCTYPE, addressof, create_unicode_buffer, cast, create_string_buffer
from pyforms.src.control import Control
import pyforms.src.constants as con
from pyforms.src.commons import MyMessages
from pyforms.src.enums import ControlType, DateFormat
from pyforms.src.events import EventArgs, DateTimeEventArgs
from pyforms.src.apis import LPNMHDR, LPNMDATETIMECHANGE, SUBCLASSPROC
import pyforms.src.apis as api
from pyforms.src.colors import Color
from datetime import datetime
# from horology import Timing

dtpDict = {}
dtpStyle = con.WS_CHILD | con.WS_VISIBLE
OBJ_BRUSH = 0x00000002


class DateTimePicker(Control):

    """DateTimePicker control """
    Control.icc.initCommCtls(con.ICC_DATE_CLASSES)
    _count = 1
    __slots__ = ( "_shoWeekNum", "_noTodayCircle", "_noToday", "_noTrailDates", "_shotDateNames",
                "_showUpdown", "_format", "_fmtString", "_4DYear", "_value", "_eventHandled",
                "_rightAlign", "_calStyle", "_autoSize", "onCalendarOpened", "onValueChanged",
                "onCalendarClosed"  )


    def __init__(self, parent, xpos: int = 10, ypos: int = 10) -> None:
        super().__init__()

        self._clsName = "SysDateTimePick32"
        self.name = f"DateTimePicker{DateTimePicker._count}"
        self._ctlType = ControlType.DATE_TIME_PICKER
        self._parent = parent
        self._bgColor = Color(0xFFFFFF)
        # self._fgColor = Color(0x000000) # Not needed, since Control's init function is doing this.
        # self._font = parent._font
        self._font.colneFrom(parent._font)
        self._width = 0
        self._height = 0
        self._xpos = xpos
        self._ypos = ypos
        self._style = dtpStyle
        self._exStyle = 0
        self._shoWeekNum = False
        self._noTodayCircle = False
        self._noToday = False
        self._noTrailDates = False
        self._shotDateNames = False
        self._value = 0
        self._format = DateFormat.CUSTOM_DATE
        self._fmtString = "dd-MMM-yyyy"
        self._showUpdown = False
        self._4DYear = False
        self._rightAlign = False
        self._calStyle = 0
        self._eventHandled = False
        self._autoSize = True

        # Events
        self.onValueChanged = None
        self.onCalendarOpened = None
        self.onCalendarClosed = None
        self._hwnd = None
        parent._controls.append(self)

        DateTimePicker._count += 1


    # Create's combo box handle
    def createHandle(self):

        """Create's calendar handle"""

        self._setStyles()
        self._createControl()
        if self._hwnd:
            dtpDict[self._hwnd] = self
            self._setSubclass(dtpWndProc)
            self._setFontInternal()
            #
            if self._format == DateFormat.CUSTOM_DATE:
                # with Timing("pyforms unicode time : "):
                buff = create_unicode_buffer(self._fmtString)
                api.SendMessage(self._hwnd, con.DTM_SETFORMATW, 0, addressof(buff))

            if self._calStyle > 0:
                api.SendMessage(self._hwnd, con.DTM_SETMCSTYLE, 0, self._calStyle)

            if self._autoSize:
                ss = api.SIZE()
                api.SendMessage(self._hwnd, con.DTM_GETIDEALSIZE, 0, addressof(ss))
                self._width = ss.cx + 2
                self._height = ss.cy + 5
                api.SetWindowPos(self._hwnd, None, self._xpos, self._ypos, self._width, self._height, con.SWP_NOZORDER)

            # Get current selection from date picker
            st = api.SYSTEMTIME()
            res = api.SendMessage(self._hwnd, con.DTM_GETSYSTEMTIME, 0, addressof(st))

            if res == 0: self._value = self._makeDateTime(st)



    # -region private_funcs

    # Set dtp styles
    def _setStyles(self):
        match self._format:
            case DateFormat.CUSTOM_DATE:
                self._style = con.WS_TABSTOP | con.WS_CHILD| con.WS_VISIBLE | con.DTS_LONGDATEFORMAT | con.DTS_APPCANPARSE
            case DateFormat.LONG_DATE:
                self._style = con.WS_TABSTOP | con.WS_CHILD| con.WS_VISIBLE| con.DTS_LONGDATEFORMAT
            case DateFormat.SHORT_DATE:
                if self._4DYear:
                    self._style = con.WS_TABSTOP | con.WS_CHILD| con.WS_VISIBLE| con.DTS_SHORTDATECENTURYFORMAT
                else:
                    self._style = con.WS_TABSTOP | con.WS_CHILD| con.WS_VISIBLE| con.DTS_SHORTDATEFORMAT
            case DateFormat.TIME_ONLY:
                self._style = con.WS_TABSTOP | con.WS_CHILD| con.WS_VISIBLE| con.DTS_TIMEFORMAT

        if self._shoWeekNum: self._style |= con.MCS_WEEKNUMBERS
        if self._noTodayCircle: self._style |= con.MCS_NOTODAYCIRCLE
        if self._noToday: self._style  |= con.MCS_NOTODAY
        if self._noTrailDates: self._style |= con.MCS_NOTRAILINGDATES
        if self._shotDateNames: self._style |= con.MCS_SHORTDAYSOFWEEK
        if self._rightAlign: self._style |= con.DTS_RIGHTALIGN
        if self._showUpdown: self._style ^= con.DTS_UPDOWN
        self._bkgBrush = self._bgColor.createHBrush()

    # -endregion Private funcs

    # -region Properties

    @property
    def formatString(self):
        """Get format string from DTP"""
        return self._fmtString

    @formatString.setter
    def formatString(self, value: str):
        """Set the format string for this DTP"""
        self._fmtString = value
        self._format = DateFormat.CUSTOM_DATE
        if self._isCreated:
            buff = create_string_buffer(self._fmtString.encode())
            api.SendMessage(self._hwnd, con.DTM_SETFORMATA, 0, addressof(buff))
    #-----------------------------------------------------------------------------1

    @property
    def format(self)-> DateFormat:
        """Get the format of this DTP. Check for DateFormat enum"""
        return self._format

    @format.setter
    def format(self, value: DateFormat):
        """Set the format of this DTP. Check for DateFormat enum"""
        self._format = value
    #------------------------------------------------------------------------2

    @property
    def rightAlign(self)-> bool:
        """Get true if this DTP is right aligned"""
        return self._rightAlign

    @rightAlign.setter
    def rightAlign(self, value: bool):
        """Set true to right aligne this DTP"""
        self._rightAlign = value
    #------------------------------------------------------------------------3

    @property
    def fourDigitYear(self)-> bool:
        """Returns true if this DTP has four digit year"""
        return self._4DYear

    @fourDigitYear.setter
    def fourDigitYear(self, value: bool):
        """Set true if this DTP has four digit year"""
        self._4DYear = value
    #------------------------------------------------------------------------4

    @property
    def showUpdown(self)-> bool:
        """Returns true if this DTP has an updown button"""
        return self._showUpdown

    @showUpdown.setter
    def showUpdown(self, value: bool):
        """Set true if this DTP has an updown button"""
        self._showUpdown = value
    #------------------------------------------------------------------------5

    @property
    def value(self)-> datetime:
        """Get the value of DTP - type is DateTime"""
        return self._value

    @value.setter
    def value(self, value: datetime):
        """Set the value of DTP - type is DateTime"""
        self._value = value
        st = self._makeSysTime(value)
        if self._isCreated: api.SendMessage(self._hwnd, con.DTM_SETSYSTEMTIME, 0, addressof(st))
    #--------------------------------------------------------------------------------------------6

    @property
    def showWeekNumber(self)-> bool:
        """Returns true if this DTP has week number"""
        return self._shoWeekNum

    @showWeekNumber.setter
    def showWeekNumber(self, value):
        """Set true if this DTP has week number"""
        self._shoWeekNum = value
    #----------------------------------------------------------------------7

    @property
    def noTodayCircle(self)-> bool:
        """Returns true if this DTP has no Today Circle"""
        return self._noTodayCircle

    @noTodayCircle.setter
    def noTodayCircle(self, value):
        """Set true if this DTP has no Today Circle"""
        self._noTodayCircle = value
    #-------------------------------------------------------------------------8

    @property
    def noToday(self)-> bool:
        """Returns true if this DTP has no Today"""
        return self._noToday

    @noToday.setter
    def noToday(self, value):
        """Set true if this DTP has no Today"""
        self._noToday = value
    #---------------------------------------------------------9

    @property
    def noTrailingDates(self)-> bool:
        """Returns true if this DTP has no trailing dates"""
        return self._noTrailDates

    @noTrailingDates.setter
    def noTrailingDates(self, value):
        """Set true if this DTP has no trailing"""
        self._noTrailDates = value
    #-------------------------------------------------------------------------10

    @property
    def shortDateNames(self)-> bool:
        """Returns true if this DTP has short date names"""
        return self._shotDateNames

    @shortDateNames.setter
    def shortDateNames(self, value):
        """Set true if this DTP has short date names"""
        self._shotDateNames = value
    #---------------------------------------------------------------------------11

    # -endregion Properties

# End DateTimePicker


@SUBCLASSPROC
def dtpWndProc(hw, msg, wp, lp, scID, refData):
    # printWinMsg(msg)
    dtp = dtpDict[hw]
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, dtpWndProc, scID)
            del dtpDict[hw]

        case MyMessages.CTRL_NOTIFY:
            nm = cast(lp, LPNMHDR).contents
            match nm.code:
                case con.DTN_USERSTRINGW:
                     # if dtp.on_text_changed:
                     dts = cast(lp, api.LPNMDATETIMESTRINGW).contents
                     dea = DateTimeEventArgs(dts.pszUserString, dts.st)
                    #  print(dts.st.wYear)
                     return 0

                case con.DTN_DROPDOWN:
                    if dtp.onCalendarOpened:
                        dtp.onCalendarOpened(dtp, EventArgs())
                        return 0

                case con.DTN_CLOSEUP:
                    if dtp.onCalendarClosed:
                        dtp.onCalendarClosed(dtp, EventArgs())
                        return 0

                case con.DTN_DATETIMECHANGE:
                    # For unknown reason, this notification occurs two times back to back.
                    # So, we need to use a boolean flag to suppress one notification.
                    if dtp._eventHandled:
                        dtp._eventHandled = False
                    else:
                        # print("273")
                        dtp._eventHandled = True
                        dic = cast(lp, LPNMDATETIMECHANGE).contents
                        dtp._value = dtp._makeDateTime(dic.st)
                        if dtp.onValueChanged:
                            dtp.onValueChanged(dtp, EventArgs())
                            return 0

        case con.WM_SETFOCUS: dtp._gotFocusHandler()
        case con.WM_KILLFOCUS: dtp._lostFocusHandler()
        case con.WM_LBUTTONDOWN: dtp._leftMouseDownHandler(msg, wp, lp)
        case con.WM_LBUTTONUP: dtp._leftMouseUpHandler(msg, wp, lp)
        case con.WM_RBUTTONDOWN: dtp._rightMouseDownHandler(msg, wp, lp)
        case con.WM_RBUTTONUP: dtp._rightMouseUpHandler(msg, wp, lp)
        case con.WM_MOUSEWHEEL: dtp._mouseWheenHandler(msg, wp, lp)
        case con.WM_MOUSEMOVE: dtp._mouseMoveHandler(msg, wp, lp)
        case con.WM_MOUSELEAVE: dtp._mouseLeaveHandler()

    return api.DefSubclassProc(hw, msg, wp, lp)
