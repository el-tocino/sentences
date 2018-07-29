#!/usr/bin/python3

# https://github.com/el-tocino/sentences

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
            ofile = open (file,"a")
            testsentence = ifile.read()
            print ("Working on parsed file %s" % ifile.name)
            print (testsentence)
            ofile.write ("----- matching sentences -----")
            ratios = (process.extract(testsentence, sentences, scorer = fuzz.partial_ratio, limit = 3))
            for item in ratios:
                ofile.write(str(item))
            ifile.close()
            ofile.close()

sourcetext.close()
           
