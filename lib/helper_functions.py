# -*- coding: utf-8 -*-
### Helper functions for metadata creation ###
from nltk.corpus import wordnet as wn
import nltk#
from lib import shared as g
#import kitchen.text.converters as k
import re

import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
rname = os.path.dirname(dname) #root directory of
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
        self.objectType = ''
        self.materialType = ''
        
    def get_raw_text(self):
        """Returns raw text."""
        return self.raw_text
        
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
        
        rg = r'(\d+\.\d+\.\d+\.?)'
        m = re.search(rg, self.raw_text)        #should only match the digits.digits.digits(.'s) pattern
        #m.group has ['x.x.xx', and maybe some others...]
        
        if m:
            rg_beg = r'^(\d+)\.(\d+)'
            mm = re.search(rg_beg, m.group(0)) #m.group(0) is the first and only match of the first part
            
            
            return mm.group(0)
        else:
            return g.not_found
        

    def get_figure_num(self):
        """Uses the unicode text to output the figure number (as unicode)."""

        #n = l[0] #in current configuration, first word contains all the information

        rg = r'(\d+\.\d+\.\d+\.?)'
        m = re.search(rg, self.raw_text)        #should only match the digits.digits.digits(.'s) pattern
        
        if m:
            rg_end = r'((\d+)(\.)*)$' #searches at end of string for xxx with maybe a dot at the end
            ss = m.group(0)            
            mm = re.search(rg_end, ss) #m.group(0) is the first and only match of the first part

            if mm:
                rg_sss = r'^(\d+)' #searches for just the digits at the front of the substring
                sss = mm.group(0)   
                
                mmm = re.search(rg_sss, sss)
                
                if mmm:
                    return mmm.group(0)
            
            
            return mm.group(0)
        else:
            return g.not_found


    
    def get_caption(self):
        """Returns caption (after figure number)."""
        
        rg = r'(\d+\.\d+\.\d+(\.)*(\s)*)' #\d = digits. \s = whitespace
        m = re.split(rg, self.raw_text)        #should only match the digits.digits.digits(.'s) pattern
                        
        if m and len(m[-1]) > 0:
            result = m[-1].replace('\n', '')
            return result #last part of split lsit; should be caption
        else:
            return g.not_found
        
#        #copypasta from txt2re.com with a bit of modification...
#        #as we get weirder and weirder formats, we'd have to expand our regexp to look for these other formats
#        
#        re1='((?:(?:[0-2]?\\d{1})|(?:[3][01]{1}))[-:\\/.](?:[0]?[1-9]|[1][012])[-:\\/.](?:(?:\\d{1}\\d{1})))(?![\\d])'	# DDMMYY 1
#        re2='.*?'	# Non-greedy match on filler
#        re3='(\\s+)'	# White Space 1
#        
#        rg = re.compile(re1+re2+re3,re.IGNORECASE|re.DOTALL)
#        m = rg.search(self.raw_text)
#        if m:   #we'll bypass the figure number...
#            ddmmyy1=m.group(1)
#            c1=m.group(2)
#            ws1=m.group(3)
#            l = len(ddmmyy1) + len(c1) + len(ws1) #get the length of the figure number and whitespace
#            return self.raw_text[l:] #return the substring of everything after the figure number
#        else:
#            return g.not_found
    
    def get_copyright(self):
        """Returns associated copyright privilege level."""
        #unless I get some file explaining the permissions, let's pass...
        return g.not_found
    
    
    def get_type(self):
        """Gets each noun. Sees if it exists in any of the current dictionaries. Otherwise, asks user."""
        nouns = self.get_nouns(self)
        dicts = [g.objectTypeDict, g.docTypeDict, g.materialTypeDict]
        types = [self.objectType, self.docType, self.materialType]
        leftover_nouns = []
        is_matched = False
        for noun in nouns:
            is_matched = False
            for n,d in enumerate(dicts): #provides a pair of (0,dict0),(1,dict1), etc
                if noun in d:
                    print("The script has found a match in the " + d[noun][0] + "dictionary where " + noun + "maps to " + d[noun][1] ". The two have been matched together " +d[noun][2] + " times. The line in which the current token has been matched is shown below: ")
                    print('\n\n' + self.get_raw_text() + '\n\n')
                    response = input("Would you like to make the match of " + noun + "to " + d[noun][1] "? (Y/N)")
                    if response == 'Y' or response == 'y':
                        is_matched = True
                        types[n] = d[noun][1]
                        # TODO: ask to put into permanent map?
                    else if response == 'N' or response == 'n':
                        #leftover_nouns.append(noun)
                        print("Skipping...\n\n\n")
                
                if not is_matched:
                    leftover_nouns.append(noun)
        
        for noun in leftover_nouns:
            pass
            # TODO: ask user which category to put into (or leave blank if not a word of interest), which controlled vocabulary to match it to. Update appropriate dict
        
        
    
    
    
    def get_object_type(self):
        """Given the string, returns a guess of what type of object is being described in the caption (as unicode)."""
        
        targets = ""                        
                    
        for lemma in self.lemmas: #for each noun chunk
            for key in g.objectTypeDict:
                if lemma in g.objectTypeDict[key]: #xxxTypeDict[key] is a list containing words that map to the term "key"
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
            for key in g.materialTypeDict:
                if lemma in g.materialTypeDict[key]: #xxxTypeDict[key] is a list containing words that map to the term "key"
                    targets += key + ', '
        
        if len(targets) > 2: #targets is a string, not the number of actual matches
            targets = targets[:-2]    #remove last set of ', '      
        return targets 
    
    def get_doc_type(self):
        """Returns a guess of how the figure was captured (as unicode)."""
        #### SEE GET_OBJECT_TYPE         
        
        targets = ""                        
                    
        for lemma in self.lemmas: #for each noun chunk
            for key in g.docTypeDict:
                if lemma in g.docTypeDict[key]: #xxxTypeDict[key] is a list containing words that map to the term "key"
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
        
        return g.not_found
        
        ### Below should be debugged. Problem with dTypeToRole_map...
#        creatorRole = g.not_found
#        
#        if self.creator != g.not_found and self.docType != g.not_found: #if there's a doc type and creator
#            creatorRole =  g.dTypeToRole_map[self.docType]#look up corresponding tuple in doc-->role dictionary
#        return creatorRole
    
    def get_cultural_term(self):
        """Returns guess of cultural term by comparing chunks to a given dict."""
        return g.not_found
        #pass #no such dict quite yet

    def get_date_type(self):
        return g.not_found
    
    def get_temporal_term(self):
        return g.not_found
    
    def get_geographic_term(self):
        return g.not_found
    
    def get_status(self):
        """Returns status of caption, which, when first uploading, is always 'Needs Review.'"""
        return 'Needs Review.'
        
    def get_permissions(self):
        return g.not_found
    
    def get_image_id(self):
        return g.not_found
    
    def get_image(self):
        """Returns image."""
        return g.not_found
        #don't have those files on this computer, and wouldn't be able to do much with them anyway...
        
    def get_info_for_file(self):
        """Writes out information contained in Line in the order described by the metadata field headers.
        Uses in-cell and between-cell delimiters as defined in globals.py"""
        
        ### Currently have to manually force the printing order. Hoping to fix this..
        
        to_be_printed = [self.get_image_id(),
                        g.book_title,
                        g.year_published,
                        g.book_description,
                        g.editor,
                        g.publisher,
                        g.publisher_location,
                        g.book_doi,
                        g.book_isbn,
                        self.get_chapter_num(),
                        self.get_figure_num(),
                        self.get_caption(),
                        self.get_copyright(),
                        self.get_object_type(),
                        self.get_material_type(),
                        self.get_doc_type(),
                        self.get_creator(),
                        self.get_creator_role(),
                        self.get_cultural_term(),
                        self.get_date_type(),
                        self.get_temporal_term(),
                        self.get_geographic_term(),
                        self.get_status(),
                        self.get_permissions(),
                        self.get_image()
                        ]
        
        s = ''
        
        for entry in to_be_printed:
            s = s + entry + g.DELIMITER
        
        s = s[:-1] #remove last delimiter
        
        return s

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
    Returns a checked list of strings, each string corresponding to a person's name.
    Returns list of tuples if list of tuples is given."""
    
    result = []

    
    if len(l) == 0:
        return result
    
    x = 0
    
    
    if type(l[0]) is str: #for line.get_people(). Need to update that to use tuples too...
        while x < len(l):
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
                
            x += 1
            
    elif type(l[0]) is tuple:
        nl = [n[0] for n in l] #just the strings...
        
        
        while x < len(l):
            temp = []
            #l[x] is a singular person's name in tuples along with position tag. l[x][y][0] gives the y'th part of the name.
            i = 0
            temp.append(nl[x+i]) #first word...
            while x + i + 1 < len(l): #while the next "Persons" after them also obinly have one part of a name
                dist = abs(s.find(nl[x+i]) + len(nl[x+i]) - s.find(nl[x+i+1]))
                if dist == 1 and l[x+i][1][:2] == l[x+i+1][1][:2]:
                #if the distance between the two "Persons" is less than one char away
                #(i.e. there's a ' ' between the two)
                # AND the POS tags match (e.g. 'NNP' and 'NN')
                    temp.append(nl[x+i+1]) #add the consecutive words...
                    i += 1 #increment i
                else:
                    break 
            
            if len(temp) > 1: #if there were a set of words in a row,
                t = ' '.join(temp) #join them together
                result.append([t, l[x][1]]) #and add to list. Keep tuple of first word in phrase to maintain information
            
            if len(temp) == 1 and l[x+i][1][:2] == 'NN': #if one noun is by itself, can still be important
                result.append(l[x+i]) #add the tuple
            
            #so result, in this version, has a list of two-entry lists (i.e. tuples)
            
            x += i #update x after matching together string   
            x += 1 #necessary to avoid infinite loop...
       
       
       
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











        
        

#with open("objectType_list.txt", 'r', encoding = 'iso-8859-1') as otl: #object type list
#        formDictionaryfromFile(objectTypeDict, otl)
#with open("materialType_list.txt", 'r', encoding = 'iso-8859-1') as mtl: #material type list
#        formDictionaryfromFile(materialTypeDict, mtl)
#with open("docType_list.txt", 'r', encoding = 'iso-8859-1') as dtl: #document type list
#        formDictionaryfromFile(docTypeDict, dtl)
#with open("docTypetoCreatorRole_map.txt", 'r', encoding = 'utf-8') as dtcrm:
# formDictionaryfromFile(dTypeToRole_map, dtcrm)


#print(objectTypeDict)
#print(materialTypeDict)
#print(docTypeDict)

#should have dictionaries I want. Don't need lists anymore.
