import pickle
import re
import string
import os


class DataHelper():
    def __init__(self):
        pass

    def clean_text(self, text_doc):
        punctuations = r')(}{:؟!،؛»«.' + r"/<>?.,:;"
        punctuations = '[' + punctuations + string.punctuation + ']'
        punctuations = punctuations.replace("@", "")

        text_doc.strip()

        # pattern = ur'\s*@[a-zA-Z0-9]*\s*'
        # tmp = re.findall(pattern, text_doc)
        # newstring = re.sub(pattern, eliminate_pattern, text_doc)


        pattern = '\s*' + punctuations + '+' + '\s*'
        tmp = re.findall(pattern, text_doc)
        newstring = re.sub(pattern, self.add_space, text_doc)

        # pattern = u'([a-zA-Z0-9]+)(\s*)(' + punctuations + u')(\s*)([a-zA-Z0-9]+)'
        # rep = ur'\1\3\5'
        # tmp = re.findall(pattern, newstring)
        # newstring = re.sub(pattern, rep, newstring)


        pattern = r'[\n]+'
        tmp = re.findall(pattern, newstring)
        newstring = re.sub(pattern, "\n ", newstring)

        punctuations = r")(}{:؟!،؛»«.@$&%" + r"/<>?.,:;"
        latinLettersDigits = r"a-zA-Z0-9"
        pattern = r'[^' + punctuations + latinLettersDigits + 'آ-ی' + '‌' + '\d\s:]'
        tmp = re.findall(pattern, newstring)
        newstring = re.sub(pattern, self.eliminate_pattern, newstring)

        return newstring

    def add_space(self, mystring):
        mystring = mystring.group()  # this method return the string matched by re
        mystring = mystring.strip()  # ommiting the whitespace around the pucntuation
        mystring = " " + mystring + " "  # adding a space after and before punctuation
        return mystring

    def replace_newline_with_dot(self, mystring):
        return ' . '

    def eliminate_pattern(self, mystring):
        return ""

    def load_var(self, load_path):
        file = open(load_path, 'rb')
        variable = pickle.load(file)
        file.close()
        return variable

    def save_var(self, save_path, variable):
        print("saving vars ...")
        file = open(save_path, 'wb')
        pickle.dump(variable, file)
        print("variable saved.")
        file.close()

    def build_stem_dictionary(self, normalizer, verb_tense_path, mokasar_noun_path):
        path_dir = "resource/Persian_Dependency_Treebank/Data/2ndRep"
        lexicon_stem = set()
        verb_stem = set()
        #verb_tense_map = {}
        verb_p2f_map = {}
        verb_f2p_map = {}
        for fileName in os.listdir(path_dir):
            file_path = path_dir + "/" + fileName
            with open(file_path, "r") as input:
                input_content = input.readlines()
                for el in input_content:
                    el = normalizer.sub_alphabets(el)
                    el = el.split("\t")
                    if (len(el) > 2):
                        if (el[3] == 'V'):
                            tmp_pos = "V"
                        else:
                            tmp_pos = "N"
                        stem_word = el[2]
                        stem_word = stem_word.split("#")
                        stem_word = [x.strip('\u200c') for x in stem_word]
                        if (tmp_pos == "V" and len(stem_word) == 2):
                            if (len(stem_word[0]) != 0 and len(stem_word[1]) != 0):
                                verb_p2f_map[stem_word[0]] = stem_word[1]
                                verb_f2p_map[stem_word[1]] = stem_word[0]
                                verb_stem.add(stem_word[0])
                                verb_stem.add(stem_word[1])
                        if(tmp_pos == 'V' and len(stem_word) == 3):
                            if(len(stem_word[0]) != 0 and len(stem_word[1]) != 0 and len(stem_word[2]) !=0):
                                #verb_prifix.add(stem_word[0])
                                verb_p2f_map[stem_word[1]] = stem_word[2]
                                verb_f2p_map[stem_word[2]] = stem_word[1]
                                verb_stem.add(stem_word[1])
                                verb_stem.add(stem_word[2])
                        for t in stem_word:
                            if len(t) > 1:
                                if (tmp_pos == 'N'):
                                    lexicon_stem.add(t)


        with open(verb_tense_path, "r") as bon_file:
            bon_file_content = bon_file.readlines()
            for el in bon_file_content:
                el = el.strip()
                el = normalizer.sub_alphabets(el)
                el = el.split()
                el = [x.strip('\u200c') for x in el]

                verb_p2f_map[el[0]] = el[1]
                verb_f2p_map[el[1]] = el[0]
                verb_stem.add(el[0])
                verb_stem.add(el[1])

        irregular_noun = {}
        with open(mokasar_noun_path, "r") as input:
            input_content = input.readlines()
            for el in input_content:
                el = normalizer.sub_alphabets(el)
                el = el.replace("\t\t", "\t")
                el = el.strip().split("\t")
                el = [x.strip('\u200c') for x in el]
                irregular_noun[el[0]] = el[1]
                lexicon_stem.add(el[0])

        verb_tense_map = [verb_p2f_map, verb_f2p_map]
        return lexicon_stem, verb_stem, verb_tense_map, irregular_noun
