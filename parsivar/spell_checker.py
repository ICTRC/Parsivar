import pickle
import math
import os

from .normalizer import Normalizer
from .tokenizer import Tokenizer
from .data_helper import DataHelper


class SpellCheck:
    def __init__(self):
        self.normalizer = Normalizer()
        self.tokenizer = Tokenizer()
        self.data_helper = DataHelper()

        self.dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"

        self.bigram_lm = self.data_helper.load_var(self.dir_path + "resource/spell/mybigram_lm.pckl")
        self.onegram_lm = self.data_helper.load_var(self.dir_path + "resource/spell/onegram.pckl")
        self.ingroup_chars = [{'ا', 'آ', 'ع'},
                              {'ت', 'ط'},
                              {'ث', 'س', 'ص'},
                              {'ح', 'ه'},
                              {'ذ', 'ز', 'ض', 'ظ'},
                              {'ق', 'غ'}]

    def deletion(self, word):
        p_list = []
        for k in range(len(word)):
            if word[k] == '-' or word[k] == '#':
                continue
            begin = word[:k]
            end = word[k+1:]
            tmp_string = begin + end
            p_list.append(tmp_string)
        return p_list

    def splitting(self, word):
        p_list = set([])
        delimator = '-'
        for i, char in enumerate(word):
            begin = word[:i].strip('\u200c')
            end = word[i:].strip('\u200c')
            tmp_string = begin + delimator + end
            p_list.add(tmp_string)
        return list(p_list)

    def insertion(self, word):
        p_list = []
        alphabet = ['ا', 'آ', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ',
                    'د', 'ذ', 'ر', 'ز', 'ژ', 'س', 'ش', 'ص', 'ض', 'ط',
                    'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ', 'ل', 'م', 'ن',
                    'و', 'ه', 'ی', '‌']
        for k in range(len(word)+1):
            for char in alphabet:
                begin = word[:k]
                end = word[k:]
                tmp_string = begin + char + end
                p_list.append(tmp_string)
        return p_list

    def substitution(self, word):
        p_list = []
        alphabet = ['ا', 'آ', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ',
                    'د', 'ذ', 'ر', 'ز', 'ژ', 'س', 'ش', 'ص', 'ض', 'ط',
                    'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ', 'ل', 'م', 'ن',
                    'و', 'ه', 'ی']
        for i, char in enumerate(word):
            if char == '-' or char == '#':
                continue
            for c in alphabet:
                begin = word[:i]
                end = word[i+1:]
                tmp_string = begin + c + end
                p_list.append(tmp_string)
        return p_list

    def transposition(self, word):
        p_list = []
        word = list(word)
        tmp_word = word[:]
        for k1 in range(len(word)):
            k2 = k1 + 1
            if k2 == len(word):
                break
            tmp = tmp_word[k1]
            tmp_word[k1] = tmp_word[k2]
            tmp_word[k2] = tmp
            tmp_string = ''.join(tmp_word)
            p_list.append(tmp_string)
            tmp_word = word[:]
        return p_list

    def build_similar_words(self, word_seq, index, zi, operation):
        z_list = []
        o_list = []

        if operation == "Spell":
            tmp = self.deletion(zi)
            for i in tmp:
                z_list.append(i)
                o_list.append("Deletion")
            tmp = self.insertion(zi)
            for i in tmp:
                z_list.append(i)
                o_list.append("Insertion")
            tmp = self.substitution(zi)
            for i in tmp:
                z_list.append(i)
                o_list.append("Substitution")
            tmp = self.transposition(zi)
            for i in tmp:
                z_list.append(i)
                o_list.append("Transposition")

        elif operation == "Split":
            tmp = self.splitting(zi)
            for i in tmp:
                z_list.append(i)
                o_list.append("Split")

        elif operation == "Merg":
            if index < len(word_seq)-1:
                tmp = zi + '#' + word_seq[index+1]
                z_list.append(tmp)
                o_list.append("Merg")

        return [z_list, o_list]

    def bigram_markov_factor(self, yi_1, yi):
        bigram_counts, total_count = self.bigram_lm
        tmp = (yi_1, yi)
        if tmp in bigram_counts.keys():
            x = bigram_counts[tmp]
            x = float(x)/total_count
            x = math.log2(x)
            return x
        else:
            return -28

    def get_word_probability(self, word):
        lex_dict = self.onegram_lm[0]
        total_words = self.onegram_lm[1]

        if word in lex_dict:
            count = lex_dict[word]
            logprob = math.log2(float(count)/total_words)
            return logprob
        else:
            return -50.0

    def isword(self, x):
        if abs(x.find('#') - x.find('-')) == 1:
            return False

        dash_idx = x.find('-')
        if dash_idx != -1:
            first = x[:dash_idx]    # from beginning to n (n not included)
            secound = x[dash_idx+1:]    # n+1 through end of string
            if self.get_word_probability(first) < -49:
                return False
            elif self.get_word_probability(secound) < -49:
                return False
            else:
                return True

        sharp_idx = x.find('#')
        if sharp_idx != -1:
            begin = x[:sharp_idx]
            end = x[sharp_idx+1:]
            tmp_str = begin + end
            if self.get_word_probability(tmp_str) < -49:
                return False
            else:
                return True
        else:
            if self.get_word_probability(x) < -49:
                return False
            else:
                return True

    def get_possible_words(self, word_seq, index):
        wi = word_seq[index]
        possible_words = []
        operation_list = []

        possible_words.append(wi)
        operation_list.append("Nothing")

        if len(wi) == 1:
            return possible_words, operation_list

        '''Merg Split Spell'''
        [c_list, o_list] = self.build_similar_words(word_seq, index, wi, "Merg")
        for i, c in enumerate(c_list):
            if self.isword(c):
                possible_words.append(c)
                operation_list.append(o_list[i])

        [c_list, o_list] = self.build_similar_words(word_seq, index, wi, "Split")
        for i, c in enumerate(c_list):
            if self.isword(c):
                possible_words.append(c)
                operation_list.append(o_list[i])

        [c_list, o_list] = self.build_similar_words(word_seq, index, wi, "Spell")
        for i, c in enumerate(c_list):
            if self.isword(c):
                possible_words.append(c)
                operation_list.append(o_list[i])

        return possible_words, operation_list

    def select_n_best(self, c_list, o_list, n=3):
        my_dict = {}
        map_dict = {}
        for i, word in enumerate(c_list):
            if o_list[i] == 'Merg':
                tmp_word = word.replace("#", "")
                prob = self.get_word_probability(tmp_word)

            elif o_list[i] == 'Split':
                begin = word.split('-')[0]
                end = word.split('-')[1]
                prob = float(self.get_word_probability(begin) + self.get_word_probability(end))/2

            else:
                prob = self.get_word_probability(word)

            if word not in my_dict:
                my_dict[word] = prob
                map_dict[word] = o_list[i]

        n_best = set(sorted(my_dict, key=my_dict.get, reverse=True)[:n])
        n_best.add(c_list[0])
        n_best = list(n_best)
        n_best_op = [map_dict[key] for key in n_best]
        return n_best, n_best_op

    def is_ingroup_substitution(self, main_word, candidate_word):
        main_word = list(main_word)
        candidate_word = list(candidate_word)
        flag = False
        for i, c in enumerate(main_word):
            if c == candidate_word[i]:
                continue
            else:
                flag = False
                for l in self.ingroup_chars:
                    if c in l and candidate_word[i] in l:
                        flag = True
                        break
                break
        return flag

    def select_correct_spell(self, candidate_list, next_candidates, next_next_candidates, prev_word, current_word):
        best_candidate = None
        best_operation = None
        best_score = -1000
        next_next_candidate_list = []
        next_next_operation_list = []

        candidate_list, operation_list = candidate_list
        if next_candidates is not None:
            next_candidate_list, next_operation_list = next_candidates
        else:
            next_candidate_list, next_operation_list = [None], "Nothing"

        if next_next_candidates is not None:
            next_next_candidate_list, next_next_operation_list = next_next_candidates
        else:
            next_candidate_list, next_operation_list = [None], "Nothing"

        for i, candidate in enumerate(candidate_list):
            operation = operation_list[i]

            if operation == "Split":
                begin = candidate[:candidate.find('-')]
                end = candidate[candidate.find('-')+1:]
                candidate = begin
                next_word = end

                onegram_score = self.get_word_probability(candidate)
                bigram_score_with_prev = self.bigram_markov_factor(prev_word, candidate)

                bigram_score_next = -1000
                tmp_score_next = self.bigram_markov_factor(candidate, next_word)
                for j, next_next_word in enumerate(next_candidate_list):
                    opt = next_operation_list[j]
                    if opt == 'Merg':
                        next_next_word = next_next_word.replace("#", "")
                    elif opt == 'Split':
                        next_next_word = next_next_word.split('-')[0]

                    tmp_score_next_next = self.bigram_markov_factor(next_word, next_next_word)
                    if tmp_score_next_next > bigram_score_next:
                        bigram_score_next = tmp_score_next_next
                bigram_score_next = float(bigram_score_next + tmp_score_next)/2

            elif operation == "Merg":
                begin = candidate[:candidate.find('#')]
                end = candidate[candidate.find('#')+1:]
                candidate = begin + end

                onegram_score = self.get_word_probability(candidate)
                bigram_score_with_prev = self.bigram_markov_factor(prev_word, candidate)

                bigram_score_next = -1000
                for j, next_next_word in enumerate(next_next_candidate_list):
                    opt = next_next_operation_list[j]
                    if opt == 'Merg':
                        next_next_word = next_next_word.replace("#", "")
                    elif opt == 'Split':
                        next_next_word = next_next_word.split('-')[0]

                    tmp_score = self.bigram_markov_factor(candidate, next_next_word)
                    if tmp_score > bigram_score_next:
                        bigram_score_next = tmp_score

            else:
                onegram_score = self.get_word_probability(candidate)
                bigram_score_with_prev = self.bigram_markov_factor(prev_word, candidate)

                bigram_score_next = -1000
                for j, next_word in enumerate(next_candidate_list):
                    opt = next_operation_list[j]
                    if opt == 'Merg':
                        next_word = next_word.replace("#", "")
                    elif opt == 'Split':
                        next_word = next_word.split('-')[0]

                    tmp_score = self.bigram_markov_factor(candidate, next_word)
                    if tmp_score > bigram_score_next:
                        bigram_score_next = tmp_score

            if operation == 'Substitution':
                if self.is_ingroup_substitution(current_word, candidate):
                    onegram_score += 20
                else:
                    onegram_score += 10
            elif operation == 'Deletion' or operation == 'Insertion':
                onegram_score += 5
                if '\u200c' in candidate and '\u200c' not in current_word:
                    onegram_score += 5
            elif operation == 'Split' or operation == 'Merg':
                onegram_score += 7
            elif operation == 'Nothing':
                onegram_score += 20

            score = 1*onegram_score + 0.7*bigram_score_with_prev + 0.7*bigram_score_next

            if score > best_score:
                best_operation = operation
                best_candidate = candidate_list[i]
                best_score = score

        return best_candidate, best_operation

    def spell_corrector(self, doc_string):
        words = self.tokenizer.tokenize_words(self.normalizer.normalize(doc_string))

        best_o_list = []
        best_candidates_list = []

        yi_1 = None
        merged_before = False

        suggest_list = []

        for i, word in enumerate(words):
            [c_list, o_list] = self.get_possible_words(words, i)
            n_best = self.select_n_best(c_list, o_list, n=15)
            suggest_list.append(n_best)

        for i, candidate_list in enumerate(suggest_list):

            if merged_before:
                continue

            if (i+2) < len(suggest_list):
                next_candidates = suggest_list[i+1]
                next_next_candidates = suggest_list[i+2]
            elif (i+1) < len(suggest_list):
                next_candidates = suggest_list[i+1]
                next_next_candidates = None
            else:
                next_candidates = None
                next_next_candidates = None

            best_candidate, best_operation = self.select_correct_spell(candidate_list, next_candidates,
                                                                       next_next_candidates, yi_1, words[i])

            merged_before = False
            if best_operation == "Split":
                begin = best_candidate.split('-')[0]
                end = best_candidate.split('-')[1]
                best_candidate = [begin, end]
            if best_operation == "Merg":
                best_candidate = best_operation.replace("#", "")
                merged_before = True
            if type(best_candidate) == str:
                best_candidate = [best_candidate]

            best_o_list.append(best_operation)
            best_candidates_list.extend(best_candidate)
            yi_1 = best_candidate[-1]

        res = " ".join(best_candidates_list)
        ops = " ".join(best_o_list)

        return res


if __name__ == "__main__":
    doc_string = "نمازگذاران وارد مسلی شدند."
    myspell_checker = SpellCheck()

    res = myspell_checker.spell_corrector(doc_string)
    print(res)
