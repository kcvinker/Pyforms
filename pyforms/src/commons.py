# Common module - Created on
from ctypes import c_int, cast, windll, byref, sizeof, py_object
from pyforms.src.enums import FontWeight
import pyforms.src.apis as api
from pyforms.src.apis import RECT, LOGFONT, POINT
import pyforms.src.constants as con
from enum import Enum
import datetime

INT_MIN   =  -2147483647 - 1
INT_MAX  =     2147483647
TRANSPARENT = 0x00000001
OPAQUE = 0x00000002
menuTxtFlag = con.DT_LEFT | con.DT_SINGLELINE | con.DT_VCENTER

def getMousePosOnMsg():
    dw_value = windll.user32.GetMessagePos()
    x = api.LOWORD(dw_value)
    y = api.HIWORD(dw_value)
    return POINT(x, y)

def pointInRect(rct, pt): return api.PtInRect(byref(rct), pt)


class Font:
    __slots__ = ("_name", "_size", "_weight", "_italics", "_underLine", "_hwnd")

    def __init__(   self, name: str = "Tahoma",
                    size: int = 11,
                    weight: FontWeight = FontWeight.NORMAL,
                    italics: bool = False,
                    underLine: bool = False) -> None:
        self._name = name
        self._size = size
        self._weight = weight
        self._italics = italics
        self._underLine = underLine
        self._hwnd = 0

    def createHandle(self, hwnd):
        dcHwnd = api.GetDC(hwnd)
        iHeight = -api.MulDiv(self._size, api.GetDeviceCaps(dcHwnd, con.LOGPIXELSY), 72)
        api.ReleaseDC(hwnd, dcHwnd)

        lf = LOGFONT()
        lf.lfFaceName = self._name
        lf.lfHeight = iHeight
        lf.lfWeight = self._weight.value
        lf.lfCharSet = con.DEFAULT_CHARSET
        lf.lfOutPrecision = con.OUT_STRING_PRECIS
        lf.lfClipPrecision = con.CLIP_DEFAULT_PRECIS
        lf.lfQuality = con.PROOF_QUALITY
        lf.lfPitchAndFamily = 1
        self._hwnd = api.CreateFontIndirect(byref(lf))


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
    def handle(self): return self._hwnd

    @handle.setter
    def handle(self, value: bool): self._hwnd = value
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


msgCounter = 1
def printWinMsg(ms):
    global msgCounter
    print(f"[{msgCounter}] Message - {ms}")
    msgCounter += 1


class MyMessages:
    MOUSE_CLICK = 9000
    RIGHT_CLICK = 9001
    CTRL_NOTIFY = 9002
    CTRL_COLOR = 9003
    EDIT_COLOR = 9004
    LABEL_COLOR = 9005
    COMBO_LB_COLOR = 9006
    COMBO_TB_COLOR = 9007
    LIST_COLOR = 9008
    CTL_COMMAND = 9009
    HORI_SCROLL = 9010
    VERT_SCROLL = 9011
    TREENODE_NOTIFY = 9012 # A tree node notify it's tree view control about changes
    BUDDY_RESET = 9013
    MENU_ADDED = 9014
    THREAD_MSG = con.WM_USER + 5





def is_first_bit_set(num):
    return num & (1 << 0)

# print("is bit set ", is_first_bit_set(2, 0))

def getWheelDelta(wpm): return api.HIWORD(wpm)
def getKeyState(wpm) : return api.LOWORD(wpm)
def getMouseXpoint(lpm) : return api.LOWORD(lpm)
def getMouseYpoint(lpm) : return api.HIWORD(lpm)
def getMousePoints(lpm): return POINT(api.LOWORD(lpm), api.HIWORD(lpm))

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


