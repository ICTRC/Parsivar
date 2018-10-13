parsivar
------------

Python library for preprocessing Persian text.

+ Text Normalizing
+ Half space correction in Persian text
+ Word and sentence tokenizer (splitting words and sentences)
+ Word stemming
+ POS tagger
+ Shallow parser (Chunker)

##requirements

+ [NLTK](http://nltk.org/) compatible
+ Python 2.7 support
+ libwapiti>=0.2.1 (if speed is an important factor)
+ nltk>=3.2.2


## Usage

```python
>>> tmp_text = u"به گزارش ایسنا سمینار شیمی آلی از امروز ۱۱ شهریور ۱۳۹۶ در دانشگاه علم و صنعت ایران آغاز به کار کرد. این سمینار تا ۱۳ شهریور ادامه می یابد."
>>> from parsivar import normalizer
>>> my_normalizer = normalizer.Normalizer()
>>> print my_normalizer.normalize(tmp_text)
'به گزارش ایسنا سمینار شیمی آلی از امروز 11 شهریور 1396 در دانشگاه علم و صنعت ایران آغاز به کار کرد . این سمینار تا 13 شهریور ادامه می‌یابد .'


>>> my_normalizer = normalizer.Normalizer(statistical_space_correction=True)
>>> print my_normalizer.normalize(tmp_text)
'به گزارش ایسنا سمینار شیمی آلی از امروز 11 شهریور 1396 در دانشگاه علم و صنعت ایران آغاز به کار کرد . این سمینار تا 13 شهریور ادامه می‌یابد .'


>>> my_normalizer = normalizer.Normalizer(date_normalizing_needed=True)
>>> print my_normalizer.normalize(tmp_text)
'به گزارش ایسنا سمینار شیمی آلی از امروز y1396m6d11 در دانشگاه علم و صنعت ایران آغاز به کار کرد . این سمینار تا y0m6d13 ادامه می‌یابد .'


>>> my_normalizer = normalizer.Normalizer(pinglish_conversion_needed=True)
>>> print my_normalizer.normalize("farda asman abri ast.")
'فردا اسمان ابری است .'


>>> from parsivar import tokenizer
>>> my_normalizer = normalizer.Normalizer()
>>> my_tokenizer = tokenizer.Tokenizer()
>>> sents = my_tokenizer.tokenize_sentences(my_normalizer.normalize(tmp_text))
>>> print sents
[u'به گزارش ایسنا سمینار شیمی آلی از امروز 11 شهریور 1396 در دانشگاه علم و صنعت ایران آغاز به کار کرد .',
 u'این سمینار تا 13 شهریور ادامه می‌یابد .']

 
>>> words = my_tokenizer.tokenize_words(my_normalizer.normalize(tmp_text))
>>> print words
[u'به', u'گزارش', u'ایسنا', u'سمینار', u'شیمی', u'آلی', u'از', u'امروز', u'11', u'شهریور', u'1396', u'در', u'دانشگاه', u'علم', u'و', u'صنعت', u'ایران', u'آغاز', u'به', u'کار', u'کرد', u'.', u'این', u'سمینار', u'تا', u'13', u'شهریور', u'ادامه', u'می‌یابد', u'.']
 
 
>>> from parsivar import stemmer
>>> my_stemmer = stemmer.FindStems()
>>> print my_stemmer.convert_to_stem(u"بیابیم")
u'یافت'
 
 
 
>>> from parsivar import postagger
>>> my_tagger = postagger.POSTagger(tagging_model="wapiti")# tagging_model = "wapiti" or "stanford". "wapiti" is faster than "stanford"
>>> text_tags = my_tagger.parse(my_tokenizer.tokenize_words(u"این سمینار تا 13 شهریور ادامه می‌یابد ."))
>>> print text_tags
[(u'این', u'DET'), (u'سمینار', u'N_SING'), (u'تا', u'P'), (u'13', u'NUM'), (u'شهریور', u'N_SING'), (u'ادامه', u'N_SING'), (u'می‌یابد', u'V_PRS'), (u'.', u'.')]
 
 
 
>>> from parsivar import chunker
>>> my_chunker = chunker.FindChunks()
>>> chunks = my_chunker.chunk_sentence(text_tags)
>>> print my_chunker.convert_nestedtree2rawstring(chunks)
u'[این سمینار DNP] [تا 13 شهریور NPP] [ادامه می‌یابد VP] .'



>>> from dependency import DependencyParser
>>> myparser = DependencyParser()
>>> sent = u'به گزارش ایسنا سمینار شیمی آلی از امروز ۱۱ شهریور ۱۳۹۶ در دانشگاه علم و صنعت ایران آغاز به کار کرد.'
>>> parsed_sent = myparser.parse_sent(sent)
>>> print(parsed_sent.tree())
```


## Installation
The latest verson can be installed through `pip`:

	pip install parsivar
