#!/usr/bin/python3

import sys
import nltk.data
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

fp = open(sys.argv[1] + ".txt")
data = fp.read()
#print '\n-----\n'.join(tokenizer.tokenize(data))
sentences = tokenizer.tokenize(data)
counter = 0
for line in sentences:
    outfile = open(sys.argv[1] + str(counter) + ".txt", "wt")
    outfile.write (line)
    outfile.close
    counter += 1
    print(line)


