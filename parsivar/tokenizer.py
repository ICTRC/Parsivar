import re


class Tokenizer():
    def __init__(self):
        pass

    def tokenize_words(self, doc_string):
        token_list = doc_string.strip().split()
        token_list = [x.strip("\u200c") for x in token_list if len(x.strip("\u200c")) != 0]
        return token_list

    def tokenize_sentences(self, doc_string):
        pattern = r'([!\.\?؟:]+)[ \n]+'
        rep = r'\1\t\t'
        doc_string = re.sub(pattern, rep, doc_string)
        doc_string = doc_string.split('\t\t')
        return doc_string
