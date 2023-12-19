# Created on 21-Jan-2023 00:41:20

from ctypes import byref, create_unicode_buffer
from pyforms.src.control import Control
import pyforms.src.constants as con
from pyforms.src.commons import MyMessages
from pyforms.src.enums import ControlType, ProgressBarStyle, ProgressBarState
from pyforms.src.apis import SUBCLASSPROC
import pyforms.src.apis as api
from pyforms.src.colors import Color
# from .winmsgs import log_msg

pgbDict = {}
pgbStyle = con.WS_CHILD | con.WS_VISIBLE | con.PBS_SMOOTH | con.WS_OVERLAPPED
pgbExStyle = 0# con.WS_EX_CLIENTEDGE

class ProgressBar(Control):

    _count = 1
    __slots__ = ( "_barStyle", "_vertical", "_minValue", "_maxValue", "_step", "_value",
                 "_percentage", "_state", "_speed", "_deciPrec", "_strPrec")

    def __init__(self, parent, xpos: int = 10, ypos: int = 10,
                 width: int = 180, height: int = 25, perc = False, auto = False ) -> None:
        super().__init__()
        self._clsName = "msctls_progress32"
        self.name = f"ProgressBar_{ProgressBar._count}"
        self._ctlType = ControlType.PROGRESS_BAR
        self._parent = parent
        # self._fgColor = Color(0x000000) # Control class is taking care of this
        self._font = parent._font
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._isTextable = False
        self._style = pgbStyle
        self._exStyle = pgbExStyle
        self._drawFlag = 0
        self._barStyle = ProgressBarStyle.BLOCK_STYLE
        self._state = ProgressBarState.NORMAL
        self._vertical = False
        self._minValue = 0
        self._maxValue = 100
        self._step = 1
        self._value = 0
        self._speed = 30
        self._percentage = perc
        self._strPrec = ""
        self._deciPrec = 0
        self._hwnd = None
        parent._controls.append(self)
        ProgressBar._count += 1
        if auto: self.createHandle()


    # -region Public funcs

    def createHandle(self):
        """Create progress bar's handle"""
        if self._barStyle == ProgressBarStyle.MARQUEE_STYLE: self._style |= con.PBS_MARQUEE
        if self._vertical: self._style |= con.PBS_VERTICAL
        self._createControl()
        if self._hwnd:
            pgbDict[self._hwnd] = self
            self._setSubclass(pgbWndProc)
            self._setFontInternal()
            if self._minValue != 0 or self._maxValue != 100:
                api.SendMessage(self._hwnd, con.PBM_SETRANGE32, self._minValue, self._maxValue)

            api.SendMessage(self._hwnd, con.PBM_SETSTEP, self._step, 0)


    def increment(self):
        """Increment value to one step"""
        self._value = self._step if self._value == self._maxValue else self._value + self._step
        if self._isCreated: api.SendMessage(self._hwnd, con.PBM_STEPIT, 0, 0)

    def startMarquee(self):
        """Srat marquee animation in progress bar."""
        if self._isCreated:
            self.style = ProgressBarStyle.MARQUEE_STYLE
            api.SendMessage(self._hwnd, con.PBM_SETMARQUEE, 1, self._speed)

    def stopMarquee(self):
        """Stop marquee animation of progress bar."""
        if self._isCreated:
            self.style = ProgressBarStyle.BLOCK_STYLE
            # api.SendMessage(self._hwnd, con.PBM_SETMARQUEE, 0, 0)


    # -endregion Public funcs

    # -region Private funcs

    # Draw percentage text on progress bar
    def _drawPercentage(self):
        ss = api.SIZE()
        perc = (self._value / self._maxValue) * 100
        if self._deciPrec == 0:
            formattedPerc = int(perc)
        else:
            formatStr = "{:.%df}" % self._deciPrec
            formattedPerc = formatStr.format(perc)
        txt = create_unicode_buffer(f"{formattedPerc}%")
        hdc = api.GetDC(self._hwnd)
        api.SelectObject(hdc, self._font._hwnd)
        api.GetTextExtentPoint32(hdc, txt, len(txt), byref(ss))
        x = (self._width - ss.cx) // 2
        y = (self._height - ss.cy) // 2
        api.SetBkMode(hdc, con.TRANSPARENT)
        api.SetTextColor(hdc, self._fgColor.ref)
        api.TextOut(hdc, x, y, txt, len(txt) )
        api.ReleaseDC(self._hwnd, hdc)


    # -endregion Private funcs

    # -region Properties

    @property
    def value(self):
        """Returns the value of progress bar"""
        return self._value

    @value.setter
    def value(self, value: int):
        """Set the value of progress bar"""
        self._value = value
        if self._isCreated: api.SendMessage(self._hwnd, con.PBM_SETPOS, value, 0)
    #-------------------------------------------------------------------------------[1]

    @property
    def maxValue(self):
        return self._maxValue

    @maxValue.setter
    def maxValue(self, value: int):
        """Set the maximum value of progress bar"""
        self._maxValue = value
        if self._isCreated: api.SendMessage(self._hwnd, con.PBM_SETRANGE32, 0, value)

    @property
    def step(self):
        """Returns the step property of progress bar"""
        return self._step

    @step.setter
    def step(self, value: int):
        """Set the step property of progress bar"""
        self._step = value
    #-------------------------------------------------------------------------------[2]

    @property
    def state(self):
        """Set the state of progress bar. Check ProgressBarState enum."""
        return self._state

    @state.setter
    def state(self, value: ProgressBarState):
        """Set the state of progress bar. Check ProgressBarState enum."""
        self._state = value
        api.SendMessage(self._hwnd, con.PBM_SETSTATE, value, 0);
    #-------------------------------------------------------------------------------[3]

    @property
    def style(self) -> ProgressBarStyle:
        """Returns the style of progress bar. Check ProgressBarStyle enum."""
        return self._barStyle

    @style.setter
    def style(self, value: ProgressBarStyle):
        """Set the style of progress bar. Check ProgressBarStyle enum."""
        if self._barStyle != value and self._isCreated:
            self.value = 0
            # old_val = self.
            if value == ProgressBarStyle.BLOCK_STYLE:
                self._style ^= con.PBS_MARQUEE
                self._style |= con.PBS_SMOOTH
            else:
                self._style ^= con.PBS_SMOOTH
                self._style |= con.PBS_MARQUEE

            api.SetWindowLongPtr(self.handle, con.GWL_STYLE, self._style)
            if value == ProgressBarStyle.MARQUEE_STYLE:
                api.SendMessage(self._hwnd, con.PBM_SETMARQUEE, 1, self._speed)
            else:
                api.SendMessage(self._hwnd, con.PBM_SETMARQUEE, 0, 0)

        self._barStyle = value

    @property
    def drawPercentage(self):
        return self._percentage

    @drawPercentage.setter
    def drawPercentage(self, value: bool):
        self._percentage = value

    @property
    def decimalPrecision(self):
        return self._deciPrec

    @decimalPrecision.setter
    def decimalPrecision(self, value: int):
        self._deciPrec = value
        # self._strPrec = for

    # -endregion Properties

#End ProgressBar

@SUBCLASSPROC
def pgbWndProc(hw, msg, wp, lp, scID, refData):
    # log_msg(msg)
    pgb = pgbDict[hw]
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, pgbWndProc, scID)
            del pgbDict[hw]

        case con.WM_SETFOCUS: pgb._gotFocusHandler()
        case con.WM_KILLFOCUS: pgb._lostFocusHandler()
        case con.WM_LBUTTONDOWN: pgb._leftMouseDownHandler(msg, wp, lp)
        case con.WM_LBUTTONUP: pgb._leftMouseUpHandler(msg, wp, lp)
        case con.WM_RBUTTONDOWN: pgb._rightMouseDownHandler(msg, wp, lp)
        case con.WM_RBUTTONUP: pgb._rightMouseUpHandler(msg, wp, lp)
        case con.WM_MOUSEWHEEL: pgb._mouseWheenHandler(msg, wp, lp)
        case con.WM_MOUSEMOVE: pgb._mouseMoveHandler(msg, wp, lp)
        case con.WM_MOUSELEAVE: pgb._mouseLeaveHandler()
        case con.WM_PAINT:
            ret = api.DefSubclassProc(hw, msg, wp, lp)
            if pgb._percentage and pgb._barStyle != ProgressBarStyle.MARQUEE_STYLE:
                pgb._drawPercentage()
            return ret

    return api.DefSubclassProc(hw, msg, wp, lp)

