import ctypes as ctp
import ctypes.wintypes as wtp

au3x = ctp.CDLL(r"C:\Program Files (x86)\AutoIt3\AutoItX\AutoItX3_x64.dll")

def setOption(optTxt: str, value: int):
    """Set autoit's various options. Check 'opt' in autoit help file for options.

        Params:
            1: optTxt(str) = Name of the option.
            2: value(int) = Value for the option.
        Returns:
            An int value
        Example:
        >>> setOption("WinTitleMatchMode", 2)
    """
    au3_setOption = au3x.AU3_AutoItSetOption
    au3_setOption.restype = ctp.c_int
    au3_setOption.argtypes = [wtp.LPCWSTR, ctp.c_int]
    return au3_setOption(ctp.create_unicode_buffer(optTxt), value)

def clipGet(buffSize = 4096 ):
    """Get clipboard content as text.

        Params:
            1: buffSize(int) = Size of the buffer. Default is 4096
        Returns:
            The text from clipboard.(If any)
        Example:
        >>> clipGet()
    """
    au3_clipGet = au3x.AU3_ClipGet
    au3_clipGet.argtypes = [wtp.LPWSTR, ctp.c_int]
    buffer = ctp.create_unicode_buffer(buffSize)
    au3_clipGet(buffer, buffSize)
    return buffer.value

def clipPut(text ):
    """Put text in clipboard.

        Params:
            1: text(any) = The text to put the clipboard
        Returns:
            None
        Example:
        >>> clipPut("Some string")
    """
    au3_clipPut = au3x.AU3_ClipPut
    au3_clipPut.argtypes = [wtp.LPWSTR]
    buffer = ctp.create_unicode_buffer(text)
    au3_clipPut(buffer)

def winGetTitle(partialTitle: str ):
    """Get the title of a specific window.

        Params:
            1: partialTitle(any) = The partial title of the window in question
        Returns:
            Title of the window(str)
        Example:
        >>> winGetTitle("Some window")
    """
    au3_winGetTitle = au3x.AU3_WinGetTitle
    au3_winGetTitle.argtypes = [wtp.LPCWSTR, wtp.LPCWSTR, wtp.LPWSTR, ctp.c_int]
    buffer = ctp.create_unicode_buffer(1024)
    currTitle = ctp.create_unicode_buffer(partialTitle)
    au3_winGetTitle(currTitle, None, buffer, 1024)
    return buffer.value

def winGetHandle(winTitle: str ):
    """Get the handle of a specific window.

        Params:
            1: winTitle(str) = The partial title of the window in question
        Returns:
            Handle of the window(str)
        Example:
        >>> winGetHandle("Some window")
    """
    au3_winGetHandle = au3x.AU3_WinGetHandle
    au3_winGetHandle.argtypes = [wtp.LPCWSTR, wtp.LPCWSTR, wtp.LPWSTR, ctp.c_int]
    au3_winGetHandle.restype = wtp.HWND
    currTxt = ctp.create_unicode_buffer(winTitle)
    return au3_winGetHandle(currTxt, None)

def winActivate1(winTitle: str ):
    """Activate a window with given text.

        Params:
            1: winTitle(str) = The partial title of the window in question
        Returns:
            int
        Example:
        >>> winActivate1("Some window")
    """
    au3_winActivate = au3x.AU3_WinActivate
    au3_winActivate.argtypes = [wtp.LPCWSTR, wtp.LPCWSTR]
    au3_winActivate.restype = ctp.c_int
    currTxt = ctp.create_unicode_buffer(winTitle)
    return au3_winActivate(currTxt, None)

def winActivate2(winHwnd: wtp.HWND ):
    """Activate a window with given hwnd.

        Params:
            1: winHwnd(hwnd) = The partial title of the window in question
        Returns:
            int
        Example:
        >>> winActivate2(0xabcdef)
    """
    au3_winActivateBH = au3x.AU3_WinActivateByHandle
    au3_winActivateBH.argtypes = [wtp.HWND]
    au3_winActivateBH.restype = ctp.c_int
    return au3_winActivateBH(winHwnd)

def winActivate(tite_or_hwnd):
    """Activate a window with given hwnd.

        Params:
            1: tite_or_hwnd(hwnd) = The partial title or the hwnd of the window in question
        Returns:
            None
        Example:
        >>> winActivate(0xabcdef)
    """
    if isinstance(tite_or_hwnd, str):
        winActivate1(tite_or_hwnd)
    else:
        winActivate2(tite_or_hwnd)


def mouseClick(button = "left", xpos = 10, ypos = 10, clickCount = 1, clickSpeed = 10 ):
    """Simulate mouse click on given coordinates.

        Params:
            1: button(str) = Which mouse button should get clicked.
                Possible values are ("left", "right", "middle")
            2: xpos(int) = x position.
            3: ypos(int) = y position.
            4: clickCount(int) = The number of times to click the mouse. Default is 1.
            5: clickSpeed(int) = the speed to move the mouse in the range 1 (fastest) to 100 (slowest).
                                A speed of 0 will move the mouse instantly. Default speed is 10.
        Returns:
            int
        Example:
        >>> mouseClick("right", 20, 45)
    """
    au3_mouseClick = au3x.AU3_MouseClick
    au3_mouseClick.argtypes = [wtp.LPCWSTR, ctp.c_int, ctp.c_int, ctp.c_int, ctp.c_int ]
    au3_mouseClick.restype = ctp.c_int
    buffer = ctp.create_unicode_buffer(button)
    return au3_mouseClick(buffer, xpos, ypos, clickCount, clickSpeed)


def mouseMove(xpos = 10, ypos = 10, clickSpeed = 10 ):
    """Move mouse to the given coordinates.

        Params:
            1: xpos(int) = x position.
            2: ypos(int) = y position.
            3: clickSpeed(int) = the speed to move the mouse in the range 1 (fastest) to 100 (slowest).
                                A speed of 0 will move the mouse instantly. Default speed is 10.
        Returns:
            int
        Example:
        >>> mouseMove(20, 45)
    """
    au3_mouseMove = au3x.AU3_MouseMove
    au3_mouseMove.argtypes = [ctp.c_int, ctp.c_int, ctp.c_int]
    au3_mouseMove.restype = ctp.c_int
    return au3_mouseMove(xpos, ypos, clickSpeed)