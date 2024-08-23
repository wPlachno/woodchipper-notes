import sys
import wcnFile
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


    def listCore(self):
        desc = S.EMPTY
        for index in range(0,len(self.core.notes)):
            desc += str(index+1)+": "+S.COLOR_SUPER+"C"+S.COLOR_DEFAULT+self.core.notes[index]+S.NL
        return desc

    def listLocal(self):
        currentIndex = len(self.core.notes)+1
        desc = S.EMPTY
        for index in range(0,len(self.local.notes)):
            desc += str(currentIndex)+": "+S.COLOR_SIBLING+"L"+S.COLOR_DEFAULT+self.core.notes[index]+S.NL
            currentIndex = currentIndex+1
        return desc

    def listAll(self):
        return self.listCore() + self.listLocal()

    def appendCore(self, text):
        return self.core.append(text)

    def appendLocal(self, text):
        return self.local.append(text)

    def editMajor(self, text, index):
        ptr = self.index2Pointer(index)
        if self.isValidPointer(ptr):
            lib = self.pointer2Lib(ptr)
            lib.reset(ptr.index, text)
            lib.save()
            return S.RESULT_SUCCESS
        else:
            return S.RESULT_FAILURE

    def editMinor(self, text, index):
        ptr = self.index2Pointer(index)
        if self.isValidPointer(ptr):
            lib = self.pointer2Lib(ptr)
            lib.edit(ptr.index, text)
            lib.save()
            return S.RESULT_SUCCESS
        else:
            return S.RESULT_FAILURE

    def deleteSingle(self, target):
        ptr = self.index2Pointer(target)
        if self.isValidPointer(ptr):
            lib = self.pointer2Lib(ptr)
            lib.remove(ptr.index)
            lib.save()
            return S.RESULT_SUCCESS
        else:
            return S.RESULT_FAILURE

    def deleteCore(self):
        self.core.clear()

    def deleteLocal(self):
        self.local.clear()

    def promote(self, target):
        targetPtr = self.index2Pointer(target)
        if self.isValidPointer(targetPtr):
            sourceLib = self.pointer2Lib(targetPtr)
            destLib = self.core
            if targetPtr.lib == S.LIB_LOCAL:
                destLib = self.local
            targetText = sourceLib.remove(targetPtr.index).text
            destLib.append(targetText)
            sourceLib.save()
            destLib.save()
            return S.RESULT_SUCCESS
        else:
            return S.RESULT_FAILURE

    def move(self, target, destination):
        targetPtr = self.index2Pointer(target)
        destPtr = self.index2Pointer(destination)
        if self.isValidPointer(targetPtr) and self.isValidPointer(destPtr):
            targetLib = self.pointer2Lib(targetPtr)
            targetNote = targetLib.remove(targetPtr)
            destLib = self.pointer2Lib(destPtr)
            destLib.insert(destPtr.index, targetNote)
            targetLib.save()
            if targetPtr.lib != destPtr.lib:
                destLib.save()
            return S.RESULT_SUCCESS
        else:
            return S.RESULT_FAILURE





