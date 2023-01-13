

import ctypes as ctp
from ctypes.wintypes import UINT, INT, HANDLE, LPCWSTR, HICON, HWND, WPARAM, LPARAM, DWORD, LPWSTR, LONG
from ctypes import c_int64, c_uint64, POINTER, WINFUNCTYPE, Structure, byref, sizeof, c_wchar_p
from ctypes import cast, create_unicode_buffer
from ctypes import windll as wdll

# Required types
LRESULT = c_int64
HCURSOR = HICON
UINT_PTR = c_int64
DWORD_PTR = c_uint64
LONG_PTR = c_uint64
ULONG_PTR = c_uint64
PUINT = POINTER(UINT)
WNDPROC = WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM)

# Declare required dlls
user32 = wdll.user32
kernel32 = wdll.kernel32
gdi32 = wdll.gdi32

# We need this prototype otherwise we will get this error:
# -----------'ctypes.ArgumentError: argument 4: <class 'OverflowError'>: int too long to convert
DefWindowProc = user32.DefWindowProcW
DefWindowProc.argtypes = (HWND, UINT, WPARAM, LPARAM,)
DefWindowProc.restype = LRESULT


# Declare required constants
CS_VREDRAW = 0x0001
CS_HREDRAW = 0x0002
CS_OWNDC = 0x0020
CS_CLASSDC = 0x0040
CS_PARENTDC = 0x0080

IDC_ARROW = (32512)
WS_OVERLAPPED = 0x00000000
WS_CAPTION = 0x00C00000
WS_SYSMENU = 0x00080000
WS_THICKFRAME = 0x00040000
WS_MINIMIZEBOX = 0x00020000
WS_MAXIMIZEBOX = 0x00010000
WS_OVERLAPPEDWINDOW = (WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_THICKFRAME | WS_MINIMIZEBOX | WS_MAXIMIZEBOX)

WS_CHILD = 0x40000000
WS_VISIBLE = 0x10000000
WS_BORDER = 0x00800000

SW_SHOW = 5

LVCF_FMT = 0x0001
LVCF_WIDTH = 0x0002
LVCF_TEXT = 0x0004
LVCF_SUBITEM = 0x0008

LVCFMT_LEFT = 0x0000
LVM_FIRST = 0x1000
LVM_INSERTCOLUMNW = (LVM_FIRST + 97)

LVIF_TEXT = 0x00000001
LVIF_IMAGE = 0x00000002
LVIF_PARAM = 0x00000004
LVIF_STATE = 0x00000008

LVM_INSERTITEMW = (LVM_FIRST + 77)
LVM_SETITEMTEXTW = (LVM_FIRST + 116)
LVM_SETEXTENDEDLISTVIEWSTYLE = (LVM_FIRST + 54)

LVS_EX_GRIDLINES = 0x00000001
LVS_EX_FULLROWSELECT = 0x00000020
LVS_ALIGNLEFT = 0x0800
LVS_EDITLABELS = 0x0200
LVS_REPORT = 0x0001

WM_CREATE = 0x0001
WM_DESTROY = 0x0002

# Required structs
class POINT(Structure):
    _fields_ = [
        ('x', LONG),
        ('y', LONG)
    ]

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
        ('cColumns', UINT),
        ('puColumns', PUINT),
        ('piColFmt', POINTER(INT)),
        ('iGroup', INT)
    ]



def add_column(lv, col_txt, width, indx):
	lvc = LVCOLUMNW()
	lvc.mask = LVCF_TEXT  | LVCF_WIDTH | LVCF_FMT | LVCF_SUBITEM
	lvc.fmt = LVCFMT_LEFT
	lvc.cx = width
	lvc.pszText = cast(create_unicode_buffer(col_txt), c_wchar_p)
	user32.SendMessageW(lv, LVM_INSERTCOLUMNW, indx, byref(lvc))


def add_row(lv, item_index, *items):
	lvi = LVITEMW()
	lvi.mask = LVIF_TEXT | LVIF_PARAM | LVIF_STATE
	lvi.state = 0
	lvi.stateMask = 0
	lvi.iItem = item_index
	lvi.iSubItem = 0
	lvi.pszText = cast(create_unicode_buffer(items[0]), c_wchar_p)
	lvi.cchTextMax = len(items[0]) + 1
	user32.SendMessageW(lv, LVM_INSERTITEMW, 0, byref(lvi))

	for i in range(1, len(items)):
		subitem = items[i]
		sitem = subitem if isinstance(subitem, str) else str(subitem)
		lvi2 = LVITEMW()
		lvi2.iSubItem = i
		lvi2.pszText = cast(ctp.create_unicode_buffer(sitem), c_wchar_p)
		user32.SendMessageW(lv, LVM_SETITEMTEXTW, item_index, byref(lvi2))


def create_lv(win, hins):
	print(win)
	lvs =WS_CHILD | WS_VISIBLE | LVS_ALIGNLEFT| LVS_EDITLABELS | WS_BORDER | LVS_REPORT
	hlv = user32.CreateWindowExW(0, "SysListView32", "", lvs, 10, 10, 500, 300, win, 101, hins, None)

	user32.SendMessageW(hlv, LVM_SETEXTENDEDLISTVIEWSTYLE, 0, LVS_EX_GRIDLINES | LVS_EX_FULLROWSELECT)
	# user32.SendMessageW(hlv, LVM_SETEXTENDEDLISTVIEWSTYLE, 0, LVS_EX_FULLROWSELECT)
	return hlv


def wnd_proc(hw, message, wParam, lParam):
	if message == WM_DESTROY:
		user32.PostQuitMessage(0)

	elif message == WM_CREATE:
		print("Window created")

	return user32.DefWindowProcW(hw, message, wParam, lParam)


def msg_loop():
	tMsg = MSG()
	while user32.GetMessageW(byref(tMsg), None, 0, 0) != 0:
		user32.TranslateMessage(byref(tMsg))
		user32.DispatchMessageW(byref(tMsg))



# Let's register our window
hins = kernel32.GetModuleHandleW(LPCWSTR(0))
wc = WNDCLASSEX()
wc.cbSize = sizeof(WNDCLASSEX)
wc.style = CS_HREDRAW | CS_VREDRAW | CS_OWNDC
wc.lpfnWndProc = WNDPROC(wnd_proc)
wc.hInstance = hins
wc.hCursor =  user32.LoadCursorW(0, LPCWSTR(IDC_ARROW))
wc.hbrBackground = gdi32.CreateSolidBrush(0x00B1BCBC)
wc.lpszClassName = "Python Window"

user32.RegisterClassExW(ctp.byref(wc))

# All set. Now, create or window.
hwnd = user32.CreateWindowExW(	0,
							wc.lpszClassName,
							"List View Test",
							WS_OVERLAPPEDWINDOW,
							500, 100,
							600, 400,
							0, 0, wc.hInstance, None)

#Now, create listview and add columns & rows.
hlv = create_lv(hwnd, wc.hInstance)
add_column(hlv, "Name", 100, 0)
add_column(hlv, "Job", 250, 1)
add_column(hlv, "Salary", 100, 2)

add_row(hlv, 0, "John Smith", "Manager", 45000)
add_row(hlv, 1, "Harry Clark", "Accountant", 30000)
add_row(hlv, 2, "Emily WIlson", "Cashier", 25000)

# Okay, let's display the window
user32.ShowWindow(hwnd, SW_SHOW)
user32.UpdateWindow(hwnd)

print(f"{sizeof(ctp.c_int) = }, {sizeof(c_int64) = }, {sizeof(ctp.c_size_t) = }, {sizeof(ctp.c_ssize_t) = }")


msg_loop()

print("Your window session ended...")

