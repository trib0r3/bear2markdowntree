# bear2markdowntree

Convert notes from Bear.app to Markdown tree-structured notes. This script was written for transfering notes frop Bear to Typor, may have some bugs but it worked for me ;)

## Prerequirements

- *Python3*.

## Feature

- extract tags from notes
- create structured directories based on tags
- selection of tag which should be used for note if multiple tags are used in note
- YAML heading with complete list of tags
- edit mode for incorrectly detected tags during run of script
- move attachments (and local pics) to relative directories in new paths

## Todo

- [ ] dry run
- [ ] auto-detect notes & attachments in directory
- [ ] fix tag detection
- [ ] fix incorrect grabbing local path from pics (for paths using urlencoding / special chars in name)


## How to

> __WARNING!__ script is moving directories, so if something will go wrong you need to delete all from `BEAR_DIR` and `NOTE_DIR` and repeat all steps!

1. Create empty directories and specify them in script:
   1. `BEAR_DIR` (default: `BearNotes`) - for input Bear Notes
   2. `NOTE_DIR` (default: `Notes`) - for output notes in tree structure
2. Export notes from Bear to `BEAR_DIR`:
   1. Click on **Notes** in Bear
   2. `Cmd + A` to select them all
   3. `Cmd + Shift + S`, select `Markdown` and put them in your `BEAR_DIR`.
3. Edit variables `BEAR_DIR` and `NOTE_DIR` or run script with arguments.
4. Run script: `python3 export-bear2typora.py` or `python3 export-bear2typora.py $NOTE_DIR $BEAR_DIR`.
   1. if you see multiple tags for note, you can choose which one you want use to build a directory tree structure
   2. if you see incorrect flag detected, you can edit `tags` array by entering `e` instead of index.