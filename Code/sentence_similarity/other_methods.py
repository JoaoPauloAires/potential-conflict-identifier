# -*- coding: utf-8 -*-
from __future__ import division
import nltk
import re
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer

remove_punctuation = re.compile(r'[\"\#\$\%\&\\\'\(\)\*\+\,\-\/\:\;\<\=\>\@\[\\\\\]\^\_\`\{\|\}\~]+')

def simple_similarity(sent1, sent2):
    sent1, sent2 = nltk.word_tokenize(sent1), nltk.word_tokenize(sent2)
    len1, len2   = len(sent1), len(sent2)
    equals          = 0
    for index in range(min(len1, len2)):
        for index2 in range(max(len1, len2)):
            if sent1[index] == sent2[index2]:
                if index == index2:
                    equals += 1
                else:
                    equals += 0.5
    return equals/max(len1, len2)

def medium_similarity(sent1, sent2):
    indx1 = 0
    similarity = 0
    sent1 = remove_punctuation.sub('', sent1.lower())
    sent2 = remove_punctuation.sub('', sent2.lower())
    sent1, sent2 = nltk.word_tokenize(sent1), nltk.word_tokenize(sent2)
    for word in sent1:
        # print "Current word: " + word + "\n"
        indx2 = 0
        for token in sent2:
            # print word + " comparing to: " + token + "\n"
            if word == token:
                if indx1 == indx2:
                    similarity += 1
                    break
                else:
                    similarity += 0.7
                    break
            else:
                list_syns_token = wn.synsets(token)
                list_syns_word  = wn.synsets(word)
                flag = False
                for l in list_syns_token:
                    if flag:
                        break
                    for i in list_syns_word:                    
                        if i.lemma_names()[0] == l.lemma_names()[0]:
                            if indx1 == indx2:
                                similarity += 0.7
                                flag = True
                                break
                            else:
                                similarity += 0.5
                                flag = True
                                break                        
            indx2 += 1
        indx1 += 1
    return similarity/max(len(sent1), len(sent2))
