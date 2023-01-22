
# Created on 16-Nov-2022 23:06
from ctypes.wintypes import HWND

UINT_MAX = 1 << 32
ULONG_MAX = 1 << 64
WM_USER = 1024
HWND_BOTTOM = HWND(1)
HWND_TOP = HWND(0)
HWND_TOPMOST = HWND(-1)
HWND_NOTOPMOST = HWND(-2)
ABM_SETAUTOHIDEBAR = 8

TRANSPARENT = 1
OPAQUE = 2
WHITE_BRUSH = 0
LTGRAY_BRUSH = 1
GRAY_BRUSH = 2
DKGRAY_BRUSH = 3
BLACK_BRUSH = 4
NULL_BRUSH = 5

DWL_MSGRESULT = 0
DWLP_MSGRESULT = 0

ICC_STANDARD_CLASSES = 0x00004000
ICC_LISTVIEW_CLASSES = 0x00000001# listview, header
ICC_TREEVIEW_CLASSES = 0x00000002# treeview, tooltips
ICC_BAR_CLASSES      = 0x00000004# toolbar, statusbar, trackbar, tooltips
ICC_TAB_CLASSES      = 0x00000008# tab, tooltips
ICC_UPDOWN_CLASS     = 0x00000010# updown
ICC_PROGRESS_CLASS   = 0x00000020# progress
ICC_HOTKEY_CLASS     = 0x00000040# hotkey
ICC_ANIMATE_CLASS    = 0x00000080# animate
ICC_WIN95_CLASSES    = 0x000000FF
ICC_DATE_CLASSES     = 0x00000100# month picker, date picker, time picker, updown
ICC_USEREX_CLASSES   = 0x00000200# comboex
ICC_COOL_CLASSES     = 0x00000400# rebar (coolbar) control

NM_FIRST = UINT_MAX
NM_CLICK = NM_FIRST - 2
NM_SETFOCUS = NM_FIRST - 7
NM_CUSTOMDRAW = ( NM_FIRST-12 )
NM_RELEASEDCAPTURE = NM_FIRST - 16


# -region Misc Constants
LOGPIXELSX = 88
LOGPIXELSY = 90

SC_MINIMIZE = 61472
SC_MAXIMIZE = 61448
SC_RESTORE = 61728
TME_HOVER = 1
TME_LEAVE = 2
HOVER_DEFAULT = 4294967295
DC_BRUSH = 18
SS_NOTIFY = 256
SS_SUNKEN = 4096

DCX_WINDOW = 0x00000001
DCX_CACHE = 0x00000002
DCX_NORESETATTRS = 0x00000004
DCX_CLIPCHILDREN = 0x00000008
DCX_CLIPSIBLINGS = 0x00000010
DCX_PARENTCLIP = 0x00000020
DCX_EXCLUDERGN = 0x00000040
DCX_INTERSECTRGN = 0x00000080
DCX_EXCLUDEUPDATE = 0x00000100
DCX_INTERSECTUPDATE = 0x00000200
DCX_LOCKWINDOWUPDATE = 0x00000400
DCX_VALIDATE = 0x00200000

RDW_INVALIDATE = 0x0001
RDW_INTERNALPAINT = 0x0002
RDW_ERASE = 0x0004
RDW_VALIDATE = 0x0008
RDW_NOINTERNALPAINT = 0x0010
RDW_NOERASE = 0x0020
RDW_NOCHILDREN = 0x0040
RDW_ALLCHILDREN = 0x0080
RDW_UPDATENOW = 0x0100
RDW_ERASENOW = 0x0200
RDW_FRAME = 0x0400
RDW_NOFRAME = 0x0800

CCM_FIRST = 0x2000
CCM_LAST = CCM_FIRST+0x200
CCM_SETBKCOLOR = CCM_FIRST+1
CCM_SETCOLORSCHEME = CCM_FIRST+2
CCM_GETCOLORSCHEME = CCM_FIRST+3
CCM_GETDROPTARGET = CCM_FIRST+4
CCM_SETUNICODEFORMAT = CCM_FIRST+5
CCM_GETUNICODEFORMAT = CCM_FIRST+6
CCM_SETVERSION = CCM_FIRST+0x7
CCM_GETVERSION = CCM_FIRST+0x8
CCM_SETNOTIFYWINDOW = CCM_FIRST+0x9
CCM_SETWINDOWTHEME = CCM_FIRST+0xb
CCM_DPISCALE = CCM_FIRST+0xc

# -endregion Misc Constants




# -region Window Class Constants
CS_VREDRAW = 1
CS_HREDRAW = 2
CS_DBLCLKS = 8
CS_OWNDC = 32
CS_CLASSDC = 64
CS_PARENTDC = 128
CS_NOCLOSE = 512
CS_SAVEBITS = 2048
CS_BYTEALIGNCLIENT = 4096
CS_BYTEALIGNWINDOW = 8192
CS_GLOBALCLASS = 16384
CS_IME = 65536

# -endregion

# -region Mouse Cursor & Pointer Constants
IDC_ARROW = 32512
IDC_IBEAM = 32513
IDC_WAIT = 32514
IDC_CROSS = 32515
IDC_UPARROW = 32516
IDC_SIZE = 32640  # OBSOLETE: use IDC_SIZEALL
IDC_ICON = 32641  # OBSOLETE: use IDC_ARROW
IDC_SIZENWSE = 32642
IDC_SIZENESW = 32643
IDC_SIZEWE = 32644
IDC_SIZENS = 32645
IDC_SIZEALL = 32646
IDC_NO = 32648
IDC_HAND = 32649
IDC_APPSTARTING = 32650
IDC_HELP = 32651
# -endregion

# -region Window Style Constants
WS_VISIBLE = 268435456
WS_OVERLAPPED = 0
WS_POPUP = -2147483648
WS_CHILD = 1073741824
WS_MINIMIZE = 536870912
WS_VISIBLE = 268435456
WS_DISABLED = 134217728
WS_CLIPSIBLINGS = 67108864
WS_CLIPCHILDREN = 33554432
WS_MAXIMIZE = 16777216
WS_CAPTION = 12582912
WS_BORDER = 8388608
WS_DLGFRAME = 4194304
WS_VSCROLL = 2097152
WS_HSCROLL = 1048576
WS_SYSMENU = 524288
WS_THICKFRAME = 262144
WS_GROUP = 131072
WS_TABSTOP = 65536
WS_MINIMIZEBOX = 131072
WS_MAXIMIZEBOX = 65536
WS_TILED = WS_OVERLAPPED
WS_ICONIC = WS_MINIMIZE
WS_SIZEBOX = WS_THICKFRAME
WS_OVERLAPPEDWINDOW = (
    WS_OVERLAPPED
    | WS_CAPTION
    | WS_SYSMENU
    | WS_THICKFRAME
    | WS_MINIMIZEBOX
    | WS_MAXIMIZEBOX
)
WS_POPUPWINDOW = WS_POPUP | WS_BORDER | WS_SYSMENU
WS_CHILDWINDOW = WS_CHILD
WS_TILEDWINDOW = WS_OVERLAPPEDWINDOW
# -endregion Window Style Constants

# -region Window Ex Style Constants
WS_EX_DLGMODALFRAME = 1
WS_EX_NOPARENTNOTIFY = 4
WS_EX_TOPMOST = 8
WS_EX_ACCEPTFILES = 16
WS_EX_TRANSPARENT = 32
WS_EX_MDICHILD = 64
WS_EX_TOOLWINDOW = 128
WS_EX_WINDOWEDGE = 256
WS_EX_CLIENTEDGE = 512
WS_EX_CONTEXTHELP = 1024
WS_EX_RIGHT = 4096
WS_EX_LEFT = 0
WS_EX_RTLREADING = 8192
WS_EX_LTRREADING = 0
WS_EX_LEFTSCROLLBAR = 16384
WS_EX_RIGHTSCROLLBAR = 0
WS_EX_CONTROLPARENT = 65536
WS_EX_STATICEDGE = 131072
WS_EX_APPWINDOW = 262144
WS_EX_OVERLAPPEDWINDOW = WS_EX_WINDOWEDGE | WS_EX_CLIENTEDGE
WS_EX_PALETTEWINDOW = WS_EX_WINDOWEDGE | WS_EX_TOOLWINDOW | WS_EX_TOPMOST
WS_EX_LAYERED = 0x00080000
WS_EX_NOINHERITLAYOUT = 0x00100000
WS_EX_LAYOUTRTL = 0x00400000
WS_EX_COMPOSITED = 0x02000000
WS_EX_NOACTIVATE = 0x08000000
# -endregion Window Ex Style Constants

# -region GetWindowLong Constants
GWL_WNDPROC = -4
GWL_h_instance = -6
GWL_HWNDPARENT = -8
GWL_STYLE = -16
GWL_EXSTYLE = -20
GWL_USERDATA = -21
GWL_ID = -12
# -endregion GetWindowLong Constants

# -region ShowWindow Constants
SW_HIDE = 0
SW_SHOWNORMAL = 1
SW_NORMAL = 1
SW_SHOWMINIMIZED = 2
SW_SHOWMAXIMIZED = 3
SW_MAXIMIZE = 3
SW_SHOWNOACTIVATE = 4
SW_SHOW = 5
SW_MINIMIZE = 6
SW_SHOWMINNOACTIVE = 7
SW_SHOWNA = 8
SW_RESTORE = 9
SW_SHOWDEFAULT = 10
SW_FORCEMINIMIZE = 11
SW_MAX = 11
# -endregion ShowWindow Constants

# -region DrawText Constants
DT_BOTTOM = 8
DT_CALCRECT = 1024
DT_CENTER = 1
DT_EDITCONTROL = 8192
DT_END_ELLIPSIS = 32768
DT_PATH_ELLIPSIS = 16384
DT_WORD_ELLIPSIS = 0x40000
DT_EXPANDTABS = 64
DT_EXTERNALLEADING = 512
DT_LEFT = 0
DT_MODIFYSTRING = 65536
DT_NOCLIP = 256
DT_NOPREFIX = 2048
DT_RIGHT = 2
DT_RTLREADING = 131072
DT_SINGLELINE = 32
DT_TABSTOP = 128
DT_TOP = 0
DT_VCENTER = 4
DT_WORDBREAK = 16
DT_INTERNAL = 4096
# -endregion DrawText Constants

# -region Button Styles
BS_PUSHBUTTON = 0
BS_DEFPUSHBUTTON = 1
BS_CHECKBOX = 2
BS_AUTOCHECKBOX = 3
BS_RADIOBUTTON = 4
BS_3STATE = 5
BS_AUTO3STATE = 6
BS_GROUPBOX = 7
BS_USERBUTTON = 8
BS_AUTORADIOBUTTON = 9
BS_OWNERDRAW = 11
BS_LEFTTEXT = 32
BS_TEXT = 0
BS_ICON = 64
BS_BITMAP = 128
BS_LEFT = 256
BS_RIGHT = 512
BS_CENTER = 768
BS_TOP = 1024
BS_BOTTOM = 2048
BS_VCENTER = 3072
BS_PUSHLIKE = 4096
BS_MULTILINE = 8192
BS_NOTIFY = 16384
BS_FLAT = 32768
BS_RIGHTBUTTON = BS_LEFTTEXT

BN_CLICKED = 0
BN_PAINT = 1
BN_HILITE = 2
BN_UNHILITE = 3
BN_DISABLE = 4
BN_DOUBLECLICKED = 5
BN_PUSHED = BN_HILITE
BN_UNPUSHED = BN_UNHILITE
BN_DBLCLK = BN_DOUBLECLICKED
BN_SETFOCUS = 6
BN_KILLFOCUS = 7
BM_GETCHECK = 0x00F0
BM_SETCHECK = 0x00F1
BM_GETSTATE = 0x00F2
BM_SETSTATE = 0x00F3
BM_SETSTYLE = 0x00F4
BM_CLICK = 0x00F5
BM_GETIMAGE = 0x00F6
BM_SETIMAGE = 0x00F7
BM_SETDONTCLICK = 0x00f8
BST_UNCHECKED = 0x0000
BST_CHECKED = 0x0001
BST_INDETERMINATE = 0x0002
BST_PUSHED = 0x0004
BST_FOCUS = 0x0008
# -endregion Button Styles

# -region Pen Style Constants
PS_SOLID = 0
PS_DASH = 1
PS_DOT = 2
PS_DASHDOT = 3
PS_DASHDOTDOT = 4
PS_NULL = 5
PS_INSIDEFRAME = 6
PS_USERSTYLE = 7
PS_ALTERNATE = 8
PS_STYLE_MASK = 15
PS_ENDCAP_ROUND = 0
PS_ENDCAP_SQUARE = 256
PS_ENDCAP_FLAT = 512
PS_ENDCAP_MASK = 3840
PS_JOIN_ROUND = 0
PS_JOIN_BEVEL = 4096
PS_JOIN_MITER = 8192
PS_JOIN_MASK = 61440
PS_COSMETIC = 0
PS_GEOMETRIC = 65536
PS_TYPE_MASK = 983040
# -endregion Pen Style Constants

# -region TextBox Constants
ES_AUTOHSCROLL = 128
ES_AUTOVSCROLL = 64
ES_CENTER = 1
ES_LEFT	= 0
ES_LOWERCASE = 16
ES_MULTILINE = 4
ES_NOHIDESEL = 256
ES_NUMBER = 8192
ES_OEMCONVERT = 1024
ES_PASSWORD = 32
ES_READONLY = 2048
ES_RIGHT = 2
ES_UPPERCASE = 8
ES_WANTRETURN = 4096

EM_GETSEL = 0x00B0
EM_SETSEL = 0x00B1
EM_GETRECT = 0x00B2
EM_SETRECT = 0x00B3
EM_SETRECTNP = 0x00B4
EM_SCROLL = 0x00B5
EM_LINESCROLL = 0x00B6
EM_SCROLLCARET = 0x00B7
EM_GETMODIFY = 0x00B8
EM_SETMODIFY = 0x00B9
EM_GETLINECOUNT = 0x00BA
EM_LINEINDEX = 0x00BB
EM_SETHANDLE = 0x00BC
EM_GETHANDLE = 0x00BD
EM_GETTHUMB = 0x00BE
EM_LINELENGTH = 0x00C1
EM_REPLACESEL = 0x00C2
EM_GETLINE = 0x00C4
EM_LIMITTEXT = 0x00C5
EM_CANUNDO = 0x00C6
EM_UNDO = 0x00C7
EM_FMTLINES = 0x00C8
EM_LINEFROMCHAR = 0x00C9
EM_SETTABSTOPS = 0x00CB
EM_SETPASSWORDCHAR = 0x00CC
EM_EMPTYUNDOBUFFER = 0x00CD
EM_GETFIRSTVISIBLELINE = 0x00CE
EM_SETREADONLY = 0x00CF
EM_SETWORDBREAKPROC = 0x00D0
EM_GETWORDBREAKPROC = 0x00D1
EM_GETPASSWORDCHAR = 0x00D2
EM_SETMARGINS = 0x00D3
EM_GETMARGINS = 0x00D4
EM_SETLIMITTEXT = EM_LIMITTEXT
EM_GETLIMITTEXT = 0x00D5
EM_POSFROMCHAR = 0x00D6
EM_CHARFROMPOS = 0x00D7
EM_SETIMESTATUS = 0x00D8
EM_GETIMESTATUS = 0x00D9

EN_SETFOCUS = 0x0100
EN_KILLFOCUS = 0x0200
EN_CHANGE = 0x0300
EN_UPDATE = 0x0400
EN_ERRSPACE = 0x0500
EN_MAXTEXT = 0x0501
EN_HSCROLL = 0x0601
EN_VSCROLL = 0x0602
EN_ALIGN_LTR_EC = 0x0700
EN_ALIGN_RTL_EC = 0x0701
# -endregion TextBox Constants



# -region CheckBox Constants
BCM_FIRST = 0x1600
BCN_FIRST = (UINT_MAX - 1250)
BCM_GETIDEALSIZE = BCM_FIRST+0x1
BCM_SETIMAGELIST = BCM_FIRST+0x2
BCM_GETIMAGELIST = BCM_FIRST+0x3
BCM_SETTEXTMARGIN = BCM_FIRST+0x4
BCM_GETTEXTMARGIN = BCM_FIRST+0x5
BCN_HOTITEMCHANGE = BCN_FIRST+0x1
# -endregion CheckBox Constants

# -region Combobox Constants
CBS_SIMPLE = 0x0001
CBS_DROPDOWN = 0x0002
CBS_DROPDOWNLIST = 0x0003
CBS_OWNERDRAWFIXED = 0x0010
CBS_OWNERDRAWVARIABLE = 0x0020
CBS_AUTOHSCROLL = 0x0040
CBS_OEMCONVERT = 0x0080
CBS_SORT = 0x0100
CBS_HASSTRINGS = 0x0200
CBS_NOINTEGRALHEIGHT = 0x0400
CBS_DISABLENOSCROLL = 0x0800
CBS_UPPERCASE = 0x2000
CBS_LOWERCASE = 0x4000

CB_GETEDITSEL = 0x0140
CB_LIMITTEXT = 0x0141
CB_SETEDITSEL = 0x0142
CB_ADDSTRING = 0x0143
CB_DELETESTRING = 0x0144
CB_DIR = 0x0145
CB_GETCOUNT = 0x0146
CB_GETCURSEL = 0x0147
CB_GETLBTEXT = 0x0148
CB_GETLBTEXTLEN = 0x0149
CB_INSERTSTRING = 0x014A
CB_RESETCONTENT = 0x014B
CB_FINDSTRING = 0x014C
CB_SELECTSTRING = 0x014D
CB_SETCURSEL = 0x014E
CB_SHOWDROPDOWN = 0x014F
CB_GETITEMDATA = 0x0150
CB_SETITEMDATA = 0x0151
CB_GETDROPPEDCONTROLRECT = 0x0152
CB_SETITEMHEIGHT = 0x0153
CB_GETITEMHEIGHT = 0x0154
CB_SETEXTENDEDUI = 0x0155
CB_GETEXTENDEDUI = 0x0156
CB_GETDROPPEDSTATE = 0x0157
CB_FINDSTRINGEXACT = 0x0158
CB_SETLOCALE = 0x0159
CB_GETLOCALE = 0x015A
CB_GETTOPINDEX = 0x015b
CB_SETTOPINDEX = 0x015c
CB_GETHORIZONTALEXTENT = 0x015d
CB_SETHORIZONTALEXTENT = 0x015e
CB_GETDROPPEDWIDTH = 0x015f
CB_SETDROPPEDWIDTH = 0x0160
CB_INITSTORAGE = 0x0161
CB_MULTIPLEADDSTRING = 0x0163
CB_GETCOMBOBOXINFO = 0x0164
CB_MSGMAX = 0x0165

CBN_ERRSPACE = -1
CBN_SELCHANGE = 1
CBN_DBLCLK = 2
CBN_SETFOCUS = 3
CBN_KILLFOCUS = 4
CBN_EDITCHANGE = 5
CBN_EDITUPDATE = 6
CBN_DROPDOWN = 7
CBN_CLOSEUP = 8
CBN_SELENDOK = 9
CBN_SELENDCANCEL = 10

# -endregion Combobox Constants

# -region Month Calendar Constants
MCS_DAYSTATE = 0x1
MCS_MULTISELECT = 0x2
MCS_WEEKNUMBERS = 0x4
MCS_NOTODAYCIRCLE = 0x8
MCS_NOTODAY = 0x10
MCS_NOTRAILINGDATES = 0x40
MCS_SHORTDAYSOFWEEK = 0x80
MCS_NOSELCHANGEONNAV = 0x100

MCM_FIRST = 0x1000
MCN_FIRST = (UINT_MAX - 746) #4294966547
MCN_LAST = (UINT_MAX - 752)
MCM_GETCALENDARGRIDINFO = MCM_FIRST+24
MCM_GETCALID = MCM_FIRST+27
MCM_SETCALID = MCM_FIRST+28
MCM_SIZERECTTOMIN = MCM_FIRST+29
MCM_SETCALENDARBORDER = MCM_FIRST+30
MCM_GETCALENDARBORDER = MCM_FIRST+31
MCM_SETCURRENTVIEW = MCM_FIRST+32
MCN_SELCHANGE = (MCN_FIRST - 3)
MCN_GETDAYSTATE = MCN_FIRST+3
MCN_SELECT = MCN_FIRST
MCN_VIEWCHANGE = MCN_FIRST-4

MCM_GETCURSEL = MCM_FIRST+1
MCM_SETCURSEL = MCM_FIRST+2
MCM_GETMAXSELCOUNT = MCM_FIRST+3
MCM_SETMAXSELCOUNT = MCM_FIRST+4
MCM_GETSELRANGE = MCM_FIRST+5
MCM_SETSELRANGE = MCM_FIRST+6
MCM_GETMONTHRANGE = MCM_FIRST+7
MCM_SETDAYSTATE = MCM_FIRST+8
MCM_GETMINREQRECT = MCM_FIRST+9
MCM_SETCOLOR = MCM_FIRST+10
MCM_GETCOLOR = MCM_FIRST+11

# -endregion Month Calendar Constants

# -region SetWindowPos Constants
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
SWP_NOZORDER = 0x0004
SWP_NOREDRAW = 0x0008
SWP_NOACTIVATE = 0x0010
SWP_FRAMECHANGED = 0x0020
SWP_SHOWWINDOW = 0x0040
SWP_HIDEWINDOW = 0x0080
SWP_NOCOPYBITS = 0x0100
SWP_NOOWNERZORDER = 0x0200
SWP_NOSENDCHANGING = 0x0400
SWP_DRAWFRAME = SWP_FRAMECHANGED
SWP_NOREPOSITION = SWP_NOOWNERZORDER
SWP_DEFERERASE = 0x2000
SWP_ASYNCWINDOWPOS = 0x4000
# -endregion SetWindowPos

# -region Font Constants
OUT_DEFAULT_PRECIS = 0
OUT_STRING_PRECIS = 1
CLIP_DEFAULT_PRECIS = 0
OUT_OUTLINE_PRECIS = 8
OUT_DEVICE_PRECIS = 5

DEFAULT_QUALITY = 0
ANTIALIASED_QUALITY = 4
CLEARTYPE_QUALITY = 5
PROOF_QUALITY = 2

VARIABLE_PITCH = 2
DEFAULT_CHARSET = 1
OEM_CHARSET = 255 # Variable c_int

# -endregion Font Constants

# -region  CUSTOMDRAW Constants
CDRF_DODEFAULT          = 0x00000000
CDRF_NEWFONT            = 0x00000002
CDRF_SKIPDEFAULT        = 0x00000004
CDRF_DOERASE            = 0x00000008 #// draw the background
CDRF_SKIPPOSTPAINT      = 0x00000100 #// don't draw the focus rect

CDRF_NOTIFYPOSTPAINT    = 0x00000010
CDRF_NOTIFYITEMDRAW     = 0x00000020
CDRF_NOTIFYSUBITEMDRAW  = 0x00000020  #// flags are the same, we can distinguish by context
CDRF_NOTIFYPOSTERASE    = 0x00000040

CDDS_PREPAINT           = 0x00000001
CDDS_POSTPAINT          = 0x00000002
CDDS_PREERASE           = 0x00000003
CDDS_POSTERASE          = 0x00000004
# the 0x000010000 bit means it's individual item specific
CDDS_ITEM               = 0x00010000 #65536
CDDS_ITEMPREPAINT       = CDDS_ITEM | CDDS_PREPAINT
CDDS_ITEMPOSTPAINT      = CDDS_ITEM | CDDS_POSTPAINT
CDDS_ITEMPREERASE       = CDDS_ITEM | CDDS_PREERASE
CDDS_ITEMPOSTERASE      = CDDS_ITEM | CDDS_POSTERASE
CDDS_SUBITEM            = 0x00020000

CDIS_SELECTED = 0x0001
# -endregion CUSTOMDRAW Constants

# -region DateTimePicker Constants
DTM_FIRST = 0x1000
DTN_FIRST = (UINT_MAX - 740)
DTN_LAST = (UINT_MAX - 745)

DTM_GETSYSTEMTIME = (DTM_FIRST+1)
DTM_SETSYSTEMTIME = (DTM_FIRST+2)
DTM_GETRANGE = (DTM_FIRST+3)
DTM_SETRANGE = (DTM_FIRST+4)
DTM_SETFORMATA = (DTM_FIRST+5)
DTM_SETFORMATW = (DTM_FIRST+50)
DTM_SETMCCOLOR = (DTM_FIRST+6)
DTM_GETMCCOLOR = (DTM_FIRST+7)
DTM_GETMONTHCAL = (DTM_FIRST+8)
DTM_SETMCFONT = (DTM_FIRST+9)
DTM_GETMCFONT = (DTM_FIRST+10)
DTM_SETMCSTYLE = (DTM_FIRST+11)
DTM_GETMCSTYLE = (DTM_FIRST+12)
DTM_CLOSEMONTHCAL = (DTM_FIRST+13)
DTM_GETDATETIMEPICKERINFO = (DTM_FIRST+14)
DTM_GETIDEALSIZE = (DTM_FIRST+15)
DTS_UPDOWN = 0x1
DTS_SHOWNONE = 0x2
DTS_SHORTDATEFORMAT = 0x0
DTS_LONGDATEFORMAT = 0x4
DTS_SHORTDATECENTURYFORMAT = 0xc
DTS_TIMEFORMAT = 0x9
DTS_APPCANPARSE = 0x10
DTS_RIGHTALIGN = 0x20
DTN_USERSTRINGW = (DTN_FIRST-5)
DTN_WMKEYDOWNW = (DTN_FIRST-4)
DTN_FORMATW = (DTN_FIRST-3)
DTN_FORMATQUERYW = (DTN_FIRST-2)

DTS_UPDOWN = 1 # use UPDOWN instead of MONTHCAL
DTS_SHOWNONE = 2 # allow a NONE selection
DTS_SHORTDATEFORMAT = 0 # use the short date format (app must forward WM_WININICHANGE messages)
DTS_LONGDATEFORMAT = 4 # use the long date format (app must forward WM_WININICHANGE messages)
DTS_TIMEFORMAT = 9 # use the time format (app must forward WM_WININICHANGE messages)
DTS_APPCANPARSE = 16 # allow user entered strings (app MUST respond to DTN_USERSTRING)
DTS_RIGHTALIGN = 32 # right-align popup instead of left-align it
DTN_DATETIMECHANGE = (DTN_FIRST + 1)# the systemtime has changed
DTN_USERSTRINGA = (DTN_FIRST + 2) # the user has entered a string
DTN_USERSTRINGW = (DTN_FIRST + 15)
DTN_USERSTRING = DTN_USERSTRINGW
DTN_WMKEYDOWNA = (DTN_FIRST + 3) # modify keydown on app format field (X)
DTN_WMKEYDOWNW = (DTN_FIRST + 16)
DTN_WMKEYDOWN = DTN_WMKEYDOWNA
DTN_FORMATA = (DTN_FIRST + 4) # query display for app format field (X)
DTN_FORMATW = (DTN_FIRST + 17)
DTN_FORMAT = DTN_FORMATA
DTN_FORMATQUERYA = (DTN_FIRST + 5) # query formatting info for app format field (X)
DTN_FORMATQUERYW = (DTN_FIRST + 18)
DTN_FORMATQUERY = DTN_FORMATQUERYA
DTN_DROPDOWN = (DTN_FIRST + 6) # MonthCal has dropped down
DTN_CLOSEUP = (DTN_FIRST + 7) # MonthCal is popping up

# -endregion DateTimePicker Constants

# -region ListBox Constants
LBS_NOTIFY = 1
LBS_SORT = 2
LBS_NOREDRAW = 4
LBS_MULTIPLESEL = 8
LBS_OWNERDRAWFIXED = 16
LBS_OWNERDRAWVARIABLE = 32
LBS_HASSTRINGS = 64
LBS_USETABSTOPS = 128
LBS_NOINTEGRALHEIGHT = 256
LBS_MULTICOLUMN = 512
LBS_WANTKEYBOARDINPUT = 1024
LBS_EXTENDEDSEL = 2048
LBS_DISABLENOSCROLL = 4096
LBS_NODATA = 8192
LBS_NOSEL = 16384

LB_CTLCODE = 0
LB_OKAY = 0
LB_ERR = (-1)
LB_ERRSPACE = (-2)
LBN_ERRSPACE = (-2)
LBN_SELCHANGE = 1
LBN_DBLCLK = 2
LBN_SELCANCEL = 3
LBN_SETFOCUS = 4
LBN_KILLFOCUS = 5
LB_ADDSTRING = 384
LB_INSERTSTRING = 385
LB_DELETESTRING = 386
LB_SELITEMRANGEEX = 387
LB_RESETCONTENT = 388
LB_SETSEL = 389
LB_SETCURSEL = 390
LB_GETSEL = 391
LB_GETCURSEL = 392
LB_GETTEXT = 393
LB_GETTEXTLEN = 394
LB_GETCOUNT = 395
LB_SELECTSTRING = 396
LB_DIR = 397
LB_GETTOPINDEX = 398
LB_FINDSTRING = 399
LB_GETSELCOUNT = 400
LB_GETSELITEMS = 401
LB_SETTABSTOPS = 402
LB_GETHORIZONTALEXTENT = 403
LB_SETHORIZONTALEXTENT = 404
LB_SETCOLUMNWIDTH = 405
LB_ADDFILE = 406
LB_SETTOPINDEX = 407
LB_GETITEMRECT = 408
LB_GETITEMDATA = 409
LB_SETITEMDATA = 410
LB_SELITEMRANGE = 411
LB_SETANCHORINDEX = 412
LB_GETANCHORINDEX = 413
LB_SETCARETINDEX = 414
LB_GETCARETINDEX = 415
LB_SETITEMHEIGHT = 416
LB_GETITEMHEIGHT = 417
LB_FINDSTRINGEXACT = 418
LB_SETLOCALE = 421
LB_GETLOCALE = 422
LB_SETCOUNT = 423
LB_INITSTORAGE = 424
LB_ITEMFROMPOINT = 425
LB_MSGMAX = 432

# -endregion ListBox Constants

# -region NumberPicker Constants
UDS_WRAP = 1
UDS_SETBUDDYINT = 2
UDS_ALIGNRIGHT = 4
UDS_ALIGNLEFT = 8
UDS_AUTOBUDDY = 16
UDS_ARROWKEYS = 32
UDS_HORZ = 64
UDS_NOTHOUSANDS = 128
UDS_HOTTRACK = 256

UDN_FIRST = (UINT_MAX-721)
UDM_SETRANGE = (WM_USER+101)
UDM_GETRANGE = (WM_USER+102)
UDM_SETPOS = (WM_USER+103)
UDM_GETPOS = (WM_USER+104)
UDM_SETBUDDY = (WM_USER+105)
UDM_GETBUDDY = (WM_USER+106)
UDM_SETACCEL = (WM_USER+107)
UDM_GETACCEL = (WM_USER+108)
UDM_SETBASE = (WM_USER+109)
UDM_GETBASE = (WM_USER+110)
UDM_SETRANGE32 = (WM_USER+111)
UDM_GETRANGE32 = (WM_USER+112) # wParam & lParam are LPINT
UDN_DELTAPOS = (UDN_FIRST - 1)

# -endregion NumberPicker Constants

# -region ProgressBar Constants
PBS_SMOOTH = 0x01
PBS_VERTICAL = 0x04
PBS_MARQUEE = 0x08
PBST_NORMAL = 0x0001
PBST_ERROR = 0x0002
PBST_PAUSED = 0x0003

PBM_SETRANGE = (WM_USER+1)
PBM_SETPOS = (WM_USER+2)
PBM_DELTAPOS = (WM_USER+3)
PBM_SETSTEP = (WM_USER+4)
PBM_STEPIT = (WM_USER+5)
PBM_SETRANGE32 = (WM_USER+6) # lParam = high, wParam = low
PBM_GETRANGE = (WM_USER+7) # wParam = return (TRUE ? low : high). lParam = PPBRANGE or NULL
PBM_GETPOS = (WM_USER+8)
PBM_SETBARCOLOR = (WM_USER+9) # lParam = bar color
PBM_SETBKCOLOR = CCM_SETBKCOLOR # lParam = bkColor
PBM_SETMARQUEE = (WM_USER+10)
PBM_GETSTEP = (WM_USER+13)
PBM_GETBKCOLOR = (WM_USER+14)
PBM_GETBARCOLOR = (WM_USER+15)
PBM_SETSTATE = (WM_USER+16) # wParam = PBST_[State] (NORMAL, ERROR, PAUSED)
PBM_GETSTATE = (WM_USER+17)


# -endregion ProgressBar Constants

# -region Constants For Functions
# DrawEdge
BDR_RAISEDOUTER = 0x0001
BDR_SUNKENOUTER = 0x0002
BDR_RAISEDINNER = 0x0004
BDR_SUNKENINNER = 0x0008
BDR_OUTER = (BDR_RAISEDOUTER | BDR_SUNKENOUTER)
BDR_INNER = (BDR_RAISEDINNER | BDR_SUNKENINNER)
BDR_RAISED = (BDR_RAISEDOUTER | BDR_RAISEDINNER)
BDR_SUNKEN = (BDR_SUNKENOUTER | BDR_SUNKENINNER)
EDGE_RAISED = (BDR_RAISEDOUTER | BDR_RAISEDINNER)
EDGE_SUNKEN = (BDR_SUNKENOUTER | BDR_SUNKENINNER)
EDGE_ETCHED = (BDR_SUNKENOUTER | BDR_RAISEDINNER)
EDGE_BUMP = (BDR_RAISEDOUTER | BDR_SUNKENINNER)

BF_LEFT = 0x0001
BF_TOP = 0x0002
BF_RIGHT = 0x0004
BF_BOTTOM = 0x0008
BF_TOPLEFT = (BF_TOP | BF_LEFT)
BF_TOPRIGHT = (BF_TOP | BF_RIGHT)
BF_BOTTOMLEFT = (BF_BOTTOM | BF_LEFT)
BF_BOTTOMRIGHT = (BF_BOTTOM | BF_RIGHT)
BF_RECT = (BF_LEFT | BF_TOP | BF_RIGHT | BF_BOTTOM)
BF_DIAGONAL = 0x0010
BF_DIAGONAL_ENDTOPRIGHT = (BF_DIAGONAL | BF_TOP | BF_RIGHT)
BF_DIAGONAL_ENDTOPLEFT = (BF_DIAGONAL | BF_TOP | BF_LEFT)
BF_DIAGONAL_ENDBOTTOMLEFT = (BF_DIAGONAL | BF_BOTTOM | BF_LEFT)
BF_DIAGONAL_ENDBOTTOMRIGHT = (BF_DIAGONAL | BF_BOTTOM | BF_RIGHT)
BF_MIDDLE = 0x0800
BF_SOFT = 0x1000
BF_ADJUST = 0x2000
BF_FLAT = 0x4000
BF_MONO = 0x8000
# -endregion Constants For Functions

# -region TrackBar Constants
TRBN_FIRST = UINT_MAX - 1501
TRBN_LAST = UINT_MAX - 1519
TBS_AUTOTICKS = 0x1
TBS_VERT = 0x2
TBS_HORZ = 0x0
TBS_TOP = 0x4
TBS_BOTTOM = 0x0
TBS_LEFT = 0x4
TBS_RIGHT = 0x0
TBS_BOTH = 0x8
TBS_NOTICKS = 0x10
TBS_ENABLESELRANGE = 0x20
TBS_FIXEDLENGTH = 0x40
TBS_NOTHUMB = 0x80
TBS_TOOLTIPS = 0x100
TBS_REVERSED = 0x200
TBS_DOWNISLEFT = 0x400
TBS_NOTIFYBEFOREMOVE = 0x800
TBS_TRANSPARENTBKGND = 0x1000
TBM_GETPOS = WM_USER
TBM_GETRANGEMIN = WM_USER+1
TBM_GETRANGEMAX = WM_USER+2
TBM_GETTIC = WM_USER+3
TBM_SETTIC = WM_USER+4
TBM_SETPOS = WM_USER+5
TBM_SETRANGE = WM_USER+6
TBM_SETRANGEMIN = WM_USER+7
TBM_SETRANGEMAX = WM_USER+8
TBM_CLEARTICS = WM_USER+9
TBM_SETSEL = WM_USER+10
TBM_SETSELSTART = WM_USER+11
TBM_SETSELEND = WM_USER+12
TBM_GETPTICS = WM_USER+14
TBM_GETTICPOS = WM_USER+15
TBM_GETNUMTICS = WM_USER+16
TBM_GETSELSTART = WM_USER+17
TBM_GETSELEND = WM_USER+18
TBM_CLEARSEL = WM_USER+19
TBM_SETTICFREQ = WM_USER+20
TBM_SETPAGESIZE = WM_USER+21
TBM_GETPAGESIZE = WM_USER+22
TBM_SETLINESIZE = WM_USER+23
TBM_GETLINESIZE = WM_USER+24
TBM_GETTHUMBRECT = WM_USER+25
TBM_GETCHANNELRECT = WM_USER+26
TBM_SETTHUMBLENGTH = WM_USER+27
TBM_GETTHUMBLENGTH = WM_USER+28
TBM_SETTOOLTIPS = WM_USER+29
TBM_GETTOOLTIPS = WM_USER+30
TBM_SETTIPSIDE = WM_USER+31
TBTS_TOP = 0
TBTS_LEFT = 1
TBTS_BOTTOM = 2
TBTS_RIGHT = 3
TBM_SETBUDDY = WM_USER+32
TBM_GETBUDDY = WM_USER+33
TBM_SETUNICODEFORMAT = CCM_SETUNICODEFORMAT
TBM_GETUNICODEFORMAT = CCM_GETUNICODEFORMAT
TB_LINEUP = 0
TB_LINEDOWN = 1
TB_PAGEUP = 2
TB_PAGEDOWN = 3
TB_THUMBPOSITION = 4
TB_THUMBTRACK = 5
TB_TOP = 6
TB_BOTTOM = 7
TB_ENDTRACK = 8
TBCD_TICS = 0x1
TBCD_THUMB = 0x2
TBCD_CHANNEL = 0x3
TRBN_THUMBPOSCHANGING = TRBN_FIRST-1

THUMB_PAGE_HIGH = 3
THUMB_PAGE_LOW = 2
THUMB_LINE_HIGH = 1
THUMB_LINE_LOW = 0
# -endregion TrackBar Constants

# -region TreeView Constants
TVS_HASBUTTONS = 0x0001
TVS_HASLINES = 0x0002
TVS_LINESATROOT = 0x0004
TVS_EDITLABELS = 0x0008
TVS_DISABLEDRAGDROP = 0x0010
TVS_SHOWSELALWAYS = 0x0020
TVS_RTLREADING = 0x0040
TVS_NOTOOLTIPS = 0x0080
TVS_CHECKBOXES = 0x0100
TVS_TRACKSELECT = 0x0200
TVS_SINGLEEXPAND = 0x0400
TVS_INFOTIP = 0x0800
TVS_FULLROWSELECT = 0x1000
TVS_NOSCROLL = 0x2000
TVS_NONEVENHEIGHT = 0x4000
TVS_NOHSCROLL = 0x8000 # TVS_NOSCROLL overrides this
TVS_EX_NOSINGLECOLLAPSE = 0x0001
TVS_EX_MULTISELECT = 0x0002
TVS_EX_DOUBLEBUFFER = 0x0004
TVS_EX_NOINDENTSTATE = 0x0008
TVS_EX_RICHTOOLTIP = 0x0010
TVS_EX_AUTOHSCROLL = 0x0020
TVS_EX_FADEINOUTEXPANDOS = 0x0040
TVS_EX_PARTIALCHECKBOXES = 0x0080
TVS_EX_EXCLUSIONCHECKBOXES = 0x0100
TVS_EX_DIMMEDCHECKBOXES = 0x0200
TVS_EX_DRAWIMAGEASYNC = 0x0400

TVIF_TEXT = 0x0001
TVIF_IMAGE = 0x0002
TVIF_PARAM = 0x0004
TVIF_STATE = 0x0008
TVIF_SELECTEDIMAGE = 0x0020

TVIS_SELECTED = 0x0002
TVIS_CUT = 0x0004
TVIS_DROPHILITED = 0x0008
TVIS_BOLD = 0x0010
TVIS_EXPANDED = 0x0020
TVIS_EXPANDEDONCE = 0x0040
TVIS_EXPANDPARTIAL = 0x0080
TVIS_OVERLAYMASK = 0x0F00
TVIS_STATEIMAGEMASK = 0xF000
TVIS_USERMASK = 0xF000
TVIS_EX_FLAT = 0x0001
TVIS_EX_DISABLED = 0x0002
TVIS_EX_ALL = 0x0002

from .apis import HTREEITEM

TVI_ROOT = HTREEITEM(ULONG_MAX-0x10000)
TVI_FIRST = HTREEITEM(ULONG_MAX-0x0FFFF)
TVI_LAST = HTREEITEM(ULONG_MAX-0x0FFFE)
TVI_SORT = HTREEITEM(ULONG_MAX-0x0FFFD)

TV_FIRST = 0x1100
TVM_DELETEITEM = (TV_FIRST + 1)
TVM_SETIMAGELIST = (TV_FIRST + 9)
TVM_SETBKCOLOR = (TV_FIRST + 29)
TVM_SETTEXTCOLOR = (TV_FIRST + 30)
TVM_SETLINECOLOR = (TV_FIRST + 40)
TVM_INSERTITEMW = (TV_FIRST + 50)




# -endregion TreeView Constants

# -region ScrollBar Constants
SB_HORZ = 0
SB_VERT = 1
SB_CTL = 2
SB_BOTH = 3
SB_LINEUP = 0
SB_LINELEFT = 0
SB_LINEDOWN = 1
SB_LINERIGHT = 1
SB_PAGEUP = 2
SB_PAGELEFT = 2
SB_PAGEDOWN = 3
SB_PAGERIGHT = 3
SB_THUMBPOSITION = 4
SB_THUMBTRACK = 5
SB_TOP = 6
SB_LEFT = 6
SB_BOTTOM = 7
SB_RIGHT = 7
SB_ENDSCROLL = 8

# -endregion Scrollbar Constants

# -region ListView Constants
LVM_FIRST = 4096
LVN_FIRST = (UINT_MAX-100) # 4294967196
LVS_ICON = 0
LVS_REPORT = 1
LVS_SMALLICON = 2
LVS_LIST = 3
LVS_TYPEMASK = 3
LVS_SINGLESEL = 4
LVS_SHOWSELALWAYS = 8
LVS_SORTASCENDING = 16
LVS_SORTDESCENDING = 32
LVS_SHAREIMAGELISTS = 64
LVS_NOLABELWRAP = 128
LVS_AUTOARRANGE = 256
LVS_EDITLABELS = 512
LVS_OWNERDATA = 4096
LVS_NOSCROLL = 8192
LVS_TYPESTYLEMASK = 64512
LVS_ALIGNTOP = 0
LVS_ALIGNLEFT = 2048
LVS_ALIGNMASK = 3072
LVS_OWNERDRAWFIXED = 1024
LVS_NOCOLUMNHEADER = 16384
LVS_NOSORTHEADER = 32768

LVS_EX_GRIDLINES = 1
LVS_EX_SUBITEMIMAGES = 2
LVS_EX_CHECKBOXES = 4
LVS_EX_TRACKSELECT = 8
LVS_EX_HEADERDRAGDROP = 16
LVS_EX_FULLROWSELECT = 32 # applies to report mode only
LVS_EX_ONECLICKACTIVATE = 64
LVS_EX_TWOCLICKACTIVATE = 128
LVS_EX_FLATSB = 256
LVS_EX_REGIONAL = 512
LVS_EX_INFOTIP = 1024 # listview does InfoTips for you
LVS_EX_UNDERLINEHOT = 2048
LVS_EX_UNDERLINECOLD = 4096
LVS_EX_MULTIWORKAREAS = 8192

LVM_SETUNICODEFORMAT = CCM_SETUNICODEFORMAT
LVM_GETUNICODEFORMAT = CCM_GETUNICODEFORMAT
LVM_GETBKCOLOR = (LVM_FIRST + 0)
LVM_SETBKCOLOR = (LVM_FIRST + 1)
LVM_GETIMAGELIST = (LVM_FIRST + 2)
LVSIL_NORMAL = 0
LVSIL_SMALL = 1
LVSIL_STATE = 2
LVM_SETIMAGELIST = (LVM_FIRST + 3)
LVM_GETITEMCOUNT = (LVM_FIRST + 4)
LVM_GETITEMA = (LVM_FIRST + 5)
LVM_GETITEMW = (LVM_FIRST + 75)
LVM_GETITEM = LVM_GETITEMW
LVM_GETITEM = LVM_GETITEMA
LVM_SETITEMA = (LVM_FIRST + 6)
LVM_SETITEMW = (LVM_FIRST + 76)
LVM_SETITEM = LVM_SETITEMW
LVM_SETITEM = LVM_SETITEMA
LVM_INSERTITEMA = (LVM_FIRST + 7)
LVM_INSERTITEMW = (LVM_FIRST + 77)
LVM_INSERTITEM = LVM_INSERTITEMA
LVM_DELETEITEM = (LVM_FIRST + 8)
LVM_DELETEALLITEMS = (LVM_FIRST + 9)
LVM_GETCALLBACKMASK = (LVM_FIRST + 10)
LVM_SETCALLBACKMASK = (LVM_FIRST + 11)
LVM_FINDITEMA = (LVM_FIRST + 13)
LVM_FINDITEMW = (LVM_FIRST + 83)
LVM_FINDITEM = LVM_FINDITEMA

LVIF_TEXT = 1
LVIF_IMAGE = 2
LVIF_PARAM = 4
LVIF_STATE = 8
LVIF_INDENT = 16
LVIF_NORECOMPUTE = 2048
LVIS_FOCUSED = 1
LVIS_SELECTED = 2
LVIS_CUT = 4
LVIS_DROPHILITED = 8
LVIS_ACTIVATING = 32
LVIS_OVERLAYMASK = 3840
LVIS_STATEIMAGEMASK = 61440
I_INDENTCALLBACK = (-1)
LPSTR_TEXTCALLBACKA = -1
LPSTR_TEXTCALLBACK = LPSTR_TEXTCALLBACKA
I_IMAGECALLBACK = (-1)

LVNI_ALL = 0
LVNI_FOCUSED = 1
LVNI_SELECTED = 2
LVNI_CUT = 4
LVNI_DROPHILITED = 8
LVNI_ABOVE = 256
LVNI_BELOW = 512
LVNI_TOLEFT = 1024
LVNI_TORIGHT = 2048
LVM_GETNEXTITEM = (LVM_FIRST + 12)
LVFI_PARAM = 1
LVFI_STRING = 2
LVFI_PARTIAL = 8
LVFI_WRAP = 32
LVFI_NEARESTXY = 64

LVIR_BOUNDS = 0
LVIR_ICON = 1
LVIR_LABEL = 2
LVIR_SELECTBOUNDS = 3
LVM_GETITEMRECT = (LVM_FIRST + 14)
LVM_SETITEMPOSITION = (LVM_FIRST + 15)
LVM_GETITEMPOSITION = (LVM_FIRST + 16)
LVM_GETSTRINGWIDTHA = (LVM_FIRST + 17)
LVM_GETSTRINGWIDTHW = (LVM_FIRST + 87)
LVM_GETSTRINGWIDTH = LVM_GETSTRINGWIDTHA
LVHT_NOWHERE = 1
LVHT_ONITEMICON = 2
LVHT_ONITEMLABEL = 4
LVHT_ONITEMSTATEICON = 8
LVHT_ONITEM = (LVHT_ONITEMICON | LVHT_ONITEMLABEL | LVHT_ONITEMSTATEICON)
LVHT_ABOVE = 8
LVHT_BELOW = 16
LVHT_TORIGHT = 32
LVHT_TOLEFT = 64
LVM_HITTEST = (LVM_FIRST + 18)
LVM_ENSUREVISIBLE = (LVM_FIRST + 19)
LVM_SCROLL = (LVM_FIRST + 20)
LVM_REDRAWITEMS = (LVM_FIRST + 21)
LVA_DEFAULT = 0
LVA_ALIGNLEFT = 1
LVA_ALIGNTOP = 2
LVA_SNAPTOGRID = 5
LVM_ARRANGE = (LVM_FIRST + 22)
LVM_EDITLABELA = (LVM_FIRST + 23)
LVM_EDITLABELW = (LVM_FIRST + 118)
LVM_EDITLABEL = LVM_EDITLABELW
LVM_EDITLABEL = LVM_EDITLABELA
LVM_GETEDITCONTROL = (LVM_FIRST + 24)
LVCF_FMT = 1
LVCF_WIDTH = 2
LVCF_TEXT = 4
LVCF_SUBITEM = 8
LVCF_IMAGE = 16
LVCF_ORDER = 32
LVCFMT_LEFT = 0
LVCFMT_RIGHT = 1
LVCFMT_CENTER = 2
LVCFMT_JUSTIFYMASK = 3
LVCFMT_IMAGE = 2048
LVCFMT_BITMAP_ON_RIGHT = 4096
LVCFMT_COL_HAS_IMAGES = 32768
LVM_GETCOLUMNA = (LVM_FIRST + 25)
LVM_GETCOLUMNW = (LVM_FIRST + 95)
LVM_GETCOLUMN = LVM_GETCOLUMNA
LVM_SETCOLUMNA = (LVM_FIRST + 26)
LVM_SETCOLUMNW = (LVM_FIRST + 96)
LVM_SETCOLUMN = LVM_SETCOLUMNA
LVM_INSERTCOLUMNA = (LVM_FIRST + 27)
LVM_INSERTCOLUMNW = (LVM_FIRST + 97)
LVM_INSERTCOLUMN = LVM_INSERTCOLUMNA
LVM_DELETECOLUMN = (LVM_FIRST + 28)
LVM_GETCOLUMNWIDTH = (LVM_FIRST + 29)
LVSCW_AUTOSIZE = -1
LVSCW_AUTOSIZE_USEHEADER = -2
LVM_SETCOLUMNWIDTH = (LVM_FIRST + 30)
LVM_GETHEADER = (LVM_FIRST + 31)
LVM_CREATEDRAGIMAGE = (LVM_FIRST + 33)
LVM_GETVIEWRECT = (LVM_FIRST + 34)
LVM_GETTEXTCOLOR = (LVM_FIRST + 35)
LVM_SETTEXTCOLOR = (LVM_FIRST + 36)
LVM_GETTEXTBKCOLOR = (LVM_FIRST + 37)
LVM_SETTEXTBKCOLOR = (LVM_FIRST + 38)
LVM_GETTOPINDEX = (LVM_FIRST + 39)
LVM_GETCOUNTPERPAGE = (LVM_FIRST + 40)
LVM_GETORIGIN = (LVM_FIRST + 41)
LVM_UPDATE = (LVM_FIRST + 42)
LVM_SETITEMSTATE = (LVM_FIRST + 43)
LVM_GETITEMSTATE = (LVM_FIRST + 44)
LVM_GETITEMTEXTA = (LVM_FIRST + 45)
LVM_GETITEMTEXTW = (LVM_FIRST + 115)
LVM_GETITEMTEXT = LVM_GETITEMTEXTW
LVM_GETITEMTEXT = LVM_GETITEMTEXTA
LVM_SETITEMTEXTA = (LVM_FIRST + 46)
LVM_SETITEMTEXTW = (LVM_FIRST + 116)
LVM_SETITEMTEXT = LVM_SETITEMTEXTW
LVM_SETITEMTEXT = LVM_SETITEMTEXTA
LVSICF_NOINVALIDATEALL = 1
LVSICF_NOSCROLL = 2
LVM_SETITEMCOUNT = (LVM_FIRST + 47)
LVM_SORTITEMS = (LVM_FIRST + 48)
LVM_SETITEMPOSITION32 = (LVM_FIRST + 49)
LVM_GETSELECTEDCOUNT = (LVM_FIRST + 50)
LVM_GETITEMSPACING = (LVM_FIRST + 51)
LVM_GETISEARCHSTRINGA = (LVM_FIRST + 52)
LVM_GETISEARCHSTRINGW = (LVM_FIRST + 117)
LVM_GETISEARCHSTRING = LVM_GETISEARCHSTRINGA
LVM_SETICONSPACING = (LVM_FIRST + 53)
LVM_SETEXTENDEDLISTVIEWSTYLE = (LVM_FIRST + 54)   # optional wParam == mask
LVM_GETEXTENDEDLISTVIEWSTYLE = (LVM_FIRST + 55)

LVM_GETSUBITEMRECT = (LVM_FIRST + 56)
LVM_SUBITEMHITTEST = (LVM_FIRST + 57)
LVM_SETCOLUMNORDERARRAY = (LVM_FIRST + 58)
LVM_GETCOLUMNORDERARRAY = (LVM_FIRST + 59)
LVM_SETHOTITEM = (LVM_FIRST + 60)
LVM_GETHOTITEM = (LVM_FIRST + 61)
LVM_SETHOTCURSOR = (LVM_FIRST + 62)
LVM_GETHOTCURSOR = (LVM_FIRST + 63)
LVM_APPROXIMATEVIEWRECT = (LVM_FIRST + 64)
LV_MAX_WORKAREAS = 16
LVM_SETWORKAREAS = (LVM_FIRST + 65)
LVM_GETWORKAREAS = (LVM_FIRST + 70)
LVM_GETNUMBEROFWORKAREAS = (LVM_FIRST + 73)
LVM_GETSELECTIONMARK = (LVM_FIRST + 66)
LVM_SETSELECTIONMARK = (LVM_FIRST + 67)
LVM_SETHOVERTIME = (LVM_FIRST + 71)
LVM_GETHOVERTIME = (LVM_FIRST + 72)
LVM_SETTOOLTIPS = (LVM_FIRST + 74)
LVM_GETTOOLTIPS = (LVM_FIRST + 78)
LVBKIF_SOURCE_NONE = 0
LVBKIF_SOURCE_HBITMAP = 1
LVBKIF_SOURCE_URL = 2
LVBKIF_SOURCE_MASK = 3
LVBKIF_STYLE_NORMAL = 0
LVBKIF_STYLE_TILE = 16
LVBKIF_STYLE_MASK = 16
LVM_SETBKIMAGEA = (LVM_FIRST + 68)
LVM_SETBKIMAGEW = (LVM_FIRST + 138)
LVM_GETBKIMAGEA = (LVM_FIRST + 69)
LVM_GETBKIMAGEW = (LVM_FIRST + 139)
LVKF_ALT = 1
LVKF_CONTROL = 2
LVKF_SHIFT = 4

LVN_ITEMCHANGING = (LVN_FIRST-0)
LVN_ITEMCHANGED = (LVN_FIRST-1)
LVN_INSERTITEM = (LVN_FIRST-2)
LVN_DELETEITEM = (LVN_FIRST-3)
LVN_DELETEALLITEMS = (LVN_FIRST-4)
LVN_BEGINLABELEDITA = (LVN_FIRST-5)
LVN_BEGINLABELEDITW = (LVN_FIRST-75)
LVN_ENDLABELEDITA = (LVN_FIRST-6)
LVN_ENDLABELEDITW = (LVN_FIRST-76)
LVN_COLUMNCLICK = (LVN_FIRST-8)
LVN_BEGINDRAG = (LVN_FIRST-9)
LVN_BEGINRDRAG = (LVN_FIRST-11)
LVN_ODCACHEHINT = (LVN_FIRST-13)
LVN_ODFINDITEMA = (LVN_FIRST-52)
LVN_ODFINDITEMW = (LVN_FIRST-79)
LVN_ITEMACTIVATE = (LVN_FIRST-14)
LVN_ODSTATECHANGED = (LVN_FIRST-15)
LVN_ODFINDITEM = LVN_ODFINDITEMA
LVN_HOTTRACK = (LVN_FIRST-21)
LVN_GETDISPINFOA = (LVN_FIRST-50)
LVN_GETDISPINFOW = (LVN_FIRST-77)
LVN_SETDISPINFOA = (LVN_FIRST-51)
LVN_SETDISPINFOW = (LVN_FIRST-78)
LVN_BEGINLABELEDIT = LVN_BEGINLABELEDITA
LVN_ENDLABELEDIT = LVN_ENDLABELEDITA
LVN_GETDISPINFO = LVN_GETDISPINFOA
LVN_SETDISPINFO = LVN_SETDISPINFOA
LVIF_DI_SETITEM = 4096
LVN_KEYDOWN = (LVN_FIRST-55)
LVN_MARQUEEBEGIN = (LVN_FIRST-56)
LVGIT_UNFOLDED = 1
LVN_GETINFOTIPA = (LVN_FIRST-57)
LVN_GETINFOTIPW = (LVN_FIRST-58)
LVN_GETINFOTIP = LVN_GETINFOTIPA
# -endregion ListView Constants

# -region Header Constants
HDM_FIRST = 4608
HDN_FIRST = (UINT_MAX-300)
HDM_LAYOUT = (HDM_FIRST + 5)
HDM_HITTEST = (HDM_FIRST + 6)
HDM_GETITEMRECT = (HDM_FIRST + 7)
HDM_SETIMAGELIST = (HDM_FIRST + 8)
HDM_GETIMAGELIST = (HDM_FIRST + 9)
HDM_GETITEM = HDM_FIRST+11
HDM_ORDERTOINDEX = (HDM_FIRST + 15)
HDM_CREATEDRAGIMAGE = (HDM_FIRST + 16)  # wparam = which item (by index)
HDM_GETORDERARRAY = (HDM_FIRST + 17)
HDM_SETORDERARRAY = (HDM_FIRST + 18)
HDM_SETHOTDIVIDER = (HDM_FIRST + 19)
HDM_GETFOCUSEDITEM = HDM_FIRST+27
HDM_SETUNICODEFORMAT = CCM_SETUNICODEFORMAT
HDM_GETUNICODEFORMAT = CCM_GETUNICODEFORMAT
HDN_ITEMCHANGINGA = (HDN_FIRST-0)
HDN_ITEMCHANGINGW = (HDN_FIRST-20)
HDN_ITEMCHANGEDA = (HDN_FIRST-1)
HDN_ITEMCHANGEDW = (HDN_FIRST-21)
HDN_ITEMCLICKA = (HDN_FIRST-2)
HDN_ITEMCLICKW = (HDN_FIRST-22)
HDN_ITEMDBLCLICKA = (HDN_FIRST-3)
HDN_ITEMDBLCLICKW = (HDN_FIRST-23)
HDN_DIVIDERDBLCLICKA = (HDN_FIRST-5)
HDN_DIVIDERDBLCLICKW = (HDN_FIRST-25)
HDN_BEGINTRACKA = (HDN_FIRST-6)
HDN_BEGINTRACKW = (HDN_FIRST-26)
HDN_ENDTRACKA = (HDN_FIRST-7)
HDN_ENDTRACKW = (HDN_FIRST-27)
HDN_TRACKA = (HDN_FIRST-8)
HDN_TRACKW = (HDN_FIRST-28)
HDN_GETDISPINFOA = (HDN_FIRST-9)
HDN_GETDISPINFOW = (HDN_FIRST-29)
HDN_BEGINDRAG = (HDN_FIRST-10)
HDN_ENDDRAG = (HDN_FIRST-11)
HDN_ITEMCHANGING = HDN_ITEMCHANGINGA
HDN_ITEMCHANGED = HDN_ITEMCHANGEDA
HDN_ITEMCLICK = HDN_ITEMCLICKA
HDN_ITEMDBLCLICK = HDN_ITEMDBLCLICKA
HDN_DIVIDERDBLCLICK = HDN_DIVIDERDBLCLICKA
HDN_BEGINTRACK = HDN_BEGINTRACKA
HDN_ENDTRACK = HDN_ENDTRACKA
HDN_TRACK = HDN_TRACKA
HDN_GETDISPINFO = HDN_GETDISPINFOA
HHT_ONHEADER = 0x0002
# -endregion Header Constants







# -region Windowm Messages
WM_NULL = 0
WM_CREATE = 1
WM_DESTROY = 2
WM_MOVE = 3
WM_SIZE = 5
WM_ACTIVATE = 6
WA_INACTIVE = 0
WA_ACTIVE = 1
WA_CLICKACTIVE = 2
WM_SETFOCUS = 7
WM_KILLFOCUS = 8
WM_ENABLE = 10
WM_SETREDRAW = 11
WM_SETTEXT = 12
WM_GETTEXT = 13
WM_GETTEXTLENGTH = 14
WM_PAINT = 15
WM_CLOSE = 16
WM_QUERYENDSESSION = 17
WM_QUIT = 18
WM_QUERYOPEN = 19
WM_ERASEBKGND = 20
WM_SYSCOLORCHANGE = 21
WM_ENDSESSION = 22
WM_SHOWWINDOW = 24
WM_WININICHANGE = 26
WM_SETTINGCHANGE = WM_WININICHANGE
WM_DEVMODECHANGE = 27
WM_ACTIVATEAPP = 28
WM_FONTCHANGE = 29
WM_TIMECHANGE = 30
WM_CANCELMODE = 31
WM_SETCURSOR = 32
WM_MOUSEACTIVATE = 33
WM_CHILDACTIVATE = 34
WM_QUEUESYNC = 35
WM_GETMINMAXINFO = 36
WM_PAINTICON = 38
WM_ICONERASEBKGND = 39
WM_NEXTDLGCTL = 40
WM_SPOOLERSTATUS = 42
WM_DRAWITEM = 43
WM_MEASUREITEM = 44
WM_DELETEITEM = 45
WM_VKEYTOITEM = 46
WM_CHARTOITEM = 47
WM_SETFONT = 48
WM_GETFONT = 49
WM_SETHOTKEY = 50
WM_GETHOTKEY = 51
WM_QUERYDRAGICON = 55
WM_COMPAREITEM = 57
WM_GETOBJECT = 61
WM_COMPACTING = 65
WM_COMMNOTIFY = 68
WM_WINDOWPOSCHANGING = 70
WM_WINDOWPOSCHANGED = 71
WM_POWER = 72
PWR_OK = 1
PWR_FAIL = -1
PWR_SUSPENDREQUEST = 1
PWR_SUSPENDRESUME = 2
PWR_CRITICALRESUME = 3
WM_COPYDATA = 74
WM_CANCELJOURNAL = 75
WM_NOTIFY = 78
WM_INPUTLANGCHANGEREQUEST = 80
WM_INPUTLANGCHANGE = 81
WM_TCARD = 82
WM_HELP = 83
WM_USERCHANGED = 84
WM_NOTIFYFORMAT = 85
NFR_ANSI = 1
NFR_UNICODE = 2
NF_QUERY = 3
NF_REQUERY = 4
WM_CONTEXTMENU = 123
WM_STYLECHANGING = 124
WM_STYLECHANGED = 125
WM_DISPLAYCHANGE = 126
WM_GETICON = 127
WM_SETICON = 128
WM_NCCREATE = 129
WM_NCDESTROY = 130
WM_NCCALCSIZE = 131
WM_NCHITTEST = 132
WM_NCPAINT = 133
WM_NCACTIVATE = 134
WM_GETDLGCODE = 135
WM_SYNCPAINT = 136
WM_NCMOUSEMOVE = 160
WM_NCLBUTTONDOWN = 161
WM_NCLBUTTONUP = 162
WM_NCLBUTTon_double_click = 163
WM_NCRBUTTONDOWN = 164
WM_NCRBUTTONUP = 165
WM_NCRBUTTon_double_click = 166
WM_NCMBUTTONDOWN = 167
WM_NCMBUTTONUP = 168
WM_NCMBUTTon_double_click = 169
WM_KEYFIRST = 256
WM_KEYDOWN = 256
WM_KEYUP = 257
WM_CHAR = 258
WM_DEADCHAR = 259
WM_SYSKEYDOWN = 260
WM_SYSKEYUP = 261
WM_SYSCHAR = 262
WM_SYSDEADCHAR = 263
WM_KEYLAST = 264
WM_IME_STARTCOMPOSITION = 269
WM_IME_ENDCOMPOSITION = 270
WM_IME_COMPOSITION = 271
WM_IME_KEYLAST = 271
WM_INITDIALOG = 272
WM_COMMAND = 273
WM_SYSCOMMAND = 274
WM_TIMER = 275
WM_HSCROLL = 276
WM_VSCROLL = 277
WM_INITMENU = 278
WM_INITMENUPOPUP = 279
WM_MENUSELECT = 287
WM_MENUCHAR = 288
WM_ENTERIDLE = 289
WM_MENURBUTTONUP = 290
WM_MENUDRAG = 291
WM_MENUGETOBJECT = 292
WM_UNINITMENUPOPUP = 293
WM_MENUCOMMAND = 294
WM_CTLCOLORMSGBOX = 306
WM_CTLCOLOREDIT = 307
WM_CTLCOLORLISTBOX = 308
WM_CTLCOLORBTN = 309
WM_CTLCOLORDLG = 310
WM_CTLCOLORSCROLLBAR = 311
WM_CTLCOLORSTATIC = 312
WM_MOUSEFIRST = 512
WM_MOUSEMOVE = 512
WM_LBUTTONDOWN = 513
WM_LBUTTONUP = 514
WM_LBUTTon_double_click = 515
WM_RBUTTONDOWN = 516
WM_RBUTTONUP = 517
WM_RBUTTon_double_click = 518
WM_MBUTTONDOWN = 519
WM_MBUTTONUP = 520
WM_MBUTTon_double_click = 521
WM_MOUSEWHEEL = 522
WM_MOUSELAST = 522
WHEEL_DELTA = 120  # Value for rolling one detent
WHEEL_PAGESCROLL = -1  # Scroll one page
WM_PARENTNOTIFY = 528
MENULOOP_WINDOW = 0
MENULOOP_POPUP = 1
WM_ENTERMENULOOP = 529
WM_EXITMENULOOP = 530
WM_NEXTMENU = 531
WM_SIZING = 532
WM_CAPTURECHANGED = 533
WM_MOVING = 534
WM_POWERBROADCAST = 536

WM_DEVICECHANGE = 537
WM_MDICREATE = 544
WM_MDIDESTROY = 545
WM_MDIACTIVATE = 546
WM_MDIRESTORE = 547
WM_MDINEXT = 548
WM_MDIMAXIMIZE = 549
WM_MDITILE = 550
WM_MDICASCADE = 551
WM_MDIICONARRANGE = 552
WM_MDIGETACTIVE = 553
WM_MDISETMENU = 560
WM_ENTERSIZEMOVE = 561
WM_EXITSIZEMOVE = 562
WM_DROPFILES = 563
WM_MDIREFRESHMENU = 564
WM_IME_SETCONTEXT = 641
WM_IME_NOTIFY = 642
WM_IME_CONTROL = 643
WM_IME_COMPOSITIONFULL = 644
WM_IME_SELECT = 645
WM_IME_CHAR = 646
WM_IME_REQUEST = 648
WM_IME_KEYDOWN = 656
WM_IME_KEYUP = 657
WM_MOUSEHOVER = 673
WM_MOUSELEAVE = 675
WM_CUT = 768
WM_COPY = 769
WM_PASTE = 770
WM_CLEAR = 771
WM_UNDO = 772
WM_RENDERFORMAT = 773
WM_RENDERALLFORMATS = 774
WM_DESTROYCLIPBOARD = 775
WM_DRAWCLIPBOARD = 776
WM_PAINTCLIPBOARD = 777
WM_VSCROLLCLIPBOARD = 778
WM_SIZECLIPBOARD = 779
WM_ASKCBFORMATNAME = 780
WM_CHANGECBCHAIN = 781
WM_HSCROLLCLIPBOARD = 782
WM_QUERYNEWPALETTE = 783
WM_PALETTEISCHANGING = 784
WM_PALETTECHANGED = 785
WM_HOTKEY = 786
WM_PRINT = 791
WM_PRINTCLIENT = 792
WM_HANDHELDFIRST = 856
WM_HANDHELDLAST = 863
WM_AFXFIRST = 864
WM_AFXLAST = 895
WM_PENWINFIRST = 896
WM_PENWINLAST = 911
WM_APP = 32768
WM_SETFONT = 48
WM_GETFONT = 49
WM_SETHOTKEY = 50
WM_GETHOTKEY = 51
WM_POINTERUPDATE = 0x0245
WM_POINTERDOWN = 0x0246
WM_POINTERUP = 0x0247
WM_POINTERENTER = 0x0249
WM_POINTERLEAVE = 0x024A
WM_POINTERACTIVATE = 0x024B
WM_POINTERCAPTURECHANGED = 0x024C
WM_TOUCHHITTESTING = 0x024D
WM_POINTERWHEEL = 0x024E
WM_POINTERHWHEEL = 0x024F
DM_POINTERHITTEST = 0x0250
WM_POINTERROUTEDTO = 0x0251
WM_POINTERROUTEDAWAY = 0x0252
WM_POINTERROUTEDRELEASED = 0x0253
WM_NCPOINTERUPDATE = 0x0241
WM_NCPOINTERDOWN = 0x0242
WM_NCPOINTERUP = 0x0243


# -endregion Windowm Messages



