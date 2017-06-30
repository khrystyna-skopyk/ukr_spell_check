"""
Created on June 22, 2017
by Khrystyna Skopyk
"""

from scripts.parse_data import flatten_snippet
from scripts.split_tokenize import snippet_to_tokens
from scripts.med import med_dl_main
import re
import json

PUNCT = re.compile(r"[.,:!@#$%^&*()~`_+=';<>/\[\]\\{}\"-]+")
ENGLISH_ABC = re.compile(r".*[abcdefghijklmnopqrstuvwxyz].*")
DEFAULT_MED = 2

with open("../data/ukr_stop_words.txt", 'r') as stop:
    STOP_WORDS = [w.strip() for w in stop.readlines()]

with open("../data/wiki_2M_2v_uni.txt", 'r') as uni:
    UNIGRAMS = json.load(uni)
    N_UNI = len(UNIGRAMS)


def qualifies(word1, word2, limit):
    """
    Checks if the word isn't too dissimilar with the target word.
    :param word1: 
    :param word2: 
    :param limit: 
    :return: 
    """
    return (abs(len(word1) - len(word2)) <= DEFAULT_MED
            and len(set(word1).symmetric_difference(set(word2)))
                <= DEFAULT_MED * limit)


def proba(word):
    """
    Returns probability of the word.
    :param word: string 
    :return: float
    """
    if word in UNIGRAMS:
        return UNIGRAMS[word] / N_UNI
    return 0


def analyze_file(input_file):
    """
    Go through the sentence to detect the misspelling.
    :param input_file: input file name
    :return: list of dictionaries with a tokenized sentence, true corrections 
    and suggested corrections
    """
    with open(input_file, "r") as f:
        tokenized = snippet_to_tokens(f.read())
        new_tokenized = flatten_snippet(tokenized)
    return analyze_tokenized(new_tokenized)


def analyze_tokenized(new_tokenized):
    data = []
    for emain, sent in enumerate(new_tokenized):
        instance = dict()
        instance['sentence'] = sent
        instance['suggested_corrections'] = {}
        instance['max_suggested'] = {}
        for e, token in enumerate(sent):
            # disregard punctuation and words with latin letters
            if not re.match(PUNCT, token) \
                    and not re.match(ENGLISH_ABC, token.lower()) and \
                    not token.lower() in STOP_WORDS:
                if (e == 0 and token.isupper()) or (e > 0 and token.islower()):
                    corrections = list(candidates_2(token))
                    # add bigrams
                    c_max = max(corrections, key=proba)
                    if c_max != token:
                        instance['max_suggested'][e] = c_max
                        instance['suggested_corrections'][e] = corrections
        data.append(instance)
        # if emain % 1000 == 0:
        #     print(emain)
    return data


##################
# The following functions generate candidates for a misspelling using
# Damerau-Levenstain minimum edit distance.


def candidates_1(word):
    """
    Generates possible spelling corrections for word.
    :param word: string 
    :return: set of strings
    """
    if word in UNIGRAMS:
        return [word]
    return minimum_edit_distance(word) or [word]


def minimum_edit_distance(word):
    cands_1 = []
    cands_2 = []
    for cand in UNIGRAMS:
        if qualifies(word, cand, 2):
            m = med_dl_main(word, cand)
            if m == DEFAULT_MED - 1:
                cands_1.append(cand)
            if m == DEFAULT_MED:
                cands_2.append(cand)
    return cands_1 or cands_2


##################
# The following functions generate candidates for a misspelling using
# "dummy" iteration.


def candidates_2(word):
    """
    Generates possible spelling corrections for word.
    :param word: string 
    :return: set of strings
    """
    return (known([word]) or known(edits1(word)) or known(edits2(word))
            or [word])


def known(words):
    """
    Returns the subset of `words` that appear in the dictionary of UNIGRAMS.
    :param words: list of strings
    :return: set of strings
    """
    return set(w for w in words if w in UNIGRAMS)


def edits1(word):
    """
    Returns all edits that are one edit away from `word`.
    :param word: string
    :return: set of strings
    """
    letters = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    """
    Returns all edits that are two edits away from `word`.
    :param word: string
    :return: set of strings
    """
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


if __name__ == '__main__':
    test_file = "../data/test_corpus.txt"
    print(analyze_file(test_file))
