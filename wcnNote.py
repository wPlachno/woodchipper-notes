import constants as S
from datetime import datetime


# wcnNote.py
# This file contains the WCNote class, which is a model class of an individual note.
# A note consists of a timestamp and some text.

class WCNote:
    def __init__(self):
        self.time = datetime.now()
        self.text = S.EMPTY

    def __str__(self):
        return S.COLOR_SUB+self.time.strftime(S.TIME_READABLE)+S.COLOR_DEFAULT+" - "+self.text

    def read(self, record: str):
        record_pieces = record.split(S.NOTE_DELIMITER)
        self.time = datetime.fromtimestamp(float(record_pieces[0]))
        self.text = record_pieces[1]
        return self

    def write(self):
        return self.time.strftime(S.TIME_EPOCH)+S.NOTE_DELIMITER+self.text+S.NOTE_DELIMITER+S.NL

    def define(self, text):
        self.time = datetime.now()
        self.text = text


