"""
Created on June 22, 2017
by Khrystyna Skopyk
"""
from scripts.parse_data import spell_parse
from scripts.spell_correct import candidates_1, candidates_2, proba, PUNCT, \
    ENGLISH_ABC, STOP_WORDS
import re

def analyze_annotated_file(input_file):
    """
    Go through the sentence to detect the misspelling.
    :param input_file: input file name
    :return: list of dictionaries with a tokenized sentence, true corrections 
    and suggested corrections
    """
    tokenized = spell_parse(input_file)
    data = []
    for sent in tokenized:
        sentence = sent['sentence']
        sent['suggested_corrections'] = {}
        sent['max_suggested'] = {}
        for e, token in enumerate(sentence):
            # disregard punctuation and words with latin letters
            if not re.match(PUNCT, token) \
                    and not re.match(ENGLISH_ABC, token.lower()) and\
                    not token.lower() in STOP_WORDS:
                if (e == 0 and token.isupper()) or (e > 0 and token.islower()):
                    corrections = list(candidates_2(token))
                    # add bigrams
                    c_max = max(corrections, key=proba)
                    if c_max != token:
                        sent['max_suggested'][e] = c_max
                        sent['suggested_corrections'][e] = corrections
        data.append(sent)
    return tokenized

def prec_rec(corpus, func):
    """
    Counts precision and recall
    :param corpus: file name to analyze
    :param func: 
    :return: 
    """
    returned = analyze_annotated_file(corpus)
    fn, fp, tp = func(returned)
    precision = round(tp / (tp + fp) * 100, 3)
    recall = round(tp / (tp + fn) * 100, 3)
    print("TPs: {}\nFPs: {}\nFNs: {}\n" \
          "\nPrecision: {}\nRecall: {}".format(tp, fp, fn, precision, recall))

def detection(data):
    """
    
    :param data: 
    :return: 
    """
    tp, fn, fp = 0, 0, 0
    for instance in data:
        suggested_set = set(instance['max_suggested'])
        true_set = set(instance['true_corrections'])
        fn += len(true_set - suggested_set)
        fp += len(suggested_set - true_set)
        tp += len(suggested_set.intersection(true_set))
    return fn, fp, tp

def corrections_max(data):
    """
    
    :param data: 
    :return: 
    """
    tp, fn, fp = 0, 0, 0
    for instance in data:
        suggested = instance['max_suggested']
        true = instance['true_corrections']
        suggested_set = set(suggested)
        true_set = set(true)
        for i in suggested_set.intersection(true_set):
            if true[i] == suggested[i]:
                tp += 1
                print(true[i])
            else:
                fp += 1
                fn += 1
        fn += len(true_set - suggested_set)
        fp += len(suggested_set - true_set)

    return fn, fp, tp

def corrections_all(data):
    """
    
    :param data: 
    :return: 
    """
    tp, fn, fp = 0, 0, 0
    for instance in data:
        suggested = instance['suggested_corrections']
        true = instance['true_corrections']
        suggested_set = set(suggested)
        true_set = set(true)
        for i in suggested_set.intersection(true_set):
            if true[i] in suggested[i]:
                tp += 1
                print(true[i])
            else:
                fp += 1
                fn += 1
        fn += len(true_set - suggested_set)
        fp += len(suggested_set - true_set)

    return fn, fp, tp

if __name__ == '__main__':
    test_corpus = "../data/test_corpus_anno.txt"
    prec_rec(test_corpus, corrections_max)