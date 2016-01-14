#import kitchen.text.converters as k
from nltk.corpus import wordnet as wn
import nltk
import os
import re

REFRESH_NUMBER = 10 #to check if things are still running

IGNORE_SEQ = '#' #if at beginning of the line, means not to process it...
excluded = ['(',')'] #exclude from tags looking for 'NN.'
not_found = ""
creator_leading_phrases = ['by', 'courtesy of', 'Photo:', 'Photos:']
wnl = nltk.WordNetLemmatizer()

objectTypeDict = {}
materialTypeDict = {}
docTypeDict = {}
dTypeToRole_map = {}


discriminating_figure_phrases = ['fig', 'fig.', 'table', 'tables'] #use str.lower() on input that is being compared to this list

#figure_pattern = (r'(\d+\.\d+\.\d+\.?\s*\w*)', re.VERBOSE)

# in below regexp, can't use \w because \w is alphaNUMERIC; need to match specifically letters...
rg = r"""(
    ^     # only counts as a match if the figure number is at the start of the line (should be enough of a check for most cases...)
    (
    \d+\.\d+   # captures x.x, that all figure captions will have. (Looks like a decimal number though...)
    (
    
    (
    \.\d+        # the last .x
    (\.?\s*[a-zA-Z]+)? # may contain a subfigure letter (with some spacing that shouldn't be there...), e.g. 2.4.7 b
    )
    
    |       #either all of the paren'd above if it looks like x.x.xx; or
          
    (\s*[a-zA-Z]*)   # a possible subfigure letter if it's eg 1.2a
    
    )    
    )
    )
    """
figure_num_pattern = re.compile(rg, re.VERBOSE)

book_title = not_found
year_published = not_found
book_description = not_found
editor = not_found
publisher = not_found
publisher_location = not_found
book_doi = not_found
book_isbn = not_found


###############################################
######### A bunch of declarations...###########
###############################################

#Worth noting: when writing to file, will need to convert strings to bytes using bytes(string, encoding scheme)

DELIMITER = '\t'  #will be tab-separated
ROW_DELIMITER = '\n'
IN_CELL_DELIMITER = ',' #when phrases need to be differentiated within a cell in the CSV
PERSONS_MAX = 10 #total number of people of a specific type, e.g. Creator or Author, in a row. Determined by Metadata Fields.txt.
                #To simplify code, all the different types of people have the same max.

excelHeader = ""
metadataFields = [] #list

book_title = 'Scaloria' #to be automated...


####
abspath = os.path.abspath(__file__)
lib_dir = os.path.dirname(abspath) #base, where main file is stored
root_dir = os.path.dirname(lib_dir) #takes the "head" of basename to get the rootname, i.e., where main should be
#os.path.dirname(path) is equivalent to os.path.split(path)[0]
dep_dir = os.path.join(root_dir, 'dependencies')
out_dir = os.path.join(root_dir, 'outputs')
####
####to get proper path to metadata fields



with open(os.path.join(dep_dir,"Metadata Fields.txt"), 'r') as mf:
        #may want to change the wording of the below lines, would mess up if there were more than one line
        for line in mf: #should only be the one line with column headers
                metadataFields = line.split('\t') #splits into list using comma as delimiter (for .csv)
        for entry in metadataFields:
                excelHeader = excelHeader + entry + DELIMITER
#        for line in mf:
#                metadataFields.append(line[:-1])    #line[:-1] removes '\n' from line
#                excelHeader = excelHeader + line[:-1] + DELIMITER
        #excelHeader has extra \t at end
        excelHeader = excelHeader[0:-1] #cut off last \t
        #excelHeader does NOT have a \n at the end



###########################################################
################## COPYPASTA FROM SAIS SCRIPT #############
###########################################################

####    HELPER FUNCTIONS    ####

def getWordInQuotes(s):
    "Takes in a string. Returns a string with the contents of the first word or phrase enveloped in double-quotes."
    "Returns an empty string if no quotes in string."
    "(For use with files containing lists of interest.)"
    "For example, \"I like pie!\" will return the string literal 'I like pie!' (with no '' surrounding it)."

    contents = ""
    i = j = 0

    if '\"' in s:
        i = s.find('\"')
        i += 1 #goes to right after the first quote

    if '\"' in s[i:]: #if another quote in rest of string, get it
        j = s.rfind('\"')
        if j == -1: #prevent backslicing if not located
            j = 0

    if i >= 0 and j > 0:
        contents = s[i:j]

#    print(i)
#    print(j)
#    print(contents)

    return contents

#test = "="
#print(getWordInQuotes(test))

##### TEST CASES ###
##
##extraQuotes = "\"I like pie!\""
##withoutQuotes = getWordInQuotes(extraQuotes)
##noQuotes = "I like pie!"
##
##print(withoutQuotes)
##print(extraQuotes)
##print(noQuotes)







##############
######### From Files Containing Controlled Vocabulary #########
##############

#text files are structured so that the master list of all possible entries starts with a "{". All entries are enclosed in quotes ("").
#Associations are denoted in the following way: the entry from the master list is written first, followed by an equals sign "=",
#followed by words that map to this first word, also in quotes.
#Each newline corresponds to a new masterword being mapped.
#If there is a line that may cause confusion or otherwise should not be parsed,
#place at least two backslashes ('\') at the front of the line.

### DICTS in shared.py



def formDictionaryfromFile(d, f):
    "Takes in a file with lines indicating dictionary values and associated keys. Forms the corresponding dictioary from this file."
    "The values of the dictionary are lists."
    "(Specifics as to file format is given in comments above.)"

    lines = f.readlines()
#    word = ""

    for line in lines:
        if len(line) >= 2 and line[0:2] == "\\":
                continue #allow to pass lines if necessary
#        word = ""
        
        unclean_words = line.split()
        words = unclean_words #want to test line below before including...
#        words = [g.wnl.lemmatize(word) for word in unclean_words] #use root-words (lemmas) to have to worry less about odd conjugations
        
#        print(words)
        
        x = 0
        n = len(words)
            
        while x < n:
#            print(x)
            s = getWordInQuotes(words[x])
            if s == "":     #if returns empty string, no "" in word, not one of the desired words
                words.remove(words[x])
                n = len(words) #to update the length of list, equivalent to " n -= 1 "
            else:
                words[x] = s #otherwise update with non-quoted word
                x += 1

        #print(words)

        
        if '{' in line and len(d) == 0: #'{' is what's used to recognize it's the line with all the keys
            for entry in words:
                d.setdefault(entry,[]).append(entry) #if the caption has the specific word itself, it maps to itself (i.e., a stela is a stela...)
                #setdefault checks to see if entry is in d (it shouldn't be); if not, it makes d[entry] = []. The append function then adds entry to the newly formed list

        #above if statement should occur before anything else. Use this to check which word to

        

        elif '=' in line and len(words) > 0 and words[0] in d.keys():   #'=' is used to recognize it has the words associated to the keys
            for x in range(1,len(words)):
                d.setdefault(words[0],[]).append(words[x])
       
       


#### MAKE SURE THAT the indices of the two lists correspond appropriately
list_of_maps = [objectTypeDict,
                materialTypeDict,
                docTypeDict,
                dTypeToRole_map]
list_of_files = ['objectType_list.txt',
                 'materialType_list.txt',
                 'docType_list.txt',
                 'docTypetoCreatorRole_map.txt']


for x in range(len(list_of_files)):
    with open(os.path.join(dep_dir, list_of_files[x]), 'r', encoding = 'iso-8859-1') as mapfile: #opens a mapfile from list_of_files
        formDictionaryfromFile(list_of_maps[x], mapfile) #and forms dictionary using matching entry in list_of_maps













#
###### COPYPASTA #####
#
#
################################################
########## A bunch of declarations...###########
################################################
#
##Worth noting: when writing to file, will need to convert strings to bytes using bytes(string, encoding scheme)
#
#DELIMITER = '\t'  #will be tab-separated
#IN_CELL_DELIMITER = ',' #when phrases need to be differentiated within a cell in the CSV
#PERSONS_MAX = 10 #total number of people of a specific type, e.g. Creator or Author, in a row. Determined by Metadata Fields.txt.
#                #To simplify code, all the different types of people have the same max.
#
#excelHeader = ""
#metadataFields = [] #list
#
#with open("Metadata_fields.csv", 'r') as mf:
#        for line in mf: #should only be the one line with column headers
#                metadataFields = line.split(',') #splits into list using comma as delimiter (for .csv)
#        for entry in metadataFields:
#                excelHeader = excelHeader + entry + DELIMITER
##        for line in mf:
##                metadataFields.append(line[:-1])    #line[:-1] removes '\n' from line
##                excelHeader = excelHeader + line[:-1] + DELIMITER
#        #excelHeader has extra \t at end
#        excelHeader = excelHeader[0:-1] #cut off last \t
#        #excelHeader does NOT have a \n at the end
#
