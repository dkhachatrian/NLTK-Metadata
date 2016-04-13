# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 14:40:15 2016

@author: dkhachatrian
"""

#### To ensure the working directory starts at where the script is located...
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
####

import urllib.request #lets us request information (GET) from websites
import urllib.parse #helps encode POST request parameters

# example: urllib.parse.urlencode(dictionaryOfVariableNamesToValues)
# data = data.encode('uft-8') //converts data (e.g. dictionary) to bytes


# open our file with all the caption lines separated by newlines

PRECONDITION: have a sanitized caption file




for each line in the file:
  request an annotation of the line with confidence=0.35(?) to URL http://spotlight.sztaki.hu:2222/rest/annotate
  save into a hashmap file lineNumber->annotatedText i(use linked list?) //so we don't have to call DBPedia service constantly...
  
  for each annotated phrase:
      follow associated link //surrounded by <a href="http://www.example.com">example text</a>
      get page source
      search for and grab the information of interest // classification (the word(s) that comes after "An Entity of Type : ") 
      save into a hashmap (word->DBPType) //we will manually create a common-sense mapping of DBPedia type -> our types
      


// later, when actually making spreadsheet,
// will search for values in the hashmaps (line->annotatedText->dbpediaType->ourType) for each entity
// (This will have trouble coupling names with roles...)