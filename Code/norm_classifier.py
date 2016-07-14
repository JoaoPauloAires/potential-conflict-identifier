"""
    Algorithm to test the norm classifier in the Australian Contract Corpus.
"""

# -*- coding: utf-8 -*-
import nltk
import random
from nltk import word_tokenize as wt

class Classifier:
    # Main class that allow one to use the norm classifier.
    
    def __init__(self):
        
        self.sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        self.modal_verbs = ['can', 'could', 'may', 'might', 'must', 'shall', 'should', 'will', 'would', 'ought']

    def classify(self, text):

        if type(text) == str:
            tokens = wt(text)
            for token in tokens:
                if token in self.modal_verbs:
                    return 'norm'
            return 'noNorm'

        elif type(text) == list and text:
            output = [] 
            for sent in text:
                classified = 0
                tokens = wt(sent)
                for token in tokens:
                    if token in self.modal_verbs:
                        output.append('norm')
                        classified = 1
                        break
                
                if not classified:
                    output.append('noNorm')

            return output

    def extract_norms(self, contract_sents):
        
        output = []
        
        if type(contract_sents) != list:
            contract_sents = self.sent_tokenizer.tokenize(contract_sents)
        
        for sentence in contract_sents:
            tokens = wt(sentence)
            for token in tokens:
                if token in self.modal_verbs:
                    output.append(sentence)
                    break
        return output

if __name__ == "__main__":
    run_classifier(10)    

    c = Classifier(1)
    norms = c.extract_norms(open(home + "data/manufacturing/adaptec.mfg.2001.04.01.shtml", 'r').read())

    for norm in norms:
        print norm + "\n"