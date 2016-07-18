# -*- coding: utf-8 -*-
#Algorithm that receives either a contract file or folder path and returns the entities annotated in the norms.
import os
import nltk
from norm_classifier import *
from nltk.tag import stanford
# from nltk.tag.stanford import POSTagger
from extracting_parties import *

# Global variables.
# jar = 'stanford-postagger.jar'
# model = 'wsj-0-18-bidirectional-distsim.tagger'
# stanford = POSTagger(model, jar)
output = open('data/annotated_entities.xml', 'w')
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
        print path + contract
        
        entities, nicknames = extract_parties(path + contract)
        statinfo = os.stat(path + contract)
        size = statinfo.st_size
        contract_text = open(path + contract, 'r').read()
        
        print contract + " will have its norms extracted. With " + str(size)
        
        norms = classifier.extract_norms(contract_text)
        
        print "Norms have been successful extracted!"
        
        if entities and norms:
            print entities, nicknames
            annotate_entities(entities, nicknames, norms)
            print "The contract " + contract + " had its norms and entities annotated.\n"
        else:
            print contract + " has no entities or norms founded!"
    # return annotated_norms
        

def annotate_entities(entities, nicknames, norms):
    modalVerbs = ['can', 'could', 'may', 'might', 'must', 'shall', 'should', 'will', 'would', 'ought']
    annotated_norms  = []
    for norm_index in range(len(norms)):
        flag = False
        index = -1        
        norm = nltk.word_tokenize(norms[norm_index])
        for verb in modalVerbs:
            if verb in norm:
                index = norm.index(verb) + 1
                break
        if index == -1:
            continue                

        pre_m_verb = norm[:index]

        for word in pre_m_verb[::-1]:
            found = False
            for nickname in nicknames:
                nick = ' '.join(nickname.split()).split()
                if word in nick:
                    found = find_entity(word, pre_m_verb, nick, nicknames.index(nickname) + 1)
                    break

            for ent in entities:
                entity = ent.split()
                if word in entity:
                    found = find_entity(word, pre_m_verb, entity, entities.index(ent) + 1)
            if found:
                norm = found + norm[index:]
                norms[norm_index] = ' '.join(norm)
                # annotated_norms.append(norms[norm_index])
                output.write(norms[norm_index] + "\n\n")
                break
    # return annotated_norms

def find_entity(word, phrase, party, index):
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