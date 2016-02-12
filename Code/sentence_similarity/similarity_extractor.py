import nltk
from nltk.corpus import wordnet as wn
import math

sent1 = ""
sent2 = ""
list1 = ['mouse', 'fox', 'somthing', 'dog']

dog = wn.synset('dog.n.01')

for l in list1:
	pos_tag =  nltk.pos_tag(l.split())
	print pos_tag
	if pos_tag[0][1].startswith("N"):
		try:
			syn = wn.synset(l + '.n.01')
		except:
			print str(syn) + " error!"
			continue
	elif pos_tag[0][1].startswith("V"):
		try:
			syn = wn.synset(l + '.v.01')
		except:
			print str(syn) + " error!"
			continue
	else:
		print l + " does not fit with any pattern."
		continue
	
	print "Similarity between dog and " + l + ": " + str(dog.path_similarity(syn))