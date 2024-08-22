import constants as S
from datetime import datetime


# wcnNote.py
# This file contains the WCNote class, which is a model class of an individual note.
# A note consists of a timestamp and some text.

TIME_READABLE = "%m/%d/%Y, %H:%M:%S"
TIME_EPOCH = "%s"

NOTE_DELIMITER = "`~`"

class WCNote:
    def __init__(self):
        self.time = datetime.now()
        self.text = ""

    def __str__(self):
        return S.COLOR_SUPER+self.time.strftime(TIME_READABLE)+S.COLOR_DEFAULT+" - "+self.text

    def read(self, record: str):
        record_pieces = record.split(NOTE_DELIMITER)
        self.time = datetime.fromtimestamp(float(record_pieces[0]))
        self.text = record_pieces[1]

    def write(self):
        return self.time.strftime(TIME_EPOCH)+NOTE_DELIMITER+self.text


