"""
    Algorithm to test the norm classifier in the Australian Contract Corpus.
"""

# -*- coding: utf-8 -*-
import nltk
from nltk import word_tokenize as wt

class Classifier:
    # Main class that allows one to use the norm classifier.
    
    def __init__(self):
        
        self.sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')     # Used to split text into sentences.
        self.modal_verbs = ['can', 'could', 'may', 'might', 'must', 'shall', 'should', 'will', 'would', 'ought']

    def classify(self, text):
        # Classify a sentence string or a list of sentences as norm and noNorm.

        if type(text) == str:
            # If text is a string, break it into tokens.
            # If among the tokens there is a modal verb, consider it a norm.
            # If it does not have a modal verb among the tokens, consider it a noNorm.
            
            tokens = wt(text)
            for token in tokens:
                if token in self.modal_verbs:
                    return 'norm'
            return 'noNorm'

        elif type(text) == list and text:
            # If text is a list of sentences, classify each sentence based on the existence or absence of modal verbs among the sentence tokens.
            output = [] 
            for sent in text:
                classified = 0
                tokens = wt(sent)
                for token in tokens:
                    if token in self.modal_verbs:
                        output.append((sent, 'norm'))
                        classified = 1
                        break
                
                if not classified:
                    output.append((sent, 'noNorm'))

            return output

    def extract_norms(self, contract_sents):
        # Return norms from a list of sentences.
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
    
    c = Classifier()
    norms = c.extract_norms(open("../data/manufacturing/adaptec.mfg.2001.04.01.shtml", 'r').read())

    for norm in norms:
        print norm + "\n"