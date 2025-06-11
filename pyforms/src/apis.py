
# Created on 13-Nov-2022 15:06:46
from ctypes import WINFUNCTYPE, Structure, windll, POINTER, c_void_p, c_char_p
from ctypes.wintypes import HICON, HWND, UINT, DWORD, LONG, HDC, LPCWSTR, LPWSTR, INT, HMENU, HINSTANCE, LPVOID, USHORT
from ctypes.wintypes import HMODULE, ATOM, BOOL, HBRUSH, HGDIOBJ, HBITMAP, COLORREF, HPEN, HANDLE, BYTE, WCHAR, HFONT, WORD, HRGN
import ctypes as ct
import os
# from .colors import clrReffrom_RGB

LONG_PTR = ct.c_longlong
UINT_PTR = ct.c_ulonglong
ULONG_PTR = ct.c_ulonglong

LRESULT = LONG_PTR
HCURSOR = HICON
DWORD_PTR = ULONG_PTR
WPARAM = UINT_PTR
LPARAM = LONG_PTR
PUINT = POINTER(UINT)
HTREEITEM = HANDLE

WNDPROC = WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM)
SUBCLASSPROC = WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR)
LPOFNHOOKPROC = WINFUNCTYPE(UINT_PTR, HWND, UINT, WPARAM, LPARAM)
BROWSERCBPROC = WINFUNCTYPE(INT, HWND, UINT, LPARAM, LPARAM)
TIMERPROC = WINFUNCTYPE(UINT_PTR, HWND, UINT, UINT_PTR, DWORD)

# -region Structures

class SIZE(Structure):
    _fields_ = [
        ('cx', LONG),
        ('cy', LONG)
    ]

class POINT(Structure):
    _fields_ = [
        ('x', LONG),
        ('y', LONG)
    ]

LPPOINT = POINTER(POINT)

class RECT(Structure):
    _fields_ = [
        ('left', LONG),
        ('top', LONG),
        ('right', LONG),
        ('bottom', LONG)
    ]

LPRECT = POINTER(RECT)


class WNDCLASSEX(Structure): # tagWNDCLASSEXW
    _fields_ = [("cbSize", UINT),
                ("style", UINT),
                ("lpfnWndProc", WNDPROC),
                ("cbClsExtra", INT),
                ("cbWndExtra", INT),
                ("hInstance", HANDLE),
                ("hIcon", HANDLE),
                ("hCursor", HANDLE),
                ("hbrBackground", HANDLE),
                ("lpszMenuName", LPCWSTR),
                ("lpszClassName", LPCWSTR),
                ("hIconSm", HANDLE),
            ]

class WINDOWPOS(Structure):
    _fields_ = [
        ('hwnd', HWND),
        ('hwndInsertAfter', HWND),
        ('x', INT),
        ('y', INT),
        ('cx', INT),
        ('cy', INT),
        ('flags', UINT)
    ]
LPWINDOWPOS = POINTER(WINDOWPOS)

class MSG(Structure):
    _fields_ = [
        ("hwnd", HWND),
        ("message", UINT),
        ("wParam", WPARAM),
        ("lParam", LPARAM),
        ("time", DWORD),
        ("pt", POINT),
        ("lPrivate", DWORD),

    ]

MSGPTR = POINTER(MSG)

class PAINTSTRUCT(Structure):
    _fields_ = [
        ("hdc", HDC),
        ("fErase", BOOL),
        ("rcPaint", RECT),
        ("fRestore", BOOL),
        ("fIncUpdate", BOOL),
        ("rgbReserved", BYTE * 32),
    ]


class INITCOMMONCONTROLSEX(Structure):
    _fields_ = [
        ('dwSize', DWORD),
        ('dwICC', DWORD)
    ]

LPINITCOMMONCONTROLSEX = POINTER(INITCOMMONCONTROLSEX)


class NMHDR(Structure):
    _fields_ = [
        ('hwndFrom', HWND),
        ('idFrom', UINT_PTR),
        ('code', UINT)
    ]
LPNMHDR = POINTER(NMHDR)

class NMCUSTOMDRAW(Structure):
    _fields_ = [
        ('hdr', NMHDR),
        ('dwDrawStage', DWORD),
        ('hdc', HDC),
        ('rc', RECT),
        ('dwItemSpec', DWORD_PTR),
        ('uItemState', UINT),
        ('lItemParam', LPARAM)
    ]
LPNMCUSTOMDRAW = POINTER(NMCUSTOMDRAW)

class TRACKMOUSEEVENT(Structure):
     _fields_ = [
        ('cbSize', DWORD),
        ('dwFlags', DWORD),
        ('hwndTrack', HWND),
        ('dwHoverTime', DWORD)
    ]

class LOGFONT(Structure):
    _fields_ = [("lfHeight", LONG),
                ("lfWidth", LONG),
                ("lfEscapement", LONG),
                ("lfOrientation", LONG),
                ("lfWeight", LONG),
                ("lfItalic", BYTE),
                ("lfUnderline", BYTE),
                ("lfStrikeOut", BYTE),
                ("lfCharSet", BYTE),
                ("lfOutPrecision", BYTE),
                ("lfClipPrecision", BYTE),
                ("lfQuality", BYTE),
                ("lfPitchAndFamily", BYTE),
                ("lfFaceName", WCHAR * 32),
            ]
LOGFONTPTR = POINTER(LOGFONT)

class COMBOBOXINFO(Structure):
    _fields_ = [
        ("cbSize", DWORD),
        ("rcItem", RECT),
        ("rcButton", RECT),
        ("stateButton", DWORD),
        ("hwndCombo", HWND),
        ("hwndItem", HWND),
        ("hwndList", HWND),
    ]

class SYSTEMTIME(Structure):
    _fields_ = [
        ("wYear", WORD),
        ("wMonth", WORD),
        ("wDayOfWeek", WORD),
        ("wDay", WORD),
        ("wHour", WORD),
        ("wMinute", WORD),
        ("wSecond", WORD),
        ("wMilliseconds", WORD),
    ]

class NMSELCHANGE(Structure):
    _fields_ = [
        ("nmhdr", NMHDR),
        ("stSelStart", SYSTEMTIME),
        ("stSelEnd", SYSTEMTIME),
    ]
LPNMSELCHANGE = POINTER(NMSELCHANGE)

class NMVIEWCHANGE(Structure):
    _fields_ = [
        ("nmhdr", NMHDR),
        ("dwOldView", DWORD),
        ("dwNewView", DWORD),
    ]
LPNMVIEWCHANGE = POINTER(NMVIEWCHANGE)

class NMDATETIMECHANGE(Structure):
    _fields_ = [
        ("nmhdr", NMHDR),
        ("dwFlags", DWORD),
        ("st", SYSTEMTIME),
    ]
LPNMDATETIMECHANGE = POINTER(NMDATETIMECHANGE)

class NMDATETIMESTRINGW(Structure):
    _fields_ = [
        ("nmhdr", NMHDR),
        ("pszUserString", LPCWSTR),
        ("st", SYSTEMTIME),
        ("dwFlags", DWORD),
    ]
LPNMDATETIMESTRINGW = POINTER(NMDATETIMESTRINGW)

class NMUPDOWN(Structure):
    _fields_ = [
        ("hdr", NMHDR),
        ("iPos", INT),
        ("iDelta", INT),
    ]
LPNMUPDOWN = POINTER(NMUPDOWN)

class WTA_OPTIONS(Structure):
    _fields_ = [
        ("dwFlags", DWORD),
        ("dwMask", DWORD),
    ]
LPWTA_OPTIONS = POINTER(WTA_OPTIONS)

class LOGPEN(Structure):
    _fields_ = [
        ("lopnStyle", UINT),
        ("lopnWidth", POINT),
        ("lopnColor", COLORREF),
    ]
LPLOGPEN = POINTER(LOGPEN)

class TRBTHUMBPOSCHANGING(Structure):
    _fields_ = [
        ("hdr", NMHDR),
        ("dwPos", DWORD),
        ("nReason", INT),
    ]
LPTRBTHUMBPOSCHANGING = POINTER(TRBTHUMBPOSCHANGING)

class NMLVCUSTOMDRAW(Structure):
    _fields_ = [
        ("nmcd", NMCUSTOMDRAW),
        ("clrText", COLORREF),
        ("clrTextBk", COLORREF),
        ("iSubItem", INT),
        ("dwItemType", DWORD),
        ("clrFace", COLORREF),
        ("iIconEffect", INT),
        ("iIconPhase", INT),
        ("iPartId", INT),
        ("iStateId", INT),
        ("rcText", RECT ),
        ("uAlign", UINT ),
    ]
LPNMLVCUSTOMDRAW = POINTER(NMLVCUSTOMDRAW)


class LVCOLUMNW(Structure):
    _fields_ = [
        ("mask", UINT),
        ("fmt", INT),
        ("cx", INT),
        ("pszText", LPWSTR),
        ("cchTextMax", INT),
        ("iSubItem", INT),
        ("iImage", INT),
        ("iOrder", INT),
        ("cxMin", INT),
        ("cxDefault", INT),
        ("cxIdeal", INT),
    ]
LPLVCOLUMNW = POINTER(LVCOLUMNW)

class LVITEMW(Structure):
    _fields_ = [
        ('mask', UINT),
        ('iItem', INT),
        ('iSubItem', INT),
        ('state', UINT),
        ('stateMask', UINT),
        ('pszText', LPWSTR),
        ('cchTextMax', INT),
        ('iImage', INT),
        ('lParam', LPARAM),
        ('iIndent', INT),
        ('iGroupId', INT),
        ('cColumns', UINT),  # tile view columns
        ('puColumns', PUINT),
        ('piColFmt', POINTER(INT)),
        ('iGroup', INT)

    ]

LPLVITEMW = POINTER(LVITEMW)

class HDITEM(Structure):
    _fields_ = [
        ("mask", UINT),
        ("cxy", INT),
        ("pszText", LPWSTR),
        ("hbm", HBITMAP),
        ("cchTextMax", INT),
        ("fmt", INT),
        ("lParam", LPARAM),
        ("iImage", INT),
        ("iOrder", INT),
        ("type", UINT),
        ("pvFilter", c_void_p),
        ("state", UINT),
    ]

LPHDITEM = POINTER(HDITEM)

class HDLAYOUT(Structure):
    _fields_ = [
        ('prc', POINTER(RECT)),
        ('pwpos', LPWINDOWPOS),
    ]

LPHDLAYOUT = POINTER(HDLAYOUT)

class NMITEMACTIVATE(Structure):
    _fields_ = [
        ("hdr", NMHDR),
        ("iItem", INT),
        ("iSubItem", INT),
        ("uNewState", UINT),
        ("uOldState", UINT),
        ("uChanged", UINT),
        ("ptAction", POINT),
        ("lParam", LPARAM),
        ("uKeyFlags", UINT),
    ]

    def __str__(self) -> str:
        s1 = f"iItem: {self.iItem}, iSubItem: {self.iSubItem}, uOldState: "
        s2 = f"{self.uOldState}, uNewState: {self.uNewState}, uChanged: {self.uChanged}"
        return s1 + s2

LPNMITEMACTIVATE = POINTER(NMITEMACTIVATE)

class NMHEADER(Structure):
    _fields_ = [
        ("hdr", NMHDR),
        ("iItem", INT),
        ("iButton", INT),
        ("pitem", LPHDITEM),
    ]

LPNMHEADER = POINTER(NMHEADER)

class HDHITTESTINFO(Structure):
    _fields_ = [
        ("pt", POINT),
        ("flags", UINT),
        ("iItem", INT),
    ]

LPHDHITTESTINFO = POINTER(HDHITTESTINFO)

class APPBARDATA(Structure):
    _fields_ = [
        ("cbSize", DWORD),
        ("hWnd", HWND),
        ("uCallbackMessage", UINT),
        ("uEdge", UINT),
        ("rc", RECT),
        ("lParam", LPARAM),
    ]

LPAPPBARDATA = POINTER(APPBARDATA)

class TVITEMEXW(Structure):
    _fields_ = [
        ("mask", UINT),
        ("hItem", HTREEITEM),
        ("state", UINT),
        ("stateMask", UINT),
        ("pszText", LPCWSTR),
        ("cchTextMax", INT),
        ("iImage", INT),
        ("iSelectedImage" , INT),
        ("cChildren", INT),
        ("lParam", LPARAM),
        ("iIntegral", INT),
        ("uStateEx", UINT),
        ("hwnd", HWND),
        ("iExpandedImage", INT),
        ("iReserved", INT),
    ]
LPTVITEMEXW = POINTER(TVITEMEXW)

class TVINSERTSTRUCT(Structure):
    _fields_ = [
        ("hParent", HTREEITEM),
        ("hInsertAfter", HTREEITEM),
        ("itemEx", TVITEMEXW),
    ]

class NMTVCUSTOMDRAW(Structure):
    _fields_ = [
        ("nmcd", NMCUSTOMDRAW),
        ("clrText", COLORREF),
        ("clrTextBk", COLORREF),
        ("iLevel", INT),
    ]
LPNMTVCUSTOMDRAW = POINTER(NMTVCUSTOMDRAW)

class MENUINFO(Structure):
    _fields_ = [
        ("cbSize", DWORD),
        ("fMask", DWORD),
        ("dwStyle", DWORD),
        ("cyMax", UINT),
        ("hbrBack", HBRUSH),
        ("dwContextHelpID", DWORD),
        ("dwMenuData", ULONG_PTR),
    ]
LPMENUINFO = POINTER(MENUINFO)

class MENUITEMINFO(Structure):
    _fields_ = [
        ("cbSize", UINT),
        ("fMask", UINT),
        ("fType", UINT),
        ("fState", UINT),
        ("wID", UINT),
        ("hSubMenu", HMENU),
        ("hbmpChecked", HBITMAP),
        ("hbmpUnchecked", HBITMAP),
        ("dwItemData", ULONG_PTR),
        ("dwTypeData", LPWSTR),
        ("cch", UINT),
        ("hbmpItem", HBITMAP),
    ]
LPMENUITEMINFO = POINTER(MENUITEMINFO)

class MEASUREITEMSTRUCT(Structure):
    _fields_ = [
        ("CtlType", UINT),
        ("CtlID", UINT),
        ("itemID", UINT),
        ("itemWidth", UINT),
        ("itemHeight", UINT),
        ("itemData", ULONG_PTR),
    ]
LPMEASUREITEMSTRUCT = POINTER(MEASUREITEMSTRUCT)

class DRAWITEMSTRUCT(Structure):
    _fields_ = [
        ("CtlType", UINT),
        ("CtlID", UINT),
        ("itemID", UINT),
        ("itemAction", UINT),
        ("itemState", UINT),
        ("hwndItem", HWND),
        ("hDC", HDC),
        ("rcItem", RECT),
        ("itemData", ULONG_PTR),
    ]
LPDRAWITEMSTRUCT = POINTER(DRAWITEMSTRUCT)

class OPENFILENAMEW(Structure):
    _fields_ = [
        ("lStructSize", DWORD),
        ("hwndOwner", HWND),
        ("hInstance", HINSTANCE),
        ("lpstrFilter", LPCWSTR),
        ("lpstrCustomFilter", LPWSTR),
        ("nMaxCustFilter", DWORD),
        ("nFilterIndex", DWORD),
        ("lpstrFile", LPWSTR),
        ("nMaxFile", DWORD),
        ("lpstrFileTitle", LPWSTR),
        ("nMaxFileTitle", DWORD),
        ("lpstrInitialDir", LPCWSTR),
        ("lpstrTitle", LPCWSTR),
        ("Flags", DWORD),
        ("nFileOffset", WORD),
        ("nFileExtension", WORD),
        ("lpstrDefExt", LPCWSTR),
        ("lCustData", LPARAM),
        ("lpfnHook", LPOFNHOOKPROC),
        ("lpTemplateName", LPCWSTR),
        ("pvReserved", c_void_p),
        ("dwReserved", DWORD),
        ("FlagsEx", DWORD),
    ]
LPOPENFILENAMEW = POINTER(OPENFILENAMEW)

class SHITEMID(Structure):
    _fields_ = [
        ("cb", USHORT),
        ("abID", BYTE * 1),
    ]

class ITEMIDLIST(Structure):
    _fields_ = [
        ("mkid", SHITEMID),
    ]
LPITEMIDLIST = POINTER(ITEMIDLIST)
ITEMIDLIST_ABSOLUTE = ITEMIDLIST
PCIDLIST_ABSOLUTE = POINTER(ITEMIDLIST_ABSOLUTE)
PIDLIST_ABSOLUTE = POINTER(ITEMIDLIST_ABSOLUTE)

class BROWSEINFOW(Structure):
    _fields_ = [
        ("hwndOwner", HWND),
        ("pidlRoot", PCIDLIST_ABSOLUTE),
        ("pszDisplayName", LPWSTR),
        ("lpszTitle", LPCWSTR),
        ("ulFlags", UINT),
        ("lpfn", BROWSERCBPROC),
        ("lParam", LPARAM),
        ("iImage", INT),
    ]
LPBROWSEINFOW = POINTER(BROWSEINFOW)

class NIDUN(ct.Union):
    _fields_ = [
        ("uTimeout", UINT),
        ("uVersion", UINT)
    ]

class NOTIFYICONDATA(Structure):
    _fields_ = [
        ("cbSize", DWORD),            # Size of this structure, in bytes.
        ("hWnd", HWND),               # Win Handle that receives notifications from the taskbar icon.
        ("uID", UINT),                # Application-defined identifier of the taskbar icon.
        ("uFlags", UINT),             # Flags indicating which members are valid.
        ("uCallbackMessage", UINT),   # App-defined message ID for icon notifications.
        ("hIcon", HICON),             # Handle to the icon to display.
        ("szTip", WCHAR * 128),       # WCHAR string for the tooltip text (max 127 chars + null).
        ("dwState", DWORD),           # Current state of the icon (e.g., hidden).
        ("dwStateMask", DWORD),       # Mask for dwState.
        ("szInfo", WCHAR * 256),      # WCHAR string for the balloon tooltip text (max 255 + null).
        ("uVerOrTime", NIDUN),           # Version of the NOTIFYICONDATA structure.
        ("szInfoTitle", WCHAR * 64),  # WCHAR string for the title of the balloon tooltip (max 63 + null).
        ("dwInfoFlags", DWORD),       # Flags for the balloon tooltip icon.
    ]
LPNOTIFYICONDATA = POINTER(NOTIFYICONDATA)

class TRBTHUMBPOSCHANGING(Structure):
    _fields_ = [
        ("hdr", NMHDR),    # Notification message header
        ("dwPos", DWORD),  # Position of the thumb (DWORD)
        ("nReason", INT)   # Reason for position change (int)
    ]
LP_TRB_THUMB_POS_CHANGING = POINTER(TRBTHUMBPOSCHANGING)
# -endregion Structures


# -region Functions

# -region USER32 Functions

MessageBox = windll.user32.MessageBoxW
MessageBox.argtypes = [HWND, LPCWSTR, LPCWSTR, UINT]
MessageBox.restype = INT

CreateWindowEx = windll.user32.CreateWindowExW
""" ( DWORD, LPCWSTR, LPCWSTR, DWORD, INT, INT, INT, INT, HWND, HMENU, HINSTANCE, LPVOID,) -> HWND"""
CreateWindowEx.argtypes = ( DWORD, LPCWSTR, LPCWSTR, DWORD, INT, INT, INT, INT, HWND, HMENU, HINSTANCE, LPVOID,)
CreateWindowEx.restype = HWND

RegisterClassEx = windll.user32.RegisterClassExW
""" (POINTER(WNDCLASSEX),) -> ATOM"""
RegisterClassEx.argtypes = (POINTER(WNDCLASSEX),)
RegisterClassEx.restype = ATOM

LoadCursor = windll.user32.LoadCursorW
""" (HINSTANCE, LPCWSTR) -> HCURSOR"""
LoadCursor.argtypes = (HINSTANCE, LPCWSTR)
LoadCursor.restype = HCURSOR

# LoadCursor = windll.user32.LoadCursorW
# """ (HINSTANCE, LPCWSTR) -> HCURSOR"""
# LoadCursor.argtypes = (HINSTANCE, LPCWSTR)
# LoadCursor.restype = HCURSOR

LoadImage = windll.user32.LoadImageW
""" (HINSTANCE, LPCWSTR name, UINT type, INT cx, INT cy, UINT fuLoad) -> HANDLE"""
LoadImage.argtypes = (HINSTANCE, LPCWSTR, UINT, INT, INT, UINT)
LoadImage.restype = HANDLE

CloseWindow = windll.user32.CloseWindow
""" (HWND,) -> BOOL"""
CloseWindow.argtypes = (HWND,)
CloseWindow.restype = BOOL

InflateRect = windll.user32.InflateRect
""" (LPRECT, INT, INT) -> BOOL"""
InflateRect.argtypes = (LPRECT, INT, INT)
InflateRect.restype = BOOL

SetFocus = windll.user32.SetFocus
""" (HWND,) -> HWND"""
SetFocus.argtypes = (HWND,)
SetFocus.restype = HWND

ShowWindow = windll.user32.ShowWindow
""" (HWND, INT,) -> BOOL"""
ShowWindow.argtypes = (HWND, INT,)
ShowWindow.restype = BOOL

UpdateWindow = windll.user32.UpdateWindow
""" (HWND,) -> BOOL"""
UpdateWindow.argtypes = [HWND]
UpdateWindow.restype = BOOL

GetMessage = windll.user32.GetMessageW
""" (MSGPTR, HWND, UINT, UINT,) -> BOOL"""
GetMessage.argtypes = (MSGPTR, HWND, UINT, UINT,)
GetMessage.restype = BOOL

TranslateMessage = windll.user32.TranslateMessage
""" (MSGPTR,) -> BOOL"""
TranslateMessage.argtypes = [MSGPTR]
TranslateMessage.restype = BOOL

DispatchMessage = windll.user32.DispatchMessageW
""" (MSGPTR, ) -> LRESULT"""
DispatchMessage.argtypes = [MSGPTR]
DispatchMessage.restype = LRESULT

PostQuitMessage = windll.user32.PostQuitMessage
""" (INT, ) -> None"""
PostQuitMessage.argtypes = (INT, )
PostQuitMessage.restype = None

TrackMouseEvent = windll.user32.TrackMouseEvent
""" [POINTER(TRACKMOUSEEVENT)] -> BOOL"""
TrackMouseEvent.argtypes = [POINTER(TRACKMOUSEEVENT)]
TrackMouseEvent.restype = BOOL

GetClientRect = windll.user32.GetClientRect
""" (HWND, LPRECT, ) -> BOOL"""
GetClientRect.argtypes = (HWND, LPRECT, )
GetClientRect.restype = BOOL

FillRect = windll.user32.FillRect
""" (HDC, LPRECT, HBRUSH, ) -> INT"""
FillRect.argtypes = (HDC, LPRECT, HBRUSH, )
FillRect.restype = INT

FrameRect = windll.user32.FrameRect
""" (HDC, LPRECT, HBRUSH, ) -> INT"""
FrameRect.argtypes = (HDC, LPRECT, HBRUSH, )
FrameRect.restype = INT

DrawEdge = windll.user32.DrawEdge
""" (HDC, LPRECT, UINT, UINT ) -> BOOL"""
DrawEdge.argtypes = (HDC, LPRECT, UINT, UINT )
DrawEdge.restype = BOOL

SendMessage = windll.user32.SendMessageW
""" [HWND, UINT, WPARAM, LPARAM] -> LRESULT"""
SendMessage.argtypes = [HWND, UINT, WPARAM, LPARAM]
SendMessage.restype = LRESULT

PostMessage = windll.user32.PostMessageW
""" [HWND, UINT, WPARAM, LPARAM] -> LRESULT"""
PostMessage.argtypes = [HWND, UINT, WPARAM, LPARAM]
PostMessage.restype = LRESULT

SendNotifyMessage = windll.user32.SendNotifyMessageW
""" [HWND, UINT, WPARAM, LPARAM] -> LRESULT"""
SendNotifyMessage.argtypes = [HWND, UINT, WPARAM, LPARAM]
SendNotifyMessage.restype = BOOL

GetSystemMetrics = windll.user32.GetSystemMetrics
""" (INT,) -> INT"""
GetSystemMetrics.argtypes = (INT,)
GetSystemMetrics.restype = INT

DefWindowProc = windll.user32.DefWindowProcW
""" (HWND, UINT, WPARAM, LPARAM,) -> LRESULT"""
DefWindowProc.argtypes = (HWND, UINT, WPARAM, LPARAM,)
DefWindowProc.restype = LRESULT

SetWindowLongPtr = windll.user32.SetWindowLongPtrW
""" [HWND, INT, LONG_PTR] -> LONG_PTR"""
SetWindowLongPtr.argtypes = [HWND, INT, LONG_PTR]
SetWindowLongPtr.restype = LONG_PTR

SetWindowLong = windll.user32.SetWindowLongW
""" [HWND, INT, LONG] -> LONG"""
SetWindowLong.argtypes = [HWND, INT, LONG]
SetWindowLong.restype = LONG

GetWindowLong = windll.user32.GetWindowLongW
""" [HWND, INT] -> LONG"""
GetWindowLong.argtypes = [HWND, INT]
GetWindowLong.restype = LONG

GetWindowLongPtr = windll.user32.GetWindowLongPtrW
""" [HWND, INT] -> LONG_PTR"""
GetWindowLongPtr.argtypes = [HWND, INT]
GetWindowLongPtr.restype = LONG_PTR

DrawFrameControl = windll.user32.DrawFrameControl
""" [HDC, LPRECT, UINT, UINT] -> BOOL"""
DrawFrameControl.argtypes = [HDC, LPRECT, UINT, UINT]
DrawFrameControl.restype = BOOL

GetDC = windll.user32.GetDC
""" [HWND] -> HDC"""
GetDC.argtypes = [HWND]
GetDC.restype = HDC

ReleaseDC = windll.user32.ReleaseDC
""" [HWND, HDC] -> INT"""
ReleaseDC.argtypes = [HWND, HDC]
ReleaseDC.restype = INT

InvalidateRect = windll.user32.InvalidateRect
""" [HWND, LPRECT, BOOL] -> BOOL"""
InvalidateRect.argtypes = [HWND, LPRECT, BOOL]
InvalidateRect.restype = BOOL

DrawText = windll.user32.DrawTextW
""" [HDC, LPCWSTR, INT, LPRECT, UINT] -> INT"""
DrawText.argtypes = [HDC, LPCWSTR, INT, LPRECT, UINT]
DrawText.restype = INT

BeginPaint = windll.user32.BeginPaint
""" [HWND, POINTER(PAINTSTRUCT)] -> HDC"""
BeginPaint.argtypes = [HWND, POINTER(PAINTSTRUCT)]
BeginPaint.restype = HDC

EndPaint = windll.user32.EndPaint
""" [HWND, POINTER(PAINTSTRUCT)] -> HDC"""
EndPaint.argtypes = [HWND, POINTER(PAINTSTRUCT)]
EndPaint.restype = HDC

GetWindowTextLength = windll.user32.GetWindowTextLengthW
""" [HWND] -> INT"""
GetWindowTextLength.argtypes = [HWND]
GetWindowTextLength.restype = INT

GetWindowText = windll.user32.GetWindowTextW
""" [HWND, LPWSTR, INT] -> INT"""
GetWindowText.argtypes = [HWND, LPWSTR, INT]
GetWindowText.restype = INT

SetWindowText = windll.user32.SetWindowTextW
""" [HWND, LPCWSTR] -> INT"""
SetWindowText.argtypes = [HWND, LPCWSTR]
SetWindowText.restype = INT

MoveWindow = windll.user32.MoveWindow
""" [HWND, INT, INT, INT, INT, BOOL] -> BOOL"""
MoveWindow.argtypes = [HWND, INT, INT, INT, INT, BOOL]
MoveWindow.restype = BOOL

GetComboBoxInfo = windll.user32.GetComboBoxInfo
""" [HWND, POINTER(COMBOBOXINFO)] -> BOOL"""
GetComboBoxInfo.argtypes = [HWND, POINTER(COMBOBOXINFO)]
GetComboBoxInfo.restype = BOOL

DestroyWindow = windll.user32.DestroyWindow
""" [HWND] -> BOOL"""
DestroyWindow.argtypes = [HWND]
DestroyWindow.restype = BOOL

GetWindowRect = windll.user32.GetWindowRect
""" (HWND, POINTER(RECT),) -> BOOL"""
GetWindowRect.argtypes = (HWND, POINTER(RECT),)
GetWindowRect.restype = BOOL

PtInRect = windll.user32.PtInRect
""" [POINTER(RECT), POINT] -> BOOL"""
PtInRect.argtypes = [POINTER(RECT), POINT]
PtInRect.restype = BOOL

ScreenToClient = windll.user32.ScreenToClient
""" [HWND, POINTER(POINT)] -> BOOL"""
ScreenToClient.argtypes = [HWND, POINTER(POINT)]
ScreenToClient.restype = BOOL

GetCursorPos = windll.user32.GetCursorPos
""" [POINTER(POINT)] -> BOOL"""
GetCursorPos.argtypes = [POINTER(POINT)]
GetCursorPos.restype = BOOL

SetWindowPos = windll.user32.SetWindowPos
""" [HWND, HWND, INT, INT, INT, INT, UINT] -> BOOL"""
SetWindowPos.argtypes = [HWND, HWND, INT, INT, INT, INT, UINT]
SetWindowPos.restype = BOOL

GetDCEx = windll.user32.GetDCEx
""" [HWND, HRGN, DWORD] -> HDC"""
GetDCEx.argtypes = [HWND, HRGN, DWORD]
GetDCEx.restype = HDC

RedrawWindow = windll.user32.RedrawWindow
""" [HWND, POINTER(RECT), HRGN, UINT] -> BOOL"""
RedrawWindow.argtypes = [HWND, POINTER(RECT), HRGN, UINT]
RedrawWindow.restype = BOOL

GetUpdateRect = windll.user32.GetUpdateRect
""" [HWND, POINTER(RECT), BOOL] -> BOOL"""
GetUpdateRect.argtypes = [HWND, POINTER(RECT), BOOL]
GetUpdateRect.restype = BOOL

SetForegroundWindow = windll.user32.SetForegroundWindow
""" [HWND] -> BOOL"""
SetForegroundWindow.argtypes = [HWND]
SetForegroundWindow.restype = BOOL

HideCaret = windll.user32.HideCaret
""" [Optional HWND] -> BOOL"""
HideCaret.argtypes = [HWND]
HideCaret.restype = BOOL

GetClassInfoExW = windll.user32.GetClassInfoExW
""" [HINSTANCE, LPCWSTR(The class name), POINTER(WNDCLASSEX)] -> BOOL"""
GetClassInfoExW.argtypes = [HINSTANCE, LPCWSTR, POINTER(WNDCLASSEX)]
GetClassInfoExW.restype = BOOL

SetRect = windll.user32.SetRect
""" [POINTER(RECT), INT, INT, INT, INT] -> BOOL"""
SetRect.argtypes = [POINTER(RECT), INT, INT, INT, INT]
SetRect.restype = BOOL

GetClassLongPtrW = windll.user32.GetClassLongPtrW
""" [HWND, INT] -> ULONG_PTR"""
GetClassLongPtrW.argtypes = [HWND, INT]
GetClassLongPtrW.restype = ULONG_PTR

WindowFromDC = windll.user32.WindowFromDC
""" [HDC] -> HWND"""
WindowFromDC.argtypes = [HDC]
WindowFromDC.restype = HWND

CreateMenu = windll.user32.CreateMenu
""" [] -> HMENU"""
CreateMenu.argtypes = []
CreateMenu.restype = HMENU

CreatePopupMenu = windll.user32.CreatePopupMenu
""" [] -> HMENU"""
CreatePopupMenu.argtypes = []
CreatePopupMenu.restype = HMENU

TrackPopupMenu = windll.user32.TrackPopupMenu
""" [HMENU, UINT, INT, INT, INT, HWND, LPRECT] -> BOOL"""
TrackPopupMenu.argtypes = [HMENU, UINT, INT, INT, INT, HWND, LPRECT]
TrackPopupMenu.restype = BOOL

SetMenuItemInfo = windll.user32.SetMenuItemInfoW
""" [HMENU, UINT, BOOL, LPMENUITEMINFO] -> BOOL"""
SetMenuItemInfo.argtypes = [HMENU, UINT, BOOL, LPMENUITEMINFO]
SetMenuItemInfo.restype = BOOL

GetSubMenu = windll.user32.GetSubMenu
""" [HMENU, INT] -> HMENU"""
GetSubMenu.argtypes = [HMENU, INT]
GetSubMenu.restype = HMENU


DestroyMenu = windll.user32.DestroyMenu
""" [HMENU] -> BOOL"""
DestroyMenu.argtypes = [HMENU]
DestroyMenu.restype = BOOL

EnableMenuItem = windll.user32.EnableMenuItem
""" [HMENU, UINT, UINT] -> BOOL"""
EnableMenuItem.argtypes = [HMENU, UINT, UINT]
EnableMenuItem.restype = BOOL

AppendMenu = windll.user32.AppendMenuW
""" [HMENU, UINT: flags, UINT_PTR: menu id, LPCWSTR: text] -> BOOL"""
AppendMenu.argtypes = [HMENU, UINT, UINT_PTR, LPCWSTR]
AppendMenu.restype = BOOL

SetMenu = windll.user32.SetMenu
""" [HWND, HMENU] -> BOOL"""
SetMenu.argtypes = [HWND, HMENU]
SetMenu.restype = BOOL

SetMenuInfo = windll.user32.SetMenuInfo
""" [HWND, LPMENUINFO] -> BOOL"""
SetMenuInfo.argtypes = [HWND, LPMENUINFO]
SetMenuInfo.restype = BOOL

InsertMenuItemW = windll.user32.InsertMenuItemW
""" [HWND, LPMENUITEMINFO] -> BOOL"""
InsertMenuItemW.argtypes = [HMENU, UINT, BOOL, LPMENUITEMINFO]
InsertMenuItemW.restype = BOOL

InsertMenuW = windll.user32.InsertMenuW
""" [HMENU, UINT, UINT, UINT_PTR, LPCWSTR] -> BOOL"""
InsertMenuW.argtypes = [HMENU, UINT, UINT, UINT_PTR, LPCWSTR]
InsertMenuW.restype = BOOL

ModifyMenu = windll.user32.ModifyMenuW
""" [HMENU, UINT, UINT, UINT_PTR, LPCWSTR] -> BOOL"""
ModifyMenu.argtypes = [HMENU, UINT, UINT, UINT_PTR, LPCWSTR]
ModifyMenu.restype = BOOL

DrawMenuBar = windll.user32.DrawMenuBar
""" [HWND] -> BOOL"""
DrawMenuBar.argtypes = [HWND]
DrawMenuBar.restype = BOOL

ClientToScreen = windll.user32.ClientToScreen
""" [HWND, LPPOINT] -> BOOL"""
ClientToScreen.argtypes = [HWND, LPPOINT]
ClientToScreen.restype = BOOL

MapWindowPoints = windll.user32.MapWindowPoints
""" [HWND, HWND, LPPOINT, UINT] -> BOOL"""
MapWindowPoints.argtypes = [HWND, HWND, LPPOINT, UINT]
MapWindowPoints.restype = BOOL

EnableWindow = windll.user32.EnableWindow
""" [HWND, BOOL - true for enable] -> BOOL"""
EnableWindow.argtypes = [HWND, BOOL]
EnableWindow.restype = BOOL

SetTimer = windll.user32.SetTimer
""" [HWND, UINT_PTR, UINT, TIMERPROC] -> UINT_PTR"""
SetTimer.argtypes = [HWND, UINT_PTR, UINT, TIMERPROC]
SetTimer.restype = UINT_PTR

KillTimer = windll.user32.KillTimer
""" [HWND, UINT_PTR, UINT, TIMERPROC] -> BOOL"""
KillTimer.argtypes = [HWND, UINT_PTR]
KillTimer.restype = BOOL

DestroyIcon = windll.user32.DestroyIcon
DestroyIcon.argtypes = [HICON]
DestroyIcon.restype = BOOL

LoadIcon = windll.user32.LoadIconW
LoadIcon.argtypes = [HINSTANCE, LPCWSTR]
LoadIcon.restype = HICON





# -region USER32 Functions



# -region GDI32 Functions

DeleteObject = windll.gdi32.DeleteObject
""" (HGDIOBJ, ) -> BOOL"""
DeleteObject.argtypes = (HGDIOBJ, )
DeleteObject.restype = BOOL

GetDeviceCaps = windll.gdi32.GetDeviceCaps
""" [HDC, INT] -> INT"""
GetDeviceCaps.argtypes = [HDC, INT]
GetDeviceCaps.restype = INT

CreateSolidBrush = windll.gdi32.CreateSolidBrush
""" [COLORREF] -> HBRUSH"""
CreateSolidBrush.argtypes = [COLORREF]
CreateSolidBrush.restype = HBRUSH

SetTextColor = windll.gdi32.SetTextColor
""" [HDC, COLORREF] -> COLORREF"""
SetTextColor.argtypes = [HDC, COLORREF]
SetTextColor.restype = COLORREF

SetBkMode = windll.gdi32.SetBkMode
""" [HDC, INT] -> INT"""
SetBkMode.argtypes = [HDC, INT]
SetBkMode.restype = INT

SelectObject = windll.gdi32.SelectObject
""" [HDC, HGDIOBJ] -> HGDIOBJ"""
SelectObject.argtypes = [HDC, HGDIOBJ]
SelectObject.restype = HGDIOBJ

CreatePen = windll.gdi32.CreatePen
""" [INT, INT, COLORREF] -> HPEN"""
CreatePen.argtypes = [INT, INT, COLORREF]
CreatePen.restype = HPEN

Rectangle = windll.gdi32.Rectangle
""" [HDC, INT, INT, INT, INT] -> BOOL"""
Rectangle.argtypes = [HDC, INT, INT, INT, INT]
Rectangle.restype = BOOL

DeleteDC = windll.gdi32.DeleteDC
""" [HDC] -> BOOL"""
DeleteDC.argtypes = [HDC]
DeleteDC.restype = BOOL

CreatePatternBrush = windll.gdi32.CreatePatternBrush
""" [HBITMAP] -> HBRUSH"""
CreatePatternBrush.argtypes = [HBITMAP]
CreatePatternBrush.restype = HBRUSH

CreateCompatibleDC = windll.gdi32.CreateCompatibleDC
""" [HDC] -> HDC"""
CreateCompatibleDC.argtypes = [HDC]
CreateCompatibleDC.restype = HDC

CreateCompatibleBitmap = windll.gdi32.CreateCompatibleBitmap
""" [HDC, INT, INT] -> HBITMAP"""
CreateCompatibleBitmap.argtypes = [HDC, INT, INT]
CreateCompatibleBitmap.restype = HBITMAP

CreateFontIndirect = windll.gdi32.CreateFontIndirectW
""" [LOGFONTPTR] -> HFONT"""
CreateFontIndirect.argtypes = [LOGFONTPTR]
CreateFontIndirect.restype = HFONT

SetBkColor = windll.gdi32.SetBkColor
""" [HDC, COLORREF] -> COLORREF"""
SetBkColor.argtypes = [HDC, COLORREF]
SetBkColor.restype = COLORREF

SetDCBrushColor = windll.gdi32.SetDCBrushColor
""" [HDC, COLORREF] -> COLORREF"""
SetDCBrushColor.argtypes = [HDC, COLORREF]
SetDCBrushColor.restype = COLORREF

GetStockObject = windll.gdi32.GetStockObject
""" [INT] -> HGDIOBJ"""
GetStockObject.argtypes = [INT]
GetStockObject.restype = HGDIOBJ

GetTextExtentPoint32 = windll.gdi32.GetTextExtentPoint32W
""" [HDC, LPCWSTR, INT, POINTER(SIZE)] -> BOOL"""
GetTextExtentPoint32.argtypes = [HDC, LPCWSTR, INT, POINTER(SIZE)]
GetTextExtentPoint32.restype = BOOL

MoveToEx = windll.gdi32.MoveToEx
""" [HDC, INT, INT, POINTER(POINT)] -> BOOL"""
MoveToEx.argtypes = [HDC, INT, INT, POINTER(POINT)]
MoveToEx.restype = BOOL

LineTo = windll.gdi32.LineTo
""" [HDC, INT, INT] -> BOOL"""
LineTo.argtypes = [HDC, INT, INT]
LineTo.restype = BOOL

GetTextAlign = windll.gdi32.GetTextAlign
""" [HDC] -> UINT"""
GetTextAlign.argtypes = [HDC]
GetTextAlign.restype = UINT

SetTextAlign = windll.gdi32.SetTextAlign
""" [HDC, UINT] -> UINT"""
SetTextAlign.argtypes = [HDC, UINT]
SetTextAlign.restype = UINT

CreatePenIndirect = windll.gdi32.CreatePenIndirect
""" [POINTER(LOGPEN)] -> HPEN"""
CreatePenIndirect.argtypes = [POINTER(LOGPEN)]
CreatePenIndirect.restype = HPEN

GetCurrentObject = windll.gdi32.GetCurrentObject
""" [HDC, UINT: The object type to be queried] -> HGDIOBJ"""
GetCurrentObject.argtypes = [HDC, UINT]
GetCurrentObject.restype = HGDIOBJ

TextOut = windll.gdi32.TextOutW
""" [HDC, INT - x, INT - y, LPCWSTR - text, INT - len(text)] -> BOOL"""
TextOut.argtypes = [HDC, INT, INT, LPCWSTR, INT]
TextOut.restype = BOOL

RoundRect = windll.gdi32.RoundRect
""" [HDC, INT, INT, INT, INT, INT, INT] -> BOOL"""
RoundRect.argtypes = [HDC, INT, INT, INT, INT, INT, INT]
RoundRect.restype = BOOL

FillPath = windll.gdi32.FillPath
""" [HDC] -> BOOL"""
FillPath.argtypes = [HDC]
FillPath.restype = BOOL

GetObject = windll.gdi32.GetObjectW
GetObject.argtypes = [HANDLE, INT, LPVOID]
GetObject.restype = INT

BitBlt = windll.gdi32.BitBlt
BitBlt.argtypes = [HDC, INT, INT, INT, INT, HDC, INT, INT, DWORD]
BitBlt.restype = BOOL

SetDCPenColor = windll.gdi32.SetDCPenColor
SetDCPenColor.argtypes = [HDC, COLORREF]
SetDCPenColor.restype = COLORREF

Ellipse = windll.gdi32.Ellipse
Ellipse.argtypes = [HDC, INT, INT, INT, INT]
Ellipse.restype = BOOL


# -endregion GDI32 Functions

# -region KERNEL32 Functions

GetModuleHandle = windll.kernel32.GetModuleHandleW
""" [LPCWSTR] -> HMODULE"""
GetModuleHandle.argtypes = (LPCWSTR,)
GetModuleHandle.restype = HMODULE

MulDiv = windll.kernel32.MulDiv
""" [INT, INT, INT] -> INT"""
MulDiv.argtypes = [INT, INT, INT]
MulDiv.restype = INT

MbtWc = windll.kernel32.MultiByteToWideChar
MbtWc.argtypes = [UINT, DWORD, c_char_p, INT, LPWSTR, INT ]
MbtWc.restype = INT

WctMb = windll.kernel32.WideCharToMultiByte
WctMb.argtypes = [UINT, DWORD, LPCWSTR, INT, c_char_p, INT, c_char_p, INT]
WctMb.restype = INT

GetLastError = windll.kernel32.GetLastError
"""NONE -> DWORD"""
GetLastError.restype = DWORD
# -endregion KERNEL32 Functions

#==================================================================================MISCS
# -region MISC DLL Functions
DefSubclassProc = windll.comctl32.DefSubclassProc
""" [HWND, UINT, WPARAM, LPARAM] -> LRESULT"""
DefSubclassProc.argtypes = [HWND, UINT, WPARAM, LPARAM]
DefSubclassProc.restype = LRESULT

SetWindowSubclass = windll.comctl32.SetWindowSubclass
""" [HWND, SUBCLASSPROC, UINT_PTR, DWORD_PTR] -> BOOL"""
SetWindowSubclass.argtypes = [HWND, SUBCLASSPROC, UINT_PTR, DWORD_PTR]
SetWindowSubclass.restype = BOOL

RemoveWindowSubclass = windll.comctl32.RemoveWindowSubclass
""" [HWND, SUBCLASSPROC, UINT_PTR] -> BOOL"""
RemoveWindowSubclass.argtypes = [HWND, SUBCLASSPROC, UINT_PTR]
RemoveWindowSubclass.restype = BOOL

InitCommonControlsEx = windll.comctl32.InitCommonControlsEx
""" [LPINITCOMMONCONTROLSEX] -> BOOL"""
InitCommonControlsEx.argtypes = (LPINITCOMMONCONTROLSEX,)
InitCommonControlsEx.restype = BOOL

SetWindowTheme = windll.uxtheme.SetWindowTheme
""" [HWND, LPCWSTR, LPCWSTR] -> LONG"""
SetWindowTheme.argtypes = [HWND, LPCWSTR, LPCWSTR]
SetWindowTheme.restype = LONG

OpenThemeData = windll.uxtheme.OpenThemeData
""" [HWND, LPCWSTR] -> HANDLE"""
OpenThemeData.argtypes = [HWND, LPCWSTR]
OpenThemeData.restype = HANDLE

CloseThemeData = windll.uxtheme.CloseThemeData
""" [HANDLE] -> HRESULT(LONG)"""
CloseThemeData.argtypes = [HANDLE]
CloseThemeData.restype = LONG

GetThemeColor = windll.uxtheme.GetThemeColor
""" [HANDLE, INT, INT, INT, COLORREF] -> HRESULT(LONG)"""
GetThemeColor.argtypes = [HANDLE, INT, INT, INT, COLORREF]
GetThemeColor.restype = LONG

SetWindowThemeAttribute = windll.uxtheme.SetWindowThemeAttribute
""" [HWND, INT, ct.c_void_p, DWORD] -> HANDLE"""
SetWindowThemeAttribute.argtypes = [HWND, INT, ct.c_void_p, DWORD]
SetWindowThemeAttribute.restype = HANDLE

GetOpenFileName = windll.Comdlg32.GetOpenFileNameW
"""[LPOPENFILENAMEW] -> BOOL"""
GetOpenFileName.argtypes = [LPOPENFILENAMEW]
GetOpenFileName.restype = BOOL

GetSaveFileName = windll.Comdlg32.GetSaveFileNameW
"""[LPOPENFILENAMEW] -> BOOL"""
GetSaveFileName.argtypes = [LPOPENFILENAMEW]
GetSaveFileName.restype = BOOL

SHBrowseForFolder = windll.Shell32.SHBrowseForFolderW
"""[LPBROWSEINFOW] -> PIDLIST_ABSOLUTE"""
SHBrowseForFolder.argtypes = [LPBROWSEINFOW]
SHBrowseForFolder.restype = PIDLIST_ABSOLUTE

SHGetPathFromIDList = windll.Shell32.SHGetPathFromIDListW
"""[PCIDLIST_ABSOLUTE, LPWSTR] -> BOOL"""
SHGetPathFromIDList.argtypes = [PCIDLIST_ABSOLUTE, LPWSTR]
SHGetPathFromIDList.restype = BOOL

Shell_NotifyIcon = windll.Shell32.Shell_NotifyIconW
Shell_NotifyIcon.argtypes = [DWORD, LPNOTIFYICONDATA]
Shell_NotifyIcon.restype = BOOL

CoTaskMemFree = windll.Ole32.CoTaskMemFree
"""[c_void_p] -> BOOL"""
CoTaskMemFree.argtypes = [c_void_p]
CoTaskMemFree.restype = None

GetScaleFactorForDevice = windll.ShCore.GetScaleFactorForDevice
GetScaleFactorForDevice.argtypes = [INT]
GetScaleFactorForDevice.restype = INT

# -endregion MISC DLL Functions

# -endregion Functions

# Sample text

# -region Misc Functions
def print_rct(rc, txt):
    print(f"{txt} --- Left = {rc.left}, Top = {rc.top}, Right = {rc.right}, Bottom = {rc.bottom}")

def get_client_rect(hw: HWND) -> RECT:
    rc = RECT()
    GetClientRect(hw, ct.byref(rc))
    return rc

def MAKE_LONG(a, b): return (a | (b << 16))
def HIWORD(value): return value >> 16
def LOWORD(value): return value & 0x0000FFFF
def MAKEWORD(byte1, byte2): return byte1 | (byte2 << 8)
def MAKELONG(word1, word2): return word1 | (word2 << 16)
def LOBYTE(value): return value & 0x000000FF
def HIBYTE(value): return value >> 8
# -endregion Misc Functions

# ddll = ct.WinDLL(r"C:\Users\kcvin\OneDrive\Programming\D_Lang\PyHelper\pydhelper.dll")
# src_dir = script_directory = os.path.dirname(os.path.abspath(__file__))
# ddll = ct.WinDLL(f"{src_dir}\\pydhelper.dll")

# ddll = ct.WinDLL(r"E:\OneDrive Folder\OneDrive\Programming\Python\PyForms\pyforms\pydhelper.dll")

# nimdll = ct.WinDLL(r"C:\Users\kcvin\OneDrive\Programming\Nim\PyNim\pynim\pynim.dll")
# c3dll = ct.WinDLL(r"C:\Users\kcvin\OneDrive\Programming\C3\Pyc3\pyhelper\pyhelper.dll")

# gbrushInD = ddll.createGBrushInD
# gbrushInD.argtypes = [HDC, RECT, ct.c_uint, ct.c_uint, ct.c_uint, ct.c_uint, ct.c_uint, ct.c_uint, ct.c_bool ]
# gbrushInD.restype = HBRUSH

# drawHdrD = ddll.drawHeaderInD
# drawHdrD.argtypes = [LPNMCUSTOMDRAW, HBRUSH, HBRUSH, HFONT, COLORREF, INT, ct.c_bool, LPCWSTR, DWORD]

# gbrushInNimDll = nimdll.gradientNimDLL
# gbrushInNimDll.argtypes = [HDC, RECT, ct.c_uint, ct.c_uint, ct.c_uint, ct.c_uint, ct.c_uint, ct.c_uint, ct.c_bool ]
# gbrushInNimDll.restype = HBRUSH

# gBrushInC3 = c3dll.gBrushInC3
# gBrushInC3.argtypes = [HDC, RECT, ct.c_uint, ct.c_uint, ct.c_uint, ct.c_uint, ct.c_uint, ct.c_uint, ct.c_bool ]
# gBrushInC3.restype = HBRUSH

# pyniminit = nimdll.pynimInit
# pyniminit()