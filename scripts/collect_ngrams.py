"""
Created on June 22, 2017
by Khrystyna Skopyk
"""

# -*- coding: utf-8 -*-

from nltk import ngrams, bigrams
from scripts.split_tokenize import snippet_to_tokens
from collections import defaultdict
import re
import json
import time

PUNCT = re.compile(r"[.,:!@#$%^&*()~`_+=';<>/\[\]\\{}\"-]+")
ENGLISH_ABC = re.compile(r".*[abcdefghijklmnopqrstuvwxyz].*")
with open("../data/ukr_stop_words.txt", 'r') as stop:
    STOP_WORDS = [w.strip() for w in stop.readlines()]


def remap_keys(d):
    """
    
    :param d: 
    :return: 
    """
    return [{'key': k, 'value': v} for k, v in d.items()]


def timing(func):
    """
    Times the function.
    :param func: function
    :return: None. Print the time it took to process a function.
    """
    def wrap(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        print("It took {:.4f} secs to process the file.".format(time.time() -
                                                                start))
    return wrap


@timing
def collect_from_file(input_file, base):
    """
    Collects uni-, bi-, trigrams from the given data.
    :param input_file: file to collect ngrams from
    :param base: string to add to the output files
    :return: None. Saves files with collected ngrams to the files.
    """
    with open(input_file, 'r') as inf:
        text = inf.read()
    tokenized_all = snippet_to_tokens(text)
    dct_uni = defaultdict(int)
    dct_bi = defaultdict(int)
    dct_tri = defaultdict(int)
    for big_e, par in enumerate(tokenized_all):
        for sent in par:
            # unigrams
            for e, token in enumerate(sent):
                if not re.match(PUNCT, token) \
                        and not re.match(ENGLISH_ABC, token.lower()) and \
                        not token.lower() in STOP_WORDS:
                    if (e == 0 and token.isupper()) or \
                            (e > 0 and token.islower()):
                        dct_uni[token] += 1
            sent = ["<S>"] + sent + ["</S>"]
            # bigrams
            for bi in bigrams(sent):
                dct_bi[bi] += 1
            # trigrams
            for tri in ngrams(sent, 3):
                dct_tri[tri] += 1
        if big_e % 10000 == 0:
            print(big_e)
    dct_bi = remap_keys(dct_bi)
    dct_tri = remap_keys(dct_tri)
    with open("../data/"+base+"_uni.txt", 'w', encoding='ascii') as u, \
            open("../data/"+base+"_bi.txt", 'w', encoding='ascii') as bi, \
            open("../data/"+base+"_tri.txt", 'w', encoding='ascii') as tri:
        json.dump(dct_uni, u)
        json.dump(dct_bi, bi)
        json.dump(dct_tri, tri)

if __name__ == '__main__':
    collect_from_file('../data/wiki_dump_2M.txt', 'wiki_2M_2v')
