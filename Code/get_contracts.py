import os
from conflict_finder import *

#constants
BASE_PATH = 'data/Conflitos/'
identifier = Conflict_finder()

def read_contracts():
	#Read contracts with conflicting norms
	contract_folders = os.listdir(BASE_PATH)
	n_conflicts = 0
	i = 0
	text = ""
	for folder in contract_folders:
		#open each folder to read the contracts inside
		i += 1
		if os.path.exists(BASE_PATH + folder):
			list_files = os.listdir(BASE_PATH + folder)
			
			for contract_file in list_files:

				if contract_file[:3] == 'new':
					conflicts = open(BASE_PATH + folder + "/" + contract_file, 'r').readlines()
					text += "Conflicts to be found:\n\n"
					for conflict in conflicts:
						text += "\t" + conflict + "\n"

				else:
					print contract_file + "\n"
					text = "Contract: " + contract_file + "\n\n"
					text += identifier.process(BASE_PATH + folder + "/" + contract_file)
				text += "============================================\n\n"

			output = open(BASE_PATH + "results"+ str(i) +".txt", 'w')
			output.write(text)
			output.close()
			text = ""

if __name__ == "__main__":
    read_contracts()