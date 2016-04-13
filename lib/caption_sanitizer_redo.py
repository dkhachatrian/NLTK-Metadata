# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 14:45:45 2016

@author: dkhachatrian
"""

import re

r = r'((\d+)\.?(\d*)(\w*)\.?(\d*)\s*(\w*))'
# ^ to match caption format. Will house in a 5-tuple (entirePattern,1,2,3,4,5)

# 1 ==> chapter number
# 2 ==> section number, or caption number if no sections
# 3 ==> empty if 2 is sectionNum; else caption letter if applicable
# 4 ==> caption number
# 5 ==> caption letter if applicable

# Can use this to determine whether a match is the next caption (a clear increment of one of 1-5),
# or just a reference to another figure.

# (Can reuse regexp to separate caption line into chapter number, section number, figure number, etc.)

#### To ensure the working directory starts at where the script is located...
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
####

root = os.path.dirname(dname) #pulls back from lib to root

dep = os.path.join(root, 'dependencies') #dependencies folder


s = ''
temp = ''

with open(os.path.join(dep,'Figure Captions.txt'), 'r', encoding = 'UTF-8') as r: #open captions
    with open(os.path.join(root, 'outputs', 'Sanitized Captions.txt'), 'w', encoding = 'UTF-8') as w: #open file to write cleaned captions
        