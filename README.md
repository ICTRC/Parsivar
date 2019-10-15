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
>>> tmp_text = "به گزارش ایسنا سمینار شیمی آلی از امروز ۱۱ شهریور ۱۳۹۶ در دانشگاه علم و صنعت ایران آغاز به کار کرد. این سمینار تا ۱۳ شهریور ادامه می یابد."
>>> from parsivar import Normalizer
>>> my_normalizer = Normalizer()
>>> print(my_normalizer.normalize(tmp_text))
'به گزارش ایسنا سمینار شیمی آلی از امروز 11 شهریور 1396 در دانشگاه علم و صنعت ایران آغاز به کار کرد . این سمینار تا 13 شهریور ادامه می‌یابد .'


>>> my_normalizer = Normalizer(statistical_space_correction=True)
>>> print(my_normalizer.normalize(tmp_text))
'به گزارش ایسنا سمینار شیمی آلی از امروز 11 شهریور 1396 در دانشگاه علم و صنعت ایران آغاز به کار کرد . این سمینار تا 13 شهریور ادامه می‌یابد .'


>>> my_normalizer = Normalizer(date_normalizing_needed=True)
>>> print(my_normalizer.normalize(tmp_text))
'به گزارش ایسنا سمینار شیمی آلی از امروز y1396m6d11 در دانشگاه علم و صنعت ایران آغاز به کار کرد . این سمینار تا y0m6d13 ادامه می‌یابد .'


>>> my_normalizer = Normalizer(pinglish_conversion_needed=True)
>>> print(my_normalizer.normalize("farda asman abri ast."))
'فردا اسمان ابری است .'


>>> from parsivar import Tokenizer
>>> my_normalizer = Normalizer()
>>> my_tokenizer = Tokenizer()
>>> sents = my_tokenizer.tokenize_sentences(my_normalizer.normalize(tmp_text))
>>> print(sents)
['به گزارش ایسنا سمینار شیمی آلی از امروز 11 شهریور 1396 در دانشگاه علم و صنعت ایران آغاز به کار کرد .', 'این سمینار تا 13 شهریور ادامه می\u200cیابد .']

 
>>> words = my_tokenizer.tokenize_words(my_normalizer.normalize(tmp_text))
>>> print(words)
['به', 'گزارش', 'ایسنا', 'سمینار', 'شیمی', 'آلی', 'از', 'امروز', '11', 'شهریور', '1396', 'در', 'دانشگاه', 'علم', 'و', 'صنعت', 'ایران', 'آغاز', 'به', 'کار', 'کرد', '.', 'این', 'سمینار', 'تا', '13', 'شهریور', 'ادامه', 'می\u200cیابد', '.']
 
 
>>> from parsivar import FindStems
>>> my_stemmer = FindStems()
>>> print(my_stemmer.convert_to_stem("بیابیم"))
'یافت'
 
 
 
>>> from parsivar import POSTagger
>>> my_tagger = POSTagger(tagging_model="wapiti")  # tagging_model = "wapiti" or "stanford". "wapiti" is faster than "stanford"
>>> text_tags = my_tagger.parse(my_tokenizer.tokenize_words("این سمینار تا 13 شهریور ادامه می‌یابد ."))
>>> print(text_tags)
[('این', 'DET'), ('سمینار', 'N_SING'), ('تا', 'P'), ('13', 'NUM'), ('شهریور', 'N_SING'), ('ادامه', 'N_SING'), ('می\u200cیابد', 'V_PRS'), ('.', '.')]
 
 
 
>>> from parsivar import FindChunks
>>> my_chunker = FindChunks()
>>> chunks = my_chunker.chunk_sentence(text_tags)
>>> print(my_chunker.convert_nestedtree2rawstring(chunks))
[این سمینار DNP] [تا 13 شهریور NPP] [ادامه می‌یابد VP] .



>>> from parsivar import DependencyParser
>>> myparser = DependencyParser()
>>> sents = "به گزارش ایسنا سمینار شیمی آلی از امروز ۱۱ شهریور ۱۳۹۶ در دانشگاه علم و صنعت ایران آغاز به کار کرد. این سمینار تا ۱۳ شهریور ادامه می یابد"
>>> sent_list = my_tokenizer.tokenize_sentences(sents)
>>> parsed_sents = myparser.parse_sents(sent_list)
>>> for depgraph in parsed_sents:
>>> 	print(depgraph.tree())
(به (گزارش (ایسنا (سمینار (شیمی آلی)))))
(یابد (سمینار این) (تا (شهریور ۱۳)) ادامه می)

>>> from parsivar import SpellCheck
>>> myspell_checker = SpellCheck()
>>> res = myspell_checker.spell_corrector("نمازگذاران وارد مسلی شدند.")
'نمازگزاران وارد مصلی شدند .'

```


## Installation
The latest version can be installed through `pip`:

	pip3 install parsivar

	To use the spell checker module download it's resources from
	https://www.dropbox.com/s/tlyvnzv1ha9y1kl/spell.zip?dl=0
	and after extraction copy the spell/ directory to parsivar/resource.