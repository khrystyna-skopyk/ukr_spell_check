"""
Created on June 22, 2017
by Khrystyna Skopyk
"""

from scripts.spell_correct import analyze_file
import json
import tokenize_uk

def reformat_scraped_data():
    with open('scrape_ukr_forums/replace.json', 'r') as inf, \
            open('scraped.txt', 'w') as outf:
        alldata = json.load(inf)
        for data in alldata:
            for line in data['data']:
                outf.write(line + '\n')

def reformat_split_sents():
    with open('../data/scraped.txt', 'r') as inf, \
            open('../data/new_scraped.txt', 'w') as outf:
        new_sents = [s for snip in inf.readlines() for s in
                      tokenize_uk.tokenize_sents(snip)]
        for sent in new_sents:
            outf.write(sent+"\n")

def annotating_corpus(input_file, base):
    n = 0
    processed_data = analyze_file(input_file)
    with open('../data/{}.txt'.format(base), 'w') as outputf:
        for instance in processed_data:
            instance['annotations'] = 0
            caught = instance['max_suggested']
            if caught:
                for idx in caught:
                    instance['sentence'][idx] = "{}{{{}}}".format(instance['sentence'][idx], caught[idx])
                    instance['annotations'] += 1
                    n += 1
            outputf.write(" ".join(instance['sentence']) +
                          "\t\t|| {} ANNO\n".format(instance['annotations']))
    # print("The file was checked for spelling errors with {} annotations "
    #       "overall.".format(n))




if __name__ == '__main__':
    annotating_corpus("../data/scraped_5K.txt", "scraped_5K_anno")
    # reformat_split_sents()
    # reformat_scraped_data()
    # with open('../data/try_bi.txt', 'r', encoding='ascii') as f:
    #     data = json.load(f)
    #     print(data)
