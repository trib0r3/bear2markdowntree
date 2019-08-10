import re
import os
import sys

# NOTICE!
# Before run you have to:
#   0. Create NOTE_DIR and BEAR_DIR dirs 
#   1. Run commands near `files = [` and `dirs = [`
#   2. Paste the results in shown format
# Optionally you can also change below config dirs

# config dirs
NOTE_DIR = "Notes/"         # output dir
BEAR_DIR = "BearNotes/"     # input dir
ASSETS_DIR = NOTE_DIR + "{tag}/.{notename}.assets"

# find . -type f -name '*md'
files = [
    "note.md" 
]

# find . -type d
dirs = [
    "note"
]

def get_attachments(note):
    d = note[:-3]
    if d in dirs:
        return d
    else:
        return None

def export():
    print("Using paths:\nNOTE_DIR: {}\nBEAR_DIR: {}")
    cont = input("Do you wish to continue? (y/n")
    if cont not in ['y', 'Y']:
        return

    for note in files:
        TAG_PATTERN = r'[^\(](\#[aA-zZ][aA-zZ0-9-_//]+)'

        mdtext = ""
        # BearNote/guide.md
        with open(BEAR_DIR + note, 'r') as f:
            mdtext = f.read()
        
        # find tags
        temp = re.findall(TAG_PATTERN, mdtext)
        tags = []
        for t in temp:
            if "include" not in t and "define" not in t:
                tags.append(t.replace('#', ''))

        if len(tags) == 0:
            import code; code.interact(local=locals())

        # replace bad markup
        mdtext = mdtext.replace('::', '==')
        
        # prepare tags
        # Notes/cheat/foo/guide.md
        n = len(tags)
        tag = 0
        if n > 1:
            tag = -1
            while tag not in range(n):
                print("\n[?] {}: Which tag do you prefer to keep? ([e]dit)".format(note))
                for i in range(n):
                    print("[{}] {}".format(i, tags[i]))
                tag = input("[default: 0]> ")
                
                # pass the default value
                if tag == '':
                    tag = 0
                elif tag == 'e':
                    print(tags)
                    import code; code.interact(local=locals())
                    tag = -1
                    n = len(tags)
                else:
                    try:
                        tag = int(tag)
                    except:
                        tag = -1
        else:
            tag = 0

        try:
            tag = tags[tag]
        except:
            import code; code.interact(local=locals()) 
        
        # remove real tags
        for t in tags:
            mdtext = mdtext.replace('#' + t, '')

        # append file with yaml tags section
        mdtext = "---\ntags: [{}]\n---\n".format(",".join(['"{}"'.format(e) for e in tags])) + mdtext
        # mdtext = re.sub(TAG_PATTERN, '', mdtext)

        # prepare dirs
        dst_path = NOTE_DIR + tag
        os.makedirs(dst_path, exist_ok=True)

        attachment = get_attachments(note)
        if attachment is not None:
            dst_assets = ASSETS_DIR.format(tag=tag, notename=attachment)
            os.rename(BEAR_DIR + attachment, dst_assets)
            
            # replace old paths
            mdtext = mdtext.replace('(' + attachment, "(.{notename}.assets".format(notename=attachment))

        for bear_link in re.findall(r'bear://.*', mdtext):
            print("{}: Unmovable url found: '{}'".format(note, bear_link))

        with open(dst_path + '/' + note , 'w') as f:
            f.write(mdtext)
            print('--> Processed:', note, 'tags: ', tags)

def main():
    global NOTE_DIR
    global BEAR_DIR

    if len(sys.argv) == 3:
        NOTE_DIR = sys.argv[1]
        BEAR_DIR = sys.argv[2]
        export()
    else:
        export()
    
if __name__ == "__main__":
    main()