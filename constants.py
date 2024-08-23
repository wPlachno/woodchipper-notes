EMPTY=""
NL="\n"
BS="\\"

COLOR_RED='\033[0;31m'
COLOR_GREY='\033[90m'
COLOR_YELLOW='\033[93m'
COLOR_DARK_YELLOW='\033[0;33m'
COLOR_GREEN='\033[0;32m'
COLOR_PURPLE='\033[0;35m'
COLOR_BLACK='\033[0;30m'
COLOR_WHITE='\033[37m'
COLOR_DEFAULT='\033[0m'

COLOR_SUPER=COLOR_PURPLE
COLOR_SUB=COLOR_GREY
COLOR_SIBLING=COLOR_DARK_YELLOW
COLOR_ACTIVE=COLOR_GREEN
COLOR_CANCEL=COLOR_RED

MODE_LIST_ALL = "LIST_ALL"
MODE_LIST_CORE = "LIST_CORE"
MODE_LIST_LOCAL = "LIST_LOCAL"
MODE_APPEND_CORE = "APPEND_CORE"
MODE_APPEND_LOCAL = "APPEND_LOCAL"
MODE_EDIT_MAJOR = "EDIT_MAJOR"
MODE_EDIT_MINOR = "EDIT_MINOR"
MODE_MOVE = "MOVE"
MODE_PROMOTE = "PROMOTE"
MODE_DELETE_SINGLE = "DELETE_SINGLE"
MODE_DELETE_CORE = "DELETE_CORE"
MODE_DELETE_LOCAL = "DELETE_LOCAL"

CL_DESC_SUCCESS = COLOR_ACTIVE+"Success"+COLOR_DEFAULT
CL_DESC_FAILURE = COLOR_CANCEL+"Failure"+COLOR_DEFAULT

CL_DESC_TASK = COLOR_SUPER+"Task"+COLOR_DEFAULT+": "
CL_DESC_UNIMPLEMENTED = " ["+COLOR_CANCEL+"UNIMPLEMENTED"+COLOR_DEFAULT+"]"
CL_DESC_TEXT = COLOR_SIBLING+"Text"+COLOR_DEFAULT+": {0}"+NL
CL_DESC_INDEX = COLOR_SIBLING+"Index"+COLOR_DEFAULT+": {1}"+NL
CL_DESC_DEL_INDEX = COLOR_SIBLING+"Index"+COLOR_DEFAULT+": {0}"+NL
CL_DESC_TARGET = COLOR_SIBLING+"Target"+COLOR_DEFAULT+": {0}"+NL
CL_DESC_DESTINATION = COLOR_SIBLING+"Destination"+COLOR_DEFAULT+": {1}"+NL

CL_DESC_LIST_ALL = CL_DESC_TASK+"List all notes."+CL_DESC_UNIMPLEMENTED+NL
CL_DESC_LIST_CORE = CL_DESC_TASK+"List Core notes."+CL_DESC_UNIMPLEMENTED+NL
CL_DESC_LIST_LOCAL = CL_DESC_TASK+"List Local notes."+CL_DESC_UNIMPLEMENTED+NL
CL_DESC_APPEND_CORE = CL_DESC_TASK+"Append new note to Core."+CL_DESC_UNIMPLEMENTED+NL+CL_DESC_TEXT
CL_DESC_APPEND_LOCAL = CL_DESC_TASK+"Append new note to Local."+CL_DESC_UNIMPLEMENTED+NL+CL_DESC_TEXT
CL_DESC_EDIT_MAJOR = CL_DESC_TASK+"Edit text and time of note."+CL_DESC_UNIMPLEMENTED+NL+CL_DESC_TEXT+CL_DESC_INDEX
CL_DESC_EDIT_MINOR = CL_DESC_TASK+"Edit text only of note."+CL_DESC_UNIMPLEMENTED+NL+CL_DESC_TEXT+CL_DESC_INDEX
CL_DESC_PROMOTE = CL_DESC_TASK+"Promote a note to the other file."+CL_DESC_UNIMPLEMENTED+NL+CL_DESC_TARGET
CL_DESC_MOVE = CL_DESC_TASK+"Move a note from target index to destination index."+CL_DESC_UNIMPLEMENTED+NL+CL_DESC_TARGET+CL_DESC_DESTINATION
CL_DESC_DELETE_SINGLE = CL_DESC_TASK+"Delete a single note."+CL_DESC_UNIMPLEMENTED+NL+CL_DESC_DEL_INDEX
CL_DESC_DELETE_CORE = CL_DESC_TASK+"Delete all notes in Core."+CL_DESC_UNIMPLEMENTED+NL
CL_DESC_DELETE_LOCAL = CL_DESC_TASK+"Delete all notes in Local."+CL_DESC_UNIMPLEMENTED+NL

CL_DESC_NO_NOTES = "No notes to list."+NL
CL_DESC_NOTES_TOTAL = "Found "+COLOR_SUPER+"{0}"+COLOR_DEFAULT+" notes."

FLAG_CORE = "-c"
FLAG_LOCAL = "-l"
FLAG_EDIT_MINOR = "-e"
FLAG_EDIT_MAJOR = "-et"
FLAG_MOVE = "-m"
FLAG_DELETE = "-d"

FILE_NAME_CORE = ".wcn_Core.txt"
FILE_NAME_LOCAL = ".wcn_Local.txt"

LIB_CORE = "C"
LIB_LOCAL = "L"
LIB_ERROR = "E"

TIME_READABLE = "%m/%d/%Y, %H:%M:%S"
TIME_EPOCH = "%s"

RESULT_SUCCESS = True
RESULT_FAILURE = False

NOTE_DELIMITER = "`~`"
OOB = -1