# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 17:47:52 2015

@author: cliccuser
"""

#### To ensure the working directory starts at where the script is located...
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath) #base, where main file is stored
os.chdir(dname)
####

print('fake main says the abspath is ' + abspath)