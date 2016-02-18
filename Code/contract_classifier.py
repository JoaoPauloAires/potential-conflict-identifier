"""
    This algorithm receives all contracts extracted from Xibin's base and then classifies their sentences.
    After, it evaluates the f-measure for the task.
"""

from __future__ import division
from norm_dictionary import *
from norm_classifier import *
import os
import hashlib
import nltk
import threading
# from multiprocessing.pool import ThreadPool
import time
# from multiprocessing import Process

class contract_classifier():

    def __init__(self):
        self.true_positive, self.true_negative, self.false_positive, self.false_negative = 0, 0, 0, 0
        self.output = open('data/contract_classifier_result.txt', 'w')
        self.dictionary = dic()   

    def verify(self, sent, result):
        key = hashlib.md5(sent).digest()
        
        if self.dictionary.has_key(key):
            if result == 'norm':
                self.true_positive = self.true_positive + 1
            else:
                self.false_negative = self.false_negative + 1
        else:
            if result == 'norm':
                self.false_positive = self.false_positive + 1
            else:
                self.true_negative = self.true_negative + 1

    def evaluate(self):
        precision = self.true_positive / (self.true_positive + self.false_positive)
        recall = self.true_positive / (self.true_positive + self.false_negative)
        f_measure = (2 * precision * recall) / (precision + recall)
        self.output.write("\nTrue positive: " + str(self.true_positive) + "\nTrue Negative: " + str(self.true_negative) + "\nFalse Positive: " + str(self.false_positive) + "\nFalse Negative: " + str(self.false_negative))
        self.output.write("\nPrecision: " + str(precision) + "\nRecall: " + str(recall) + "\nF-Measure: " + str(f_measure) + "\n")
        self.output.close()

    def cleanSent(self, sent):
        sent_list = sent.split()
        for s in sent_list:
            if '--' in s:
                sent_list.pop(sent_list.index(s))    
        if len(sent_list) > 1:
            if sent_list[1] in ['and', 'or', 'will', 'of', 'and/or']:
                return ' '.join(sent_list)
            elif '(' in sent_list[0] or '.' in sent_list[0]:
                return ' '.join(sent_list[1:])
        return ' '.join(sent_list)

    def classifies(self, s, classifier):
        if classifier.classify(s) == 'norm':
            s = self.cleanSent(s)
            self.verify(s, 'norm')
        else:
            self.verify(s, 'noNorm')
            
    def classify(self):
        self.output.write(time.strftime("%d/%m/%Y") + " - " + time.strftime("%H:%M:%S") + "\n")
        directory = '/home/lsa-06/Dropbox/PUCRS/Dissertation/Corpus/xIbinCorpus/noHTML/'
        dir_list = os.listdir(directory)
        sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        classifier = Classifier(1)
        for dir in dir_list:
            print dir
            contract_list = os.listdir(directory+dir)
            for contract in contract_list:
                print "\t " + contract + " " + str(contract_list.index(contract) + 1) + "/" + str(len(contract_list))
                contract_text = open(directory+dir+"/"+contract, 'r').read().split()[1:-1]
                contract_text = ' '.join(contract_text)
                sents = sent_tokenizer.tokenize(contract_text)
                thread_list = []
                for sent in sents:
                    thread = threading.Thread(target = self.classifies, args = (sent ,classifier))
                    thread.start()
                    thread_list.append(thread)
                for thr in thread_list:
                    thr.join()

        self.evaluate()                            	

if __name__ == "__main__":
    c_classifier = contract_classifier()
    c_classifier.classify()