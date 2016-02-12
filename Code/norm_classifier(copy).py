"""
    Algorithm to test the norm classifier in the Australian Contract Corpus.
"""

# -*- coding: utf-8 -*-
from __future__ import division
import math
import random
import nltk
from nltk import word_tokenize as wt
from nltk.corpus import stopwords as sw
from nltk.stem.lancaster import LancasterStemmer
from os.path import expanduser

home = expanduser("~")

modalVerbs = ['can', 'could', 'may', 'might', 'must', 'shall', 'should', 'will', 'would', 'ought']
st = LancasterStemmer()
stop_words = [word for word in sw.words('english') if word not in modalVerbs]
        
#main class that allow one to use the norm classifier
class Classifier:

    classifier     = None
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    precision      = None
    recall         = None
    fMeasure       = None

    def __init__(self, *arg):
        l = list(arg)
        if not l:
            evl = 0
        else:
            evl = 1
        #print "Starting the Norm Classifier. . ."        
        normSents = self.sent_tokenizer.tokenize(open('data/trainData/normsList.txt', 'r').read())      #Extract sentences in the text
        noNormSents = self.sent_tokenizer.tokenize(open('data/trainData/noNormList.txt', 'r').read())
        
        sentences = ([(self.feature(sent), 'norm') for sent in normSents[:2027]] + [(self.feature(sent), 'noNorm') for sent in noNormSents[:2027]]) #2928
        
        self.process(sentences, evl) 
        # sentences = ([(self.feature(sent), 'norm') for sent in normSents[:5900]] + [(self.feature(sent), 'noNorm') for sent in noNormSents[:5900]]) #95910
        # self.process(sentences, evl)        

    def classify(self, text):
  #   	list_terms = text.split()
  #   	for modal in modalVerbs:
  #   		if modal in list_terms and len(list_terms) > 2:
  #   			return 'norm'
		# return 'noNorm'
        if type(text) == str:
            return self.classifier.classify(self.feature(text))
        elif type(text) == list and text:
            output = []
            for element in text:
                output.append((element, self.classifier.classify(self.feature(element))))
            return output

    def extract_norms(self, contract_sents):
        output = []
        if type(contract_sents) != list:
            contract_sents = self.sent_tokenizer.tokenize(contract_sents)
        for sentence in contract_sents:
            if self.classify(sentence) == 'norm':
                output.append(sentence)
        return output

    def feature(self, sent):                                              #Feature method, which is responsible of extracting relevant features from sentences
        lSent = nltk.word_tokenize(sent)#sent.split()
        features = {}
        for word in modalVerbs:
            features["count(%s)" % word] = sent.lower().count(word)     #count how many modal verbs the sentence has
            features["has(%s)" % word] = (word in lSent)                #see if the sentence has a modal verb
        if len(lSent) > 2:                                          
            features["firstword"] = st.stem(lSent[0].lower())                    #Gets the first word in the sentence
            features["preLastWord"] = st.stem(lSent[-2].lower())
            features["secondword"] = st.stem(lSent[1].lower())
        return features

    def fmeasure(self, testSet):                                  #method that calculates F-Measure
        truePositive = 0
        trueNegative = 0
        falsePositive = 0
        falseNegative = 0
        for test in testSet:
            if self.classifier.classify(test[0]) == 'norm' and test[1] == 'norm':
                truePositive = truePositive + 1
            elif self.classifier.classify(test[0]) == 'norm' and test[1] == 'noNorm':
                falsePositive = falsePositive + 1 
            elif self.classifier.classify(test[0]) == 'noNorm' and test[1] == 'noNorm':
                trueNegative = trueNegative + 1            
            elif self.classifier.classify(test[0]) == 'noNorm' and test[1] == 'norm':
                falseNegative = falseNegative + 1            
        
        self.precision = truePositive/(truePositive+falsePositive)
        self.recall = truePositive/(truePositive+falseNegative)
        self.fMeasure = (2*self.precision*self.recall)/(self.precision + self.recall)
        # print "Precision: "+str(self.precision)+"\nRecall: "+str(self.recall)+"\nF-Measure: "+str(self.fMeasure)+"\n"

    def evaluate(self, testSet):
        # print "Accuracy: "+ str(nltk.classify.accuracy(self.classifier, testSet))+"\n"                           #obtain the classifier accuracy
        # print self.classifier.show_most_informative_features(10)                          
        self.fmeasure(testSet)
               
    def process(self, sentences, evl):
        limit = int(len(sentences) * .9)                                            #define a limit of 80% of the sentences for training
        random.shuffle(sentences)
        trainSet, testSet = sentences[:limit], sentences[limit:]                    #define train and test sets
        self.classifier = nltk.NaiveBayesClassifier.train(trainSet)                      #train a naive bayes classifier from NLTK
        if evl:
            self.evaluate(testSet)

def run_classifier(num):
    total     = 0
    precision = 0
    recall    = 0

    for i in range(num):
        c         = Classifier(1)
        total     += c.fMeasure
        precision += c.precision
        recall    += c.recall

if __name__ == "__main__":
    # run_classifier(10)    

    c = Classifier()
    # norms = c.extract_norms(open(home + "/Dropbox/PUCRS/Dissertation/Corpus/xIbinCorpus/noHTML/manufacturing/adaptec.mfg.2001.04.01.shtml", 'r').read())
    print c.extract_norms("You should never come back.")
    # for norm in norms:
    #     print norm + "\n"