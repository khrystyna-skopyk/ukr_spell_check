import tokenize_uk

def snippet_to_tokens(snip):
    """
    Tokenizes snippets (one sentence or more).
    :param snip: string 
    :return: [[str, str, ...], [...], ...]
    """
    return tokenize_uk.tokenize_text(snip)

if __name__ == '__main__':
    case = "А,хто розуміє,що її немає, той мовчить собі у ганчірочку," \
             "ато не дай Боже,розгнівати ВВ і бути покараним на кшталт Політковської."
    print(snippet_to_tokens(case))