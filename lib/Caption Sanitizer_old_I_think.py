# -*- coding: utf-8 -*-
## Caption Sanitizer (puts captions on same line)

#### To ensure the working directory starts at where the script is located...
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
####

dep = os.path.join(dname, 'dependencies')


import re
#import codecs
#import kitchen.text.converters as k
import string
import shared as g
import helper_functions as hf

def sanitize_Caption_File(i, o):
    """ Takes in a file for input and a file to ouptput. Creates a new file where there are no '\n' within a single caption
    (denoted by a line beginning with the form '*.*.*'. """
    
    ## Regular expression match below gotten from txt2re.com
    #### These are most likely the lines that need to be changed...
    
  #  sw = codecs.StreamWriter(o)
    
    re1='(\\d+)'	# Integer Number 1
    re2='(\\.)'	# Any Single Character 1
    re3='(\\d+)'	# Integer Number 2
    re4='(\\.)'	# Any Single Character 2
    re5='(\\d+)'	# Integer Number 3
    
    rg = re.compile(re1+re2+re3+re4+re5,re.IGNORECASE|re.DOTALL)
    s = ''
   # chf = False #chf = CaptionHeaderFound
    lines = i.readlines()
    
    i = 0 #to make sure it's running...    
    
    #sw = codecs.StreamWriter(o)
    
    for line in lines:
        cleanLine = ''

        u = line.replace('“', '"').replace('”', '"') #removes smart-quotes?

        #check if things are still running...

        if i < 20:
            i+=1
        elif i == 20:
            print('Yup, still going...')
            i = 0
        

        #uLine = k.to_unicode(line) #defaults to utf-8
        ### replace tabs with spaces so it doesn't confuse the tab-delimited .txt file...

        for ch in u:
            if ch in string.whitespace:
                cleanLine += ' '
            #elif ch == '“' or ch == '”': #refers to smartquotes
            #    cleanLine += '"'
            #elif ch == '\n':
            #    continue
            else:
                cleanLine += ch
                
        
        
        num = sum(1 for m in re.finditer(rg, cleanLine[:10]))
        
        cleanLine = re.sub(r' +', ' ', cleanLine)
        #caption number should be in the beginning of the line...
        #
        #if line == '\n':
        #    o.write('\n')
        #elif num == 1:
        #    o.write('\n' + cleanLine + ' ') #newline to make sure there's at least some separation
        #elif num != 1:
        #    o.write(cleanLine + ' ')
        #    
        #
        if num != 1 and len(s) == 0: #no caption number associated with lines before it...
            continue
        elif num != 1 and len(s) > 0: #no match, s i
            s += cleanLine
        elif num == 1 and len(s) == 0:
            s = cleanLine
        elif num == 1 and len(s) > 0:
            o.write(s + '\n' + '\n')
            s = cleanLine
            
    if len(s)>0:
        o.write(s) #for anything remaining...
    
    print('Done!')
    #clean up spacing with NLTK (because for some reason, unless I used string.whitespace, I couldn't deal with \t and \n as I wanted...)
    #not necessary?
    

with open(os.path.join(dep,"Figure Captions.txt"), 'r', encoding = 'utf-8') as f1:
    with open(os.path.join(dep,"Cleaned Captions.txt"), 'w', encoding = 'utf-8') as f2:
        sanitize_Caption_File(f1,f2)
