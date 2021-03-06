# NLTK Metadata Creator.py

#### To ensure the working directory starts at where the script is located...
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
####


#### To have Python look for the modules where I want them to)
#import sys
#sys.path.insert(0, os.path.join(dname, 'dependencies'))
#sys.path.insert(0, os.path.join(dname, 'lib'))
#sys.path.insert(0, '.\\lib')
#sys.path.insert(0, 'E:/Work/dependencies/')
#sys.path.insert(0, './dependencies/')
#import helper_functions


#import sys
#if sys.hexversion < 0x030000a1: #hex value corresponds to 3.0.0rev1
#    from __future__ import print_function

#import helper_functions.*
#from helper_functions import * #figure out how to get this to work?
from lib import helper_functions as hf
from lib import shared as g

#import nltk
#from nltk.corpus import wordnet as wn

#keywords = [] #will be built from words given by authors
#with open(os.path.join(dname, 'dependencies', 'Keywords.txt'), 'r') as kw:
#    keywords = hf.build_keywords_from_file(kw) 
#expanded_keywords = hf.build_expanded_keywords(keywords)
                
captions = os.path.join(g.dep_dir, 'Cleaned Captions.txt') #the captions
output = os.path.join(g.out_dir, 'Caption Metadata.txt')
#first_names = nltk.corpus.names.words() # first names corpus, as a list, if necessary


#now that I have the expanded keywords, a list of list of strings,
#we can see whether these words are found in a line. 



####

#####
########
#########
#########   Now for each line, let's see if I can find the words of interest in my extended keywords
#########   If I can, look up that word in our list of associations (TODO: set up list of associations)
#########   and then spit it out for the field...

i = 0
j = 1

with open(captions, 'r') as r:
    with open(output, 'w') as o:
        r_lines = r.readlines()
        
        o.write(g.excelHeader + g.ROW_DELIMITER)
                
        
        for r_line in r_lines:
            
            ### to ensure things are still moving...
            if i < g.REFRESH_NUMBER:
                i+=1
            elif i == g.REFRESH_NUMBER:
                print("Yup, still going... Number of times you've seen this message: " + str(j))
                j += 1
                i = 0
            

            line = hf.Line(r_line)
            
            s = line.get_info_for_file()
            o.write(s + g.ROW_DELIMITER)
        
        

        
#        cNum = line.get_chapter_num()
#        nouns = line.get_nouns()
#        people = line.get_people()
#	
#        for noun in nouns:
#            loc_info = hf.in_container(noun, expanded_keywords) # gives a tuple, (the element in which
#            if noun in keywords or loc_info != (None, -1):
#                pass
                


#### SCRATCHPAD ####
#Things from NLTK that will likely be of use.
### Wordnet (see Chapter 2 Section 5 of NLTK Book)


### When writing to file, will need to encode the unicode (== "str" in Python 3)  with s.encode('utf8')


