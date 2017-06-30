"""
Created on June 22, 2017
by Khrystyna Skopyk
"""

from scripts.split_tokenize import snippet_to_tokens
import re

CORRECTION = re.compile(r"\w[\w'-]+\{[\w '-]+\}")

def spell_parse(filename):
    """
    Parse the spellchecker test and train corpora.
    :param filename: str
    :return: list of dicts
            {'corrections': {id: correction}, 'sentence':[list of tokens]}
    """
    with open(filename, "r") as f:
        tokens = snippet_to_tokens(re.sub(r"(\w[\w'-]+)\{[\w '-]+\}", r"\1",
                                          f.read()))
        new_tokens = flatten_snippet(tokens)
    data = []
    with open(filename, "r") as f:
        i = 0
        for line in f.readlines():
            print(line)
            spans = [m.span() for m in re.finditer(CORRECTION, line)]
            corrections = [line[b:e].strip("}").split("{") for b, e in spans]
            mapping = {}
            prev = -1
            for orig, corr in corrections:

                prev = new_tokens[i].index(orig, prev + 1)
                mapping[prev] = corr
            data.append({"sentence": new_tokens[i], "true_corrections":
                mapping})
            i += 1
    return data


def flatten_snippet(tokens):
    """
    
    :param tokens: 
    :return: 
    """
    new_tokens = []
    for par in tokens:
        new_sent = []
        for sent in par:
            new_sent.extend(sent)
        new_tokens.append(new_sent)
    return new_tokens


if __name__ == '__main__':
    print(spell_parse("../data/test_corpus_anno.txt"))