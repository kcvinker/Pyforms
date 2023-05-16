
# Dialogs module - Created on 14-May-2023 16:55

from . apis import OPENFILENAMEW, BROWSEINFOW, GetOpenFileName, GetSaveFileName, SHBrowseForFolder, SHGetPathFromIDList, CoTaskMemFree
from ctypes import create_unicode_buffer, sizeof, byref, c_wchar_p, cast

MAX_PATH = 260
OFN_ALLOWMULTISELECT = 0x200
OFN_PATHMUSTEXIST = 0x800
OFN_FILEMUSTEXIST = 0x1000
OFN_FORCESHOWHIDDEN = 0x10000000
OFN_OVERWRITEPROMPT = 0x2
BIF_RETURNONLYFSDIRS = 0x00000001
BIF_NEWDIALOGSTYLE = 0x00000040
BIF_EDITBOX = 0x00000010
BIF_NONEWFOLDERBUTTON = 0x00000200
BIF_BROWSEINCLUDEFILES = 0x00004000
# BIF_UAHINT = 0x00000100


class DialogBase:
    def __init__(self, title, initD, filterStr = None) -> None:
        self._title = title
        self._initDir = initD
        self._filter = filterStr
        self._fileNameStart = 0
        self._extStart = 0
        self._selPath = ""

    @property
    def title(self): return self._title

    @title.setter
    def title(self, value: str): self._title = value
    #---------------------------------------------------------

    @property
    def initialFolder(self): return self._initDir

    @initialFolder.setter
    def initialFolder(self, value: str): self._initDir = value
    #---------------------------------------------------------

    @property
    def filter(self): return self._filter

    @filter.setter
    def filter(self, value: str): self._filter = value
    #---------------------------------------------------------

    @property
    def fileNameStartPos(self): return self._fileNameStart

    @property
    def extensionStartPos(self): return self._extStart

    @property
    def selectedFile(self): return self._selPath



class FileOpenDialog(DialogBase):
    def __init__(self, title = "Open File", initDir = "", filterStr = "All files\0*.*\0") -> None:
        super().__init__(title, initDir, filterStr)
        self._multiSel = False
        self._showHidden = False

    def showDialog(self, hwnd = None):
        ofn = OPENFILENAMEW()
        ofn.hwndOwner = hwnd
        buffer = create_unicode_buffer(MAX_PATH)
        idBuff = None if self._initDir == "" else cast(create_unicode_buffer(self._initDir), c_wchar_p)
        ofn.lStructSize = sizeof(OPENFILENAMEW)
        ofn.lpstrFilter = cast(create_unicode_buffer(self._filter), c_wchar_p)
        ofn.lpstrFile = cast(buffer, c_wchar_p)
        ofn.Flags = OFN_PATHMUSTEXIST | OFN_FILEMUSTEXIST
        if self._multiSel: ofn.Flags |= OFN_ALLOWMULTISELECT
        if self._showHidden: ofn.Flags |= OFN_FORCESHOWHIDDEN
        ofn.lpstrInitialDir = idBuff
        ofn.lpstrTitle = self._title
        ofn.nMaxFile = MAX_PATH
        ret = GetOpenFileName(byref(ofn))
        if ret != 0:
            self._fileNameStart = ofn.nFileOffset
            self._extStart = ofn.nFileExtension
            self._selPath = buffer.value
            return True
        return False


    @property
    def multiSelection(self): return self._multiSel

    @multiSelection.setter
    def multiSelection(self, value: bool): self._multiSel = value
    #---------------------------------------------------------

    @property
    def showHiddenFiles(self): return self._showHidden

    @showHiddenFiles.setter
    def showHiddenFiles(self, value: bool): self._showHidden = value
    #---------------------------------------------------------

# End of FileOpenDialog================================================



class FileSaveDialog(DialogBase):
    def __init__(self, title = "Save File", initDir = "", filterStr = "All files\0*.*\0") -> None:
        super().__init__(title, initDir, filterStr)
        self._defExt = "txt"

    def showDialog(self, hwnd = None):
        ofn = OPENFILENAMEW()
        ofn.hwndOwner = hwnd
        buffer = create_unicode_buffer(MAX_PATH)
        idBuff = None if self._initDir == "" else cast(create_unicode_buffer(self._initDir), c_wchar_p)
        ofn.lStructSize = sizeof(OPENFILENAMEW)
        ofn.lpstrFilter = cast(create_unicode_buffer(self._filter), c_wchar_p)
        ofn.lpstrFile = cast(buffer, c_wchar_p)
        ofn.Flags = OFN_PATHMUSTEXIST | OFN_OVERWRITEPROMPT
        ofn.lpstrInitialDir = idBuff
        ofn.lpstrTitle = self._title
        ofn.lpstrDefExt = cast(create_unicode_buffer(self._defExt), c_wchar_p)
        ofn.nMaxFile = MAX_PATH
        ret = GetSaveFileName(byref(ofn))
        if ret != 0:
            self._fileNameStart = ofn.nFileOffset
            self._extStart = ofn.nFileExtension
            self._selPath = buffer.value
            return True
        return False

    @property
    def defaultExtension(self): return self._defExt

    @defaultExtension.setter
    def defaultExtension(self, value: str):
        """Set the default extension(without period). If user didn't type an extension, this will be selected."""
        self._defExt = value

# End of FileSaveDialog=================================================


class FolderBrowserDialog(DialogBase):
    def __init__(self, title = "Select Folder", initDir = None) -> None:
        super().__init__(title, initDir)
        self._newFolBtn = False
        self._showFiles = False

    def showDialog(self, hwnd = None):
        buffer = create_unicode_buffer(MAX_PATH)
        bi = BROWSEINFOW()
        bi.hwndOwner = hwnd
        bi.lpszTitle = cast(create_unicode_buffer(self._title), c_wchar_p)
        bi.ulFlags = BIF_RETURNONLYFSDIRS | BIF_NEWDIALOGSTYLE
        if self._newFolBtn: bi.ulFlags |= BIF_NONEWFOLDERBUTTON
        if self._showFiles: bi.ulFlags |= BIF_BROWSEINCLUDEFILES
        pidl = SHBrowseForFolder(byref(bi))
        if pidl != None:
            if SHGetPathFromIDList(pidl, buffer):
                CoTaskMemFree(pidl)
                self._selPath = buffer.value
                return True
            CoTaskMemFree(pidl)
        return False

    @property
    def newFolderButton(self): return self._newFolBtn

    @newFolderButton.setter
    def newFolderButton(self, value: bool):
        self._newFolBtn = value

    @property
    def showFiles(self): return self._showFiles

    @showFiles.setter
    def showFiles(self, value: bool):
        self._showFiles = value
