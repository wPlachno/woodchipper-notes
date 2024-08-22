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