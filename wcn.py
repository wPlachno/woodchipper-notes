import os
import sys

import constants as S
import wcutil
from pathlib import Path

from constants import LIB_CORE, LIB_LOCAL
from wcnLibrary import WCLibrary
from wcutil import bool_from_user, string_from_bool

settings = None
debug = None
dbg = None

class CommandLineInformation:
    def __init__(self):
        self.success = False
        self.type = S.EMPTY
        self.libraries = S.LIB_ALL
        self.text = S.EMPTY
        self.target = S.EMPTY
        self.destination = S.EMPTY
        self.description = S.EMPTY
        self.summary = S.EMPTY

def decipher_command_line(args):
    cl = CommandLineInformation()
    flags = wcutil.FlagFarm(S.FLAG_LIST)
    nodes = wcutil.decipher_command_line(args, flags)
    if flags[S.FLAG_CORE]:
        cl.libraries = LIB_CORE
    elif flags[S.FLAG_LOCAL]:
        cl.libraries = LIB_LOCAL

    cl.type = S.MODE_LIST_ALL
    cl.description = S.CL_DESC_LIST_ALL

    if flags[S.FLAG_DELETE] or flags[S.FLAG_REMOVE]:    # -d or -r
        if len(nodes)>0:                                # -d [target]
            cl.type = S.MODE_DELETE_SINGLE
            cl.target = int(nodes[0])
            cl.description = S.CL_DESC_DELETE_SINGLE.format(cl.target)
        else:                                           # -d
            if cl.libraries == S.LIB_ALL:
                cl.type = S.MODE_DELETE_ALL
                cl.description = S.CL_DESC_DELETE_ALL
            elif cl.libraries == S.LIB_CORE:
                cl.type = S.MODE_DELETE_CORE
                cl.description = S.CL_DESC_DELETE_CORE
            else:
                cl.type = S.MODE_DELETE_LOCAL
                cl.description = S.CL_DESC_DELETE_LOCAL
    elif flags[S.FLAG_MOVE]:                            # -m
        if len(nodes) == 2:                             # -m [target] [destination]
            cl.type = S.MODE_MOVE
            cl.target = int(nodes[0])
            cl.destination = int(nodes[1])
            cl.description = S.CL_DESC_MOVE.format(cl.target, cl.destination)
        elif len(nodes) == 1:                           # -m [target]
            cl.type = S.MODE_PROMOTE
            cl.target = int(nodes[0])
            cl.description = S.CL_DESC_PROMOTE.format(cl.target)
    elif flags[S.FLAG_CONFIG]:                          # -config
        cl.type = S.MODE_CONFIG
        if flags[S.FLAG_DEBUG]:                         # -config -debug [val]
            cl.target = S.TAG_DEBUG
            cl.text = S.TAG_DEBUG
        elif flags[S.FLAG_VERBOSE]:                     # -config -verbose [val]
            cl.target = S.DISPLAY_COMMAND
            cl.text = S.TAG_VERBOSE
        cl.destination = bool_from_user(nodes[0] if len(nodes)>0 else False)
        cl.description = S.CL_DESC_CONFIG.format(cl.text, wcutil.string_from_bool(cl.destination, True))
    elif flags[S.FLAG_EDIT_MINOR]:                      # -e
        if len(nodes) == 2:
            cl.type = S.MODE_EDIT_MINOR
            cl.target = int(nodes[0])
            cl.text = nodes[1]
            cl.description = S.CL_DESC_EDIT_MINOR.format(cl.text, cl.target)
    elif flags[S.FLAG_EDIT_MAJOR]:                      # -et
        if len(nodes) == 2:
            cl.type = S.MODE_EDIT_MAJOR
            cl.target = int(nodes[0])
            cl.text = nodes[1]
            cl.description = S.CL_DESC_EDIT_MAJOR.format(cl.text, cl.target)
    else:
        if len(nodes)>0:                                # [targets] APPEND
            match cl.libraries:
                case S.LIB_LOCAL:
                    cl.type = S.MODE_APPEND_LOCAL
                    cl.text = nodes[0]
                    cl.description = S.CL_DESC_APPEND_LOCAL.format(cl.text)
                case _:
                    cl.type = S.MODE_APPEND_CORE
                    cl.text = nodes[0]
                    cl.description = S.CL_DESC_APPEND_CORE.format(cl.text)
        else:                                           # LIST
            match cl.libraries:
                case S.LIB_CORE:
                    cl.type = S.MODE_LIST_CORE
                    cl.description = S.CL_DESC_LIST_CORE
                case S.LIB_LOCAL:
                    cl.type = S.MODE_LIST_LOCAL
                    cl.description = S.CL_DESC_LIST_LOCAL
    return cl

def operate(cl, lib):
    match cl.type:
        # Mode: Config
        case S.MODE_CONFIG:
            settings[cl.target] = string_from_bool(cl.destination)
            settings.save()
            dbg(cl.description)
            cl.success = True
        # Mode: Debug
        case S.MODE_DEBUG:
            settings.flip_debug()
            settings.save()
            debugText = S.CL_DESC_ACTIVE if settings.get_debug() else S.CL_DESC_INACTIVE
            print(S.CL_DESC_ATTRIBUTE.format("Debug", debugText))
            cl.success = True
        # Mode: List All
        case S.MODE_LIST_ALL:
            print(lib.listAll())
            cl.success = True
        # Mode: List Core
        case S.MODE_LIST_CORE:
            print(lib.listCore())
            cl.success = True
        # Mode: List Local
        case S.MODE_LIST_LOCAL:
            print(lib.listLocal())
            cl.success = True
        # Mode: Append Core
        case S.MODE_APPEND_CORE:
            print(lib.appendCore(cl.text))
            cl.success = True
        # Mode: Append Local
        case S.MODE_APPEND_LOCAL:
            print(lib.appendLocal(cl.text))
            cl.success = True
        # Mode: Edit Major
        case S.MODE_EDIT_MAJOR:
            print(lib.editMajor(cl.text, cl.target))
            cl.success = True
        # Mode: Edit Minor
        case S.MODE_EDIT_MINOR:
            print(lib.editMinor(cl.text, cl.target))
            cl.success = True
        # Mode: Delete Single
        case S.MODE_DELETE_SINGLE:
            print(lib.deleteSingle(cl.target))
            cl.success = True
        # Mode: Delete Core
        case S.MODE_DELETE_CORE:
            print(lib.deleteCore())
            cl.success = True
        # Mode: Delete Local
        case S.MODE_DELETE_LOCAL:
            print(lib.deleteLocal())
            cl.success = True
        # Mode: Delete All
        case S.MODE_DELETE_ALL:
            print(lib.deleteCore()+lib.deleteLocal())
            cl.success = True
        # Mode: Move
        case S.MODE_MOVE:
            print(lib.move(cl.target, cl.destination))
            cl.success = True
        # Mode: Promote
        case S.MODE_PROMOTE:
            print(lib.promote(cl.target))
            cl.success = True
        case _:
            print(S.RESULT_FAILURE)
            cl.success = False

def _main(args):
    settings = wcutil.WoodchipperSettingsFile()
    settings.load()
    debug = wcutil.Debug(active=(settings.get_debug()))
    dbg = debug.scribe

    cl = decipher_command_line(args)
    if settings.get_or_default(S.DISPLAY_COMMAND, S.TAG_ON) == S.TAG_ON or settings.get_debug():
        print(cl.description)
"""
    lib = WCLibrary()
    lib.setPaths(Path.home(), Path(os.getcwd()))
    dbg(lib.getPaths())
    operate(cl,lib)
"""

if __name__ == "__main__":
    _main(sys.argv)
