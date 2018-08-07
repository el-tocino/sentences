#!/usr/bin/python3

import os
import sys
import nltk.data
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from nltk import metrics, stem, tokenize
from difflib import SequenceMatcher

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

sourcetext = open (sys.argv[1])
sourcedata = sourcetext.read()
sentences = tokenizer.tokenize(sourcedata)


def get_best_match(query, corpus, step=4, flex=3, case_sensitive=False, verbose=False):
    """Return best matching substring of corpus.

    Parameters
    ----------
    query : str
    corpus : str
    step : int
        Step size of first match-value scan through corpus. Can be thought of
        as a sort of "scan resolution". Should not exceed length of query.
    flex : int
        Max. left/right substring position adjustment value. Should not
        exceed length of query / 2.

    Outputs
    -------
    output0 : str
        Best matching substring.
    output1 : float
        Match ratio of best matching substring. 1 is perfect match.
    """

    def _match(a, b):
        """Compact alias for SequenceMatcher."""
        return SequenceMatcher(None, a, b).ratio()

    def scan_corpus(step):
        """Return list of match values from corpus-wide scan."""
        match_values = []

        m = 0
        while m + qlen - step <= len(corpus):
            match_values.append(_match(query, corpus[m : m-1+qlen]))
            #if verbose:
                #print query, "-", corpus[m: m + qlen], _match(query, corpus[m: m + qlen])
            m += step

        return match_values

    def index_max(v):
        """Return index of max value."""
        return max(range(len(v)), key=v.__getitem__)

    def adjust_left_right_positions():
        """Return left/right positions for best string match."""
        # bp_* is synonym for 'Best Position Left/Right' and are adjusted 
        # to optimize bmv_*
        p_l, bp_l = [pos] * 2
        p_r, bp_r = [pos + qlen] * 2

        # bmv_* are declared here in case they are untouched in optimization
        bmv_l = match_values[int(p_l / step)]
        bmv_r = match_values[int(p_l / step)]

        for f in range(flex):
            ll = _match(query, corpus[p_l - f: p_r])
            if ll > bmv_l:
                bmv_l = ll
                bp_l = p_l - f

            lr = _match(query, corpus[p_l + f: p_r])
            if lr > bmv_l:
                bmv_l = lr
                bp_l = p_l + f

            rl = _match(query, corpus[p_l: p_r - f])
            if rl > bmv_r:
                bmv_r = rl
                bp_r = p_r - f

            rr = _match(query, corpus[p_l: p_r + f])
            if rr > bmv_r:
                bmv_r = rr
                bp_r = p_r + f

            if verbose:
                print ("\n" + str(f))
                print ("ll: -- value: %f -- snippet: %s" % (ll, corpus[p_l - f: p_r]))
                print ("lr: -- value: %f -- snippet: %s" % (lr, corpus[p_l + f: p_r]))
                print ("rl: -- value: %f -- snippet: %s" % (rl, corpus[p_l: p_r - f]))
                print ("rr: -- value: %f -- snippet: %s" % (rl, corpus[p_l: p_r + f]))

        return bp_l, bp_r, _match(query, corpus[bp_l : bp_r])

    if not case_sensitive:
        query = query.lower()
        corpus = corpus.lower()

    qlen = len(query)

    if flex >= qlen/2:
        print ("Warning: flex exceeds length of query / 2. Setting to default.")
        flex = qlen / 4

    match_values = scan_corpus(step)
    pos = index_max(match_values) * step

    pos_left, pos_right, match_value = adjust_left_right_positions()

    return corpus[pos_left: pos_right].strip(), match_value


for file in os.listdir(sys.argv[2]):
        if file.endswith(".txt"):
            ifile = open (file,"r")
            ## when I tried opening a+, I had failures reading from the file.  So....yeah.
            ofile = open (file,"a")
            print (ifile.name)
            testsentence = ifile.read()
            step_size = int(len(testsentence) * 3/4)
            flex_size = int(len(testsentence) / 3)
            ofile.write ("\n----- matching sentences -----\n")
            ratios = (process.extract(testsentence, sentences, scorer = fuzz.partial_ratio, limit = 3))
            print(*ratios, sep = "\n", file=ofile)                
            diffmatch = get_best_match(testsentence, sourcedata, step_size, flex_size)
            ofile.write ("\n----- diff matching -----\n")
            print (diffmatch, sep = "\n", file=ofile)
            ifile.close()
            ofile.close()

sourcetext.close()
