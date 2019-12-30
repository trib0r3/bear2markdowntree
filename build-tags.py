import os
import glob
import datetime
from pathlib import Path
from json import loads

# Variables for handling location to notes directory
HOME_USER = str(Path.home())
NOTES_DIR = HOME_USER + "/Dropbox/Notes/" # FIXME:  add path to your Notes folder (relative to $HOME)

# Location of 'index' file for all indexed tags, change it if you want
# By default this file is stored in the root of your notes directory
TAGS_FILE = NOTES_DIR + "index.md"

# Work-tag (used only for script purposes), make sure that this tag is not used in your notes
ART_TAG = "__notes-qweewq1p1__"

# If you want ignore some tags in the final listing add them to this list
# WARNING: this feature is actually taking only subtag, 
#  Ex#1: you have note with tag: "dev/python/code-snippets"
#    if you decide to ignore tag "dev", then all subtags ("python", "code-snippets")  will be also ignored!
#  Ex#2: you have 2 notes with tags: note1: 'q/w/e', 'e/w/q' (you have the same subtab 'w', but in totally different subtrees)
#    Ignoring tag 'w' will affect BOTH subtrees, 
#    It isn't possible to ignore subtag only from specified tree! Ignoring "q/w" will not work!
IGNORE_TAGS = [] # FIXME

def get_files(path, extension):
    for filename in Path(path).rglob('*.' + extension):
        yield filename

def grab_tags_str(f):
    with open(f, 'r') as f:
        # simple file parsing
        ret = ""
        line = f.readline()
        if '---' in line:
            line = f.readline()
            while '---' not in line:
                ret += line.replace('\n', '').replace(' ', '').replace('tags:', '')
                line = f.readline()
            return ret
        else:
            return None


def parse_tags(tags_str, filename):
    # this func should parse tags and return them as separate objects:
    # simple (tag singleton)
    # complex (inherited tags)
    # tag objects are held as {}, articles are inside "arts" key in array
    arr = loads(tags_str)
    tags = {}

    for elem in arr:
        paths = elem.split('/')
        
        # find the leave
        ptr = tags
        while len(paths) != 0:
            v = paths[0]
            ptr[v] = {}
            ptr = ptr[v]
            paths.pop(0)
        ptr[ART_TAG] = [filename.replace(NOTES_DIR, './')] 

    return tags

def merge_tags(old, new):
    # divide & conquer

    if type(new) == list:
        # we are on the top of the tree
        return old + new
    else:
        # we need to traverse the tree
        for key, value in new.items():
            if key not in old:
                # key not exists, so just put it
                old[key] = value
            else:
                # we need to trave through tree
                old[key] = merge_tags(old[key], value)
        
        return old

def dump_tag(d, ret, indent=0, filler=' '):
    def sline(f, i, k):
        return "{}- {}\n".format(f * i * 3, k)

    for key, value in d.items():
        # FIXME blacklist may be too wide (for tags in diff path)
        if key in IGNORE_TAGS:
            continue
        
        # header
        if key == ART_TAG:
            indent -= 1
        else:
            ret += sline(filler, indent, key)

        if type(value) == list:
            for v in sorted(value):
                name = os.path.basename(v)
                #v = v.replace('[', '\[').replace(']', '\]')#.replace(' ', '\ ')
                ret += sline(filler, indent + 1, "[{}]({})".format(name, v))
        else:
            ret = dump_tag(value, ret, indent+1)
    
    return ret

def write_tags(tags):
    template = """#Index Tags

{}

```txt
Last Update: {}
```
"""
    
    md_text = dump_tag(tags, "")
    out = template.format(md_text, str(datetime.datetime.now()))
    with open(TAGS_FILE, 'w') as f:
        f.write(out)

def main():
    tags = {}
    # tags = { "tag1" : { "sub1" : { "art": [ "/path/to/art.md" ] }, "sub2" : { "subsub": { ... } } } }
    for f in get_files(NOTES_DIR, 'md'):
        try:
            tag_str = grab_tags_str(f)
            if tag_str is None:
                continue
            
            new = parse_tags(tag_str, str(f))
            tags = merge_tags(tags, new)
        except Exception as e:
            print("[Error]: Exception occured during processing file: {}".format(f))
        
    write_tags(tags)

if __name__ == "__main__":
    main()
