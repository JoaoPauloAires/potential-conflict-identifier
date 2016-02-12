# -*- coding: utf-8 -*-

# Imports (many of them)

# Constants
CONTRACT_PATH = "SOMETHING YOU STILL HAVE TO FILL"

if __name__ == "__main__":
	# It could have a contract reader...
	nr = Norm_Representation()
	nc = Norm_Comparison()
	norm_representations = nr.process(contract)
	potential_conflicts  = nc.process(norm_representations)	