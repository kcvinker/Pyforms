# Common module - Created on
from ctypes import c_int, cast, windll, byref, sizeof, py_object
from pyforms.src.enums import FontWeight, FontOwner
import pyforms.src.apis as api
from pyforms.src.colors import Color
from pyforms.src.apis import RECT, LOGFONT, POINT
import pyforms.src.constants as con
from enum import Enum, IntEnum
# from pyforms.src.forms import globalScaleFactor, globalSysDPI
import datetime
# from collections import defaultdict

INT_MIN   =  -2147483647 - 1
INT_MAX  =     2147483647
TRANSPARENT = 0x00000001
OPAQUE = 0x00000002
menuTxtFlag = con.DT_LEFT | con.DT_SINGLELINE | con.DT_VCENTER

globalScaleFactor = 1.25
globalSysDPI = 96

def createDefFont():
    fnsz = int(globalScaleFactor * 11.0)
    iHeight = -api.MulDiv(fnsz, globalSysDPI, 72)
    lf = LOGFONT()
    lf.lfFaceName = "Tahoma"
    lf.lfHeight = iHeight
    lf.lfWidth = 0
    lf.lfWeight = 400
    lf.lfItalic = 0
    lf.lfUnderline = 0
    lf.lfCharSet = con.DEFAULT_CHARSET
    lf.lfOutPrecision = con.OUT_STRING_PRECIS
    lf.lfClipPrecision = con.CLIP_DEFAULT_PRECIS
    lf.lfQuality = con.PROOF_QUALITY
    lf.lfPitchAndFamily = 1
    return api.CreateFontIndirect(byref(lf))


class StaticData: # A singleton object which used to hold essential data for a form to start
    hInstance = 0
    className = "PyForms_Window"
    loopStarted = False
    screenWidth = api.GetSystemMetrics(0) # Need to calculate the form position
    screenHeight = api.GetSystemMetrics(1)
    defWinColor = Color(0xf0f0f0)# Color.from_RGB(230, 230, 230)
    defBackBrush = api.CreateSolidBrush(0x00F0F0F0)
    defHfont = createDefFont()
    currForm = None
    trayHandles = [] # A list to hold any TrayIcon hidden window handles.
    grayBrush = api.CreateSolidBrush(0x00DAD4CE)

    @staticmethod
    def registerMsgWinClass(clsname, wndproc):
        wc = api.WNDCLASSEX()
        wc.cbSize = sizeof(api.WNDCLASSEX)
        wc.lpfnWndProc = wndproc
        wc.hInstance = StaticData.hInstance
        wc.lpszClassName = clsname
        api.RegisterClassEx(byref(wc))

    
      

    @staticmethod
    def finalize():
        if len(StaticData.trayHandles):
            for hw in StaticData.trayHandles:
                if hw != None: 
                    api.DestroyWindow(hw)
                    # print("destroy tray icon")
        api.DeleteObject(StaticData.defHfont)
        api.DeleteObject(StaticData.grayBrush)
        api.DeleteObject(StaticData.defBackBrush)
        print("Pyforms closed...")


def getSystemDPI():
    global globalScaleFactor
    global globalSysDPI
    hdc = api.GetDC(None)
    globalSysDPI = api.GetDeviceCaps(hdc, con.LOGPIXELSY)
    api.ReleaseDC(None, hdc)
    scaleF = api.GetScaleFactorForDevice(0)
    globalScaleFactor = scaleF / 100.0

def getMousePosOnMsg():
    dw_value = windll.user32.GetMessagePos()
    x = api.LOWORD(dw_value)
    y = api.HIWORD(dw_value)
    return POINT(x, y)

def pointInRect(rct, pt): return api.PtInRect(byref(rct), pt)

    

class Font:
    # userDict = defaultdict(list)
    __slots__ = ("_name", "_size", "_weight", "_italics", 
                 "_underLine", "_handle", "_ownership")

    def __init__(   self, nameOrHandle,
                    size: int = 11,
                    weight: FontWeight = FontWeight.NORMAL,
                    italics: bool = False,
                    underLine: bool = False) -> None:
        self._size = size
        self._weight = weight
        self._italics = italics
        self._underLine = underLine
        if isinstance(nameOrHandle, str):
            self._name = nameOrHandle
            self._handle = 0
            self._ownership = FontOwner.NONE
        else:
            self._name = "Tahoma"
            self._handle = nameOrHandle
            self._ownership = FontOwner.USER


    def createHandle(self):   
        if self._handle > 0 and self._ownership == FontOwner.OWNER:
            api.DeleteObject(self._handle)

        fnsz = int(globalScaleFactor * float(self._size))
        iHeight = -api.MulDiv(fnsz, globalSysDPI, 72)

        lf = LOGFONT()
        lf.lfFaceName = self._name
        lf.lfHeight = iHeight
        lf.lfWeight = self._weight
        lf.lfItalic = self._italics
        lf.lfUnderline = self._underLine
        lf.lfCharSet = con.DEFAULT_CHARSET
        lf.lfOutPrecision = con.OUT_STRING_PRECIS
        lf.lfClipPrecision = con.CLIP_DEFAULT_PRECIS
        lf.lfQuality = con.PROOF_QUALITY
        lf.lfPitchAndFamily = 1
        self._handle = api.CreateFontIndirect(byref(lf))
        self._ownership = FontOwner.OWNER


    def colneFrom(self, srcFont):   
        self._name = srcFont._name
        self._size = srcFont._size
        self._weight = srcFont._weight
        self._italics = srcFont._italics
        self._underLine = srcFont._underLine
        if srcFont._handle:
            lf = LOGFONT()
            x = api.GetObject(srcFont._handle, sizeof(LOGFONT), byref(lf))
            if x :
                self._handle = api.CreateFontIndirect(byref(lf))
                self._ownership = FontOwner.OWNER
            else:
                print("Font handle error, line 77, commons.py")

    
    


    @property
    def name(self): return self._name

    @name.setter
    def name(self, value: str): self._name = value
    #---------------------------------------------------

    @property
    def size(self): return self._size

    @size.setter
    def size(self, value: int): self._size = value
    #-----------------------------------------------------

    @property
    def weight(self): return self._weight

    @weight.setter
    def weight(self, value: FontWeight): self._weight = value
    #------------------------------------------------------

    @property
    def italics(self): return self._italics

    @italics.setter
    def italics(self, value: bool): self._italics = value
    #-----------------------------------------------------

    @property
    def underLine(self): return self._underLine

    @underLine.setter
    def underLine(self, value: bool): self._underLine = value
    #-----------------------------------------------------

    @property
    def handle(self): return self._handle

    @handle.setter
    def handle(self, value: bool): self._handle = value
#-----------------End of Font Class----------------------------


class Timing:
    def __init__(self, msg: str) -> None:
        self.message = msg

    def __enter__(self):
        self.start = datetime.datetime.now()

    def __exit__(self, etp, evalue, etb):
        self.finish = datetime.datetime.now()
        self.dur = self.finish - self.start
        if self.dur.microseconds > 999:
            print(f"{self.message} : {self.dur.microseconds // 1000}.{self.dur.microseconds % 1000} ms")
        else:
            print(f"{self.message} : {self.dur.microseconds} us")


class Area:
    __slots__ = ("width", "height")
    def __init__(self, w, h) -> None:
        self.width = w
        self.height = h

rpc = 1
def print_rect(rc):
    global rpc
    print(f"[{rpc}] Left:{rc.left}, Top:{rc.top}, Right:{rc.right}, Bottom:{rc.bottom}")
    rpc += 1

msgCounter = 1
def printWinMsg(ms):
    global msgCounter
    print(f"[{msgCounter}] Message - {ms}")
    msgCounter += 1

y = 1
def log_cnt(msg):
	global y
	print(f"[{y}] {msg}")
	y += 1


WM_APP = 0x8000

class MyMessages(IntEnum):
    MOUSE_CLICK       = WM_APP + 1
    RIGHT_CLICK       = WM_APP + 2
    CTRL_NOTIFY       = WM_APP + 3
    CTRL_COLOR        = WM_APP + 4
    EDIT_COLOR        = WM_APP + 5
    LABEL_COLOR       = WM_APP + 6
    COMBO_LB_COLOR    = WM_APP + 7
    COMBO_TB_COLOR    = WM_APP + 8
    LIST_COLOR        = WM_APP + 9
    CTL_COMMAND       = WM_APP + 10
    HORI_SCROLL       = WM_APP + 11
    VERT_SCROLL       = WM_APP + 12
    TREENODE_NOTIFY   = WM_APP + 13
    BUDDY_RESET       = WM_APP + 14
    MENU_ADDED        = WM_APP + 15
    NOTIFY_GPBOX      = WM_APP + 16
    MM_TRAY_MSG       = WM_APP + 17
    THREAD_MSG        = WM_APP + 18
    MM_MENUITEM_NOTIFY  = WM_APP + 19
    HFONT_NOTIFY  = WM_APP + 20






def is_first_bit_set(num):
    return num & (1 << 0)

# print("is bit set ", is_first_bit_set(2, 0))

def getWheelDelta(wpm): return api.HIWORD(wpm)
def getKeyState(wpm) : return api.LOWORD(wpm)
def getMouseXpoint(lpm) : return api.LOWORD(lpm)
def getMouseYpoint(lpm) : return api.HIWORD(lpm)
def getMousePoints(lpm): return POINT(api.LOWORD(lpm), api.HIWORD(lpm))

def getMousePos(pt, lpm):
    if lpm == 0:
        api.GetCursorPos(byref(pt))
    else:
        pt.x = api.LOWORD(lpm)
        pt.y = api.HIWORD(lpm)

def inflateRect(rct, value) -> RECT:
    left = rct.left - value
    right = rct.right + value
    top = rct.top - value
    bottom = rct.bottom + value
    rc = RECT()
    rc.left = left
    rc.top = top
    rc.right = right
    rc.bottom = bottom
    return rc

def inflateRectTuple(rct, value):
    # print(f"Old Rc {rct[0] = }, {rct[1] = }, {rct[2] = }, {rct[3] = }")
    left = rct.left - value
    right = rct.right + value
    top = rct.top - value
    bottom = rct.bottom + value
    # print(f"New Rc {left = }, {top = }, {right = }, {bottom = }")
    rc = RECT(left, top, right, bottom)
    return rc


def getHalfOfRect(rct, isUpper):
    if isUpper:
        height = rct[3] - rct[1]
        bottom = int(rct[1] + (height / 2))
        return (rct[0], rct[1], rct[2], bottom)
    else:
        height = rct[3] - rct[1]
        top = int(rct[1] + (height / 2))
        return (rct[0], top, rct[2], rct[3])


def sendThreadMsg(hwnd, wpm, lpm):
    """Send a message to the window ownd the 'hwnd' and pass the wpm & lpm to it's wndproc function.
        You can use the 'onThreadMsg' event handler to handle this message. Signature is 'func(wpm, lpm)'

        Params: hwnd - Window handle which receives the message.
                wpm - 64 bit wParam type (Pass any python object)
                lpm - 64 bit lParam type (Pass any python object)
    """
    return api.SendNotifyMessage(hwnd, MyMessages.THREAD_MSG, wpm, lpm )


def castPyObj(value):
    return cast(value, py_object).value


