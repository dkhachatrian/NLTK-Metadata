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
        with codecs.open("Content_Words_List.txt" , 'w', encoding = 'utf-8') as w:
                lines = f.readlines()

                for line in lines:
                    #print(line)
                    u = k.to_unicode(line, encoding = 'utf-8')
                    s = hf.Line(u)
                    tuples = s.get_content_tuples()
                    tokens = [t[0] for t in tuples]
                    cList = hf.consolidate_tokens(tokens, line)
                    tList = [] #tuple list
                    
                    for phrase in cList:
                        for t in tuples:
                            if phrase.split()[-1] in t[0]: #phrase.split()[-1] = first word of phrase, should have corresponding pos tag in tuples
                                tList.append( (phrase, t[1]) )
                    
                    
                    #people = s.get_people()

                    if len(tList) > 0:
                                w.write(g.IGNORE_SEQ + "List of content words longer than two characters found in " + line.split()[0] + " are the following: " + '\n')
                                for tuple in tList:
                                    if len(tuple[0]) > 2:
                                        w.write(tuple[0] + ': ' + tuple[1] + '\t' + '\t')
#                                w.write('\n' + "And the people found in this caption are the following: " + '\n')
#                                for person in people:
#                                    w.write(person + '; ')
                                ##debugging...
                                #w.write("Corresponding tuples:" + '\n')
                                #for tup in all_tuples:
                                #    w.write(str(tup) + '\t')
                                #    
                                for x in range(2):                                      
                                    w.write('\n')
                                w.write(g.IGNORE_SEQ + "And the caption the above list came from is the following: '\n'")
                                w.write(g.IGNORE_SEQ + u)
                                for x in range(3):
                                    w.write('\n') #thrice to make it easier on the eyes to separate captions

