# Created on 09-Nov-2022 12:15:29
from enum import IntEnum

class FormPosition(IntEnum):
    CENTER = 0
    TOP_LEFT = 1
    TOP_MID = 2
    TOP_RIGHT = 3
    MID_LEFT = 4
    MID_RIGHT = 5
    BOTTOM_LEFT = 6
    BOTTOM_MID = 7
    BOTTOM_RIGHT = 8
    MANUAL = 9

class ControlType(IntEnum):
    NONE = 0
    BUTTON = 1
    CALENDAR_BOX = 2
    CHECK_BOX = 3
    COMBO_BOX = 4
    DATE_TIME_PICKER = 5
    GROUP_BOX = 6
    HEADER = 7
    LABEL = 8
    LIST_BOX = 9
    LIST_VIEW = 10
    NUM_PICKER = 11
    PROGRESS_BAR = 12
    RADIO_BUTTON = 13
    TEXT_BOX = 14
    TRACK_BAR = 15
    TREE_VIEW = 16


class FormStyle(IntEnum):
    NONE = 0
    FIXED_SINGLE = 1
    FIXED_3D = 2
    FIXED_DIALOG = 3
    FIXED_TOOL = 4
    SIZABLE = 5
    SIZABLE_TOOL = 6
    HIDDEN = 7


class FormState(IntEnum):
    NORMAL = 0
    MAXIMIZED = 1
    MINIMIZED = 2

class FontWeight(IntEnum):
    THIN = 100
    EXTRA_LIGHT = 200
    LIGHT = 300
    NORMAL = 400
    MEDIUM = 500
    SEMI_BOLD = 600
    BOLD = 700
    EXTRA_BOLD = 800
    THICK = 900

class GroupBoxStyle(IntEnum):
    SYSTEM = 0
    CLASSIC = 1
    OVERRIDEN = 2

class HeaderItemState(IntEnum):
    NONE = 0
    USE_DEF_ITEMS = 1

class HeaderStyle(IntEnum):
    FLAT = 0
    CURVED = 1

class MouseButton(IntEnum):
    NONE = 0
    RIGHT = 20_97_152
    MIDDLE = 41_94_304
    LEFT = 10_48_576
    XBUTTON1 = 83_88_608
    XBUTTON2 = 167_77_216

class MouseButtonState(IntEnum):
    RELEASED = 0
    PRESSED = 1

class SizedPositions(IntEnum):
    LEFT_EDGE = 1
    RIGHT_EDGE = 2
    TOP_EDGE = 3
    TOP_LEFT_CORNER = 4
    TOP_RIGHT_CORNER = 5
    BOTTOM_EDGE = 6
    BOTTOM_LEFT_CORNER = 7
    BOTTOM_RIGHT_CORNER = 8

class FormDrawMode(IntEnum):
    NORMAL = 0
    COLORED = 1
    GRADIENT = 2

class ButtonDrawMode(IntEnum):
    NORMAL = 0
    TEXT_ONLY = 1
    BKG_ONLY = 2
    TEXT_BKG = 3
    GRADIENT = 4
    GRADIENT_TEXT = 5

class TextCase(IntEnum):
    NORMAL = 0
    LOWER = 1
    UPPER = 2

class TextType(IntEnum):
    NORMAL = 0
    NUM_ONLY = 1
    PASSWORD = 2

class TextAlignment(IntEnum): # For TextBox
    LEFT = 0
    CENTER = 1
    RIGHT = 2

class ControlDrawMode(IntEnum):
    NO_DRAW = 0
    FG_DRAW = 1
    BG_DRAW = 2
    BOTH_DRAW = 3


class LabelBorder(IntEnum):
    NONE = 0
    SINGLE = 1
    SUNKEN = 2


class LabelAlignment(IntEnum):
    TOPLEFT = 0
    TOPCENTER = 1
    TOPRIGHT = 2
    MIDLEFT = 3
    CENTER  = 4
    MIDRIGHT = 5
    BOTTOMLEFT = 6
    BOTTOMCENTER = 7
    BOTTOMRIGHT = 8

class ViewMode(IntEnum): # For CalendarBox
    MONTH_VIEW = 0
    YEAR_VIEW = 1
    DECADE_VIEW = 2
    CENTUARY_VIEW = 3

class DateFormat(IntEnum): # For DateTimePicker
    LONG_DATE = 1
    SHORT_DATE = 2
    TIME_ONLY = 4
    CUSTOM_DATE = 8

class TickPosition(IntEnum): # For TrackBar
    DOWN = 1
    UP = 2
    LEFT = 3
    RIGHT = 4
    BOTH = 5

class ChannelStyle(IntEnum):
    DEFAULT = 0
    CLASSIC = 1
    OUTLINE = 2

class TrackChange(IntEnum):
    NONE = 0
    ARROW_LOW = 1
    ARROW_HIGH = 2
    PAGE_LOW = 3
    PAGE_HIGH = 4
    MOUSE_CLICK = 5
    MOUSE_DRAG = 6

class TrayMenuTrigger(IntEnum):
    NONE = 0
    LEFT_CLICK = 1
    LEFT_DBLCLICK = 2
    RIGHT_CLICK = 4
    ANY_CLICK = 7

class BalloonIcon(IntEnum):
    NONE = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CUSTOM = 4

class ListViewStyle(IntEnum):
    LARGE_ICON = 0
    REPORT_VIEW = 1
    SMALL_ICON = 2
    LIST_VIEW = 3
    TILE_VIEW = 4

class NodeOp(IntEnum): # Used in TreeView
    ADD_NODE = 0
    INSERT_NODE = 1
    ADD_CHILD = 2
    INSERT_CHILD = 3

class ProgressBarStyle(IntEnum):
    BLOCK_STYLE = 0
    MARQUEE_STYLE = 1

class ProgressBarState(IntEnum):
    NORMAL = 1
    ERROR = 2
    PAUSED = 3

class MenuStyle(IntEnum):
    SYSTEM = 0
    CUSTOM = 1
    



class MessageButtons(IntEnum):
	OKAY = 0x00000000
	OKAY_CANCEL = 0x00000001
	ABORT_RETRY_IGNORE = 0x00000002
	YES_NO_CANCEL = 0x00000003
	YES_NO = 0x00000004
	RETRY_CANCEL = 0x00000005
	CANCEL_TRY_CONTINUE = 0x00000006

class MessageIcons(IntEnum):
	NONE = 0x0
	ERROR = 0x00000010
	QUESTION = 0x00000020
	WARNING = 0x00000030
	INFORMATION = 0x00000040

class MessageResult(IntEnum):
	OKAY = 1
	CANCEL = 2
	ABORT = 3
	RETRY = 4
	IGNORE = 5
	YES = 6
	NO = 7
	TRY_AGAIN = 10
	CONTINUE = 11



class Keys(IntEnum):
    MODIFIER = -65_536
    NONE = 0
    LBUTTON = 1
    RBUTTON = 2
    CANCEL = 3
    MBUTTON = 4
    XBUTTO1 = 5
    XBUTTON2 = 6
    BACK_SPACE = 8
    TAB = 9
    LINE_FEED = 10
    CLEAR = 12
    ENTER = 13
    SHIFT = 16
    CTRL = 17
    ALT = 18
    PAUSE = 19
    CAPS_LOCK = 20
    ESCAPE = 27
    SPACE = 32
    PAGE_UP = 33
    PAGE_DOWN = 34
    END = 35
    HOME = 36
    LEFTA_RROW = 37
    UP_ARROW = 38
    RIGHT_ARROW = 39
    DOWN_ARROW = 39
    SELECT = 40
    PRINT = 41
    EXECUTE = 42
    PRINT_SCREEN = 43
    INSERT = 44
    DEL = 45
    HELP = 46
    D0 = 47
    D1 = 48
    D2 = 49
    D3 = 50
    D4 = 51
    D5 = 52
    D6 = 53
    D7 = 54
    D8 = 55
    D9 = 56
    A = 65
    B = 66
    C = 67
    D = 68
    E = 69
    F = 70
    G = 71
    H = 72
    I = 73
    J = 74
    K = 75
    L = 76
    M = 77
    N = 78
    O = 79
    P = 80
    Q = 81
    R = 82
    S = 83
    T = 84
    U = 85
    V = 86
    W = 87
    X = 88
    Y = 89
    Z = 90
    LEFT_WIN = 91
    RIGH_TWIN = 92
    APPS = 93
    SLEEP = 95
    NUM_PAD0 = 96
    NUM_PAD1 = 97
    NUM_PAD2 = 98
    NUM_PAD3 = 99
    NUM_PAD4 = 100
    NUM_PAD5 = 101
    NUM_PAD6 = 102
    NUM_PAD7 = 103
    NUM_PAD8 = 104
    NUM_PAD9 = 105
    MULTIPLY = 106
    ADD = 107
    SEPERATOR = 108
    SUBTRACT = 109
    DECIMAL = 110
    DIVIDE = 111
    F1 = 112
    F2 = 113
    F3 = 114
    F4 = 115
    F5 = 116
    F6 = 117
    F7 = 118
    F8 = 119
    F9 = 120
    F10 = 121
    F11 = 122
    F12 = 123
    F13 = 124
    F14 = 125
    F15 = 126
    F16 = 157
    F17 = 128
    F18 = 129
    F19 = 130
    F20 = 131
    F21 = 132
    F22 = 133
    F23 = 134
    F24 = 135
    NUM_LOCK = 144
    SCROLL = 145
    LEFT_SHIFT = 160
    RIGHT_SHIFT = 161
    LEFT_CTRL = 162
    RIGHT_CTRL = 163
    LEFT_MENU = 164
    RIGHT_MENU = 165
    BROWSER_BACK = 166
    BROWSER_FORWARD = 167
    BROWER_REFRESH = 168
    BROWSER_STOP = 169
    BROWSER_SEARCH = 170
    BROWSER_FAVORITES = 171
    BROWSER_HOME = 172
    VOLUME_MUTE = 173
    VOLUME_DOWN = 174
    VOLUME_UP = 175
    MEDIA_NEXT_TRACK = 176
    MEDIA_PRE_VTRACK = 177
    MEDIA_STOP = 178
    MEDIA_PLAY_PAUSE = 179
    LAUNCH_MAIL = 180
    SELECT_MEDIA = 181
    LAUNCH_APP1 = 182
    LAUNCH_APP2 = 183
    OEM1 = 186
    OEM_PLUS = 187
    OEM_COMMA = 188
    OEM_MINUS = 188
    OEM_PERIOD = 189
    OEM_QUESTION = 190
    OEM_TILDE = 191
    OEM_OPEN_BRACKET = 219
    OEM_PIPE = 220
    OEM_CLOSE_BRACKET = 221
    OEM_QUOTES = 222
    OEM8 = 223
    OEM_BACK_SLASH = 226
    PROCESS = 229
    PACKET = 231
    ATTN = 246
    CRSEL = 247
    EXSEL = 248
    ERASE_EOF = 249
    PLAY = 250
    ZOOM = 251
    NONAME = 252
    PA1 = 253
    OEM_CLEAR = 254
    KEY_CODE = 65_535
    SHIFT_MODIFIER = 65_536
    CTRL_MODIFIER = 131_072
    ALT_MODIFIER = 262_144
