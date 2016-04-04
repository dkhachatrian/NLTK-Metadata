# -*- coding: utf-8 -*-
### Helper functions for metadata creation ###
from nltk.corpus import wordnet as wn
import nltk#
from lib import shared as g
#import kitchen.text.converters as k
import re


######## DOWNLOADING NECESSARY COMPONENTS FROM NLTK ##############

# ...For now, will install everything from NLTK,
# because the list of models that needs to be installed is too long for my tastes





#installed = nltk.downloader.download('all')
#if not installed:
#    raise ValueError('NLTK did not install! Lines cannot be processed! All hope is lost!')








### When we try to go a bit leaner...
#components = ['punkt', 'averaged_perceptron_tagger']
#for c in components:
#    installed = nltk.downloader.download(c)
#    
#    #checks to see that everything installed properly
#    if not installed:
#        raise ValueError(c + 'did not install! Lines cannot be processed!')
#        #assumes internet connection?...
#        
    
#TODO: find a way to check for punkt's existence without this
#(not a normal module, so can't check using
#'punkt' in sys.modules
#...)

#IGNORE_CHAR = '#'

class Line:
    def __init__(self, s = ''):
        self.raw_text = s
        self.tokens = nltk.word_tokenize(s) #break line into word "tokens"
        self.tagged = nltk.pos_tag(self.tokens) #assign tags to token's role in sentence
        self.entities = nltk.ne_chunk(self.tagged)
        self.people = self.get_people()
        self.lemmas = self.get_lemmas()
        self.creator = self.get_creator()
        self.docType = self.get_doc_type()
        
    def get_nouns(self):
        """Returns the nouns in Line as a list."""
        return [w[0] for w in self.tagged if 'NN' in w[1]] #list of nouns in line (second entry in tuple gives tag)
        
    def get_proper_nouns(self):
        """Returns the nouns in Line as a list."""
        excluded = ['(',')'] #unwanted in list. Parentheses are tagged with 'NNP'
        return [n[0] for n in self.tagged if ('NNP' in n[1] and n[0] not in excluded and n[0][0].isupper())] #list of nouns in line (second entry in tuple gives tag)
        #checks to see if it's tagged with 'NNP', isn't a paren, and is capitalized
        
    def get_people(self):
        """Returns the names of the people in that line as a list of strings."""
        excluded = ['(',')'] #unwanted in list. Parentheses are tagged with 'NNP'
        nnp = [n[0] for n in self.tagged if ('NNP' in n[1] and n[0] not in excluded and n[0][0].isupper())] #list of nouns in line (second entry in tuple gives tag)
        #checks to see if it's tagged with 'NNP', isn't a paren, and is capitalized

        return consolidate_tokens(nnp, self.raw_text)
        
    def get_content_tuples(self):
        """Returns a list of tuples (word, tag), with all adjectives, verbs, and nouns in the line."""
        excluded = ['(',')']
        toi = ['NN', 'VB', 'JJ'] #tags of interest: noun, verb, adjective
        return [w for w in self.tagged if (len(w[0])>1 and w[1][:2] in toi and w[0] not in excluded)]

    def get_lemmas(self):
        """Returns a list of lemmas (root-words) for the tokens in the line."""
        

        nouns = self.get_nouns()
        lwc = [noun.lower() for noun in nouns]
        s = set(lwc)
        
        lemmas = [g.wnl.lemmatize(t) for t in s] 
        
        return lemmas
    
    

    def get_chapter_num(self):
        """Takes in a string. Returns as a string, if existent, the number
        proceeding the string 'Chapter ' in the string."""
        s = self.raw_text
        x = -1
        y = -1
        keyString = 'Chapter '
        if keyString in s:
            x = s.index(keyString) + len(keyString)
            y = x
    
            while self[y].isdigit():
                y += 1
    	   
        return self[x:y]

    def get_figure_num(self):
        """Uses the unicode text to output the figure number (as unicode)."""

        #copypasta from txt2re.com with a bit of modification...
        #as we get weirder and weirder formats, we'd have to expand our regexp to look for these other formats
        
        re1='.*?'	# Non-greedy match on filler
        re2='\\d+'	# Uninteresting: int
        re3='.*?'	# Non-greedy match on filler
        re4='\\d+'	# Uninteresting: int
        re5='.*?'	# Non-greedy match on filler
        re6='(\\d+)'	# Integer Number 1
        
        rg = re.compile(re1+re2+re3+re4+re5+re6,re.IGNORECASE|re.DOTALL)
        m = rg.search(self.raw_text)
        if m:
            int1=m.group(1)
            return str(int1)
        else:
            return g.not_found
    
    def get_caption(self):
        """Returns caption (after figure number)."""
        
        #copypasta from txt2re.com with a bit of modification...
        #as we get weirder and weirder formats, we'd have to expand our regexp to look for these other formats
        
        re1='((?:(?:[0-2]?\\d{1})|(?:[3][01]{1}))[-:\\/.](?:[0]?[1-9]|[1][012])[-:\\/.](?:(?:\\d{1}\\d{1})))(?![\\d])'	# DDMMYY 1
        re2='.*?'	# Non-greedy match on filler
        re3='(\\s+)'	# White Space 1
        
        rg = re.compile(re1+re2+re3,re.IGNORECASE|re.DOTALL)
        m = rg.search(self.raw_text)
        if m:   #we'll bypass the figure number...
            ddmmyy1=m.group(1)
            c1=m.group(2)
            ws1=m.group(3)
            l = len(ddmmyy1) + len(c1) + len(ws1) #get the length of the figure number and whitespace
            return self.raw_text[l:] #return the substring of everything after the figure number
        else:
            return g.not_found
    
    def get_copyright(self):
        """Returns associated copyright privilege level."""
        #unless I get some file explaining the permissions, let's pass...
        return g.not_found
    
    def get_object_type(self):
        """Given the string, returns a guess of what type of object is being described in the caption (as unicode)."""
        
        targets = ""                        
                    
        for lemma in self.lemmas: #for each noun chunk
            for key in objectTypeDict:
                if lemma in objectTypeDict[key]: #xxxTypeDict[key] is a list containing words that map to the term "key"
                    targets += key + ', '
        
        if len(targets) > 2: #targets is a string, not the number of actual matches
            targets = targets[:-2]    #remove last set of ', '      
        return targets 
        
            #look to see if it can be found in the corresponding dict
        #if so
            #look in the word associations dictionary to see what object type the word maps to
        #otherwise
            #return nothing
        
    def get_material_type(self):
        """Returns a guess of what sort of material was used to create the object described in the caption (as unicode)."""
        #### SEE GET_OBJECT_TYPE         
        
        targets = ""                        
                    
        for lemma in self.lemmas: #for each noun chunk
            for key in materialTypeDict:
                if lemma in materialTypeDict[key]: #xxxTypeDict[key] is a list containing words that map to the term "key"
                    targets += key + ', '
        
        if len(targets) > 2: #targets is a string, not the number of actual matches
            targets = targets[:-2]    #remove last set of ', '      
        return targets 
    
    def get_doc_type(self):
        """Returns a guess of how the figure was captured (as unicode)."""
        #### SEE GET_OBJECT_TYPE         
        
        targets = ""                        
                    
        for lemma in self.lemmas: #for each noun chunk
            for key in docTypeDict:
                if lemma in docTypeDict[key]: #xxxTypeDict[key] is a list containing words that map to the term "key"
                    targets += key + ', '
        
        if len(targets) > 2: #targets is a string, not the number of actual matches
            targets = targets[:-2]    #remove last set of ', '      
        return targets 
    
    
    def get_creator(self):
        """Guesses the creator of the figure from caption text. Returns as unicode."""
        
        s = self.raw_text
        
        for name in self.people: #look through the names
            for phrase in g.creator_leading_phrases:
                if phrase in s:
                    if s.index(phrase) + len(phrase) + len (' ') == s.index(name): #if an obvious lead-up like "by" or "courtesy of" comes before the name
                        return name #return the name
        #else return ""                
        return g.not_found


    def get_creator_role(self):
        """Returns creator's role."""
        creatorRole = g.not_found
        
        if self.creator != g.not_found and self.docType != g.not_found: #if there's a doc type and creator
            creatorRole =  dTypeToRole_map[self.docType]#look up corresponding tuple in doc-->role dictionary
        return creatorRole
    
    def get_cultural_term(self):
        """Returns guess of cultural term by comparing chunks to a given dict."""
        pass #no such dict quite yet

    def get_date_type(self):
        pass
    
    def get_temporal_term(self):
        pass
    
    def get_geographic_term(self):
        pass
    
    def get_status(self):
        """Returns status of caption, which, when first uploading, is always 'Needs Review.'"""
        return 'Needs Review.'
        
    def get_permissions(self):
        pass
    
    def get_image(self):
        """Returns image."""
        pass #don't have those files on this computer, and wouldn't be able to do much with them anyway...
        
    def write_to_file(self):
        """Writes out information contained in Line in the order described by the metadata field headers.
        Uses in-cell and between-cell delimiters as defined in globals.py"""
        
        pass

#def tree_to_list(t, l):
#    """Takes in an object that may be a tree, and an empty list l.
#    If object is a tree, returns the tree and its subtrees as lists in l. Otherwise return object unchanged."""
#    
#    if type(t) is nltk.Tree:
#        if len(t) == 1 and type(t[0]) == tuple:
#            l.append(list(t))
#        elif len(t) == 0:
#            return []
#        else:
#            for st in t.subtrees(lambda t: t.height() == 2): #Trees are iterable over their children
#                tree_to_list(t)

def consolidate_tokens(l,s):
    """Takes in a list of strings, and the original line. Checks that they're chunked properly.
    If any Persons only have a first name, uses the original line to check if improperly chunked.
    Returns a checked list of strings, each string corresponding to a person's name."""
    
    result = []
    
    if len(l) == 0:
        return result
    
        
    
    for x in range(len(l)):
        temp = []
        #l[x] is a singular person's name in tuples along with position tag. l[x][y][0] gives the y'th part of the name.
        i = 0
        temp.append(l[x+i]) #first word...
        while x + i + 1 < len(l): #while the next "Persons" after them also obinly have one part of a name
            dist = abs(s.find(l[x+i]) + len(l[x+i]) - s.find(l[x+i+1]))
            if dist == 1: #if the distance between the two "Persons" is less than one char away (i.e. there's a ' ' between the two)
                temp.append(l[x+i+1]) #add the consecutive words...
                i += 1 #increment i
            else:
                break
        x += i #update x after matching together string    
        
        if len(temp) > 1: #if there were a set of words in a row,
            t = ' '.join(temp)
            result.append(t)
       
    return result

def in_container(e, c, n = 0):
    """ Takes an entry to search for and a container, which may contain containers.
    Returns the index in the main container which holds the entry and the number of levels deep in the subcontainer the entry is located.
    (For example cases, see below.)
    If entry not found, returns (None, -1). """
    
    #Examples: for li = ['albert', ['brenda', 'carl'], 'david', [['evelyn']]]
    #in_container('david', li) should return (3, 0).
    #in_container('evelyn', li) should return (4, 2).
    #in_container('jonathan', li) should return (None, -1).
    
    #breadth first, hence the separate for loops
    #list_of_types
    
    #first check current level
    if type(c) is list:
        for x in range(len(c)):
            if e == c[x]:
                return (x, n)
    elif type(c) is dict:
        for entry in c:
            if e == entry:
                return(x, n)
    
    for x in range(len(c)):
        if type(c[x]) is list or type(c[x]) is dict:
            t = in_container(e, c[x], n + 1)
            if t != (None, -1):
                return (x, t[1])
            else:
                return (None, -1)
            
                                                
def build_keywords_from_file(f, l):
    """ Takes in a file (f) containing keywords and a list (l) that may or may not be empty.
    Returns a list of said keywords as lemmas recognized by WordNet (if applicable),
    checking to see that there are no duplicates in the list."""
    wnl = nltk.WordNetLemmatizer()
    
    for line in f:
        if line.startswith(g.IGNORE_SEQ):
            continue
        
        nLine = Line(line)
        nouns = nLine.get_nouns()
        lwc = [noun.lower() for noun in nouns]
        s = set(lwc)
        
        lemmas = [wnl.lemmatize(t) for t in s]
        for lemma in lemmas:
#            loc_info = in_container(noun, l) # gives a tuple, (the element in which
#            if noun in l or loc_info != (None, -1):
#                pass
#            else:
            if lemma not in l:
                l.append(lemma)
    return l
    
    #
        
      
    #pass #waiting on file to see how to parse


def build_expanded_keywords(l):
    """ Takes in the list of keywords (l).
    Uses Wordnet from NLTK package to build a dictionary (d) of synonyms to go along with each word.
    d will be a dictionary whose values are lists of strings.
    If WordNet does not recognize the word as a lemma, the corresponding value will be the empty list, [].
    """
    #from nltk import corpus
    # keywords == l
    # expanded_keywords == d

    d = {}

    for word in l:
    #    if is_in_container(word, expanded_keywords) == True: #if already covered in synonyms of a similar word, likely not needed (?)
    #        continue
    #    else:
    ## Above commented out to allow for every word in the keywords to have their own list
            d.setdefault(word, [word]) #if word is not in the dict already (which it shouldn't be!), adds dict[word] = [word]
            temp = []
            for synset in wn.synsets(word): #synset = "synonym set" for the word
                temp.extend(synset.lemma_names()) #lemmas are basically just synonyms
            for entry in set(temp): 
                if entry not in d[word]: #keep list shorter so later searching is quicker
                    d[word].append(entry)

    return d







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

objectTypeDict = {}
materialTypeDict = {}
docTypeDict = {}
dTypeToRole_map = {}

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
        


#with open("objectType_list.txt", 'r', encoding = 'iso-8859-1') as otl: #object type list
#        formDictionaryfromFile(objectTypeDict, otl)
#with open("materialType_list.txt", 'r', encoding = 'iso-8859-1') as mtl: #material type list
#        formDictionaryfromFile(materialTypeDict, mtl)
#with open("docType_list.txt", 'r', encoding = 'iso-8859-1') as dtl: #document type list
#        formDictionaryfromFile(docTypeDict, dtl)
#with open("docTypetoCreatorRole_map.txt", 'r', encoding = 'utf-8') as dtcrm:
#    formDictionaryfromFile(dTypeToRole_map, dtcrm)


#print(objectTypeDict)
#print(materialTypeDict)
#print(docTypeDict)

#should have dictionaries I want. Don't need lists anymore.
