# test.sh
# Tests the functionality of wcn

SUP='\033[0;35m'
SUB='\033[90m'
DEF='\033[0m'

# printBorder: Displays a graphical delineation between two console entries
printBorder() { echo -e "${SUB}---------------------------------${DEF}"; }

# printHeader: Displays a header with the given text
printModeHeader() {
    printBorder;
    printf "$SUB%s ${SUB}MODE${DEF}: %.22s ${SUB} %s${DEF}\n" '-' "$1" '-';
    printBorder;
}

printModeHeader "List All"
python3 wcn.py
printModeHeader "List Local"
python3 wcn.py -l
printModeHeader "List Core"
python3 wcn.py -c
printModeHeader "Append Core"
python3 wcn.py "Save us!"
printModeHeader "Append Local"
python3 wcn.py -l "Save us!"
printModeHeader "Edit Minor (1)"
python3 wcn.py -e 1 "Save me!"
printModeHeader "Edit Major (2)"
python3 wcn.py -et 2 "Save us all!"
printModeHeader "Move (1 -> 2)"
python3 wcn.py -m 1 2
printModeHeader "Delete Single (3)"
python3 wcn.py -d 3
printModeHeader "Delete Core"
python3 wcn.py -d -c
printModeHeader "Delete Local"
python3 wcn.py -d -l
