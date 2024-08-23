import constants as S
from wcutil import WoodChipperFile as Scribe
from wcnNote import WCNote

# wcnFile.py
# This file contains the WCFile class, which is a model class of a collection of notes.
# The WCFile is a hidden file in which WCNotes are saved, 1 per line.
# The lifetime of the WCFile class goes from simple initialization, to loading the date, and then possibly to saving the date.
# Outside influences should be able to add and edit and delete between loading and saving.

class WCFile:
    def __init__(self):
        self.path = S.EMPTY
        self.notes = []
        self.file = None

    def append(self, text):
        newNote = WCNote().define(text)
        self.notes.append(newNote)
        return newNote

    def appendNote(self, note):
        self.notes.append(note)
        return note

    def remove(self,index):
        return self.notes.pop(index)

    def clear(self):
        while len(self.notes):
            self.notes.pop()

    def insert(self, targetIndex, note):
        self.notes.insert(targetIndex,note)

    def move(self, target, destination):
        dest = destination
        if dest != target:
            if dest > target:
                dest = dest-1
            targetNote = self.notes.pop(target)
            self.notes.insert(dest, targetNote)

    def edit(self, index, text):
        self.notes[index].text = text

    def reset(self, index, text):
        self.notes[index].define(text)

    def load(self, path):
        self.path = path
        self.file = Scribe(path)
        self.file.read()
        for line in self.file.text:
            self.notes.append(WCNote().read(line))

    def save(self):
        fileText = list(())
        for index in range(0,len(self.notes)):
            fileText.append(self.notes[index].write())
        self.file.text = fileText
        self.file.write()