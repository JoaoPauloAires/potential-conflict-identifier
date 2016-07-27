norm = open("norms/all_sentences.txt", 'r').readlines()
len_norm = len(norm)
noNorm = open("no_norms.txt", 'r').readlines()
len_noNorm = len(noNorm)

modalVerbs = ['can', 'could', 'may', 'might', 'must', 'shall', 'should', 'will', 'would', 'ought']

def identify(text):
    t = text.split()
    for modal in modalVerbs:
        if modal in t:
            return 'norm'        

    return 'noNorm'    

norm_counter = 0
noNorm_counter = 0

for n in norm:
	if identify(n) == 'norm':
		norm_counter += 1
	else:
		print n
		noNorm_counter += 1

print "Identifying norms ", str(float(norm_counter/len_norm))

for n in noNorm:
	if identify(n) == 'noNorm':
		noNorm_counter += 1		
	else:
		norm_counter += 1

print "Identifying nonNorms ", str(float(noNorm_counter/len_noNorm))		