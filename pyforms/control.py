# Control module - Created on 08-Nov-2022 00:08:28


from ctypes.wintypes import UINT, HWND
from ctypes import (create_unicode_buffer, byref, 
                    sizeof, cast, addressof)
from pyforms.enums import ControlType, FontWeight
from pyforms.commons import Font, MyMessages, StaticData, FontOwner
from pyforms.apis import (MapWindowPoints, LPPOINT, 
                            INITCOMMONCONTROLSEX, DWORD)
import pyforms.apis as api
import pyforms.constants as con
from pyforms.events import (MouseEventArgs, KeyEventArgs, 
                            KeyPressEventArgs, GEA)
from pyforms.colors import Color
import datetime
# from horology import Timing



def initCommonCtls(icx, cls_value):
    icx.dwICC = cls_value
    api.InitCommonControlsEx(byref(icx))
    return 1

class InitComCtls:
    """
    Most of the Windows controls uses CommCtrl32 dll for functioning.
    So we need to initiate that dll with proper class names.
    This task is needed to be done at once per class.
    So this class will handle the job for us. First, it will initiate...
    standard control classes like button, edit etc. Then we need to...
    intentionaly call the 'initCommCtls' function for special controls.
    """
    started = False
    icc_ex = INITCOMMONCONTROLSEX()

    def __init__(self) -> None:
        self.icc_ex.dwICC = con.ICC_STANDARD_CLASSES
        self.is_date_init = False
        ret = api.InitCommonControlsEx(byref(self.icc_ex))
        InitComCtls.started = True
        # print("init common ctrl res = ", ret)

    def initCommCtls(self, ctl_value):
        flag = False
        if ctl_value == 0x100: # If it's ICC_DATECLASS, we need to take special care.
            if self.is_date_init:
                flag = False
            else:
                flag = True
                self.is_date_init = True
        else:
            flag = True

        if flag:
            self.icc_ex.dwICC = ctl_value
            self.icc_ex.dwSize = sizeof(INITCOMMONCONTROLSEX)
            res = api.InitCommonControlsEx(byref(self.icc_ex))

class CommonBuffer:
    # This class is to speed up things a little bit.
    # Often, we need a unicode buffer to pass in SendMessage function.
    # This class will work as a common buffer for all that purpose.

    __slots__ = ("length", "buffer")
    def __init__(self, size = 64):
        self.length = size
        self.buffer = create_unicode_buffer(self.length)

    def fillBuffer(self, txt):
        # slen = api.MbtWc(65001, 0, txt.encode('utf-8'), len(txt), None, 0)
        slen = len(txt)
        if self.length <=slen:
            self.length = slen + 1
            self.buffer = create_unicode_buffer(self.length)
        self.buffer.value = txt

    def ensureSize(self, size):
        """Ensure that the buffer can hold 'size' characters"""
        if self.length <=size:
            self.length = size + 1
            self.buffer = create_unicode_buffer(self.length)

    def getTextFromAPI(self, hwnd):
        size = api.GetWindowTextLength(hwnd) + 1
        if self.length <=size:
            self.length = size + 1
            self.buffer = create_unicode_buffer(self.length)

        api.GetWindowText(hwnd, self.buffer, size)
        return self.buffer.value
    
    @property
    def addr(self):
        """Return the unicode buffer address"""
        return addressof(self.buffer)

    @property
    def toStr(self):
        """Return the string in the buffer"""
        return self.buffer.value
    
CLSNAME_DICT = {
    0: StaticData.className,
    1: "Button",              # BUTTON
    2: "SysMonthCal32",       # CALENDAR_BOX
    3: "Button",              # CHECK_BOX
    4: "ComboBox",            # COMBO_BOX
    5: "SysDateTimePick32",   # DATE_TIME_PICKER
    6: "Button",              # GROUP_BOX
    7: "SysHeader32",         # HEADER
    8: "Static",              # LABEL
    9: "ListBox",             # LIST_BOX
    10: "SysListView32",      # LIST_VIEW
    11: "msctls_updown32",    # NUM_PICKER
    12: "msctls_progress32",  # PROGRESS_BAR
    13: "Button",             # RADIO_BUTTON
    14: "Edit",               # TEXT_BOX
    15: "msctls_trackbar32",  # TRACK_BAR
    16: "SysTreeView32",      # TREE_VIEW
}

class Control:
    """
    Control class is the base for all other controls and even Form too.
    It supplys plenty of common features like text, background color etc.
    """
    _ctl_id = 101
    _subclass_id = 1001
    # _bufSize = 64
    _smBuffer = CommonBuffer(64)
    icc = InitComCtls()
    __slots__ = ("tvar", "name", "_hwnd", "_text", "_width", "_height", 
                 "_style", "_exStyle", "_hInst", "_visible",
                 "_clsName", "_cid", "_xpos", "_ypos", "_parent", 
                 "_isCreated", "_isTextable", "_lBtnDown",
                 "_rBtnDown", "_isMouseEntered", "_ctlType", 
                 "_font", "_fgColor", "_bgColor", "_drawFlag",
                 "_hasBrush", "_bkgBrush", "_contextMenu", "_cmenuUsed", 
                 "_keyMod", "_disable", "_onMouseEnter", "onMouseDown", 
                 "onMouseUp", "onRightMouseDown", "onRightMouseUp",
                  "onRightClick", "_onMouseLeave", "onDoubleClick", 
                  "onMouseWheel", "onMouseMove", "onMouseHover", 
                  "onKeyDown", "onKeyUp", "onKeyPress", "onPaint", 
                  "onGotFocus", "onLostFocus", "onClick", "_tabOrderHwnd")

    def __init__(self, parent, ctyp, w=0, h=0) -> None:        
        self.name = ""
        self._hwnd = 0
        self._text = ""
        self._width = w
        self._height = h        
        if ctyp != ControlType.NONE:
            self._style = con.WS_CHILD | con.WS_VISIBLE | con.WS_TABSTOP
            self._font = Font(parent._font)
        else:            
            self._font = Font(StaticData.defFont)

        self._exStyle = 0
        self._hInst = 0
        self._visible = True
        self._clsName = CLSNAME_DICT[ctyp]
        self._xpos = 0
        self._ypos = 0
        self._parent = parent
        self._isCreated = False
        self._cmenuUsed = False
        self._isTextable = False
        self._isMouseEntered = False
        self._ctlType = ctyp
        
        self._fgColor = Color(0x000000)
        self._bgColor = Color(0xFFFFFF)
        self._bkgBrush = None
        self._drawFlag = 0
        self._hasBrush = False
        self._contextMenu = None
        self._keyMod = 0
        self._disable = False
        self._tabOrderHwnd = None

        # Events
        self.onMouseEnter = None
        self.onMouseDown = None
        self.onMouseUp = None
        self.onClick = None
        self.onRightMouseDown = None
        self.onRightMouseUp = None
        self.onRightClick = None
        self.onMouseLeave = None
        self.onDoubleClick = None
        self.onMouseWheel = None
        self.onMouseMove = None
        self.onMouseHover = None
        self.onKeyDown = None
        self.onKeyUp = None
        self.onKeyPress = None
        self.onPaint = None
        self.onGotFocus = None
        self.onLostFocus = None


    def __del__(self):
        if self._font._ownership == FontOwner.OWNER:
            api.DeleteObject(self._font._handle)
            # print("Font handle deleted")
        if self._bkgBrush:
            api.DeleteObject(self._bkgBrush)

        if self._contextMenu:
            self._contextMenu.finalize()

    # -region Public funcs

    def delete(self):
        """Delete this control"""
        api.DestroyWindow(self._hwnd)


    def setSize(self, width : int, height : int):
        """Set the size of this control. Give the width & height."""
        self._width = width
        self._height = height
        if self._isCreated:
            api.SetWindowPos(self._hwnd, None, self._xpos, self._ypos, self._width, self._height, con.SWP_NOZORDER)
    #----------------------------------------------

    def setPosition(self, xpos : int, ypos : int):
        """Set the position of this control. Give the X & Y points."""
        self._xpos = xpos
        self._ypos = ypos
        if self._isCreated:
            api.SetWindowPos(self._hwnd, None, self._xpos, self._ypos, self._width, self._height, con.SWP_NOZORDER)

    def setPosInternal(self, flag = con.SWP_NOZORDER):
        api.SetWindowPos(self._hwnd, None, self._xpos, self._ypos, 
                         self._width, self._height, flag)

    def updateFontInternal(self):
        if self._font._handle != None:
            if self._font._ownership == FontOwner.OWNER:
                api.DeleteObject(self._font._handle)
            else:
                self._font._handle = None

        self._font.createHandle()
        api.SendMessage(self._hwnd, con.WM_SETFONT, self._font._handle, True)
    #------------------------------------------------------------------------------
        

    def focus(self):
        if self._isCreated: api.SetFocus(self._hwnd)

    def setFont(self, fname, fsize, fweight=FontWeight.NORMAL, bItalics=False, bUnderLine=False):
        fnt = Font(fname, fsize, fweight, bItalics, bUnderLine)
        fnt.createHandle()
        self._font = fnt
        if self._isCreated:
            self._sendMsg(con.WM_SETFONT, self._font._handle, 1)
            self._setAutoSize(True)

    # -endregion


    # -region Private funcs

    # Internal function for create controls
    def _createControl(self):
        """This function will create control handles with 'CreateWindowEx' function.
        And it will set the '_isCreated' property to True.
        We can use this single function to create all of our controls.
        """
        if self._disable: self._style |= con.WS_DISABLED
        self._setCtlID()
        self._hwnd = api.CreateWindowEx( DWORD(self._exStyle),
                                            self._clsName,
                                            self._text,
                                           DWORD(self._style),
                                            self._xpos,
                                            self._ypos,
                                            self._width,
                                            self._height,
                                            self._parent._hwnd,
                                            self._cid,
                                            self._parent.wnd_class.hInstance, None )

        if self._hwnd:
            self._isCreated = True
            self.font._pHwnd = self._hwnd
            # print(f"Created {self.name} with handle {self._hwnd}")
    #-----------------------------------------------------------------------------------END

    # Internal function to set the control IDs
    def _sendMsg(self, m, w, l ):
        return api.SendMessage(self._hwnd, m, w, l)


    def rpos(self, add = 10):
        return self._xpos + self._width + add

    def bpos(self, add = 10):
        return self._ypos + self._height + add
        

    def _setCtlID(self):
        """Before creating control, we need to set the control ID."""
        self._cid = Control._ctl_id
        Control._ctl_id += 1


    # Creating font handle if needed and apply it in the control.
    def _setFontInternal(self):
        # print(f"self.font.handle {self._font._handle}")
        if self._font._handle == 0:
            self._font.createHandle()

        api.SendMessage(self._hwnd, con.WM_SETFONT, self._font._handle, True)


    # Setting subclass for this control.
    def _setSubclass(self, subClsFunc):
        """Replacing the 'WndProc' function for this control."""
        api.SetWindowSubclass(self._hwnd, subClsFunc, Control._subclass_id, 0)
        Control._subclass_id += 1

    # Internal function to get the text from control
    def _getCtrlText(self):
        """Return the text from this control."""

        # with Timing("get text time : "):
        tLen = api.GetWindowTextLength(self._hwnd) + 1
        buffer = create_unicode_buffer(tLen)
        api.GetWindowText(self._hwnd, buffer, tLen)
        return buffer.value

    # Internal function to set the text for this control
    def _setCtrlText(self, value: str):
        """Set the text for this control."""
        api.SetWindowText(self._hwnd, value)
        if self._ctlType == ControlType.LABEL:
            if self._autoSize: self._setAutoSize(True)


    # Internal function for get the text in given hwnd
    def _getCtrlTextEx(self, hwnd):
        """Returns the control text with given hwnd.
        Used in combination controls like ComboBox, NumberPicker etc."""
        tLen = api.GetWindowTextLength(hwnd) + 1
        buffer = create_unicode_buffer(tLen)
        api.GetWindowText(hwnd, buffer, tLen)
        return buffer.value

    # Internal function to invalidate controls if needed
    def _manageRedraw(self, flag = False):
        """If this control is created, send a command to redraw it"""
        if self._isCreated: api.InvalidateRect(self._hwnd, None, flag)


    # Internal function to convert date time class to systime.
    def _makeSysTime(self, tm: datetime) -> api.SYSTEMTIME:
        """Create a SYSTEMTIME struct from given datetime object"""
        st = api.SYSTEMTIME()
        st.wYear = tm.year
        st.wMonth = tm.month
        st.wDayOfWeek = tm.weekday()
        st.wDay = tm.day
        st.wHour = tm.hour
        st.wMinute = tm.minute
        st.wSecond = tm.second
        st.wMilliseconds = tm.microsecond // 1000
        return st


    # Internal function to convert systime to date time class
    def _makeDateTime(self, st: api.SYSTEMTIME):
        """Create a datetime object from given SYSTEMTIME object"""
        return datetime.datetime(st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond, st.wMilliseconds)


    # Internal function to log the message in wndproc function in readable manner
    def log(self, msg: UINT, arg = None):
        """Print the given message with a counter variable."""
        if arg != None:
            print(f"Log from {self.name} [{self.tvar}] {msg}, {arg}")
        else:
            print(f"Log from {self.name} [{self.tvar}] {msg}")
        self.tvar += 1

    # -endregion

    # -region Props

    @property
    def handle(self):
        """Returns the hwnd of this control"""
        return self._hwnd
    #------------------------------------------------------HANDLE

    @property
    def contextMenu(self):
        """Get the context menu of this Control """
        return self._contextMenu

    @contextMenu.setter
    def contextMenu(self, value):
        """Set the context menu for this Control"""
        self._contextMenu = value
        self._contextMenu._font = self._font
        self._contextMenu._formHwnd = self._hwnd
        self._cmenuUsed = True



    @property
    def parent(self):
        """Returns the parent Form of this control"""
        return self._parent
    #------------------------------------------------------PARENT

    @property
    def tabNextItem(self): return self._tabOrderHwnd

    @tabNextItem.setter
    def tabNextItem(self, value):
        self._tabOrderHwnd = value.handle

    @property
    def font(self):
        """Get the control's font"""
        return self._font

    @font.setter
    def font(self, value : Font):
        """Set the font for this control
            Args :
                value : Font object
        """
        self._font = value
        if self._isCreated:
            if self._font._handle == 0:
                self._font.createHandle()
            self._sendMsg(con.WM_SETFONT, self._font._handle, 1)
    #-------------------------------------------------FONT

    @property
    def text(self):
        """Get the control's text"""
        return self._text

    @text.setter
    def text(self, value:str):
        """Set the control's text"""
        self._text = value
        if self._isCreated and self._isTextable: self._setCtrlText(value)
    #----------------------------------------------------------------TEXT


    @property
    def xpos(self):
        """Get the control's x position"""
        return self._xpos

    @xpos.setter
    def xpos(self, value : int):
        """Set the control's x position"""
        self._xpos = value
        if self._isCreated:
            api.SetWindowPos(self._hwnd, None, self._xpos, self._ypos, 
                            self._width, self._height, con.SWP_NOZORDER)
    #--------------------------------------------XPOS

    @property
    def ypos(self):
        """Get the control's Y position"""
        return self._ypos

    @ypos.setter
    def ypos(self, value : int):
        """Set the control's Y position"""
        self._ypos = value
        if self._isCreated:
            api.SetWindowPos(self._hwnd, None, self._xpos, self._ypos, 
                            self._width, self._height, con.SWP_NOZORDER)

    #--------------------------------------------YPOS

    @property
    def width(self):
        """Get the control's width"""
        return self._width

    @width.setter
    def width(self, value : int):
        """Set the control's width"""
        self._width = value
        if self._isCreated:
            pass
    #--------------------------------------------WIDTH

    @property
    def height(self):
        """Get the control's height"""
        return self._height

    @height.setter
    def height(self, value : int):
        """Set the control's height"""
        self._height = value
        if self._isCreated:
            api.SetWindowPos(self._hwnd, None, self._xpos, self._ypos, self._width, self._height, con.SWP_NOMOVE)
    #--------------------------------------------HEIGHT

    @property
    def visible(self):
        """Get the control's visibility"""
        return self._visible

    @visible.setter
    def visible(self, value : bool):
        """Set the control's visibility"""
        self._visible = value
        if self._isCreated:
            uFlag = con.SW_SHOW if value else con.SW_HIDE
            x = api.ShowWindow(self._hwnd, uFlag)
            print(f"visible result {x}, {uFlag = }")
    #--------------------------------------------VISIBLE

    @property
    def backColor(self):
        """Get the control's back color"""
        return self._bgColor

    @backColor.setter
    def backColor(self, value):
        """Set the control's back color"""
        if isinstance(value, int):
            self._bgColor.updateColor(value)
        elif isinstance(value, Color):
            self._bgColor = value

        if self._bkgBrush != None: 
            # api.DeleteObject(self._bkgBrush)
            self._bkgBrush = api.CreateSolidBrush(self._bgColor.ref)

        if self._drawFlag & 2 != 2: self._drawFlag += 2 # _drawFlag --> 0=no_color, 1=fore_color, 2=back_color
        if self._isCreated and self._hasBrush:
        #     if self._bkgBrush != None: 
        #         api.DeleteObject(self._bkgBrush) 
            self._bkgBrush = self._bgColor.createHBrush()
        self._manageRedraw()
    #--------------------------------------------BACKCOLOR

    @property
    def foreColor(self):
        """Get the control's text color"""
        return self._fgColor.value

    @foreColor.setter
    def foreColor(self, value : int):
        """Set the control's text color"""
        if isinstance(value, int):
            self._fgColor.updateColor(value)
        elif isinstance(value, Color):
            self._fgColor = value
        if not self._drawFlag & 1: self._drawFlag += 1 # _drawFlag --> 0=no_color, 1=fore_color, 2=back_color
        self._manageRedraw()
    #--------------------------------------------[9]---------

    @property
    def onMouseEnter(self):
        return self._onMouseEnter

    @onMouseEnter.setter
    def onMouseEnter(self, value): self._onMouseEnter = value
    #--------------------------------------------[10]---------

    @property
    def onMouseLeave(self): return self._onMouseLeave

    @onMouseLeave.setter
    def onMouseLeave(self, value): self._onMouseLeave = value
    #--------------------------------------------[11]---------

    @property
    def right(self):
        """Get the right point of control's rect"""
        return self._getMappedPoints(True)

    @property
    def bottom(self):
        """Get the bottom point of control's rect"""
        return self._getMappedPoints(False)

    @property
    def disable(self):
        """Get the disble state of this Control """
        return self._disable

    @disable.setter
    def disable(self, value):
        """Set this control disable or enable"""
        self._disable = value
        if self._isCreated: api.EnableWindow(self._hwnd, not value)



    # -endregion


    # -region Private members
    def _getMappedPoints(self, isRight):
        if self._isCreated:
            rc = api.get_client_rect(self._hwnd)
            hwnd1 = self._hwnd
        else:
            rc = api.RECT(self._xpos, self._ypos, self._xpos + self._width, self._ypos + self._height)
            hwnd1 = self._parent._hwnd
        MapWindowPoints(hwnd1, self._parent._hwnd, cast(byref(rc), LPPOINT), 2)
        return rc.right if isRight else rc.bottom
    # -endregion



    # -region Event handlers
    def _leftMouseDownHandler(self, msg, wpm, lpm):
        if self.onMouseDown:
            self.onMouseDown(self, MouseEventArgs(msg, wpm, lpm))
            return 0


    def _leftMouseUpHandler(self, msg, wpm, lpm):
        if self.onMouseUp: self.onMouseUp(self, MouseEventArgs(msg, wpm, lpm))
        if self.onClick: self.onClick(self, GEA)


    def _rightMouseDownHandler(self, msg, wpm, lpm):
        if self.onRightMouseDown: self.onRightMouseDown(self, MouseEventArgs(msg, wpm, lpm))
        return 0


    def _rightMouseUpHandler(self, msg, wpm, lpm):
        if self.onRightMouseUp: self.onRightMouseUp(self, MouseEventArgs(msg, wpm, lpm))
        if self.onRightClick: self.onRightClick(self, GEA)



    def _mouseWheenHandler(self, msg, wpm, lpm):
        if self.onMouseWheel: self.onMouseWheel(self, MouseEventArgs(msg, wpm, lpm))



    def _mouseMoveHandler(self, msg, wpm, lpm):
        if self._isMouseEntered:
            if self.onMouseMove: self.onMouseMove(self, MouseEventArgs(msg, wpm, lpm))
        if not self._isMouseEntered:
            self._isMouseEntered = True
            if self._onMouseEnter: self._onMouseEnter(self, GEA)



    def _mouseLeaveHandler(self):
        self._isMouseEntered = False
        if self._onMouseLeave: self._onMouseLeave(self, GEA)



    def _keyDownHandler(self, wpm):
        if self.onKeyDown: self.onKeyDown(self, KeyEventArgs(self, True, wpm))
        return 0

    def _keyUpHandler(self, wpm):
        if self.onKeyUp: self.onKeyUp(self, KeyEventArgs(self, False, wpm))
        return 0

    def _keyPressHandler(self, wp):
        if self.onKeyPress: self.onKeyPress(self, KeyPressEventArgs(wp))
        return 0

    def _gotFocusHandler(self):
        if self.onGotFocus: self.onGotFocus(self, GEA)
        return 0


    def _lostFocusHandler(self):
        if self.onLostFocus: self.onLostFocus(self, GEA)
        return 0

    def _wmContextMenuHandler(self, lpm):
        if self._contextMenu:
            self._contextMenu.showMenu(lpm)

    # Use this as a decorator for connection functions to event handlers
    def connect(self, event_name):
        def wrapper(func):
            if hasattr(self, event_name):
                setattr(self, event_name, func)
            else:
                raise AttributeError(f"No event '{event_name}' in {type(self).__name__}")
            return func
        return wrapper

    # -endregion Event handlers



# A handy connection function for connecting functions to events.
def connect(obj: Control, event: str):
    def wrapper(func):
        setattr(obj, event, func)

    return wrapper
