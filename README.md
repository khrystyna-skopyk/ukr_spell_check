# ukr-spell-check

This code implements **the noisy channel model** for the Ukrainian spelling corrector.
The project was started as a pet research task for [the Lancaster summer school on Corpus-based NLP](http://ucrel.lancs.ac.uk/summerschool/nlp.php) that I attended in June 2017.
I also prepared a small poster for this project which could be found [here](https://drive.google.com/file/d/0B4ZvRIQJjnSec0J5WUNJbkUtSTg/view?usp=sharing).

## Requirements

The code is written in python 3.5 and uses [tokenize_uk](http://tokenize-uk.readthedocs.io/en/latest/) and [nltk](http://www.nltk.org/install.html) library.
If you're using a UNIX-based OS, installing the dependencies should look like:

```bash
$ pip install tokenize_uk
$ sudo pip install -U nltk
$ sudo pip install -U numpy
```

See the documentation provided above for more details.

## Usage

### Data

Some data used is stored inside the `data/` directory.
The LM was collected from a part of [UberText Corpus](http://lang.org.ua/en/corpora/#anchor4), namely 2M sentences of Wikipedia corpus. This data is not in this repository.
The system was tested on the scraped corpus (`/data/scraped.txt`) from the [http://replace.org.ua/](http://replace.org.ua/) forum.
The `/data/scraped_5K_anno.txt` file contains auto-annotated 5K sentences from the scraped corpus.
The `/data/test_corpus_anno.txt` contains 14 sentences with 15 manually annotated spelling mistakes.

### Demo and code

All the code is availanle in `/scripts` directory.
You can run `/scripts/demo.py` to try out the system.
The main algorithm is written in `/scripts/spell_correct.py`.

## TODO

**Step 1:**

1.1. Recollect stop words (`/data/ukr_stop_words.txt`).

1.2. Remove inflections from the candidate set.

1.3. Add hyphenated words on the candidate generation step.

1.4. Use bigger corpus for language modelling and ngrams.

1.5. Add ngram logic to the candidate generation step.

**Step 2:**

2.1 Rerun the system on the scraped data and automatically annotated it.

2.2. Manually annotate the resulting corpus and use it for error model for the same system.

## License

To be decided.

