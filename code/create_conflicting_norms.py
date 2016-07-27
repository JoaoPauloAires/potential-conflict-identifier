"""
    Creates a strucuture for conflict insertion into real contracts.
"""

import os
import nltk
from norm_identification.norm_classifier import * 
from party_identification.extracting_parties import extract_parties
import random
import time
import shutil

class Structure:

    def __init__(self):
        self.path = "data/manufacturing/"
        self.contract_list = os.listdir(self.path)
        self.directory = "data/conflicting_contracts/"
        self.sentence_classifier = Classifier()
        self.contract_structure = {}
        self.sentences = {}
        self.username = ''
        self.contract = None
        self.norm     = None
        self.new_norms = []
        self.access    = False
        self.modalVerbs = ['can', 'could', 'may', 'might', 'must', 'shall', 'should', 'will', 'ought']

    def start(self):
        # Initialize the conflict insertion by asking for a username and an option to be selected.
        while self.username == '':
            self.username = raw_input("Please insert your name: ")
        if not self.access:
            self.access = True
            print "Hi, here you can choose what action to take."
    
        sentence = "Press: \n\t1 to pick up a random contract;"
        if self.contract:
            sentence += "\n\t2 to pick up a random norm;"
        if self.norm:
            sentence +="\n\t3 to make a conflict for a norm;"
        sentence += "\n\t4 to finish.\n"
        print sentence
            
        choice = raw_input("So, what it will be?: ")
        print "\n"
        try:
            int(choice)
        except:
            print "Please, choose one of the options, just press the number without quotes.\n"
            self.start()

        ret = self.choose(int(choice))
        if ret:
            self.start()

    def choose(self, choice):
        # Based on choice, direct the user to a certain task.
        if choice == 1:
            try:
                return self.pick_a_contract()
            except:
                print "\n\nError during processing this contract, please get another one.\nDo not worry it is my fault."
                self.start()
                self.contract = None
        elif choice == 2 and self.contract:
            return self.pick_a_norm()
        elif choice == 3 and self.norm:
            return self.make_a_conflict()                
        elif choice == 4:
            return self.finish()
        else:
            print "Please, choose one of the options, just press the number without quotes.\n"
            self.start()

    def create_structure(self):
        # Create a structure with norms and their entities to the selected contract.
        print "Creating the contract structure. . .\n"
        sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        contract_sentences = sent_tokenizer.tokenize(open(self.path + self.contract, 'r').read())
        self.sentences[self.contract] = contract_sentences
        self.extract_entities(self.path + self.contract)
        norm_sentences = [x[0] for x in self.sentence_classifier.classify(contract_sentences) if x[1] == 'norm']
        ent_norms = self.entity_norms(norm_sentences)
        self.contract_structure[self.contract] = ent_norms
        if len(ent_norms):
            print "Structure ready!\n" + str(len(ent_norms)) + " norms extracted.\n"
        else:
            print "\n\nError during processing this contract, please get another one.\nDo not worry it is my fault."
            self.contract = None
            return 0            
        return 1

    def extract_entities(self, path):
        # Using a contract path it extracts the entities and their nicknames, if it exists.
        try:
            print "Extracting contract entities and nicknames."
            self.entities, self.nicknames = extract_parties(path)
            if self.entities:
                print "Entities found: ", self.entities
            if self.nicknames:
                print "Nicknames found: ", self.nicknames
        except:
            print "The extractor can't find neither entities nor nicknames"

    def entity_norms(self, norm_set):
        # From norms, it extracts the ones that has at least one modal verb and then identifies the entity
        ent_norms = []

        for n in norm_set:
            if len(n) > 200 or len(n) == 0:
                continue
            find = 0
            index = self.identify_modal(n)
            norm = n.split()
            if not index:
                continue
            for element in norm[:index][::-1]:
                if not find:
                    for word in self.nicknames:
                        if not find:
                            for w in word.split():
                                if w.lower() == element.lower():
                                    ent_norms.append(n)
                                    find = 1
                                    break
                    for word in self.entities:
                        if not find:
                            for w in word.split():
                                if w.lower() == element.lower():
                                    ent_norms.append(n)
                                    find = 1
                                    break
        return ent_norms

    def identify_modal(self, norm):
        # Identifies the index in which the modal is placed in the norm when receiving more than one parameter
        # Returns the norm modality
        index = None
        norm = norm.split()
        for verb in self.modalVerbs:
            if verb in norm:
                return norm.index(verb)


    def pick_a_contract(self):
        # From a list of contracts, select one randomly.
        self.contract = random.choice(self.contract_list)

        self.create_structure()
        
        print "You got: " + self.contract + "\n"
        
        return 1

    def pick_a_norm(self):
        # From a list of norms identified in the contract, select one randomly.
        if self.contract:
            self.norm = random.choice(range(len(self.contract_structure[self.contract])))
            if self.norm != None:
                print "You got: " + self.contract_structure[self.contract][self.norm] + "\n"
        else:
            print "Pick a contract before picking a norm.\n"
        return 1

    def make_a_conflict(self):
        # From the selected norm, create a new one that conflicts with it.
        if self.norm:
            print "From the following norm, create a conflict or a redundancy.\n" + self.contract_structure[self.contract][self.norm] + "\n"
            self.new_norms.append(raw_input("Enter the norm: "))
        else:
            print "You must pick a norm first.\n"
        return 1

    def create_new_contract(self):
        # Using the created conflict, create a new contract containing the conflict(s).
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        
        self.folder = self.directory + self.username + "-" + time.strftime("%d_%m_%Y") + "-" + time.strftime("%H:%M:%S") + "/"

        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

        self.new_contract = open(self.folder + self.contract, 'w')
        self.contract_norms = open(self.folder + "new_norms" + "_" +self.contract, 'w')

        return 1

    def finish(self):
        if self.new_norms:
            self.create_new_contract()

            for new_norm in self.new_norms:
                self.sentences[self.contract].append(new_norm)
                self.contract_norms.write(new_norm + "\n")

            for sentence in self.sentences[self.contract]:
                self.new_contract.write(sentence + " ")

        self.remove_empty_folders()    
        print "Done!\n"

        return 0

    def remove_empty_folders(self):
    	# For each user, we create a folder, if the user do not create a conflict, at the end of process remove empty folders.
        print "Searching for empty folders in /conflicting_contracts.\n"
        folder_list = os.listdir(self.directory)

        for folder in folder_list:
            if not os.listdir(self.directory + folder):
                print folder + " deleted!\n"
                shutil.rmtree(self.directory + folder)

if __name__ == "__main__":
    s = Structure()
    s.start()