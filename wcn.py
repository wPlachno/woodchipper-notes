import sys

import constants as S
import wcutil

debug = wcutil.Debug(active=True)
dbg = debug.scribe

class CommandLineInformation:
    def __init__(self):
        self.success = False
        self.type = S.EMPTY
        self.text = S.EMPTY
        self.target = S.EMPTY
        self.destination = S.EMPTY
        self.description = S.EMPTY

def decipher_command_line(args):
    cl = CommandLineInformation()
    if len(args) == 1:
        cl.type = S.MODE_LIST_ALL
        cl.description = S.CL_DESC_LIST_ALL
    elif len(args) == 4:
        if args[1] == S.FLAG_MOVE:
            cl.type = S.MODE_MOVE
            cl.target = args[2]
            cl.destination = args[3]
            cl.description = S.CL_DESC_MOVE.format(cl.target, cl.destination)
        elif args[1] == S.FLAG_EDIT_MAJOR:
            cl.type = S.MODE_EDIT_MAJOR
            cl.target = args[2]
            cl.text = args[3]
            cl.description = S.CL_DESC_EDIT_MAJOR.format(cl.target, cl.text)
        elif args[1] == S.FLAG_EDIT_MINOR:
            cl.type = S.MODE_EDIT_MINOR
            cl.target = args[2]
            cl.text = args[3]
            cl.description = S.CL_DESC_EDIT_MINOR.format(cl.target, cl.text)
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
                cl.target = args[2]
                cl.description = S.CL_DESC_DELETE_SINGLE.format(cl.target)
    return cl

cl = decipher_command_line(sys.argv)
print(cl.description)
