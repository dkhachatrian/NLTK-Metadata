# -*- coding: utf-8 -*-
### Helper functions for metadata creation ###
from nltk.corpus import wordnet as wn
import nltk
import shared as g
import kitchen.text.converters as k
import re

#IGNORE_CHAR = '#'

class Line:
    def __init__(self, s = ''):
        self.raw_text = s
        self.tokens = nltk.word_tokenize(s) #break line into word "tokens"
        self.tagged = nltk.pos_tag(self.tokens) #assign tags to token's role in sentence
        self.entities = nltk.ne_chunk(self.tagged)
        
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
        return [w for w in self.tagged if (len(w[1])>1 and w[1][:2] in toi and w[0] not in excluded)]



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
        #for each noun chunk
        #look to see if it can be found in the extended keywords list
        #if so
            #look in the word associations dictionary to see what object type the word maps to
        #otherwise
            #return nothing
        pass
        
    def get_material_type(self):
        """Returns a guess of what sort of material was used to create the object described in the caption (as unicode)."""
        #if an object type was found
            #look in object<-->material dictionary to see what it was probably made from
        #otherwise
            #return ""
        pass
    
    def get_doc_type(self):
        """Returns a guess of how the figure was captured (as unicode)."""
        #look through interesting word chunks
        #for each word chunk
            #if there is a word that matches with the keyword<-->documentation dictionary
            #return the documentation guess
        #else
            #return "picture" #usually when not stated, is a photograph
        pass
    
    def get_creator(self):
        """Guesses the creator of the figure from caption text. Returns as unicode."""
        #look through the names
        #if an obvious lead-up like "by" or "courtesy of" comes before the name
            #return the name
        #else return ""
        pass

    def get_creator_role(self):
        """Returns creator's role."""
        #if there's a doc type and creator
            #look up corresponding tuple in tupe-->role dictionary
        #else return ""
        pass
    
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
        while x + i + 1 < len(l): #while the next "Persons" after them also only have one part of a name
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
