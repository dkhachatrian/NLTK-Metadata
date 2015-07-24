#!/usr/bin/python
# -*- coding: utf-8 -*-
import nltk
#import codecs  #Python 2

#### To ensure the working directory starts at where the script is located...
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
####


#with codecs.open("Scaloria Figure Captions.txt", 'r', encoding = 'utf-8') as f:    #Python 2
with open("Cleaned Captions.txt", 'r', encoding = 'utf-8') as f:
        with open("Capitalized_Word_List.txt" , 'w', encoding = 'utf-8') as w:
                lines = f.readlines()

                for line in lines:
                    s = line
#                    s = line.decode('utf8')    #Python 2 (?)
                    tokens = nltk.word_tokenize(s) #break line into word "tokens"
                    tagged = nltk.pos_tag(tokens) #assign tags to token's role in sentence
                    entities = nltk.ne_chunk(tagged)
                    proper_nouns = [n[0] for n in tagged if 'NNP' in n[1]] #list of nouns in line (second entry in tuple gives tag)

                    if len(proper_nouns) > 0:
                                w.write("List of capitalized phrases found in " + s.split()[0] + " are the following: " + '\n')
                                for noun in proper_nouns:
                                        w.write(noun + '\t')
                                for x in range(2):
                                        w.write('\n') #twice to make it easier on the eyes to separate captions

