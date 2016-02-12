import os
from conflict_finder import *
from os.path import expanduser

HOME = expanduser("~")

class Error_finder:

	def __init__(self):
		self.working_files = open("data/working_files.txt", 'w')
		self.defective_files = open("data/defective_files.txt", 'w')
		self.conf_finder = Conflict_finder()

	def evaluate_conflict_finder(self, path, folder=False):
		if folder:
			contract_list = os.listdir(path)
			i = 0
			for contract in contract_list:
				
				if i < 2:
					print "Processing ", contract
					try:
						self.conf_finder.process(path + contract)
						self.working_files.write(contract + "\n")
					except:
						print "here"
						self.defective_files.write(contract + "\n")
				i += 1			
		
			self.working_files.close()
			self.defective_files.close()
		else:
			self.conf_finder.process(path)	

if __name__ == "__main__":
    err_finder = Error_finder()
    err_finder.evaluate_conflict_finder(HOME+"/Dropbox/PUCRS/Dissertation/Corpus/xIbinCorpus/noHTML/manufacturing/", True)