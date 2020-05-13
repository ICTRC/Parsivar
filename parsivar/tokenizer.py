import re


class Tokenizer():
    def __init__(self):
        pass

    def tokenize_words(self, doc_string):
        token_list = doc_string.strip().split()
        token_list = [x.strip("\u200c") for x in token_list if len(x.strip("\u200c")) != 0]
        return token_list

    def tokenize_sentences(self, doc_string):
        #finding the numbers
        pattern = r"[-+]?\d*\.\d+|\d+"
        nums_list = re.findall(pattern, doc_string)
        doc_string = re.sub(pattern, 'floatingpointnumber', doc_string)

        pattern = r'([!\.\?؟]+)[\n]*'
        tmp = re.findall(pattern, doc_string)
        doc_string = re.sub(pattern, self.add_tab, doc_string)

        pattern = r':\n'
        tmp = re.findall(pattern, doc_string)
        doc_string = re.sub(pattern, self.add_tab, doc_string)

        pattern = r';\n'
        tmp = re.findall(pattern, doc_string)
        doc_string = re.sub(pattern, self.add_tab, doc_string)

        pattern = r'؛\n'
        tmp = re.findall(pattern, doc_string)
        doc_string = re.sub(pattern, self.add_tab, doc_string)

        pattern = r'[\n]+'
        doc_string = re.sub(pattern, self.add_tab, doc_string)

        for number in nums_list:
            pattern = 'floatingpointnumber'
            doc_string = re.sub(pattern, number, doc_string, 1)

        doc_string = doc_string.split('\t\t')
        doc_string = [x for x in doc_string if len(x) > 0]
        return doc_string

    def add_tab(self, mystring):
        mystring = mystring.group()  # this method return the string matched by re
        mystring = mystring.strip(' ')  # ommiting the whitespace around the pucntuation
        mystring = mystring.strip('\n') # ommiting the newline around the pucntuation
        mystring = " " + mystring + "\t\t"  # adding a space after and before punctuation
        return mystring