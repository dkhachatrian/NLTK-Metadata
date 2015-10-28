import kitchen.text.converters as k
from nltk.corpus import wordnet as wn

IGNORE_SEQ = '#' #if at beginning of the line, means not to process it...
excluded = ['(',')'] #exclude from tags looking for 'NN.'s
not_found = ""
creator_leading_phrases = ['by', 'courtesy of']
wnl = nltk.WordNetLemmatizer()

objectTypeDict = {}
materialTypeDict = {}
docTypeDict = {}
dTypeToRole_map = {}
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
