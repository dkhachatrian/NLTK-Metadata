# NLTK Metadata Creator.py

#import sys
#sys.path.insert(0, '.\\dependencies')
#sys.path.insert(0, 'E:/Work/dependencies/')
#sys.path.insert(0, './dependencies/')
#import helper_functions

#import sys
#if sys.hexversion < 0x030000a1: #hex value corresponds to 3.0.0rev1
#    from __future__ import print_function

#### To ensure the working directory starts at where the script is located...
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
####
from lib import helper_functions as hf

import nltk
#from nltk import corpus

text_file = os.path.join(dname, 'test.txt')
#first_names = nltk.corpus.names.words() # first names corpus, as a list, if necessary

with open(text_file, 'r') as f:
    for line in f:
	n = hf.get_Chapter_Num(line)
	tokens = nltk.word_tokenize(line) #break line into word "tokens"
	tagged = nltk.pos_tag(tokens) #assign tags to token's role in sentence
        entities = nltk.ne_chunk(tagged)
        tList = list(entities.subtrees(lambda t: t.label() == 'PERSON')) #argument provided to subtree serves as filter (by label)
		
	people = hf.clean_List_Of_People(tList, line)




#### SCRATCHPAD ####
#Things from NLTK that will likely be of use.
### Wordnet (see Chapter 2 Section 5 of NLTK Book)
# from nltk.corpus import wordnet as wn
# wn.synset('car.n.01').lemma_names() Wordnet synonym set for words...


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

