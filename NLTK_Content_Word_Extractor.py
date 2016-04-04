#!/usr/bin/python
# -*- coding: utf-8 -*-

#os.path.join(path, path, ...)
#### To ensure the working directory starts at where the script is located...
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath) #base, where main file is stored
os.chdir(dname)
####
#import nltk
#import codecs  #Python 2
from lib import helper_functions as hf
#import kitchen.text.converters as k
from lib import shared as g

dep = os.path.join(dname, 'dependencies') #gives ./dependencies/, for easier file opening
#probably will require os.sep, the directory separating constant



def extract_words(f,w):
    
                lines = f.readlines()

                i = 0

                for line in lines:
                    
                    if i < 20:
                        i+=1
                    elif i == 20:
                        print('Yup, still going...')
                        i = 0
                    
                    #print(line)
                    #u = k.to_unicode(line, encoding = 'utf-8')
                    u = line#.replace('“', '"').replace('”', '"') #should remove those annoying smart-quotes...
                    s = hf.Line(u)
                    tuples = s.get_content_tuples()
                    #tokens = [t[0] for t in tuples]
                    tList = hf.consolidate_tokens(tuples, line)
                    
                   ####Above code makes the extractor print a SET of words, not a LIST of words!
                    tSet = []
                    for tup in tList:
                        if len(tSet) == 0:
                            tSet.append(tup)
                        elif tup[0] not in [n[0] for n in tSet]: #if the string isn't already in the set of tuples...
                            tSet.append(tup)                           
                   #### 
                    
                    #tSet = set(tList) #ERROR! Lists (two-entry lists ~= tuples) are not hashable...
#                    tList = [] #tuple list. Contains (phrase, appropriate part-of-speech tag)
                    
#                    for phrase in cList:
#                        for t in tuples:
#                            if phrase.split()[-1] in t[0]: #phrase.split()[-1] = first word of phrase, should have corresponding pos tag in tuples
#                                tList.append( (phrase, t[1]) ) #
                    
                    
                    #people = s.get_people()

                    if len(tSet) > 0:
                                w.write(g.IGNORE_SEQ + "A set of the content words/phrases longer than two characters found in " + line.split()[0] + " are the following: " + '\n')
                                for tup in tSet:
                                    if len(tup[0]) > 2:
                                        w.write(tup[0] + ': ' + tup[1] + '\t' + '\t')
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
                                w.write(g.IGNORE_SEQ + "And the caption the above set came from is the following: '\n'")
                                w.write(g.IGNORE_SEQ + u)
                                for x in range(3):
                                    w.write('\n') #thrice to make it easier on the eyes to separate captions

                print('Done!')
                
                
#with codecs.open("Scaloria Figure Captions.txt", 'r', encoding = 'utf-8') as f:    #Python 2
with open(os.path.join(dep,"Cleaned Captions.txt"), 'r', encoding = 'utf-8') as f:
        with open(os.path.join(dep,"Content_Words_Set.txt"), 'w', encoding = 'utf-8') as w:
            extract_words(f,w)
            