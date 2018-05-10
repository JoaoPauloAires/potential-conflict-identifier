# -*- coding:utf-8 -*-
import os
import time
import sys
from conflict_finder import Conflict_finder

TP              = 0
TN              = 1
FP              = 2
FN              = 3
THRESHOLD_RANGE = [0.4, 0.5, 0.6, 0.7, 0.8]


class Test_Conf_Finder:

    """
        Test conflict_finder.py by passing a series of thresholds to the class.
        For each threshold, measure how much true and false positives they generate.
        We consider true positives when the conflict_finder finds potential conflicts
        that were manually inserted in the contracts.
        Whereas, we consider false positives those potential conflicts found that are not
        in the list of inserted conflicts.
    """

    def __init__(self, threshold_range, folders_path):

        self.threshold_range = threshold_range  # List of thresholds.
        self.folders_path = folders_path        # Path to the folder where contracts w/ inserted conflicts are located.
        self.dict_thr_tp_fp = dict()            # Dictionary to store true and false positives for each threshold.
        self.list_of_conf_norms_found = dict()

        for thr in self.threshold_range:
            # Create a dict in which each key leads to a tuple where the first position is
            # the number of true positives and the second is the number of false positives.
            self.dict_thr_tp_fp[thr] = [0, 0, 0, 0]  # Sequence: True positives, True Negatives, False Positives, False Negatives.
            self.list_of_conf_norms_found[thr] = []

    def test_identifier(self):
        # Check each folder in the folders_path and then each contract in the folder.
        # Process contracts and compute true and false positives.

        folders_list = os.listdir(self.folders_path)

        for folder in folders_list:

            folder_files = os.listdir(self.folders_path + folder)

            print "Processing " + self.folders_path + folder

            for file in folder_files:

                print "\tProcessing contract " + self.folders_path + folder + "/" + file

                if 'new_norms' not in file:

                    contract_path = self.folders_path + folder + "/" + file
                    new_contract_path = self.folders_path + folder + "/new_norms_" + file

                    self.process_contract(contract_path, new_contract_path)
                    
        self.write_results()

    def process_contract(self, contract_path, new_contract_path):
        # Read contract path and inserted conflicts file and identify potential conflicts.
        print "\tProcessing Contract..."

        c_finder = Conflict_finder()
        potential_conflicts = c_finder.process(contract_path, self.threshold_range)

        inserted_conflicts = [sent[:-1] for sent in open(new_contract_path, 'r').readlines()]

        self.process_result(potential_conflicts, inserted_conflicts)

    def process_result(self, result, inserted_conflicts):
        # Compute the true and false positives based on the results of process_contracts.
        # Add 1 to true positive

        print "\tProcessing the result..."

        for thr in self.threshold_range:
            self.dict_thr_tp_fp[thr][TN] += result[-1] - len(inserted_conflicts)      # True negatives
            self.dict_thr_tp_fp[thr][FN] += len(inserted_conflicts)                   # False negatives

        for p_conflict in result[:-1]:

            thr = p_conflict[0]

            if self.dict_thr_tp_fp.has_key(thr):
                
                # Check if one of the norms in the potential conflict is in the set of inserted conflicts.
                if p_conflict[1] in inserted_conflicts and p_conflict[1] not in self.list_of_conf_norms_found[thr]: 
                    self.dict_thr_tp_fp[thr][TP] += 1
                    self.dict_thr_tp_fp[thr][FN] -= 1
                    self.list_of_conf_norms_found[thr].append(p_conflict[1])

                elif p_conflict[2] in inserted_conflicts and p_conflict[2] not in self.list_of_conf_norms_found[thr]:
                    self.dict_thr_tp_fp[thr][TP] += 1
                    self.dict_thr_tp_fp[thr][FN] -= 1
                    self.list_of_conf_norms_found[thr].append(p_conflict[2])

                else:
                    self.dict_thr_tp_fp[thr][FP] += 1
                    self.dict_thr_tp_fp[thr][TN] -= 1

            else:
                sys.exit("Something's wrong, I don't know this threshold %.1f!!!" % p_conflict[0])

    def write_results(self):

        output_file = "thr_tr_and_fl_positives.txt"
        wrt_file = open(output_file, 'w')

        for key in self.dict_thr_tp_fp.keys():

            accuracy = (self.dict_thr_tp_fp[key][TP] + self.dict_thr_tp_fp[key][TN])/float(self.dict_thr_tp_fp[key][TP] + self.dict_thr_tp_fp[key][TN] + self.dict_thr_tp_fp[key][FP] + self.dict_thr_tp_fp[key][FN])
            precision = self.dict_thr_tp_fp[key][TP]/float(self.dict_thr_tp_fp[key][TP] + self.dict_thr_tp_fp[key][FP])
            recall = self.dict_thr_tp_fp[key][TP]/float(self.dict_thr_tp_fp[key][TP] + self.dict_thr_tp_fp[key][FN])
            f_measure = 2 * ((precision * recall)/(precision + recall))
            sensitivity = recall
            specificity = self.dict_thr_tp_fp[key][TN]/float(self.dict_thr_tp_fp[key][FP] + self.dict_thr_tp_fp[key][TN])
            fallout = self.dict_thr_tp_fp[key][FP]/float(self.dict_thr_tp_fp[key][FP] + self.dict_thr_tp_fp[key][TN])

            wrt_file.write("""For threshold %.1f:\n\tTrue positives: %d\n\tFalse positives: %d\n\tTrue negatives: %d\n\tFalse negatives: %d\n\tAccuracy: %.2f\n\tPrecision: %.2f\n\tRecall: %.2f\n\tF-Measure: %.2f
                            \n\tSensitivity: %.2f\n\tSpecificity: %.2f\n\tFall-out: %.2f\n\n""" % (key, self.dict_thr_tp_fp[key][TP], self.dict_thr_tp_fp[key][FP],
                             self.dict_thr_tp_fp[key][TN], self.dict_thr_tp_fp[key][FN], accuracy, precision, recall, f_measure, sensitivity, specificity, fallout))

        print "Writing is done."
        wrt_file.close()


if __name__ == "__main__":
    start = time.time()
    tcf = Test_Conf_Finder(THRESHOLD_RANGE, 'data/conflicting_contracts/')
    tcf.test_identifier()
    print time.time() - start