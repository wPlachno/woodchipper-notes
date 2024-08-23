import sys
import wcnFile
from constants import LIB_CORE, LIB_LOCAL
from wcnFile import WCFile
import constants as S


# wcnLibrary.py
class _WCLibraryPointer:
    def __init__(self, lib, index):
        self.lib = lib
        self.index = index

class WCLibrary:

    def __init__(self):
        self.core = WCFile()
        self.local = WCFile()
        self.cutoff = 0

    def setPaths(self, homePath, workPath):
        self.loadCore(homePath / S.FILE_NAME_CORE)
        self.loadLocal(workPath / S.FILE_NAME_LOCAL)

    def getPaths(self):
        corePathLine = S.CL_DESC_CORE.format(self.core.path)
        localPathLine = S.CL_DESC_LOCAL.format(self.local.path)
        return corePathLine + localPathLine

    def loadCore(self, corePath):
        self.core.load(corePath)
        self.cutoff = len(self.core.notes)

    def loadLocal(self, localPath):
        self.local.load(localPath)

    def saveCore(self):
        self.core.save()

    def saveLocal(self):
        self.local.save()

    def isValidPointer(self, pointer):
        if pointer.lib == S.LIB_CORE:
            return pointer.index > -1 and pointer.index < len(self.core.notes)
        elif pointer.lib == S.LIB_LOCAL:
            return pointer.index > -1 and pointer.index < len(self.local.notes)
        return False

    def index2Pointer(self, index):
        totalIndex = index-1
        cutoff = len(self.core.notes)
        if totalIndex < cutoff:
            return _WCLibraryPointer(S.LIB_CORE, totalIndex)
        else:
            return _WCLibraryPointer(S.LIB_LOCAL, totalIndex-cutoff)


    def pointer2Index(self, pointer):
        if pointer.lib == S.LIB_ERROR:
            return -1
        elif pointer.lib == S.LIB_CORE:
            return pointer.index+1
        else:
            return len(self.core.notes)+(pointer.index+1)

    def pointer2Note(self, pointer):
        if pointer.lib == S.LIB_CORE:
            return self.core.notes[pointer.index]
        elif pointer.lib == S.LIB_LOCAL:
            return self.local.notes[pointer.index]
        return None

    def pointer2Lib(self, pointer):
        if pointer.lib == S.LIB_CORE:
            return self.core
        elif pointer.lib == S.LIB_LOCAL:
            return self.local
        return None


    def describeCore(self):
        desc = S.EMPTY
        curPtr = _WCLibraryPointer(S.LIB_CORE, -1)
        for index in range(0,len(self.core.notes)):
            curPtr.index = index
            desc += self.describeSingle(curPtr)
        return desc

    def listCore(self):
        if len(self.core.notes) < 1:
            return S.CL_DESC_NO_NOTES
        return self.describeCore()

    def describeSingle(self,pointer):
        if pointer.lib == S.LIB_CORE:
            userIndex = pointer.index+1
            noteString = str(self.core.notes[pointer.index])
            return S.CL_DESC_FRAME_CORE.format(str(userIndex), noteString)
        elif pointer.lib == S.LIB_LOCAL:
            userIndex = pointer.index + len(self.core.notes) +1
            noteString = str(self.local.notes[pointer.index])
            return S.CL_DESC_FRAME_LOCAL.format(str(userIndex), noteString)

    def describeLocal(self):
        desc = S.EMPTY
        curPtr = _WCLibraryPointer(S.LIB_LOCAL, -1)
        for index in range(0,len(self.local.notes)):
            curPtr.index = index
            desc += self.describeSingle(curPtr)
        return desc

    def listLocal(self):
        if len(self.local.notes) < 1:
            return S.CL_DESC_NO_NOTES
        return self.describeLocal()

    def listAll(self):
        text = S.EMPTY
        if len(self.core.notes)<1 and len(self.local.notes)<1:
            return S.CL_DESC_NO_NOTES
        return self.describeCore() + self.describeLocal()

    def appendCore(self, text):
        ptr = _WCLibraryPointer(S.LIB_CORE, self.core.append(text))
        self.core.save()
        return self.describeSingle(ptr)

    def appendLocal(self, text):
        ptr = _WCLibraryPointer(S.LIB_LOCAL, self.local.append(text))
        self.local.save()
        return self.describeSingle(ptr)

    def editMajor(self, text, index):
        ptr = self.index2Pointer(index)
        if self.isValidPointer(ptr):
            lib = self.pointer2Lib(ptr)
            lib.reset(ptr.index, text)
            lib.save()
            return self.describeSingle(ptr)
        else:
            return S.RESULT_FAILURE

    def editMinor(self, text, index):
        ptr = self.index2Pointer(index)
        if self.isValidPointer(ptr):
            lib = self.pointer2Lib(ptr)
            lib.edit(ptr.index, text)
            lib.save()
            return self.describeSingle(ptr)
        else:
            return S.RESULT_FAILURE

    def deleteSingle(self, target):
        ptr = self.index2Pointer(target)
        if self.isValidPointer(ptr):
            lib = self.pointer2Lib(ptr)
            lib.remove(ptr.index)
            lib.save()
            return "Note deleted."+S.NL
        else:
            return S.RESULT_FAILURE

    def deleteCore(self):
        self.core.clear()
        self.core.save()
        return S.CL_DESC_CORE.format("Cleared")

    def deleteLocal(self):
        self.local.clear()
        self.local.save()
        return S.CL_DESC_LOCAL.format("Cleared")

    def promote(self, target):
        targetPtr = self.index2Pointer(target)
        if self.isValidPointer(targetPtr):
            sourceLib = self.pointer2Lib(targetPtr)
            destLibFlag = S.LIB_CORE
            destLib = self.core
            if targetPtr.lib == S.LIB_CORE:
                destLibFlag = S.LIB_LOCAL
                destLib = self.local
            targetText = sourceLib.remove(targetPtr.index).text
            destPtr = _WCLibraryPointer(destLibFlag,destLib.append(targetText))
            sourceLib.save()
            destLib.save()
            return self.describeSingle(destPtr)
        else:
            return S.RESULT_FAILURE

    def move(self, target, destination):
        targetPtr = self.index2Pointer(target)
        destPtr = self.index2Pointer(destination)
        if self.isValidPointer(targetPtr) and self.isValidPointer(destPtr):
            targetLib = self.pointer2Lib(targetPtr)
            targetNote = targetLib.remove(targetPtr.index)
            destLib = self.pointer2Lib(destPtr)
            destLib.insert(destPtr.index, targetNote)
            targetLib.save()
            if targetPtr.lib != destPtr.lib:
                destLib.save()
            return self.describeSingle(destPtr)
        else:
            return S.RESULT_FAILURE





