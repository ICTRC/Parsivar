# coding=utf-8

import normalizer
import os
import data_helper

class FindStems():

    def __init__(self):

        self.dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"

        self.noun_lex_path = self.dir_path + "resource/stemmer/stem_lex.pckl"
        self.verb_lex_path = self.dir_path + "resource/stemmer/verbStemDict.pckl"
        self.verb_tense_map_path = self.dir_path + "resource/stemmer/stem_verbMap.pckl"
        self.irregular_nouns_path = self.dir_path + "resource/stemmer/stem_irregularNounDict.pckl"
        self.prefix_list_path = self.dir_path + "resource/stemmer/pishvand.txt"
        self.postfix_list_path = self.dir_path + "resource/stemmer/pasvand.txt"
        self.verb_tense_file_path = self.dir_path + "resource/stemmer/verb_tense.txt"
        self.mokasar_noun_path = self.dir_path + "resource/stemmer/mokasar.txt"


        if(os.path.isfile(self.noun_lex_path) and os.path.isfile(self.verb_lex_path)
           and os.path.isfile(self.verb_tense_map_path) and os.path.isfile(self.irregular_nouns_path)):
            self.noun_lexicon = data_helper.load_var(self.noun_lex_path)
            self.verb_lexicon = data_helper.load_var(self.verb_lex_path)
            self.verb_tense_map = data_helper.load_var(self.verb_tense_map_path)
            self.irregular_nouns = data_helper.load_var(self.irregular_nouns_path)

            self.verb_p2f_map, self.verb_f2p_map = self.verb_tense_map[0], self.verb_tense_map[1]

        else:
            self.mynormalizer = normalizer.Normalizer()
            self.noun_lexicon, self.verb_lexicon, \
            self.verb_tense_map, self.irregular_nouns = \
                data_helper.build_stem_dictionary(self.mynormalizer,
                                                  self.verb_tense_file_path,
                                                  self.mokasar_noun_path)
            data_helper.save_var(save_path=self.noun_lex_path, variable=self.noun_lexicon)
            data_helper.save_var(save_path=self.verb_lex_path, variable=self.verb_lexicon)
            data_helper.save_var(save_path=self.verb_tense_map_path, variable=self.verb_tense_map)
            data_helper.save_var(save_path=self.irregular_nouns_path, variable=self.irregular_nouns)

            self.verb_p2f_map, self.verb_f2p_map = self.verb_tense_map[0], self.verb_tense_map[1]


        self.prefix_list = set({})
        with open(self.prefix_list_path, "r") as pishvand_input_file:
            pishvandFile_content = pishvand_input_file.readlines()
            for el in pishvandFile_content:
                el = el.decode("utf-8")
                self.prefix_list.add(el.strip())

        self.postfix_list = set({})
        with open(self.postfix_list_path, "r") as pasvand_input_file:
            pasvandFile_content = pasvand_input_file.readlines()
            for el in pasvandFile_content:
                el = el.decode("utf-8")
                self.postfix_list.add(el.strip())

    def select_candidate(self, candidate_list, lexicon_set=None):
        length = 1000
        selected = ""
        for tmp_candidate in candidate_list:
            if lexicon_set == None and len(tmp_candidate) < length:
                selected = tmp_candidate
                length = len(tmp_candidate)
            elif (lexicon_set != None) and (tmp_candidate in lexicon_set):
                if(length == 1000):
                    selected = tmp_candidate
                    length = len(tmp_candidate)
                else:
                    if(len(tmp_candidate) > length):
                        selected = tmp_candidate
                        length = len(tmp_candidate)
        return selected

    def is_prefix(self, word, prefix):
        word = word.strip(u"\u200c")
        return word.startswith(prefix)

    def is_postfix(self, word, post):
        word = word.strip(u"\u200c")
        return word.endswith(post)

    def remove_prefixes(self, word, prefix):
        word = word.strip(u"\u200c")
        candidateStem = set({})
        for el in prefix:
            if word.startswith(el):
                if (len(el) > 0):
                    tmp = word[len(el):].strip().strip(u'\u200c')
                else:
                    tmp = word
                candidateStem.add(tmp)
        return candidateStem

    def remove_postfixes(self, word, postfix):
        word = word.strip(u"\u200c")
        candidateStem = set({})
        for el in postfix:
            if word.endswith(el):
                if (len(el) > 0):
                    tmp = word[:-len(el)].strip().strip(u'\u200c')
                else:
                    tmp = word
                candidateStem.add(tmp)
        return candidateStem

    def map_irregular_noun(self, word):
        if word in self.irregular_nouns:
            return self.irregular_nouns[word]
        else:
            return word

    def convert_to_stem(self, word, word_pos=None):
        if word in self.noun_lexicon:
            if (word_pos == None or word_pos == 'N'):
                #print("in word dict...")
                return self.map_irregular_noun(word)

        elif word in self.verb_lexicon:
            if (word_pos == None or word_pos == 'V'):
                #print("in verb dict...")
                if (word in self.verb_f2p_map):
                    stem = self.verb_f2p_map[word] + u"&" + word
                elif (word in self. verb_p2f_map):
                    stem = word + u"&" + self.verb_p2f_map[word]
                else:
                    stem = word
                return stem

        # if word is a verb
        if word_pos == None or word_pos == "V":
            # ماضی مستمر
            candidate_list = self.remove_prefixes(word, [u"داشتم", u"داشتی", u"داشت",
                                                         u"داشتیم", u"داشتید", u"داشتند"])
            if len(candidate_list) > 0:
                new_word = self.select_candidate(candidate_list)
                candidate_list = self.remove_prefixes(new_word, [u"می"])
                if len(candidate_list) > 0:
                    new_word = self.select_candidate(candidate_list)
                    candidate_list = self.remove_postfixes(new_word, [u"یم", u"ید", u"ند",
                                                                      u"م", u"ی", u""])
                    if len(candidate_list) > 0:
                        new_word = self.select_candidate(candidate_list, self.verb_lexicon)
                        if new_word:
                            if (new_word in self.verb_p2f_map):
                                stem = new_word + u"&" +self.verb_p2f_map[new_word]
                                return stem

            # مضارع مستمر
            candidate_list = self.remove_prefixes(word, [u"دارم", u"داری", u"دارد",
                                                         u"داریم", u"دارید", u"دارند"])
            if len(candidate_list) > 0:
                new_word = self.select_candidate(candidate_list)
                candidate_list = self.remove_prefixes(new_word, [u"می"])
                if len(candidate_list) > 0:
                    new_word = self.select_candidate(candidate_list)
                    candidate_list = self.remove_postfixes(new_word, [u"یم", u"ید", u"ند",
                                                                      u"م", u"ی", u"د"])
                    if len(candidate_list) > 0:
                        new_word = self.select_candidate(candidate_list, self.verb_lexicon)
                        if new_word:
                            if (new_word in self.verb_f2p_map):
                                stem = self.verb_f2p_map[new_word] + u"&" + new_word
                                return stem

            # مضارع اخباری
            candidate_list = self.remove_prefixes(word, [u"می", u"نمی", u"همی"])
            if len(candidate_list) > 0:
                new_word = self.select_candidate(candidate_list)
                candidate_list = self.remove_postfixes(new_word, [u"یم", u"ید", u"ند",
                                                                  u"م", u"ی", u"د"])
                if len(candidate_list) > 0:
                    new_word = self.select_candidate(candidate_list, self.verb_lexicon)
                    if new_word:
                        if (new_word in self.verb_f2p_map):
                            stem = self.verb_f2p_map[new_word] + u"&" + new_word
                            return stem

            # ماضی استمراری
            candidate_list = self.remove_prefixes(word, [u"می", u"نمی", u"همی"])
            if len(candidate_list) > 0:
                new_word = self.select_candidate(candidate_list)
                candidate_list = self.remove_postfixes(new_word, [u"یم", u"ید", u"ند",
                                                                  u"م", u"ی", u""])
                if len(candidate_list) > 0:
                    new_word = self.select_candidate(candidate_list, self.verb_lexicon)
                    if new_word:
                        if (new_word in self.verb_p2f_map):
                            stem = new_word + u"&" + self.verb_p2f_map[new_word]
                            return stem

            # ماضی بعید و التزامی
            candidate_list = self.remove_postfixes(word, [u"یم", u"ید", u"ند",
                                                          u"م", u"ی", u""])
            if len(candidate_list) > 0:
                new_word = self.select_candidate(candidate_list)
                candidate_list = self.remove_postfixes(new_word, [u"بود", u"باشد", u"باش"])
                if len(candidate_list) > 0:
                    new_word = self.select_candidate(candidate_list)
                    candidate_list = self.remove_postfixes(new_word, [u"ه"])
                    if len(candidate_list) > 0:
                        new_word = self.select_candidate(candidate_list)
                        candidate_list = self.remove_prefixes(new_word, [u"ن", u""])
                        if len(candidate_list) > 0:
                            new_word = self.select_candidate(candidate_list, self.verb_lexicon)
                            if new_word:
                                if(new_word in self.verb_p2f_map):
                                    stem = new_word + u"&" + self.verb_p2f_map[new_word]
                                    return stem

            # ماضی نقلی
            candidate_list = self.remove_postfixes(word, [u"ام", u"ای", u"است",
                                                          u"ایم", u"اید", u"اند"])
            if len(candidate_list) > 0:
                new_word = self.select_candidate(candidate_list)
                candidate_list = self.remove_postfixes(new_word, [u"ه"])
                if len(candidate_list) > 0:
                    new_word = self.select_candidate(candidate_list)
                    candidate_list = self.remove_prefixes(new_word, [u"ن", u""])
                    if len(candidate_list) > 0:
                        new_word = self.select_candidate(candidate_list, self.verb_lexicon)
                        if new_word:
                            if (new_word in self.verb_p2f_map):
                                stem = new_word + u"&" + self.verb_p2f_map[new_word]
                                return stem

            # ماضی ابعد
            candidate_list = self.remove_postfixes(word, [u"ام", u"ای", u"است",
                                                          u"ایم", u"اید", u"اند"])
            if len(candidate_list) > 0:
                new_word = self.select_candidate(candidate_list)
                candidate_list = self.remove_postfixes(new_word, [u"ه"])
                if len(candidate_list) > 0:
                    new_word = self.select_candidate(candidate_list)
                    candidate_list = self.remove_postfixes(new_word, [u"بود"])
                    if len(candidate_list) > 0:
                        new_word = self.select_candidate(candidate_list)
                        candidate_list = self.remove_postfixes(new_word, [u"ه"])
                        if len(candidate_list) > 0:
                            new_word = self.select_candidate(candidate_list)
                            candidate_list = self.remove_prefixes(new_word, [u"ن", u""])
                            if len(candidate_list) > 0:
                                new_word = self.select_candidate(new_word, self.verb_lexicon)
                                if new_word:
                                    if (new_word in self.verb_p2f_map):
                                        stem = new_word + u"&" + self.verb_p2f_map[new_word]
                                        return stem

            # آینده
            candidate_list = self.remove_prefixes(word, [u"خواه", u"نخواه"])
            if len(candidate_list) > 0:
                new_word = self.select_candidate(candidate_list)
                candidate_list = self.remove_prefixes(new_word, [u"یم", u"ید", u"ند",
                                                                 u"م", u"ی", u"د"])
                if len(candidate_list) > 0:
                    new_word = self.select_candidate(candidate_list, self.verb_lexicon)
                    if new_word:
                        if (new_word in self.verb_p2f_map):
                            stem = new_word + u"&" + self.verb_p2f_map[new_word]
                            return stem

            # مضارع التزامی و امر
            candidate_list = self.remove_prefixes(word, [u"ب", u"ن", u""])
            if len(candidate_list) > 0:
                new_word = self.select_candidate(candidate_list)
                candidate_list = self.remove_postfixes(new_word, [u"یم", u"ید", u"ند", u"م",
                                                                  u"ی", u"د", u""])
                if len(candidate_list) > 0:
                    new_word = self.select_candidate(candidate_list)
                    if ((self.is_prefix(new_word, u"یا")) and (new_word not in self.verb_lexicon)):
                        candidate_list = self.remove_prefixes(new_word, [u"یا"])
                        new_word = self.select_candidate(candidate_list)
                        new_word = u"آ" + new_word
                    if (self.is_postfix(new_word, u"آی") or self.is_postfix(new_word, u"ای")):
                        if (new_word not in self.verb_lexicon):
                            candidate_list = self.remove_postfixes(new_word, [u"ی"])
                            new_word = self.select_candidate(candidate_list)
                    if (self.is_prefix(new_word, u"ی")):
                        candidate_list = self.remove_prefixes(new_word, [u"ی"])
                        tmp_word = self.select_candidate(candidate_list)
                        if tmp_word and (u"ا" + tmp_word) in self.verb_lexicon:
                            new_word = u"ا" + tmp_word

                if new_word and new_word in self.verb_lexicon:
                    if (new_word in self.verb_f2p_map):
                        stem = self.verb_f2p_map[new_word] + u"&" + new_word
                        return stem

            # ماضی ساده
            candidate_list = self.remove_postfixes(word, [u"م", u"ی", u"",
                                                          u"یم", u"ید", u"ند"])
            if len(candidate_list) > 0:
                new_word = self.select_candidate(candidate_list)
                candidate_list = self.remove_prefixes(new_word, [u"ن", u""])
                if len(candidate_list) > 0:
                    new_word = self.select_candidate(candidate_list, self.verb_lexicon)
                    if new_word:
                        if (new_word in self.verb_p2f_map):
                            stem = new_word + u"&" + self.verb_p2f_map[new_word]
                            return stem

            # حالت مصدر
            candidate_list = self.remove_postfixes(word, [u"ن"])
            if len(candidate_list) > 0:
                new_word = self.select_candidate(candidate_list, self.verb_lexicon)
                if new_word:
                    if (new_word in self.verb_p2f_map):
                        stem = new_word + u"&" + self.verb_p2f_map[new_word]
                        return stem


        if word_pos == None or word_pos == "N":
            # پسوندهای مالکیت
            stem_candidate = word
            candidate_list = self.remove_postfixes(word, [u"م", u"ت", u"ش", u"یم", u"یت", u"یش",
                                                          u"یتان", u"یشان", u"یمان",
                                                          u"مان",  u"تان", u"شان", u"ان"])
            if len(candidate_list) > 0:
                stem_candidate = self.select_candidate(candidate_list, self.noun_lexicon)
                if stem_candidate:
                    new_word = stem_candidate
                else:
                    new_word = self.select_candidate(candidate_list)
                stem_candidate = new_word
            else:
                new_word = stem_candidate
            if new_word in self.noun_lexicon:
                return self.map_irregular_noun(new_word)

            candidate_list = self.remove_postfixes(new_word, [u"ها", u"ات", u"های",
                                                              u"ان", u"هایی", u"ین"])
            if len(candidate_list) > 0:
                stem_candidate = self.select_candidate(candidate_list, self.noun_lexicon)
                if stem_candidate:
                    new_word = stem_candidate
                else:
                    new_word = self.select_candidate(candidate_list)
                stem_candidate = new_word
            else:
                new_word = stem_candidate

            if new_word in self.noun_lexicon:
                return self.map_irregular_noun(new_word)

            candidate_list = self.remove_postfixes(new_word, [u"گ"])
            if len(candidate_list) > 0:
                new_word = self.select_candidate(candidate_list)
                new_word = new_word + u"ه"
                stem_candidate = new_word
            else:
                new_word = stem_candidate
            if new_word in self.noun_lexicon:
                return self.map_irregular_noun(new_word)

            candidate_list = self.remove_postfixes(new_word, self.postfix_list)
            if len(candidate_list) > 0:
                stem_candidate = self.select_candidate(candidate_list, self.noun_lexicon)
                if stem_candidate:
                    new_word = stem_candidate
                else:
                    new_word = self.select_candidate(candidate_list)
                stem_candidate = new_word
            else:
                new_word = stem_candidate
            if new_word in self.noun_lexicon:
                return self.map_irregular_noun(new_word)
                # stem = new_word

            candidate_list = self.remove_prefixes(new_word, self.prefix_list)
            if len(candidate_list) > 0:
                stem_candidate = self.select_candidate(candidate_list, self.noun_lexicon)
                if stem_candidate:
                    new_word = stem_candidate
                else:
                    new_word = self.select_candidate(candidate_list)
                stem_candidate = new_word
            else:
                new_word = stem_candidate

            if new_word in self.noun_lexicon:
                return self.map_irregular_noun(new_word)
                # stem = new_word


        # افعال پیشوندی
        candidate_list = self.remove_prefixes(word, [u'در', u'بر', u'پر', u'باز',
                                                     u'ور', u'فرو', u'فرا', u'وا'])

        suse = list(u'در‌آن')
        if word == u'در‌آن':

            suse = 5
        if len(candidate_list) > 0:
            new_word = self.select_candidate(candidate_list)
            if new_word:
                tmp_pr = word[:-len(new_word)].strip().strip(u'\u200c')
                new_word = self.convert_to_stem(new_word, word_pos='V')
                if new_word and new_word in self.verb_lexicon:
                    return tmp_pr + new_word

        return word