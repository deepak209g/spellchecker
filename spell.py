from __future__ import division
# from autocorrect import spell
import sys
import re
# import File_Utils as fu
import os
from collections import Counter
import math
from spellnovig import correction as novig_correction

from timeit import default_timer as timer

start = timer()
# ...
end = timer()

def evaluate_speed(f, funame):
    def helper(*x):
        start = timer()
        toret = f(*x)
        end = timer()
        print '[+] ' + funame + ' ' + str(end - start)
        return toret
    return helper

def memoize(f):
    memo = {}
    def helper(*x):
        if x not in memo:
            memo[x] = f(*x)
        return memo[x]
    return helper


novig_correction = evaluate_speed(novig_correction, 'NovigCorrection')
def jaccards_coefficient(seta, setb):
    # print seta
    # print setb
    intersecton = seta & setb
    union = seta | setb
    return len(intersecton) / len(union)


# jaccards_coefficient = memoize(jaccards_coefficient)

def get_bigrams(name):
    bigrams = set()
    for i in range(0, len(name) - 1):
        bigrams.add(name[i: i + 2])

    if len(bigrams) == 0:
        bigrams.add(name)
    return bigrams


get_bigrams = memoize(get_bigrams)


def best_match_against_dict(keyword, listofwords):
    orignal = keyword.lower()
    keyword = keyword.lower()
    keyword_bigrams = get_bigrams(keyword)
    best_match_word = None
    best_coefficient = 0
    if keyword in listofwords:
        return keyword, 1.0

    for word in listofwords:
        # first optimization
        # ignore word from dictionary if size difference is more than 2
        if abs(len(keyword) - len(word)) > 2:
            continue

        word_bigrams = get_bigrams(word)
        coeff = jaccards_coefficient(keyword_bigrams, word_bigrams)
        if coeff > best_coefficient:
            best_coefficient = coeff
            best_match_word = word

    if best_match_word is None:
        return orignal, 1 / math.e

    return best_match_word, best_coefficient

# best_match_against_dict = memoize(best_match_against_dict)

best_match_against_dict = evaluate_speed(best_match_against_dict, 'MySpellChecker')

def myspell(phrase, origlen = None):
    best_sep = None
    max_score = -1
    if origlen == None:
        origlen = len(phrase)
    for i in range(len(phrase) - 1):
        pref = phrase[:i]
        if len(pref) <= 3:
            continue

        pref_match, pref_score = best_match_against_dict(pref, bigramsdict)
        suff_match = myspell(phrase[i:], origlen)
        best_score = math.log(pref_score * len(pref_match)) * len(pref_match) / origlen
        for tup in suff_match:
            best_score = best_score * math.log(tup[1] * len(tup[0]) ) * len(tup[0]) / origlen

        best_score = math.fabs(best_score)
        best_score = best_score
        if best_score > max_score:
            max_score = best_score
            best_sep = []
            best_sep.append((pref_match, pref_score))
            best_sep.extend(suff_match)
    if best_sep == None:
        best_sep = []
        best_sep.append(best_match_against_dict(phrase, bigramsdict))
    return best_sep


myspell = memoize(myspell)



def words(text):
    return re.findall('[a-z]+', text.lower())



if __name__ == '__main__':
    # print words(open('data/5000words.txt').read())
    dictionary = Counter(words(open('data/5000words.txt').read()))
    print best_match_against_dict('autoo', dictionary)
    print novig_correction('autoo')