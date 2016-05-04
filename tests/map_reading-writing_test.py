# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 15:37:42 2016

@author: dkhachatrian
"""

#### To ensure the working directory starts at where the script is located...
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
####

import ast #allows us to use the safer version of eval(), literal_eval()


def mergeDicts(d_old, d_new):
    """Merge two dictionaries of lists containing (lists of strings). All values will be lists of strings, with list lengths of at least 1. No distinguishing between values according to their origins."""
    data = d_old
    for k in d_new.keys():
        if k not in data:
            data[k] = []
        for entry in d_new[k]:
            if entry not in data[k]: #no duplicates
                data[k].append(entry)
    
    return data



def appendDictToFile(dmap, ofile):
    """Appends dictionary dmap to a file that may or may not already have previous dictionary entries, ofile."""
    s = ofile.readlines()
    fmap = ast.literal_eval(s)
    merged = mergeDicts(fmap, dmap)
    ofile.seek(offset = 0, from_what = 0) #go to beginning of file
    s = str(merged)
    s = s.encode(encoding = 'utf-8')
    ofile.write(merged)



def main():
    with open(os.path.join(dname,'test_map.dat'), 'r+') as w:
        #.read()
        data = {'Alice': ['apples'], 'Bob': ['bananas'], 'Foo':['bars']}
        data2 = {'dracula': ['awesome'], 'edward': ['sparkly'], 'alucard': ['dracula backwards!']}
        data3 = {'edward': ['stupid']}
        for dmap in (data, data2, data3):
            appendDictToFile(dmap = dmap, ofile = w)
    #    s1 = str(data)[1:] #remove first brace to prepare merging
    #    s2 = str(data2)[:-1] + ', ' #prepare s2 to be shoved together with s1
    #    s3 = str(data3)[1:-1] + ', ' #squeeze in middle
    #    s = s2 + s3 + s1 #+ str(data2)
    #    b = s.encode(encoding = 'utf-8')
    #    w.write(b)
#    
    
main()    
    
with open(os.path.join(dname,'test_map.dat'), 'r') as r:
    for line in r:
        print(line)
        #if line[-1] == '\n':
        #    line = line[:-1]
        rdata = ast.literal_eval(line)
        k = 'edward'
        if k in rdata:
            print(rdata[k])
        else:
            print("Nope!")
