# -*- coding: utf-8 -*-
#Algorithm that receives either a contract file or folder path and returns the entities annotated in the norms.
import os
import nltk
from norm_identification.norm_classifier import *
from extracting_parties import *

# Global variables.
output = open('../data/annotated_entities.xml', 'w')
classifier = Classifier()

def annotate_norms(path):
    # Function that reads a contract, selects the norms and finds the parties in it.

    # Check the file extension.
    file_name, file_extension = os.path.splitext(path)

    if file_extension == '':
        # If it has no extension, it is a path to a folder with files.
        list_files = os.listdir(path)
    else:
        name = file_name.split('/')[-1]
        path = '/'.join(file_name.split('/')[:-1]) + '/'
        list_files = [name + file_extension]

    for contract in list_files:

        print contract + " will now have its parties identified."
        contract_path = path + contract
        print contract_path

        
        # Return the entities and nicknames present in the sentence.
        entities, nicknames = extract_parties(contract_path)
        statinfo = os.stat(contract_path)
        size = statinfo.st_size
        contract_text = open(contract_path, 'r').read()
        
        print contract + " will have its norms extracted. With " + str(size)

        # Extract norms from the contract.        
        norms = classifier.extract_norms(contract_text)
        
        print "Norms have been successful extracted!"
        
        if entities and norms:
            # If entities and norms were correctly identified.
            print entities, nicknames
            annotate_entities(entities, nicknames, norms)
            print "The contract " + contract + " had its norms and entities annotated.\n"
        else:
            print contract + " has no entities or norms founded!"
    # return annotated_norms
        

def annotate_entities(entities, nicknames, norms):
    modalVerbs = ['can', 'could', 'may', 'might', 'must', 'shall', 'should', 'will', 'would', 'ought']
    # annotated_norms  = []
    for norm in norms:
        flag = False
        index = -1        
        norm = nltk.word_tokenize(norm)     # Break norm sentence into tokens.
        for verb in modalVerbs:
            # Identify the modal verb in the sentence.
            if verb in norm:
                # Save the modal verb index on the norm sentnece.
                index = norm.index(verb) + 1
                break
        if index == -1:
            # If the norm sentence has no modal verb, go to the next norm sentence.
            continue                

        pre_m_verb = norm[:index]   # Get the range in norm sentence that goes from the beggining to the index of the modal verb.

        for word in pre_m_verb[::-1]:
            # Check the tokens in the range backwards searching for the entity.
            found = False
            for nickname in nicknames:
                # Search for the nicknames among the tokens, if it finds, it breaks the last for.
                nick = ' '.join(nickname.split()).split()
                if word in nick:
                    found = find_entity(word, pre_m_verb, nick, nicknames.index(nickname) + 1)
                    break

            for ent in entities:
                # Same case of the nicknames.
                entity = ent.split()
                if word in entity:
                    found = find_entity(word, pre_m_verb, entity, entities.index(ent) + 1)
            if found:
                norm = found + norm[index:]
                norm = ' '.join(norm)
                # annotated_norms.append(norms[norm_index])
                output.write(norm + "\n\n")
                break
    # return annotated_norms

def find_entity(word, phrase, party, index):
    # If the entity is composed of two or more tokens, we look for all of them and address a tag <PARTY> to it.
    
    final_phrase_index = phrase.index(word)
    final_party_index   = party.index(word)
    equal = True
    counter = 1
    initial_index = final_phrase_index
    while equal:
        if phrase[final_phrase_index - counter] == party[final_party_index - counter] and final_party_index - counter >= 0 and final_phrase_index - counter >= 0:
            initial_index = final_phrase_index - counter
            counter += 1
        else:
            phrase = ' '.join(phrase[:initial_index]) + " <PARTY_" + str(index) + ">" + ' '.join(phrase[initial_index:final_phrase_index+1]) + "<PARTY_" + str(index) + ">" + ' ' + ' '.join(phrase[final_phrase_index+1:])
            equal = False

    return phrase.split()


if __name__ == "__main__":
    a_norms = annotate_norms('data/manufacturing/chiron.mfg.2000.04.13.shtml')
    output.close()