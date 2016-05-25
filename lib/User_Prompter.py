# -*- coding: utf-8 -*-
"""
Created on Wed May 25 15:35:17 2016

@author: dkhachatrian
"""
#
#take in captions
#get dictionaries from saved maps
#
#for each line in captions:
#    (sanitize if necessary)
#    find all nouns
#    for each noun:
#        if it is in a map of interest:
#            if it is in the "permanent map":
#                copy over value to the Line function's (information to be printed)
#                continue
#            ask user "is this word a [type] that falls under the [category] category"?
#            if yes:
#                ask user "would this always be the case for this book? (It's been matched n times.)" #input()
#                if yes:
#                    save into "permanent" map. (Don't ask user when it pops up next time)
#                if no:
#                    if not in map already:
#                        add it to the map as [key = word, value = (specific categorization, number of matches)]
#                    else:
#                        increment the number of times it's been matched by 1     
#                add as part of the information for the line of interest
#            