# NLTK Metadata Creator.py

#### To ensure the working directory starts at where the script is located...
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
####


#### To have Python look for the modules where I want them to)
import sys
#sys.path.insert(0, os.path.join(dname, 'dependencies'))
sys.path.insert(0, os.path.join(dname, 'lib'))
s#ys.path.insert(0, '.\\lib')
#sys.path.insert(0, 'E:/Work/dependencies/')
#sys.path.insert(0, './dependencies/')
#import helper_functions

#import sys
#if sys.hexversion < 0x030000a1: #hex value corresponds to 3.0.0rev1
#    from __future__ import print_function

#import helper_functions.*
#from helper_functions import * #figure out how to get this to work?
from lib import helper_functions as hf

import nltk
from nltk.corpus import wordnet as wn

#keywords = [] #will be built from words given by authors
with open('Keywords.txt', 'r') as kw:
    keywords = hf.build_keywords_from_file(kw)
expanded_keywords = {}
                
text_file = os.path.join(dname, 'test.txt')
#first_names = nltk.corpus.names.words() # first names corpus, as a list, if necessary

with open(text_file, 'r') as f:
    for fline in f:
        line = hf.Line(fline)
	cNum = line.get_chapter_num()
	nouns = line.get_nouns()
	people = line.get_people()
	
        for noun in nouns:
            if noun in keywords or hf.is_in_container(noun, expanded_keywords):
                pass
                


#### SCRATCHPAD ####
#Things from NLTK that will likely be of use.
### Wordnet (see Chapter 2 Section 5 of NLTK Book)


### When writing to file, will need to encode the unicode (== "str" in Python 3)  with s.encode('utf8')



            
    

















##### COPYPASTA #####


###############################################
######### A bunch of declarations...###########
###############################################

#Worth noting: when writing to file, will need to convert strings to bytes using bytes(string, encoding scheme)

DELIMITER = '\t'  #will be tab-separated
IN_CELL_DELIMITER = ',' #when phrases need to be differentiated within a cell in the CSV
PERSONS_MAX = 10 #total number of people of a specific type, e.g. Creator or Author, in a row. Determined by Metadata Fields.txt.
                #To simplify code, all the different types of people have the same max.

excelHeader = ""
metadataFields = [] #list

with open("Metadata_fields.csv", 'r') as mf:
        for line in mf: #should only be the one line with column headers
                metadataFields = line.split(',') #splits into list using comma as delimiter (for .csv)
        for entry in metadataFields:
                excelHeader = excelHeader + entry + DELIMITER
#        for line in mf:
#                metadataFields.append(line[:-1])    #line[:-1] removes '\n' from line
#                excelHeader = excelHeader + line[:-1] + DELIMITER
        #excelHeader has extra \t at end
        excelHeader = excelHeader[0:-1] #cut off last \t
        #excelHeader does NOT have a \n at the end

