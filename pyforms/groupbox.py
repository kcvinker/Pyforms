# Created on 20-Jan-2023 07:49:20

from ctypes import byref
from pyforms.control import Control
import pyforms.constants as con
from pyforms.commons import MyMessages, Font
from pyforms.enums import ControlType, GroupBoxStyle, FontWeight
from pyforms.apis import SUBCLASSPROC
import pyforms.apis as api
from pyforms.colors import Color, COLOR_BLACK
# from horology import Timing
# from .winmsgs import log_msg

gbDict = {}
penWidth = 4
EMPTY_WCHAR = '\0'
gbStyle = con.BS_GROUPBOX|con.BS_NOTIFY|con.BS_TOP|con.WS_OVERLAPPED|con.WS_CLIPCHILDREN|con.WS_CLIPSIBLINGS
gbExStyle = con.WS_EX_RIGHTSCROLLBAR| con.WS_EX_CONTROLPARENT

class GroupBox(Control):

    _count = 1
    __slots__ = ("_pen", "_tmpTxt", "_rect", "_txtWidth", "_gstyle", "_dbFill", 
                 "_getWidth", "_themeOff", "_hdc", "_hbmp" )
    def __init__(self, parent, txt: str = "", xpos: int = 10, 
                 ypos: int = 10, width: int = 300, height: int = 300 ) -> None:
        super().__init__(parent, ControlType.GROUP_BOX, width, height)
        self.name = f"GroupBox_{GroupBox._count}"
        self._text = self.name if txt == "" else txt
        self._gstyle = GroupBoxStyle.SYSTEM
        self._dbFill = True
        self._getWidth = True
        self._themeOff = False
        self._hdc = None
        self._hbmp = None
        self._pen = None
        self._xpos = xpos
        self._ypos = ypos
        self._isTextable = True
        self._style |= gbStyle
        self._exStyle = gbExStyle
        self._drawFlag = 0
        self._txtWidth = 0
        self._bgColor = Color(parent._bgColor)
        parent._controls.append(self)
        GroupBox._count += 1
        if parent.createChilds: self.createHandle()


    # -region Public funcs
    def createHandle(self):
        self._bkgBrush = self._bgColor.createHBrush()
        if self._gstyle == GroupBoxStyle.OVERRIDEN:
            self._pen = self._bgColor.createHPen(pWidth=penWidth)

        self._rect = api.RECT(0, 0, self._width, self._height)
        self._createControl()
        if self._hwnd:
            gbDict[self._hwnd] = self
            if self._gstyle == GroupBoxStyle.CLASSIC:
                api.SetWindowTheme(self._handle, EMPTY_WCHAR, EMPTY_WCHAR)
                self._themeOff = True

            self._setSubclass(gbWndProc)
            self._setFontInternal()
            # print(f"group bgc {self._bgColor.value:X}")

    @Control.backColor.setter
    def backColor(self, value):
        """Set the back color of group box"""
        self._bgColor = Color(value) if isinstance(value, int) else value
        self.resetGdiObjects(True)
        self._manageRedraw()

    @Control.foreColor.setter
    def foreColor(self, value):
        # If drawing style is system, it will change to classic.
        # Because, system style doesn't support changing fore color.
        """Set the fore color of froup box"""
        self._fgColor = Color(value) if isinstance(value, int) else value
        if self._gstyle == GroupBoxStyle.SYSTEM:
            self._gstyle = GroupBoxStyle.CLASSIC
        if self._gstyle == GroupBoxStyle.CLASSIC:
            if not self._themeOff:
                api.SetWindowTheme(self._hwnd, EMPTY_WCHAR, EMPTY_WCHAR)
                self._themeOff = True
            #-------------------
        if self._gstyle == GroupBoxStyle.OVERRIDEN:
            self._getWidth = True
            if self._pen == None:
                self._pen = api.CreatePen(con.PS_SOLID, penWidth, self._bgColor.ref)
        self._manageRedraw()

    # An extra function to set fore color. It gives the opprtunity to...
    # set the drawing style of GroupBox. Default is classic. But you...
    # can choose overriden too. System style doesn't support fore color.
    def setForeColor(self, clr, style = GroupBoxStyle.CLASSIC):
        """Set fore color with drawing style"""
        self._fgColor = Color(clr) if isinstance(clr, int) else clr
        self._gstyle = style
        if self._gstyle == GroupBoxStyle.CLASSIC:
            api.SetWindowTheme(self._handle, EMPTY_WCHAR, EMPTY_WCHAR)
            self._themeOff = True

        if self._gstyle == GroupBoxStyle.OVERRIDEN:
            self._getWidth = True
            if self._pen == None:
                self._pen = self._bgColor.createHPen(pWidth=penWidth)
        self._manageRedraw()

    # An extra function to set Font. This function provides...
    # some another font options. 
    def changeFont(self, fname, fsize, fweight = FontWeight.NORMAL):  
        """Change font and font related info"""      
        self._font = Font(fname, fsize, fweight)
        self._font.createHandle()
        self.sndMsg(con.WM_SETFONT, self._font._handle, 1)
        self._getWidth = True
        self._manageRedraw()
    

    @Control.text.setter
    def text(self, value):
        """Set text for group box"""
        self._text = value
        self._getWidth = True
        api.SetWindowText(self._hwnd, value)
        self._manageRedraw()

    @Control.width.setter
    def width(self, value):
        """Set group box width"""
        self._width = value
        self.resetGdiObjects(False)
        if self._isCreated:
            self.setPosInternal()

    @Control.height.setter
    def height(self, value):
        """Set group box height"""
        self._height = value
        self.resetGdiObjects(False)
        if self._isCreated:
            self.setPosInternal()

    @Control.font.setter
    def font(self, value):
        """Set group box font"""
        self._font.colneFrom(value)
        if value._handle == 0:
            self._font.createHandle()
        self.sendMsg(con.WM_SETFONT, self._font._handle, 1)
        self._getWidth = True
        self._manageRedraw()

    def style(self, value: GroupBoxStyle):
        """Set group box drawing style, options-(system, classic, overriden)"""
        self._gstyle = value
        if value == GroupBoxStyle.CLASSIC:
            if not self._themeOff:
                # self._gstyle = GroupBoxStyle.CLASSIC
                api.SetWindowTheme(self._handle, EMPTY_WCHAR, EMPTY_WCHAR)
                self._themeOff = True

        if value == GroupBoxStyle.OVERRIDEN:
            self._getWidth = True
            if self._pen == None: 
                self._pen = api.CreatePen(con.PS_SOLID, penWidth, self._bgColor.ref)
        #----------------------------------------------------------
        if self._isCreated: 
            api.InvalidateRect(self._handle, None, 0)

    # -endregion Public funcs

    def resetGdiObjects(self, brpn):
        # brpn = Reset Hbrush and Hpen
        if brpn:
            if self._bkgBrush != None: 
                api.DeleteObject(self._bkgBrush)        
            self._bkgBrush = api.CreateSolidBrush(self._bgColor.ref)
            if self._gstyle == GroupBoxStyle.OVERRIDEN:
                if self._pen != None: 
                    api.DeleteObject(self._pen)
                self._pen = api.CreatePen(con.PS_SOLID, penWidth, self._bgColor.ref)
        #------------------------------------------------
        if self._hdc != None: 
            api.DeleteDC(self._hdc)
        if self._hbmp != None: 
            api.DeleteObject(self._hbmp)    
        self._dbFill = True


    def _draw_text(self):
        # To change the fore color, we need to draw the...
        # text on our own. Before drawing text, we need to hide...
        # the outline of group box. So we are drawing a line...
        # with back color over the existing line.
        hdc = api.GetDC(self._hwnd)
        api.SelectObject(hdc, self._pen)
        api.MoveToEx(hdc, 10, 10, None)
        api.LineTo(hdc, self._txtWidth, 10)

        # Now, we can draw the text with our color & font.
        api.SetBkMode(hdc, con.TRANSPARENT)
        api.SelectObject(hdc, self._font._handle)
        api.SetTextColor(hdc, self._fgColor.ref)
        api.TextOut(hdc, 10, 0, self._text, len(self._text))
        api.ReleaseDC(self._hwnd, hdc)

    def _setBackColorFromParent(self, clr):
        if self._drawFlag & 2 != 2: self._drawFlag += 2
        self._bgColor = clr
        self._bkgBrush = self._bgColor.createHBrush()
        self._pen = self._bgColor.createHPen()

    def handleWmEraseBKG(self, wp):
        if self._getWidth:
            # We need to get the text width.
            size = api.SIZE()
            api.SelectObject(wp, self._font._handle)
            api.GetTextExtentPoint32(wp, self._text, len(self._text), byref(size))
            self._txtWidth = size.cx + 10
            self._getWidth = False  
        #------------------------------
        if self._dbFill:
            # DC changed, we need to draw new background.
            self._hdc = api.CreateCompatibleDC(wp)
            self._hbmp = api.CreateCompatibleBitmap(wp, self._width, self._height)
            api.SelectObject(self._hdc, self._hbmp)
            api.FillRect(self._hdc, byref(self._rect), self._bkgBrush)
            self._dbFill = False
        #------------------------------------
        api.BitBlt(wp, 0, 0, self._width, self._height, self._hdc, 0, 0, con.SRCCOPY)
        return 1 

    def finalize(self):
        if self._pen != None: 
            api.DeleteObject(self._pen)
        if self._hdc != None: 
            api. DeleteDC(self._hdc)
        if self._hbmp != None: 
            api.DeleteObject(self._hbmp)
    # -endregion Private funcs

    # -region Properties


    # @property
    # def multi_line(self): return self._multi_line

    # @multi_line.setter
    # def multi_line(self, value: bool): self._multi_line = value

    # @property
    # def text_align(self): return self._txt_align

    # @text_align.setter
    # def text_align(self, value: TextAlignment): self._txt_align = value

    # @property
    # def border_style(self): return self._border_style

    # @border_style.setter
    # def border_style(self, value: GroupBoxBorder): self._border_style = value

    # -endregion Properties

#End GroupBox

# @WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR)
@SUBCLASSPROC
def gbWndProc(hw, msg, wp, lp, scID, refData):
    # printWinMsg(msg)
    # log_msg(msg)
    match msg:
        case con.WM_DESTROY:
            gb = gbDict[hw]
            api.RemoveWindowSubclass(hw, gbWndProc, scID)
            gb.finalize()
            del gbDict[hw]

        case con.WM_SETFOCUS: 
            gb = gbDict[hw]
            gb._gotFocusHandler()
        case con.WM_KILLFOCUS: 
            gb = gbDict[hw]
            gb._lostFocusHandler()
        case con.WM_LBUTTONDOWN: 
            gb = gbDict[hw]
            gb._leftMouseDownHandler(msg, wp, lp)
        case con.WM_LBUTTONUP: 
            gb = gbDict[hw]
            gb._leftMouseUpHandler(msg, wp, lp)
        case con.WM_RBUTTONDOWN: 
            gb = gbDict[hw]
            gb._rightMouseDownHandler(msg, wp, lp)
        case con.WM_RBUTTONUP: 
            gb = gbDict[hw]
            gb._rightMouseUpHandler(msg, wp, lp)
        case con.WM_MOUSEWHEEL: 
            gb = gbDict[hw]
            gb._mouseWheenHandler(msg, wp, lp)
        case con.WM_MOUSEMOVE: 
            gb = gbDict[hw]
            gb._mouseMoveHandler(msg, wp, lp)
        case con.WM_MOUSELEAVE: 
            gb = gbDict[hw]
            gb._mouseLeaveHandler()
        case con.WM_ERASEBKGND:
            gb = gbDict[hw]
            return gb.handleWmEraseBKG(wp)
            # if gb._drawFlag:
            #     rc = api.get_client_rect(hw)
            #     api.FillRect(wp, byref(rc), gb._bkgBrush)
            #     return 1
            # NOTE: Do not return anything outside the 'if', as it will make every static control a mess.
        
        case MyMessages.LABEL_COLOR:
            gb = gbDict[hw]
            if gb._gstyle == GroupBoxStyle.CLASSIC:
                api.SetBkMode(wp, 1)
                # SelectObject(wp, cast[HGDIOBJ](gb.mFont.handle))
                api.SetTextColor(wp, gb._fgColor.ref)        
        
            return gb._bkgBrush

        case con.WM_PAINT:
            gb = gbDict[hw]
            if gb._gstyle == GroupBoxStyle.OVERRIDEN:
                # Let the control do it's painting works.
                ret = api.DefSubclassProc(hw, msg, wp, lp)

                # Now, we can draw the text over this group box.
                gb._draw_text()
                return ret

        case con.WM_GETTEXTLENGTH: 
            gb = gbDict[hw]
            if gb._gstyle == GroupBoxStyle.OVERRIDEN:
                return 0

    return api.DefSubclassProc(hw, msg, wp, lp)

