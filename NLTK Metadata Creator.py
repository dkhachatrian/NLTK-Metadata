# NLTK Metadata Creator.py

#import sys
#sys.path.insert(0, '.\\dependencies')
#sys.path.insert(0, 'E:/Work/dependencies/')
#sys.path.insert(0, './dependencies/')
#import helper_functions

#### To ensure the working directory starts at where the script is located...
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
####
from lib import helper_functions as hf
import nltk
#from nltk import corpus

first_names = nltk.corpus.names.words() # first names corpus, as a list, if necessary

with open('test.txt', 'r') as f:
    for line in f:
	n = hf.get_Chapter_Num(line)
	tokens = nltk.word_tokenize(line) #break line into word "tokens"
	tagged = nltk.pos_tag(tokens) #assign tags to token's role in sentence
        entities = nltk.ne_chunk(tagged)
        tList = list(entities.subtrees(lambda t: t.label() == 'PERSON')) #argument provided to subtree serves as filter (by label)
		
	people = hf.clean_List_Of_People(tList, line)


