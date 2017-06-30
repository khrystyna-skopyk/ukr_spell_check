"""
Created on June 22, 2017
by Khrystyna Skopyk
"""

import tokenize_uk

def snippet_to_tokens(snip):
    """
    Tokenizes snippets (one sentence or more).
    :param snip: string 
    :return: list of lists of lists,
             e.g. [[[str, str, ...], [str, str, ...]], [...], ...]
    """
    return tokenize_uk.tokenize_text(snip)

if __name__ == '__main__':
    test = "А, хто розуміє,що її немає. Той мовчить собі у ганчірочку.\n" \
            "Ато не дай Боже,розгнівати ВВ і бути покараним на кшталт Політковської."
    print(snippet_to_tokens(test))