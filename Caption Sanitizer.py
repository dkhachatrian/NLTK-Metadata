# -*- coding: utf-8 -*-
## Caption Sanitizer (puts captions on same line)

#### To ensure the working directory starts at where the script is located...
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
####

import re

def sanitize_Caption_File(i, o):
    """ Takes in a file for input and a file to ouptput. Creates a new file where there are no '\n' within a single caption
    (denoted by a line beginning with the form '*.*.*'. """
    
    ## Regular expression match below gotten from txt2re.com
    #### These are most likely the lines that need to be changed...
    
    re1='(\\d+)'	# Integer Number 1
    re2='(\\.)'	# Any Single Character 1
    re3='(\\d+)'	# Integer Number 2
    re4='(\\.)'	# Any Single Character 2
    re5='(\\d+)'	# Integer Number 3
    
    rg = re.compile(re1+re2+re3+re4+re5,re.IGNORECASE|re.DOTALL)
    s = ''
    lines = i.readlines()
    
    for line in lines:
        ### replace tabs with spaces so it doesn't confuse the tab-delimited .txt file...
        cleanLine = ''
        for ch in line:
            if ch == '\t':
                cleanLine += ' '
            elif ch == '\n':
                pass
            else:
                cleanLine += ch
                
        num = sum(1 for m in re.finditer(rg, cleanLine[:10]))
        #caption number should be in the beginning of the line...
        
        if num != 1and len(s) == 0: #no caption number associated with lines before it...
            continue
        elif num != 1 and len(s) > 0:
            s += ' ' + cleanLine
        elif num == 1 and len(s) == 0:
            s = cleanLine
        elif num == 1 and len(s) > 0:
            o.write(s + '\n' + '\n')
            s = cleanLine

with open('Scaloria Figure Captions.txt', 'r') as f1:
    with open('Cleaned Captions.txt', 'w') as f2:
        sanitize_Caption_File(f1,f2)
