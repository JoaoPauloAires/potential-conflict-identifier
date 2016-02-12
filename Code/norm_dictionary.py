"""
    Dictionary for the norm representation in Xibin's norm set.
"""

import os
import hashlib

def dic():
    directory = '/home/lsa-06/Dropbox/PUCRS/Dissertation/ContractMiner/ContractMiner/ContractMiner/data/norm/'
    listFiles = os.listdir(directory)
    dictionary = {}
    for file in listFiles:
        listSents = open(directory+file, 'r').readlines()
        for sent in listSents:
            sent = ' '.join(sent.split())
            dictionary[hashlib.md5(sent.rstrip('\r\n')).digest()] = sent.rstrip('\r\n')    
    return dictionary
