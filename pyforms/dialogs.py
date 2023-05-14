
# Dialogs module - Created on 14-May-2023 16:55

from . apis import OPENFILENAMEW, GetOpenFileName
from ctypes import create_unicode_buffer, sizeof, byref, c_wchar_p, cast

MAX_PATH = 260
OFN_ALLOWMULTISELECT = 0x200
OFN_PATHMUSTEXIST = 0x800
OFN_FILEMUSTEXIST = 0x1000
OFN_FORCESHOWHIDDEN = 0x10000000


class FileOpenDialog:
    def __init__(self, title = "Open File", initDir = "", filter = "All files\0*.*\0") -> None:
        self._title = title
        self._initDir = initDir
        self._filter = filter
        self._multiSel = False
        self._showHidden = False
        self._fileNameStart = 0
        self._extStart = 0
        self._selFile = ""

    def showDialog(self):
        ofn = OPENFILENAMEW()
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
            self._selFile = buffer.value
            return True
        return False

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
    def fileNameStartPos(self): return self._fileNameStart

    @property
    def extensionStartPos(self): return self._extStart

    @property
    def selectedFile(self): return self._selFile
# End of FileOpenDialog================================================



