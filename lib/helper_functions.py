### Helper functions for metadata creation ###
from nltk.corpus import wordnet as wn
import nltk

class Line:
    def __init__(self, s = ''):
        self.raw_text = s
        self.tokens = nltk.word_tokenize(s) #break line into word "tokens"
        self.tagged = nltk.pos_tag(self.tokens) #assign tags to token's role in sentence
        self.entities = nltk.ne_chunk(self.tagged)
        
    def get_nouns(self):
        """Returns the nouns in Line as a list."""
        return [w[0] for w in self.tagged if 'NN' in w[1]] #list of nouns in line (second entry in tuple gives tag)


    def get_people(self):
        """Returns the names of the people in that line as a list of strings."""
    
        treeList = list(self.entities.subtrees(lambda t: t.label() == 'PERSON')) #argument provided to subtree serves as filter (by label)
        return clean_list_of_people(treeList, self.raw_text)

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


def clean_list_of_people(l,s):
    """Takes in a list of people and the original line. Checks that they're chunked properly.
    If any Persons only have a first name, uses the original line to check if improperly chunked.
    Returns a checked list of strings, each string corresponding to a person's name."""
    
    result = []
    
    if len(l) == 0:
        return result
    
    for x in range(len(l)): #l is main tree of all people
        temp = []
        #l[x] is a singular person's name in tuples along with position tag. l[x][y][0] gives the y'th part of the name.
        if len(l[x]) == 1: #if it couldn't find a last name,
            i = 0
            temp.append(l[x+i][0][0]) #first word...
            while x + i + 1 < len(l) and len(l[x]) == 1: #while the next "Persons" after them also only have one part of a name
                if abs(len(l[x+i+1][0][0]) - s.index(l[x + i][0][0]) + len(l[x+i][0][0])) == 1 : #if the distance between the two "Persons" is less than one char away (i.e. there's a ' ' between the two)
                    temp.append(l[x+i+1][0][0]) #add the consecutive words...
            
        elif len(l[x]) > 1: #if it isn't an oddity
            for y in range(l[x]):
                temp.append(l[x][y][0]) #add all the parts of the name. Parts of the name are controlled by second index y. String of interest in 0th index.
        
        stemp = set(temp) #should only really be necessary to do for first case...
        t = ' '.join(stemp)
        result.append(t)
       
    return result

def is_in_container(e, c, n = 0):
    """ Takes an entry to search for and a container, which may contain containers.
    Returns the most shallow subcontainer and the number of levels deep in the subcontainer the entry is located.
    If entry not found, returns (None, -1). """
    
    #breadth first
    #list_of_types =
    
    for x in range(len(c)): #first check current level
        if e == c[x]:
            return (c[x], n)
    
    if type(c) is list or type(c) is dict:
        is_in_container(e, c[x], n + 1)
    
    else:
        return (None, -1)
            
                                                
def build_keywords_from_file(f):
    """ Takes in a file (f) containing keywords.
    Returns a list of said keywords."""
    pass #waiting on file to see how to parse


def build_expanded_keywords(l, d):
    """ Takes in the list of keywords (l).
    Uses Wordnet from NLTK package to build a dictionary (d) of synonyms to go along with each word.
    """
    #from nltk import corpus
    # keywords == l
    # expanded_keywords == d

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

                
