import json

def reformat_scraped_data():
    with open('scrape_ukr_forums/replace.json', 'r') as inf, \
            open('scraped.txt', 'w') as outf:
        alldata = json.load(inf)
        for data in alldata:
            for line in data['data']:
                outf.write(line + '\n')

if __name__ == '__main__':
    # reformat_scraped_data()
    with open('../data/try_bi.txt', 'r', encoding='ascii') as f:
        data = json.load(f)
        print(data)
