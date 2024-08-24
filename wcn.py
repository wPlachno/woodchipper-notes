import os
import sys

import constants as S
import wcutil
from pathlib import Path

from wcnLibrary import WCLibrary
from wcutil import str2Bool, bool2Str

settings = wcutil.WoodchipperSettingsFile()
settings.load()
debug = wcutil.Debug(active=(settings.get_debug()))
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

    # Modes with 1 arg:
    #
    #  | MODE      | args[0] |
    # -|-----------|---------|
    # -| List All  | wcn     |
    # -|-----------|---------|
    #
    if len(args) == 1:

        # Mode: List All
        cl.type = S.MODE_LIST_ALL
        cl.description = S.CL_DESC_LIST_ALL

    # Modes with 2 args:
    #
    #  | MODE          | args[0] | args[1] |
    # -|---------------|---------|---------|
    # -| List Core     | wcn     | -c      |
    # -| List Local    | wcn     | -l      |
    # -| Delete All    | wcn     | -d      |
    # -| Debug         | wcn     | -debug  |
    # -| Append Core   | wcn     | [TEXT]  |
    # -|---------------|---------|---------|
    elif len(args) == 2:

        # Mode: List Core
        if args[1] == S.FLAG_CORE:
            cl.type = S.MODE_LIST_CORE
            cl.description = S.CL_DESC_LIST_CORE

        # Mode: List Local
        elif args[1] == S.FLAG_LOCAL:
            cl.type = S.MODE_LIST_LOCAL
            cl.description = S.CL_DESC_LIST_LOCAL

        # Mode: Delete All
        elif args[1] == S.FLAG_DELETE:
            cl.type = S.MODE_DELETE_ALL
            cl.description = S.CL_DESC_DELETE_ALL

        # Mode: Debug
        elif args[1] == S.FLAG_DEBUG:
            cl.type = S.MODE_DEBUG
            cl.description = S.CL_DESC_DEBUG_TASK

        # Mode: Append Core
        else:
            cl.type = S.MODE_APPEND_CORE
            cl.text = args[1]
            cl.description = S.CL_DESC_APPEND_CORE.format(cl.text)

    # Modes with 3 args:
    #
    #  | MODE          | args[0] | args[1] | args[2]  |
    # -|---------------|---------|---------|----------|
    # -| Append Local  | wcn     | -l      | [TEXT]   |
    # -| Promote       | wcn     | -m      | [TARGET] |
    # -| Delete Core   | wcn     | -d      | -c       |
    # -| Delete Local  | wcn     | -d      | -l       |
    # -| Delete Single | wcn     | -d      | [TARGET] |
    # -|---------------|---------|---------|----------|
    elif len(args) == 3:

        # Mode: Append Local
        if args[1] == S.FLAG_LOCAL:
            cl.type = S.MODE_APPEND_LOCAL
            cl.text = args[2]
            cl.description = S.CL_DESC_APPEND_LOCAL.format(cl.text)

        # Mode: Promote
        elif args[1] == S.FLAG_MOVE:
            cl.type = S.MODE_PROMOTE
            cl.target = int(args[2])
            cl.description = S.CL_DESC_PROMOTE.format(args[2])

        # Delete Mode Subgroup:
        elif args[1] == S.FLAG_DELETE:

            # Mode: Delete Core
            if args[2] == S.FLAG_CORE:
                cl.type = S.MODE_DELETE_CORE
                cl.description = S.CL_DESC_DELETE_CORE

            # Mode: Delete Local
            elif args[2] == S.FLAG_LOCAL:
                cl.type = S.MODE_DELETE_LOCAL
                cl.description = S.CL_DESC_DELETE_LOCAL

            # Mode: Delete Single
            else:
                cl.type = S.MODE_DELETE_SINGLE
                cl.target = int(args[2])
                cl.description = S.CL_DESC_DELETE_SINGLE.format(args[2])

    # Modes with 4 args:
    #
    #  | MODE          | args[0] | args[1] | args[2]          | args[3]
    # -|---------------|---------|---------|------------------|---------------|
    # -| Move          | wcn     | -m      | [TARGET]         | [DESTINATION] |
    # -| Edit Major    | wcn     | -et     | [TARGET]         | [TEXT]        |
    # -| Edit Minor    | wcn     | -e      | [TARGET]         | [TEXT]        |
    # -| Delete Single | wcn     | -d      | -[c/l]           | [TARGET]      |
    # -| Config        | wcn     | -config | -[debug/verbose] | [on/off]      |
    # -|---------------|---------|---------|------------------|---------------|
    elif len(args) == 4:

        # Mode: Move
        if args[1] == S.FLAG_MOVE:
            cl.type = S.MODE_MOVE
            cl.target = int(args[2])
            cl.destination = int(args[3])
            cl.description = S.CL_DESC_MOVE.format(args[2], args[3])

        # Mode: Edit Major
        elif args[1] == S.FLAG_EDIT_MAJOR:
            cl.type = S.MODE_EDIT_MAJOR
            cl.target = int(args[2])
            cl.text = args[3]
            cl.description = S.CL_DESC_EDIT_MAJOR.format(cl.text, args[2])

        # Mode: Edit Minor
        elif args[1] == S.FLAG_EDIT_MINOR:
            cl.type = S.MODE_EDIT_MINOR
            cl.target = int(args[2])
            cl.text = args[3]
            cl.description = S.CL_DESC_EDIT_MINOR.format(cl.text, args[2])

        # Mode: Delete Single (With library specification)
        elif args[1] == S.FLAG_DELETE and (args[2] == S.FLAG_LOCAL or args[2] == S.FLAG_CORE):
            cl.type = S.MODE_DELETE_SINGLE
            cl.target = int(args[3])
            cl.description = S.CL_DESC_DELETE_SINGLE.format(args[3])

        # Mode: Config
        elif args[1] == S.FLAG_CONFIG:
            cl.type = S.MODE_CONFIG
            if args[2] == S.FLAG_DEBUG:
                cl.target = S.TAG_DEBUG
                cl.text = S.TAG_DEBUG
            elif args[2] == S.FLAG_VERBOSE:
                cl.target = S.DISPLAY_COMMAND
                cl.text = S.TAG_VERBOSE
            cl.destination = str2Bool(args[3])
            cl.description = S.CL_DESC_CONFIG.format(cl.text, wcutil.bool2Str(cl.destination, True))

    return cl

def operate(cl, lib):
    match cl.type:
        # Mode: Config
        case S.MODE_CONFIG:
            settings[cl.target] = bool2Str(cl.destination)
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


cl = decipher_command_line(sys.argv)
if settings.get_or_default(S.DISPLAY_COMMAND, S.TAG_ON) == S.TAG_ON:
    print(cl.description)

lib = WCLibrary()
lib.setPaths(Path.home(), Path(os.getcwd()))
dbg(lib.getPaths())
operate(cl,lib)
