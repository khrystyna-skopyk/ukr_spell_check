from scripts.split_tokenize import snippet_to_tokens
import re
import json

PUNCT = re.compile(r"[.,:!@#$%^&*()~`_+=';<>/\[\]\\{}\"-]+")

with open("../data/wiki_2M_uni.txt", 'r') as uni:
    UNIGRAMS = json.load(uni)
    N = len(UNIGRAMS)

def proba(word):
    """
    Returns probability of the word.
    :param word: string 
    :return: float
    """
    return UNIGRAMS[word] / N

def analyze_snippet(snip):
    """
    Goes through the sentence to detect the misspelling.
    :param snippit: string
    :return: tuples of misspellings and their indices and corrections
    """
    all_mis = []
    tokenized = snippet_to_tokens(snip)
    for par in tokenized:
        p_mis = []
        for sent in par:
            misspellings = []
            for e, token in enumerate(sent):
                if not re.match(PUNCT, token):
                    if (e == 0 and token.isupper()) or (e > 0 and token.islower()):
                        c = correction(token.lower())
                        if c != token.lower():
                            misspellings.append((e, token, c))
            p_mis.append(misspellings)
        all_mis.append(p_mis)
    return all_mis


def correction(word):
    """
    Returns the most probable spelling correction for word.
    :param word: string
    :return: string
    """
    x= candidates(word)
    print(x)
    return max(x, key=proba)

def candidates(word):
    """
    Generates possible spelling corrections for word.
    :param word: string 
    :return: set of strings
    """
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

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
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
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
    case = "Кинь її і вона буде вражена твоїм пступком,"
    print(analyze_snippet(case))