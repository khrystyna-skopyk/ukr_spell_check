"""
Created on June 29, 2017
by Khrystyna Skopyk
"""

from scripts.split_tokenize import snippet_to_tokens
from scripts.parse_data import flatten_snippet
from scripts.spell_correct import analyze_tokenized

if __name__ == "__main__":
    string = input("Будь-ласка, введіть текст для перевірки\t(Please, "
                   "enter the text to check): ")
    tokenized = snippet_to_tokens(string)
    new_tokenized = flatten_snippet(tokenized)
    data = analyze_tokenized(new_tokenized)
    outp = []
    n = 0
    for instance in data:
        caught = instance['max_suggested']
        if caught:
            for idx in caught:
                instance['sentence'][idx] = "{{{}=>{}}}".format(instance[
                                                            'sentence'][idx], caught[idx])
                n += 1
            outp.append(" ".join(instance['sentence']))

    if n:
        print("\nУ тексті було знайдено такі помилки\t(Your text contains the "
              "following mistakes):\n\n\t\t{}".format(" ".join(outp)))
    else:
        print("У тексті не було знайдено помилок.\t(Your text does not "
              "contain any mistakes.)")

        # Я кохаю теюе!
        # Я кохаю {теюе=>тебе} ! І я {люлбю=>люблю} тебе !


