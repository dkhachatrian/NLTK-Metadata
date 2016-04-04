#!/usr/bin/python
# -*- coding: utf-8 -*-

#os.path.join(path, path, ...)
#### To ensure the working directory starts at where the script is located...
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
####
#import nltk
import codecs  #Python 2
from lib import helper_functions as hf
import kitchen.text.converters as k
from lib import shared as g

#with codecs.open("Scaloria Figure Captions.txt", 'r', encoding = 'utf-8') as f:    #Python 2
with codecs.open("Cleaned Captions.txt", 'r', encoding = 'utf-8') as f:
        with codecs.open("Capitalized_Word_List.txt" , 'w', encoding = 'utf-8') as w:
                lines = f.readlines()

                for line in lines:
                    #print(line)
                    u = k.to_unicode(line, encoding = 'utf-8')
                    s = hf.Line(u)
                    proper_nouns = s.get_proper_nouns()
                    people = s.get_people()

                    if len(proper_nouns) > 0:
                                w.write(g.IGNORE_SEQ + "List of capitalized phrases found in " + line.split()[0] + " are the following: " + '\n')
                                for noun in proper_nouns:
                                    w.write(noun + '\t')
                                w.write('\n' + g.IGNORE_SEQ + "And the people found in this caption are the following: " + '\n')
                                for person in people:
                                    w.write(person + '; ')
                                ##debugging...
                                #w.write("Corresponding tuples:" + '\n')
                                #for tup in all_tuples:
                                #    w.write(str(tup) + '\t')
                                #    
                                for x in range(3):
                                    w.write('\n') #twice to make it easier on the eyes to separate captions

