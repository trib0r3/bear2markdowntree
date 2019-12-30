# bear2markdowntree

Convert notes from Bear.app to Markdown tree-structured notes. This script was written for transfering notes frop [Bear](#1) to [Typora](#2), may have some bugs but it worked for me ;)

## Prerequirements

- *Python3*.

## Features

- extract tags from notes
- create structured directories based on tags
- selection of tag which should be used for note if multiple tags are used in note
- YAML heading with complete list of tags
- edit mode for incorrectly detected tags during run of script
- move attachments (and local pics) to relative directories in new paths
- build *index* file with `build-tags.py`

## Todo

- [ ] dry run
- [ ] auto-detect notes & attachments in directory
- [ ] fix tag detection
- [ ] fix incorrect grabbing local path from pics (for paths using urlencoding / special chars in name)
- [ ] add some config files / parameters


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


### Multi-tagging support

Generally it is not possible to support multiple tags with directory structure (you can try to emulate it with symbolic links, but *Typora* doesn't like this solution), but you can actually build index-tree which will contain list of all tags with relative links to notes.

I created small script which is creating *index.md* in root directory of notes, I am running it after creating new note / tags modification of existing note.

Before 1st run you need to configure it (if you are using `~/Dropbox/Notes` as your root directory of notes, then everything should be setup) check the source and comments for more info.

Final file is looking like this:

```md
# Index Tags

- tag1
   - [note1.md](path/to/note1.md)
- tag2
   - subtag1
      - [note2.md](path/to/note2.md)
   - [note3.md](path/to/note3.md)

Last Update: timestamp
```

## FAQ

#### For who are created these scripts?

~~For me :P~~ For people which are migrating from *Bear* to pure markdown based notes.


#### Can I use this script, mention it somewhere?

Yes, if you are uploading it somewhere I will be more than happy if you put also link to this repo and mention me as author :)


#### Can you add [name your feature]?

Maybe, but rather not. This is purely hobbist project - if you want you can always fork this repo and create pull request.

[1]: https://bear.app/
[2]: https://typora.io/