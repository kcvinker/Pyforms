# numberpicker module Created on 12-Dec-2022 23:04:20

from ctypes.wintypes import HWND, UINT
from ctypes import WINFUNCTYPE, byref, cast
from pyforms.src.control import Control
import pyforms.src.constants as con
from pyforms.src.commons import MyMessages
from pyforms.src.enums import ControlType, TextAlignment
from pyforms.src.events import EventArgs
import pyforms.src.apis as api
from pyforms.src.apis import LRESULT, UINT_PTR, DWORD_PTR, WPARAM, LPARAM, SUBCLASSPROC
from pyforms.src.colors import Color, clamp
# from .winmsgs import log_msg

numpDict = {}
npTbDict = {}
numpStyle = con.WS_VISIBLE | con.WS_CHILD  | con.UDS_ALIGNRIGHT | con.UDS_ARROWKEYS | con.UDS_AUTOBUDDY | con.UDS_HOTTRACK
# txtFlag = con.DT_SINGLELINE | con.DT_VCENTER | con.DT_CENTER | con.DT_NOPREFIX


class NumberPicker(Control):
    """NumberPicker class is sometimes known as Spinner or Updown control.
        In .NET family, it's name is NumericUpDown.
    """
    Control.icc.initCommCtls(con.ICC_UPDOWN_CLASS)
    _count = 1
    __slots__ = ( "_hideCaret", "_trackMouseLeave", "_btnOnLeft", "_hasSep", "_topEdgeFlag", "_botEdgeFlag",
                    "_autoRotate", "_minRange", "_maxRange", "_value", "_step", "_deciPrecis", "_buddyRect",
                    "_buddyStyle", "_buddyExStyle", "_buddyHwnd", "_buddyCID", "_buddySubclsID", "_linex", "_destroyCount",
                    "_buddySubclsProc", "_txtPos", "onValueChanged", "_myRect", "_udRect", "_keyPressed" )

    def __init__(self, parent, xpos: int = 10, ypos: int = 10, 
                 width: int = 70, height: int = 24 ) -> None:
        super().__init__()
        self._clsName = "msctls_updown32"
        self.name = f"NumberPicker_{NumberPicker._count}"
        self._ctlType = ControlType.NUM_PICKER
        self._parent = parent
        self._bgColor = Color(0xFFFFFF)
        self._font.colneFrom(parent._font)
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self._style = numpStyle
        self._exStyle = 0x00000000
        self._btnOnLeft = False
        self._maxRange = 100
        self._minRange = 0
        self._deciPrecis = 0
        self._autoRotate = False
        self._step = 1
        self._buddyStyle = con.WS_CHILD | con.WS_VISIBLE | con.ES_NUMBER | con.WS_BORDER
        self._buddyExStyle = con.WS_EX_LEFT | con.WS_EX_LTRREADING
        self._value = self._minRange
        self._txtPos = TextAlignment.LEFT
        self._buddyCID = 0
        self._hasSep = False
        self._buddyRect = api.RECT()
        self._myRect = api.RECT()
        self._udRect = api.RECT()
        self._trackMouseLeave = False
        self._keyPressed = False
        self._topEdgeFlag = con.BF_TOPLEFT
        self._botEdgeFlag = con.BF_BOTTOM
        self._hideCaret = False
        self._linex = 0
        self._destroyCount = 0
        self._hwnd = None
        parent._controls.append(self)

        #Events
        self.onValueChanged = None

        NumberPicker._count += 1
        if parent.createChilds: self.createHandle()


    # -region Public funcs
    def createHandle(self):
        self._npSetStyles()
        self._setCtlID()
        self._hwnd = api.CreateWindowEx(self._exStyle,
                                        self._clsName,
                                        self._text,
                                        self._style,
                                        0, 0, 0, 0,
                                        self._parent._hwnd,
                                        self._cid,
                                        self._parent.wnd_class.hInstance, None )
        if self._hwnd:
            numpDict[self._hwnd] = self
            self._setSubclass(npWndProc)
            self._setFontInternal()

            self._buddyCID = Control._ctl_id
            self._buddySubclsID = Control._subclass_id
            Control._subclass_id += 1
            if self._btnOnLeft: self.width -= 2
            self._buddyHwnd = api.CreateWindowEx(  self._buddyExStyle,
                                                    "Edit",
                                                    self._text,
                                                    self._buddyStyle,
                                                    self._xpos,
                                                    self._ypos,
                                                    self._width,
                                                    self._height,
                                                    self._parent._hwnd,
                                                    self._buddyCID,
                                                    self._parent.wnd_class.hInstance, None )

            if self._buddyHwnd:
                self._isCreated = True
                Control._ctl_id += 1
                api.SetWindowSubclass(self._buddyHwnd, buddyWndProc, self._buddySubclsID, self._hwnd)
                api.SendMessage(self._buddyHwnd, con.WM_SETFONT, self.font.handle, 1)
                old_buddy = api.SendMessage(self._hwnd, con.UDM_SETBUDDY, self._buddyHwnd, 0)
                api.SendMessage(self._hwnd, con.UDM_SETRANGE32, int(self._minRange), int(self._maxRange))

                api.GetClientRect(self._buddyHwnd, byref(self._buddyRect))
                api.GetClientRect(self._hwnd, byref(self._udRect))
                api.SetRect(byref(self._myRect), self._xpos, self._ypos, (self._xpos + self._width), (self._ypos + self._height))
                self._displayValue()
                self._resizeBuddy()
                if old_buddy: api.SendMessage(old_buddy, MyMessages.BUDDY_RESET, 0, 0)

    # -endregion Public funcs

    # -region Private funcs
    # Set number picker style bits
    def _npSetStyles(self):
        if self._btnOnLeft:
            self._style ^= con.UDS_ALIGNRIGHT
            self._style |= con.UDS_ALIGNLEFT
            self._topEdgeFlag = con.BF_TOP
            self._botEdgeFlag = con.BF_BOTTOMRIGHT
            if self._txtPos == TextAlignment.LEFT: self._txtPos = TextAlignment.RIGHT

        match self._txtPos:
            case TextAlignment.LEFT: self._buddyStyle |= con.ES_LEFT
            case TextAlignment.CENTER: self._buddyStyle |= con.ES_CENTER
            case TextAlignment.RIGHT: self._buddyStyle |= con.ES_RIGHT

    # Internal function to display value
    def _displayValue(self):
        if self._hasSep:
            self._text = f"{self._value:,.{self._deciPrecis}f}"
        else:
            self._text = f"{self._value:.{self._deciPrecis}f}"
            # print(f"{self._text = }")
        api.SetWindowText(self._buddyHwnd, self._text )

    # Internal function to calculate value
    def _setNpkValue(self, delta: int):
        value = self._value + (delta * self._step)
        # print("value 1 : ", value)
        if self._autoRotate:
            if value > self._maxRange:
                self._value = self._minRange
            elif value < self._minRange:
                self._value = self._maxRange
            else:
                self._value = value
        else:
            if value < self._minRange: self._value = self._minRange
            elif value > self._maxRange: self._value = self._maxRange
            else: self._value = value
            # self._value = clamp(value, self.minRange, self._maxRange) #NOTE : Delete this


    # Internal function to check if mouse is over us.
    def _isMouseUponMe(self) -> bool:
        # If this returns False, mouse_leave event will triggered
        # Since, updown control is a combo of an edit and button controls...
        # we have no better options to control the mouse enter & leave mechanism.
        # Now, we create an imaginary rect over the bondaries of these two controls.
        # If mouse is inside that rect, there is no mouse leave. Perfect hack.
        pt = api.POINT()
        api.GetCursorPos(byref(pt))
        api.ScreenToClient(self._parent._hwnd, byref(pt))
        res = api.PtInRect(byref(self._myRect), pt)
        return res

    # Internal function to resize buddy edit
    def _resizeBuddy(self):
        swp_flag = con.SWP_NOACTIVATE | con.SWP_NOZORDER
        if self._btnOnLeft:
            api.SetWindowPos(self._buddyHwnd, None,
                            self._xpos + self._udRect.right,
                            self._ypos,
                            self._buddyRect.right,
                            self._buddyRect.bottom, swp_flag)
            self._linex = self._buddyRect.left
        else:
            api.SetWindowPos(self._buddyHwnd, None,
                            self._xpos,
                            self._ypos,
                            self._buddyRect.right - 2,
                            self._buddyRect.bottom, swp_flag)

            self._linex = self._buddyRect.right - 3

    # -endregion Private funcs

    # -region Properties


    @property
    def decimalPlaces(self):
        """Get the decimal points of NumberPicker"""
        return self._deciPrecis

    @decimalPlaces.setter
    def decimalPlaces(self, value: int):
        """Set the decimal points of NumberPicker"""
        self._deciPrecis = value
    #-----------------------------------------------------------------------[1]

    @property
    def minRange(self):
        """Get minimum value of NumberPicker's range"""
        return self._minRange

    @minRange.setter
    def minRange(self, value: int | float):
        """Set minimum value of NumberPicker's range"""
        self._minRange = value
        if self._isCreated:
            api.SendMessage(self._hwnd, con.UDM_SETRANGE32, int(self._minRange), int(self._maxRange))
        else:
            self._value = value
    #----------------------------------------------------------------------------------------[2]

    @property
    def maxRange(self):
        """Get maximum value of NumberPicker's range"""
        return self._maxRange

    @maxRange.setter
    def maxRange(self, value: int | float):
        """Set maximum value of NumberPicker's range"""
        self._maxRange = value
        api.SendMessage(self._hwnd, con.UDM_SETRANGE32, int(self._minRange), int(self._maxRange))
    #-----------------------------------------------------------------------------------[3]

    @property
    def autoRotate(self):
        """Returns true if auto rotate is enabled. This means, it jumped from min value to max and vice versa."""
        return self._autoRotate

    @autoRotate.setter
    def autoRotate(self, value: bool):
        """Set true if auto rotate is enabled. This means, it jumped from min value to max and vice versa."""
        self._autoRotate = value
    #-----------------------------------------------------------------------[4]

    @property
    def step(self):
        """Get the step value of NumberPicker. Step is the amount of value jumped at one click."""
        return self._step

    @step.setter
    def step(self, value: int):
        """Set the step value of NumberPicker. Step is the amount of value jumped at one click."""
        self._step = value
        stepStr = str(value)
        if "." in stepStr:
            stArr = stepStr.split(".")
            self._deciPrecis = len(stArr)
    #-----------------------------------------------------[5]

    @property
    def value(self) -> float:
        """Get the NumberPicker's value"""
        return self._value

    @value.setter
    def value(self, value: float):
        """Set the NumberPicker's value"""
        self._value = value
        if self._isCreated:
            api.SetWindowText(self._buddyHwnd, f"{self._value:.{self._deciPrecis}f}")
    #----------------------------------------------------------------------------------[6]


    @property
    def buttonOnLeft(self):
        """Returns true if button is set on left side"""
        return self._btnOnLeft

    @buttonOnLeft.setter
    def buttonOnLeft(self, value: bool):
        """Set true if button is set on left side"""
        self._btnOnLeft = value
        if self._isCreated: pass # api.SendMessage(self._buddyHwnd, con.EM_SETSEL, -1, 0)
        # TODO : Change window style constants here to update the control.
    #-------------------------------------------------------------------[8]

    @property
    def hasSeperator(self):
        """Returns true if seperator is enabled"""
        return self._hasSep

    @hasSeperator.setter
    def hasSeperator(self, value: bool):
        """Set true if seperator is enabled"""
        self._hasSep = value
    #-----------------------------------------------------[9]

    @property
    def hideCaret(self):
        """Returns true if caret is hidden"""
        return self._hideCaret

    @hideCaret.setter
    def hideCaret(self, value: bool):
        """Set true to hide the caret"""
        self._hideCaret = value
    #-----------------------------------------------------[10]

    @Control.onMouseEnter.setter
    def onMouseEnter(self, value):
        """Set mouse evnte event handler"""
        self._onMouseEnter = value
        self._trackMouseLeave = True
    #--------------------------------------------[11]


    @Control.onMouseLeave.setter
    def onMouseLeave(self, value):
        """Set mouse leave event handler"""
        self._onMouseLeave = value
        self._trackMouseLeave = True
    #--------------------------------------------[12]
    # -endregion Properties


#End NumberPicker


@SUBCLASSPROC
def npWndProc(hw, msg, wp, lp, scID, refData) -> LRESULT:

    np = numpDict[hw]
    # log_msg(msg, f"Main proc {np.name}")
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, npWndProc, scID)
            np._destroyCount += 1
            if np._destroyCount == 2: del numpDict[hw]

        case MyMessages.CTRL_NOTIFY:
            nm = cast(lp, api.LPNMUPDOWN).contents
            if nm.hdr.code == con.UDN_DELTAPOS:
                np._value = float(np._getCtrlTextEx(np._buddyHwnd))
                np._setNpkValue(nm.iDelta)
                np._displayValue()
                if np.onValueChanged: np.onValueChanged(np, EventArgs())

        case con.WM_SETFOCUS: np._gotFocusHandler()
        case con.WM_KILLFOCUS: np._lostFocusHandler()
        case con.WM_LBUTTONDOWN: np._leftMouseDownHandler(msg, wp, lp)
        case con.WM_LBUTTONUP: np._leftMouseUpHandler(msg, wp, lp)
        case MyMessages.MOUSE_CLICK: np._mouse_click_handler()
        case con.WM_RBUTTONDOWN: np._rightMouseDownHandler(msg, wp, lp)
        case con.WM_RBUTTONUP: np._rightMouseUpHandler(msg, wp, lp)
        case MyMessages.RIGHT_CLICK: np._right_mouse_click_handler()
        case con.WM_MOUSEWHEEL: np._mouseWheenHandler(msg, wp, lp)
        case con.WM_MOUSEMOVE: np._mouseMoveHandler(msg, wp, lp)
        case con.WM_MOUSELEAVE:
            if np._trackMouseLeave:
                if not np._isMouseUponMe():
                    np._isMouseEntered = False
                    if np.on_mouse_leave: np.on_mouse_leave(np, EventArgs())

    return api.DefSubclassProc(hw, msg, wp, lp)



@WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR)
def buddyWndProc(hw, msg, wp, lp, scID, refData) -> LRESULT:

    np = numpDict[refData]
    # log_msg(msg, np.name)
    match msg:
        case con.WM_DESTROY:
            api.RemoveWindowSubclass(hw, buddyWndProc, scID)
            np._destroyCount += 1
            if np._destroyCount == 2: del numpDict[refData]

        case MyMessages.EDIT_COLOR:
            # Whether user selects a back color or not, we must set the back color.
            # Otherwise, NumberPicker will be drawn in default control back color by DefWndProc
            # hdc = HDC(wp)
            if np._drawFlag & 1: api.SetTextColor(wp, np._fgColor.ref)
            api.SetBkColor(wp, np._bgColor.ref)
            return api.CreateSolidBrush(np._bgColor.ref)

        case con.WM_MOUSELEAVE:
            if np._trackMouseLeave:
                if not np._isMouseUponMe():
                    np._isMouseEntered = False
                    if np.on_mouse_leave: np.on_mouse_leave(np, EventArgs())

        case con.WM_MOUSEMOVE: np._mouseMoveHandler(msg, wp, lp)

        case con.EM_SETSEL:
            # Edit control in NumberPicker is not support auto selection.
            return False

        case MyMessages.CTL_COMMAND:
            code = api.HIWORD(wp)
            # print("wm command ", code)
            match code:
                case con.EN_CHANGE:pass
                case con.EN_UPDATE:
                    if np._hideCaret: api.HideCaret(hw)

        case con.WM_KEYDOWN:
            np._keyPressed = True
            np._keyDownHandler(wp)

        case con.WM_KEYUP: np._keyUpHandler(wp)
        case con.WM_CHAR: np._keyPressHandler(wp)
        case con.WM_SETFOCUS: np._gotFocusHandler()
        case con.WM_KILLFOCUS:
            # When user manually enter numbers, we need to check that value
            # And displays it in as per our current value protocol.
            if np._keyPressed:
                np._value = float(np._getCtrlTextEx(hw))
                np._setNpkValue(0)
                np._keyPressed = False
                np._displayValue()
            np._lostFocusHandler()

        case con.WM_LBUTTONDOWN:
            # Some of the drawing job in edit control is not through the wm_paint message.
            # If we click on it, it will start drawing without sending wm_paint.
            # So, when a click is received in an edit control, we need an immediate redraw.
            # Otherwise, we will lost our beautiful top edge.
            # api.RedrawWindow(hw, None, None, con.RDW_INTERNALPAINT)
            np._leftMouseDownHandler(msg, wp, lp)
        case con.WM_LBUTTONUP: np._leftMouseUpHandler(msg, wp, lp)
        case con.WM_RBUTTONDOWN: np._rightMouseDownHandler(msg, wp, lp)
        case con.WM_RBUTTONUP: np._rightMouseUpHandler(msg, wp, lp)
        case con.WM_MOUSEWHEEL: np._mouseWheenHandler(msg, wp, lp)

        case con.WM_PAINT:
            # Edit control needs to be painted by DefSubclassProc function.
            # Otherwise, cursor and text will not be visible, So we need to call it.
            api.DefSubclassProc(hw, msg, wp, lp)

            # Now, Edit's painting job is done and control is ready for our drawing.
            # So, first, we are going to draw 3 edges for this Edit control.
            # Then we, will draw a single line to mask the control border.
            # with Timing("paint time : "): # 60-70 micro secs average
            hdc = api.GetDC(hw)
            api.DrawEdge(hdc, byref(np._buddyRect), con.BDR_SUNKENOUTER, np._topEdgeFlag) # Right code
            api.DrawEdge(hdc, byref(np._buddyRect), con.BDR_RAISEDINNER, np._botEdgeFlag )
            fpen = api.CreatePen(con.PS_SOLID, 1, np._bgColor.ref) # We use Edit's back color.
            api.SelectObject(hdc, fpen)
            api.MoveToEx(hdc, np._linex, 1, None)
            api.LineTo(hdc, np._linex, np._height - 1)
            api.ReleaseDC(hw, hdc)
            api.DeleteObject(fpen)
            return 1
        case MyMessages.BUDDY_RESET:
            np._resizeBuddy()

    return api.DefSubclassProc(hw, msg, wp, lp)
