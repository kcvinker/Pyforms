
# Dialogs module - Created on 14-May-2023 16:55

from . apis import OPENFILENAMEW, BROWSEINFOW, GetOpenFileName, GetSaveFileName, SHBrowseForFolder, SHGetPathFromIDList, CoTaskMemFree
from ctypes import create_unicode_buffer, sizeof, byref, c_wchar_p, cast

MAX_PATH = 260
OFN_ALLOWMULTISELECT = 0x200
OFN_PATHMUSTEXIST = 0x800
OFN_FILEMUSTEXIST = 0x1000
OFN_FORCESHOWHIDDEN = 0x10000000
OFN_EXPLORER = 0x00080000
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

    def setMultiFilters(self, description, filterList):
        self._filter = f"{description}\0"
        filCount = len(filterList) - 1
        for i, filter in enumerate(filterList):
            self._filter += f"*{filter}"
            if i < filCount: self._filter += ";"
        self._filter += "\0\0"


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

# Parameters
# 1. obj - may be a FileOpenDialog class or FileSaveDialog class.
# 2. isOpen - bool
# 3. hwnd - HWND (A window handle)
def _showDialogHelper(obj, isOpen, hwnd):
    maxArrSize = 32768 + 256 * 100 + 1
    ofn = OPENFILENAMEW()
    ofn.hwndOwner = hwnd
    buffer = create_unicode_buffer(maxArrSize)
    idBuff = None if obj._initDir == "" else cast(create_unicode_buffer(obj._initDir), c_wchar_p)
    ofn.lStructSize = sizeof(OPENFILENAMEW)
    ofn.lpstrFilter = cast(create_unicode_buffer(obj._filter), c_wchar_p)
    ofn.lpstrFile = cast(buffer, c_wchar_p)
    ofn.lpstrInitialDir = idBuff
    ofn.lpstrTitle = obj._title
    ofn.nMaxFile = maxArrSize
    ofn.nMaxFileTitle = MAX_PATH
    ofn.lpstrDefExt = '\u0000'
    retVal = 0
    if isOpen:
        ofn.Flags = OFN_PATHMUSTEXIST | OFN_FILEMUSTEXIST
        if obj._multiSel: ofn.Flags |= OFN_ALLOWMULTISELECT | OFN_EXPLORER
        if obj._showHidden: ofn.Flags |= OFN_FORCESHOWHIDDEN
        retVal = GetOpenFileName(byref(ofn))
        if retVal > 0 and obj._multiSel:
            obj._extractFileNames(buffer, ofn.nFileOffset)

    else:
        ofn.Flags = OFN_PATHMUSTEXIST | OFN_OVERWRITEPROMPT
        retVal = GetSaveFileName(byref(ofn))

    if retVal != 0:
        obj._fileNameStart = ofn.nFileOffset
        obj._extStart = ofn.nFileExtension
        obj._selPath = buffer.value
        return True
    return False

class FileOpenDialog(DialogBase):
    def __init__(self, title = "Select File", initDir = "", filterStr = "All files\0*.*\0") -> None:
        super().__init__(title, initDir, filterStr)
        self._multiSel = False
        self._showHidden = False
        self._fNames = []

    def _extractFileNames(self, buff, startPos):
        parts = buff[:].rstrip('\0')
        dirPath = parts[:startPos].rstrip('\0')
        names = parts[startPos:].split('\0')
        for name in names:
            self._fNames.append(f"{dirPath}\{name}")


    def showDialog(self, hwnd = None):
        return _showDialogHelper(self, True, hwnd)

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

    @property
    def fileNames(self): return self._fNames

# End of FileOpenDialog================================================



class FileSaveDialog(DialogBase):
    def __init__(self, title = "Save File", initDir = "", filterStr = "All files\0*.*\0") -> None:
        super().__init__(title, initDir, filterStr)
        self._defExt = "txt"

    def showDialog(self, hwnd = None):
        return _showDialogHelper(self, False, hwnd)

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
    def selectedPath(self): return self._selPath

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

