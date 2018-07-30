#!/usr/bin/python3

import os
import sys
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import nltk.data

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

sourcetext = open (sys.argv[1])
sourcedata = sourcetext.read()
sentences = tokenizer.tokenize(sourcedata)

for file in os.listdir(sys.argv[2]):
        if file.endswith(".txt"):
            ifile = open (file,"r")
            ## when I tried opening a+, I had failures reading from the file.  So....yeah.
            ofile = open (file,"a")
            testsentence = ifile.read()
            ofile.write ("\n----- matching sentences -----\n")
            ratios = (process.extract(testsentence, sentences, scorer = fuzz.partial_ratio, limit = 3))
            print(*ratios, sep = "\n", file=ofile)                
            ifile.close()
            ofile.close()

sourcetext.close()
