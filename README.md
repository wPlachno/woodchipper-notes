# woodchipper-notes
A command line python script for quick notes, both in general, as well as per-directory

## Welcome
Thank you for taking the time to look at Will Plachno's woodchipper-notes project. The description provided here is the ultimate scope of the project - it describes the intended functionality. To see what is actually written and working, follow the log notes at the bottom of this file.

This project administrates a command-line system of notes which can be quickly saved with a timestamp. These notes can be saved in a core file, making them accessible anywhere, or in a local file, making them scoped to the current working directory. 

The notes can be listed, as a whole or per-file, added to, edited, moved, or deleted.

```
wcn -- Lists the notes in the core file then in a local file with indexes
wcn [TEXT] -- Saves the text with a timestamp in the core file
wcn -l -- Lists only the notes in the local file
wcn -c -- Lists only the notes in the core file
wcn -l [TEXT] -- Saves the text with a timestamp in the core file
wcn -m [INDEX] -- Moves the note at the index to the other file
wcn -d [INDEX] -- Deletes the note with the given index, core or local
wcn -d -c -- Deletes all notes in the core file
wcn -d -l -- Deletes all notes in the local file
wcn -e [INDEX] [TEXT] -- Starts an edit procedure to edit the text, but not the timestamp, of the note at INDEX
wcn -et [INDEX] [TEXT] -- Starts an edit procedure to edit the text and reset the timestamp of the note at INDEX
wcn -m [INDEX_TARGET] [INDEX_DESTINATION] -- Moves the note at INDEX_TARGET to INDEX_DESTINATION, moving as necessary, including both within and between the core and local files.
```

## ToDo
- Convert functions and methods to the_proper_naming_scheme

## Work Log
- 8/24/24: Added settings file and config route
- 8/23/24: Added operate function and fixed bugs til feature complete. (wplachno)
- 8/22/24: Added Library and routes for each mode. Also added MODE_PROMOTE to switch files. (wplachno)
- 8/22/24: Added .gitignore, colors, test script, and models for Note and File. (wplachno)
- 8/22/24: Added command line deciphering. (wplachno)
- 8/21/24: Set readme to describe ultimate scope. (wplachno)