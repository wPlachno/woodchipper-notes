import os
import sys

import constants as S
import wcutil
from pathlib import Path

from wcnLibrary import WCLibrary

debug = wcutil.Debug(active=False)
dbg = debug.scribe

class CommandLineInformation:
    def __init__(self):
        self.success = False
        self.type = S.EMPTY
        self.text = S.EMPTY
        self.target = S.EMPTY
        self.destination = S.EMPTY
        self.description = S.EMPTY
        self.summary = S.EMPTY

def decipher_command_line(args):
    cl = CommandLineInformation()
    if len(args) == 1:
        cl.type = S.MODE_LIST_ALL
        cl.description = S.CL_DESC_LIST_ALL
    elif len(args) == 4:
        if args[1] == S.FLAG_MOVE:
            cl.type = S.MODE_MOVE
            cl.target = int(args[2])
            cl.destination = int(args[3])
            cl.description = S.CL_DESC_MOVE.format(args[2], args[3])
        elif args[1] == S.FLAG_EDIT_MAJOR:
            cl.type = S.MODE_EDIT_MAJOR
            cl.target = int(args[2])
            cl.text = args[3]
            cl.description = S.CL_DESC_EDIT_MAJOR.format(cl.text, args[2])
        elif args[1] == S.FLAG_EDIT_MINOR:
            cl.type = S.MODE_EDIT_MINOR
            cl.target = int(args[2])
            cl.text = args[3]
            cl.description = S.CL_DESC_EDIT_MINOR.format(cl.text, args[2])
    elif len(args) == 2:
        if args[1] == S.FLAG_CORE:
            cl.type = S.MODE_LIST_CORE
            cl.description = S.CL_DESC_LIST_CORE
        elif args[1] == S.FLAG_LOCAL:
            cl.type = S.MODE_LIST_LOCAL
            cl.description = S.CL_DESC_LIST_LOCAL
        else:
            cl.type = S.MODE_APPEND_CORE
            cl.text = args[1]
            cl.description = S.CL_DESC_APPEND_CORE.format(cl.text)
    elif len(args) == 3:
        if args[1] == S.FLAG_LOCAL:
            cl.type = S.MODE_APPEND_LOCAL
            cl.text = args[2]
            cl.description = S.CL_DESC_APPEND_LOCAL.format(cl.text)
        elif args[1] == S.FLAG_DELETE:
            if args[2] == S.FLAG_CORE:
                cl.type = S.MODE_DELETE_CORE
                cl.description = S.CL_DESC_DELETE_CORE
            elif args[2] == S.FLAG_LOCAL:
                cl.type = S.MODE_DELETE_LOCAL
                cl.description = S.CL_DESC_DELETE_LOCAL
            else:
                cl.type = S.MODE_DELETE_SINGLE
                cl.target = int(args[2])
                cl.description = S.CL_DESC_DELETE_SINGLE.format(args[2])
        elif args[1] == S.FLAG_MOVE:
            cl.type = S.MODE_PROMOTE
            cl.target = int(args[2])
            cl.description = S.CL_DESC_PROMOTE.format(args[2])
    return cl

def operate(cl, lib):
    match cl.type:
        case S.MODE_LIST_ALL:
            print(lib.listAll())
            cl.success = True
        case S.MODE_LIST_CORE:
            print(lib.listCore())
            cl.success = True
        case S.MODE_LIST_LOCAL:
            print(lib.listLocal())
            cl.success = True
        case S.MODE_APPEND_CORE:
            print(lib.appendCore(cl.text))
            cl.success = True
        case S.MODE_APPEND_LOCAL:
            print(lib.appendLocal(cl.text))
            cl.success = True
        case S.MODE_EDIT_MAJOR:
            print(lib.editMajor(cl.text, cl.target))
            cl.success = True
        case S.MODE_EDIT_MINOR:
            print(lib.editMinor(cl.text, cl.target))
            cl.success = True
        case S.MODE_DELETE_SINGLE:
            print(lib.deleteSingle(cl.target))
            cl.success = True
        case S.MODE_DELETE_CORE:
            print(lib.deleteCore())
            cl.success = True
        case S.MODE_DELETE_LOCAL:
            print(lib.deleteLocal())
            cl.success = True
        case S.MODE_MOVE:
            print(lib.move(cl.target, cl.destination))
            cl.success = True
        case S.MODE_PROMOTE:
            print(lib.promote(cl.target))
            cl.success = True
        case _:
            print(S.RESULT_FAILURE)
            cl.success = False


cl = decipher_command_line(sys.argv)
print(cl.description)

lib = WCLibrary()
lib.setPaths(Path.home(), Path(os.getcwd()))
dbg(lib.getPaths())
operate(cl,lib)
