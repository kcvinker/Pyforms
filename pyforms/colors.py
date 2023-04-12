# Color module - Created on 16-Nov-2022 01:37

from . apis import CreateSolidBrush, CreatePen
from . constants import PS_SOLID
from ctypes import byref
from ctypes.wintypes import HDC, COLORREF, HBRUSH
from .apis import RECT, CreateSolidBrush, FillRect, DeleteObject, DeleteDC
from .apis import CreatePatternBrush, SelectObject
from .apis import CreateCompatibleDC, CreateCompatibleBitmap

def getColorRef(clr: int) -> COLORREF:
    red = clr >> 16
    green = (clr & 0x00ff00) >> 8
    blue = clr & 0x0000ff
    return int((blue << 16) | (green << 8) | red)


class RgbColor:
    __slots__ = ("red", "green", "blue", "int_color", "ref" )
    def __init__(self, clr:int) -> None:
        self.red = clr >> 16
        self.green = (clr & 0x00ff00) >> 8
        self.blue = clr & 0x0000ff
        self.int_color = clr
        self.ref = int((self.blue << 16) | (self.green << 8) | self.red)

    def get_new_shade(self, change_value):
        r = clamp(self.red + (change_value * 8))
        g = clamp(self.green + (change_value * 8))
        b = clamp(self.blue + (change_value * 8))
        iValue = int((r << 16) | (g << 8) | b)
        return RgbColor(iValue)

    def set_color(self, clr: int):
        self.red = clr >> 16
        self.green = (clr & 0x00ff00) >> 8
        self.blue = clr & 0x0000ff
        self.int_color = clr
        self.ref = int((self.blue << 16) | (self.green << 8) | self.red)

    def bottom_color(self, adj: int):
        # Buttons and headers are drawing with two colors.
        # top side with lighter color and botton side with darker color.
        # This makes a 3D effect. So this function will make the bottom
        # color for a given color.
        rc = RgbColor(0)
        rc.red = self.red - adj
        rc.green = self.green - adj
        rc.blue = self.blue - adj
        return rc

    def change_shade_ref(self, adj: float):
        r = clamp(self.red * adj)
        g = clamp(self.green * adj)
        b = clamp(self.blue * adj)
        return int((b << 16) | (g << 8) | r)

    def change_shade_rgb(self, adj: float):
        r = RgbColor(0)
        r.red = clamp(self.red * adj)
        r.green = clamp(self.green * adj)
        r.blue = clamp(self.blue * adj)
        r.ref = int((r.blue << 16) | (r.green << 8) | r.red)
        return r

    def is_dark(self):
        x = ((self.red * 0.2126) + (self.green * 0.7152) + (self.blue * 0.0722))
        return x < 40

    def toStr(self) -> str:
        return f"Red : {self.red}, Green : {self.green}, Blue : {self.blue}"


class Color:
    __slots__ = ("value", "ref", "updated", "red", "green", "blue")
    def __init__(self, clr=0) -> None:
        if isinstance(clr, int):
            self.value = clr
            self.red = clr >> 16
            self.green = (clr & 0x00ff00) >> 8
            self.blue = clr & 0x0000ff
            self.ref = 0 if clr == 0 else int((self.blue << 16) | (self.green << 8) | self.red)
            self.updated = False
        else:
            self.value = clr.value
            self.red = clr.red
            self.green = clr.green
            self.blue = clr.blue
            self.ref = clr.ref
            self.updated = False


    def __str__(self) -> str:
        return f"Value: {self.value:X}, Ref: {self.ref:X}, Red: {self.red}, Green: {self.green}, Blue: {self.blue}"

    def __ne__(self, __o: object) -> bool:
        return self.value != __o.value


    def updateColor(self, clr: int):
        self.value = clr
        self.red = clr >> 16
        self.green = (clr & 0x00ff00) >> 8
        self.blue = clr & 0x0000ff
        self.ref = int((self.blue << 16) | (self.green << 8) | self.red)
        self.updated = True

    def getShadedColor(self, adj: float):
        r1 = clamp(self.red * adj)
        g1 = clamp(self.green * adj)
        b1 = clamp(self.blue * adj)
        return Color.fromRGB(r1, g1, b1)


    def createHBrush(self, adj: float = 0) -> HBRUSH:
        if adj == 0:
            return CreateSolidBrush(self.ref)
        else:
            r1 = clamp(self.red * adj)
            g1 = clamp(self.green * adj)
            b1 = clamp(self.blue * adj)
            cref = int((b1 << 16) | (g1 << 8) | r1)
            return CreateSolidBrush(cref)

    def createHPen(self, adj: float = 0):
        if adj > 0:
            r1 = clamp(self.red * adj)
            g1 = clamp(self.green * adj)
            b1 = clamp(self.blue * adj)
            cref = int((b1 << 16) | (g1 << 8) | r1)
            return CreatePen(PS_SOLID, 1, cref)
        else:
            return CreatePen(PS_SOLID, 1, self.ref)

    def changeToColorRef(self, adj: float):
        r1 = clamp(self.red * adj)
        g1 = clamp(self.green * adj)
        b1 = clamp(self.blue * adj)
        return int((b1 << 16) | (g1 << 8) | r1)




    def isDark(self):
        x = ((self.red * 0.2126) + (self.green * 0.7152) + (self.blue * 0.0722))
        return x < 40


    @classmethod
    def fromColor(cls, clr: int, change_value: int):
        rc = RgbColor(clr)
        red = clamp(rc.red + (change_value * 8))
        green = clamp(rc.green + (change_value * 16))
        blue = clamp(rc.blue + (change_value * 32))
        ivalue = int((red << 16) | (green << 8) | blue)
        return cls(ivalue)

    @classmethod
    def fromRGB(cls, red, green, blue):
        ivalue = int((red << 16) | (green << 8) | blue)
        return cls(ivalue)


    def makeRGB(self):
        rc = RgbColor(self.value)
        return rc;



COLOR_BLACK = Color(0x000000)
COLOR_WHITE = Color(0XFFFFFF)



class ButtonGradientColors:

    """set all the colors for a button to draw in gradient mode"""

    __slots__ = ("def_color1", "def_color2", "focus_color1", "focus_color2", "click_color1", "click_color2", "frame_color", "top_to_bottom")

    def __init__(   self, bk_clr1: int, bk_clr2: int, focus_value: int,
                    click_value: int, frame_value: int, t2b = True) -> None:

        self.def_color1 = RgbColor(bk_clr1)
        self.def_color2 = RgbColor(bk_clr2)
        self.focus_color1 = RgbColor.get_new_shade(self.def_color1, focus_value)
        self.focus_color2 = RgbColor.get_new_shade(self.def_color2, focus_value)
        self.click_color1 = RgbColor.get_new_shade(self.def_color1, click_value)
        self.click_color2 = RgbColor.get_new_shade(self.def_color2, click_value)
        self.frame_color = Color.from_color(bk_clr2, frame_value)
        self.top_to_bottom = t2b



def change_color(clr: int, change_value: float) -> COLORREF:
    rc = RgbColor(clr)
    red = clamp(rc.red + (change_value * 8))
    green = clamp(rc.green + (change_value * 16))
    blue = clamp(rc.blue + (change_value * 32))
    return ref_from_RGB(red, green, blue)


def clamp(n, minVal = 0, maxVal = 255): return int(max(min(maxVal, n), minVal))


def ref_from_RGB(r, g, b) -> COLORREF: return int((b << 16) | (g << 8) | r)


def _createGradientBrush(dc: HDC, rct: RECT, rc1, rc2, isT2B: bool):
    # tBrush = wt.HBRUSH()
    memHdc = CreateCompatibleDC(dc)
    hBmp = CreateCompatibleBitmap(dc, rct.right, rct.bottom)
    loopEnd = rct.bottom if isT2B else rct.right
    x = rc2.red - rc1.red
    y = rc2.green - rc1.green
    z = rc2.blue - rc1.blue
    SelectObject(memHdc, hBmp)
    for i in range(loopEnd):
        r, g, b = 0, 0, 0
        r = rc1.red + int((i * x) / loopEnd)
        g = rc1.green + int((i * y) / loopEnd)
        b = rc1.blue + int((i * z) / loopEnd)
        tBrush = CreateSolidBrush((b << 16) | (g << 8) | r)
        rc = RECT()
        rc.left = 0 if isT2B else i
        rc.top = i if isT2B else 0
        rc.right = rct.right if isT2B else i + 1
        rc.bottom = i + 1 if isT2B else loopEnd
        FillRect(memHdc, byref(rc), tBrush)
        DeleteObject(tBrush)

    gBrush = CreatePatternBrush(hBmp)
    DeleteDC(memHdc)
    DeleteObject(hBmp)
    return gBrush

