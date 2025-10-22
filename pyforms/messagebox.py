

# messagebox module - Created on 12-Dec-2022 19:40:20
from ctypes import windll
from ctypes.wintypes import HWND, LPCWSTR, UINT, INT
from enum import Enum

MessageBox = windll.user32.MessageBoxW
MessageBox.argtypes = [HWND, LPCWSTR, LPCWSTR, UINT]
MessageBox.restype = INT
pft = "PyForms Message"
class MessageButtons(Enum):
	OKAY = 0x00000000
	OKAY_CANCEL = 0x00000001
	ABORT_RETRY_IGNORE = 0x00000002
	YES_NO_CANCEL = 0x00000003
	YES_NO = 0x00000004
	RETRY_CANCEL = 0x00000005
	CANCEL_TRY_CONTINUE = 0x00000006

class MessageIcons(Enum):
	NONE = 0x0
	ERROR = 0x00000010
	QUESTION = 0x00000020
	WARNING = 0x00000030
	INFORMATION = 0x00000040

class MessageResult(Enum):
	OKAY = 1
	CANCEL = 2
	ABORT = 3
	RETRY = 4
	IGNORE = 5
	YES = 6
	NO = 7
	TRY_AGAIN = 10
	CONTINUE = 11



def msgbox(msg, title=pft, 
			btns: MessageButtons = MessageButtons.OKAY,
			icon: MessageIcons = MessageIcons.NONE ):
	return MessageBox(0, msg, title, btns.value | icon.value)
