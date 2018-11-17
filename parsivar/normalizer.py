from re import sub
import copy
import os
from .tokenizer import Tokenizer
from .data_helper import DataHelper
from .token_merger import ClassifierChunkParser
import tmp

class Normalizer():

    def __init__(self,
                 half_space_char='\u200c',
                 statistical_space_correction=False,
                 date_normalizing_needed=False,
                 pinglish_conversion_needed=False,
                 train_file_path="resource/tokenizer/Bijan_khan_chunk.txt",
                 token_merger_path="resource/tokenizer/TokenMerger.pckl"):
        self.dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"

        self.dic1_path = self.dir_path + 'resource/normalizer/Dic1_new.txt'
        self.dic2_path = self.dir_path + 'resource/normalizer/Dic2_new.txt'
        self.dic3_path = self.dir_path + 'resource/normalizer/Dic3_new.txt'
        self.dic1 = self.load_dictionary(self.dic1_path)
        self.dic2 = self.load_dictionary(self.dic2_path)
        self.dic3 = self.load_dictionary(self.dic3_path)

        self.statistical_space_correction = statistical_space_correction
        self.date_normalizing_needed = date_normalizing_needed
        self.pinglish_conversion_needed = pinglish_conversion_needed
        self.data_helper = DataHelper()
        self.token_merger = ClassifierChunkParser()


        if self.date_normalizing_needed or self.pinglish_conversion_needed:
            self.tokenizer = Tokenizer()
            self.date_normalizer = DateNormalizer()
            self.pinglish_conversion = PinglishNormalizer()

        if self.statistical_space_correction:
            self.token_merger_path = self.dir_path + token_merger_path
            self.train_file_path = train_file_path
            self.half_space_char = half_space_char

            if os.path.isfile(self.token_merger_path):
                self.token_merger_model = self.data_helper.load_var(self.token_merger_path)
            elif os.path.isfile(self.train_file_path):
                self.token_merger_model = self.token_merger.train_merger(self.train_file_path, test_split=0)
                self.data_helper.save_var(self.token_merger_path, self.token_merger_model)




    def load_dictionary(self, file_path):
        dict = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            g = f.readlines()
            for Wrds in g:
                wrd = Wrds.split(' ')
                dict[wrd[0].strip()] = sub('\n', '', wrd[1].strip())
        return dict

    def sub_alphabets(self, doc_string):
        # try:
        #     doc_string = doc_string.decode('utf-8')
        # except UnicodeEncodeError:
        #     pass
        a0 = "ء"
        b0 = "ئ"
        c0 = sub(a0, b0, doc_string)
        a1 = r"ٲ|ٱ|إ|ﺍ|أ"
        a11 = r"ﺁ|آ"
        b1 = r"ا"
        b11 = r"آ"
        c11 = sub(a11, b11, c0)
        c1 = sub(a1, b1, c11)
        a2 = r"ﺐ|ﺏ|ﺑ"
        b2 = r"ب"
        c2 = sub(a2, b2, c1)
        a3 = r"ﭖ|ﭗ|ﭙ|ﺒ|ﭘ"
        b3 = r"پ"
        c3 = sub(a3, b3, c2)
        a4 = r"ﭡ|ٺ|ٹ|ﭞ|ٿ|ټ|ﺕ|ﺗ|ﺖ|ﺘ"
        b4 = r"ت"
        c4 = sub(a4, b4, c3)
        a5 = r"ﺙ|ﺛ"
        b5 = r"ث"
        c5 = sub(a5, b5, c4)
        a6 = r"ﺝ|ڃ|ﺠ|ﺟ"
        b6 = r"ج"
        c6 = sub(a6, b6, c5)
        a7 = r"ڃ|ﭽ|ﭼ"
        b7 = r"چ"
        c7 = sub(a7, b7, c6)
        a8 = r"ﺢ|ﺤ|څ|ځ|ﺣ"
        b8 = r"ح"
        c8 = sub(a8, b8, c7)
        a9 = r"ﺥ|ﺦ|ﺨ|ﺧ"
        b9 = r"خ"
        c9 = sub(a9, b9, c8)
        a10 = r"ڏ|ډ|ﺪ|ﺩ"
        b10 = r"د"
        c10 = sub(a10, b10, c9)
        a11 = r"ﺫ|ﺬ|ﻧ"
        b11 = r"ذ"
        c11 = sub(a11, b11, c10)
        a12 = r"ڙ|ڗ|ڒ|ڑ|ڕ|ﺭ|ﺮ"
        b12 = r"ر"
        c12 = sub(a12, b12, c11)
        a13 = r"ﺰ|ﺯ"
        b13 = r"ز"
        c13 = sub(a13, b13, c12)
        a14 = r"ﮊ"
        b14 = r"ژ"
        c14 = sub(a14, b14, c13)
        a15 = r"ݭ|ݜ|ﺱ|ﺲ|ښ|ﺴ|ﺳ"
        b15 = r"س"
        c15 = sub(a15, b15, c14)
        a16 = r"ﺵ|ﺶ|ﺸ|ﺷ"
        b16 = r"ش"
        c16 = sub(a16, b16, c15)
        a17 = r"ﺺ|ﺼ|ﺻ"
        b17 = r"ص"
        c17 = sub(a17, b17, c16)
        a18 = r"ﺽ|ﺾ|ﺿ|ﻀ"
        b18 = r"ض"
        c18 = sub(a18, b18, c17)
        a19 = r"ﻁ|ﻂ|ﻃ|ﻄ"
        b19 = r"ط"
        c19 = sub(a19, b19, c18)
        a20 = r"ﻆ|ﻇ|ﻈ"
        b20 = r"ظ"
        c20 = sub(a20, b20, c19)
        a21 = r"ڠ|ﻉ|ﻊ|ﻋ"
        b21 = r"ع"
        c21 = sub(a21, b21, c20)
        a22 = r"ﻎ|ۼ|ﻍ|ﻐ|ﻏ"
        b22 = r"غ"
        c22 = sub(a22, b22, c21)
        a23 = r"ﻒ|ﻑ|ﻔ|ﻓ"
        b23 = r"ف"
        c23 = sub(a23, b23, c22)
        a24 = r"ﻕ|ڤ|ﻖ|ﻗ"
        b24 = r"ق"
        c24 = sub(a24, b24, c23)
        a25 = r"ڭ|ﻚ|ﮎ|ﻜ|ﮏ|ګ|ﻛ|ﮑ|ﮐ|ڪ|ك"
        b25 = r"ک"
        c25 = sub(a25, b25, c24)
        a26 = r"ﮚ|ﮒ|ﮓ|ﮕ|ﮔ"
        b26 = r"گ"
        c26 = sub(a26, b26, c25)
        a27 = r"ﻝ|ﻞ|ﻠ|ڵ"
        b27 = r"ل"
        c27 = sub(a27, b27, c26)
        a28 = r"ﻡ|ﻤ|ﻢ|ﻣ"
        b28 = r"م"
        c28 = sub(a28, b28, c27)
        a29 = r"ڼ|ﻦ|ﻥ|ﻨ"
        b29 = r"ن"
        c29 = sub(a29, b29, c28)
        a30 = r"ވ|ﯙ|ۈ|ۋ|ﺆ|ۊ|ۇ|ۏ|ۅ|ۉ|ﻭ|ﻮ|ؤ"
        b30 = r"و"
        c30 = sub(a30, b30, c29)
        a31 = r"ﺔ|ﻬ|ھ|ﻩ|ﻫ|ﻪ|ۀ|ە|ة|ہ"
        b31 = r"ه"
        c31 = sub(a31, b31, c30)
        a32 = r"ﭛ|ﻯ|ۍ|ﻰ|ﻱ|ﻲ|ں|ﻳ|ﻴ|ﯼ|ې|ﯽ|ﯾ|ﯿ|ێ|ے|ى|ي"
        b32 = r"ی"
        c32 = sub(a32, b32, c31)
        a33 = r'¬'
        b33 = r'‌'
        c33 = sub(a33, b33, c32)
        pa0 = r'•|·|●|·|・|∙|｡|ⴰ'
        pb0 = r'.'
        pc0 = sub(pa0, pb0, c33)
        pa1 = r',|٬|٫|‚|，'
        pb1 = r'،'
        pc1 = sub(pa1, pb1, pc0)
        pa2 = r'ʕ'
        pb2 = r'؟'
        pc2 = sub(pa2, pb2, pc1)
        na0 = r'۰|٠'
        nb0 = r'0'
        nc0 = sub(na0, nb0, pc2)
        na1 = r'۱|١'
        nb1 = r'1'
        nc1 = sub(na1, nb1, nc0)
        na2 = r'۲|٢'
        nb2 = r'2'
        nc2 = sub(na2, nb2, nc1)
        na3 = r'۳|٣'
        nb3 = r'3'
        nc3 = sub(na3, nb3, nc2)
        na4 = r'۴|٤'
        nb4 = r'4'
        nc4 = sub(na4, nb4, nc3)
        na5 = r'۵'
        nb5 = r'5'
        nc5 = sub(na5, nb5, nc4)
        na6 = r'۶|٦'
        nb6 = r'6'
        nc6 = sub(na6, nb6, nc5)
        na7 = r'۷|٧'
        nb7 = r'7'
        nc7 = sub(na7, nb7, nc6)
        na8 = r'۸|٨'
        nb8 = r'8'
        nc8 = sub(na8, nb8, nc7)
        na9 = r'۹|٩'
        nb9 = r'9'
        nc9 = sub(na9, nb9, nc8)
        ea1 = r'ـ|ِ|ُ|َ|ٍ|ٌ|ً|'
        eb1 = r''
        ec1 = sub(ea1, eb1, nc9)
        Sa1 = r'( )+'
        Sb1 = r' '
        Sc1 = sub(Sa1, Sb1, ec1)
        Sa2 = r'(\n)+'
        Sb2 = r'\n'
        Sc2 = sub(Sa2, Sb2, Sc1)
        return Sc2

    def space_correction(self, doc_string):
        a00 = r'^(بی|می|نمی)( )'
        b00 = r'\1‌'
        c00 = sub(a00, b00, doc_string)
        a0 = r'( )(می|نمی|بی)( )'
        b0 = r'\1\2‌'
        c0 = sub(a0, b0, c00)
        a1 = r'( )(هایی|ها|های|ایی|هایم|هایت|هایش|هایمان|هایتان|هایشان|ات|ان|ین' \
             r'|انی|بان|ام|ای|یم|ید|اید|اند|بودم|بودی|بود|بودیم|بودید|بودند|ست)( )'
        b1 = r'‌\2\3'
        c1 = sub(a1, b1, c0)
        a2 = r'( )(شده|نشده)( )'
        b2 = r'‌\2‌'
        c2 = sub(a2, b2, c1)
        a3 = r'( )(طلبان|طلب|گرایی|گرایان|شناس|شناسی|گذاری|گذار|گذاران|شناسان|گیری|پذیری|بندی|آوری|سازی|' \
             r'بندی|کننده|کنندگان|گیری|پرداز|پردازی|پردازان|آمیز|سنجی|ریزی|داری|دهنده|آمیز|پذیری' \
             r'|پذیر|پذیران|گر|ریز|ریزی|رسانی|یاب|یابی|گانه|گانه‌ای|انگاری|گا|بند|رسانی|دهندگان|دار)( )'
        b3 = r'‌\2\3'
        c3 = sub(a3, b3, c2)
        return c3

    def space_correction_plus1(self, doc_string):
        out_sentences = ''
        for wrd in doc_string.split(' '):
            try:
                out_sentences = out_sentences + ' ' + self.dic1[wrd]
            except KeyError:
                out_sentences = out_sentences + ' ' + wrd
        return out_sentences

    def space_correction_plus2(self, doc_string):
        out_sentences = ''
        wrds = doc_string.split(' ')
        L = wrds.__len__()
        if L < 2:
            return doc_string
        cnt = 1
        for i in range(0, L - 1):
            w = wrds[i] + wrds[i + 1]
            try:
                out_sentences = out_sentences + ' ' + self.dic2[w]
                cnt = 0
            except KeyError:
                if cnt == 1:
                    out_sentences = out_sentences + ' ' + wrds[i]
                cnt = 1
        if cnt == 1:
            out_sentences = out_sentences + ' ' + wrds[i + 1]
        return out_sentences

    def space_correction_plus3(self, doc_string):
        # Dict = {'گفتوگو': 'گفت‌وگو'}
        out_sentences = ''
        wrds = doc_string.split(' ')
        L = wrds.__len__()
        if L < 3:
            return doc_string
        cnt = 1
        cnt2 = 0
        for i in range(0, L - 2):
            w = wrds[i] + wrds[i + 1] + wrds[i + 2]
            try:
                out_sentences = out_sentences + ' ' + self.dic3[w]
                cnt = 0
                cnt2 = 2
            except KeyError:
                if cnt == 1 and cnt2 == 0:
                    out_sentences = out_sentences + ' ' + wrds[i]
                else:
                    cnt2 -= 1
                cnt = 1
        if cnt == 1 and cnt2 == 0:
            out_sentences = out_sentences + ' ' + wrds[i + 1] + ' ' + wrds[i + 2]
        elif cnt == 1 and cnt2 == 1:
            out_sentences = out_sentences + ' ' + wrds[i + 2]
        return out_sentences

    def normalize(self, doc_string):
        #return data_helper.clean_text(self.sub_alphabets(doc_string))
        normalized_string = self.data_helper.clean_text(self.sub_alphabets(doc_string)).strip()

        if self.statistical_space_correction:
            token_list = normalized_string.strip().split()
            token_list = [x.strip("\u200c") for x in token_list if len(x.strip("\u200c")) != 0]
            token_list = self.token_merger.merg_tokens(token_list, self.token_merger_model, self.half_space_char)
            normalized_string = " ".join(x for x in token_list)
            normalized_string = self.data_helper.clean_text(normalized_string)
        else:
            normalized_string = self.space_correction(self.space_correction_plus1(self.space_correction_plus2(self.space_correction_plus3(normalized_string)))).strip()

        if self.pinglish_conversion_needed:
            normalized_string = self.pinglish_conversion.pingilish2persian(self.tokenizer.tokenize_words(normalized_string))

        if self.date_normalizing_needed:
            normalized_string = self.date_normalizer.normalize_dates(self.date_normalizer.normalize_numbers(self.tokenizer.tokenize_words(normalized_string)).split())

        return normalized_string


class DateNormalizer():
    def __init__(self):

        self.month_dict = {"فروردین": 1, "اردیبهشت": 2, "خرداد": 3,
                           "تیر": 4, "مرداد": 5, "شهریور": 6,
                           "مهر": 7, "آبان": 8, "آذر": 9,
                           "دی": 10, "بهمن": 11, "اسفند": 12}

        self.num_dict = {"صد": 100, "هزار": 1000, "میلیون": 1000000, "دویست": 200,
                         "ده": 10, "نه": 9, "هشت": 8, "هفت": 7, "شش": 6, "پنج": 5,
                         "چهار": 4, "سه": 3, "دو": 2, "یک": 1, "یازده": 11, "سیزده": 13,
                         "چهارده": 14, "دوازده": 12, "پانزده": 15, "شانزده": 16, "هفده": 17,
                         "هجده": 18, "نوزده": 19, "بیست": 20, "سی": 30, "چهل": 40, "پنجاه": 50,
                         "شصت": 60, "هفتاد": 70, "نود": 90, "سیصد": 300, "چهارصد": 400,
                         "پانصد": 500, "ششصد": 600, "هفتصد": 700, "هشتصد": 800, "نهصد": 900,
                         "هشتاد": 80, " ": 0, "میلیارد": 1000000000,
                         "صدم": 100, "هزارم": 1000, "دویستم": 200,
                         "دهم": 10, "نهم": 9, "هشتم": 8, "هفتم": 7, "ششم": 6, "پنجم": 5,
                         "چهارم": 4, "سوم": 3, "دوم": 2, "یکم": 1, "اول": 1, "یازدهم": 11, "سیزدهم": 13,
                         "چهاردهم": 14, "دوازدهم": 12, "پانزدهم": 15, "شانزدهم": 16, "هفدهم": 17,
                         "هجدهم": 18, "نوزدهم": 19, "بیستم": 20, "چهلم": 40, "پنجاهم": 50,
                         "شصتم": 60, "هفتادم": 70, "نودم": 90, "سیصدم": 300, "چهارصدم": 400,
                         "پانصدم": 500, "ششصدم": 600, "هفتصدم": 700, "هشتصدم": 800, "نهصدم": 900,
                         "هشتادم": 80}

    def find_date_part(self, token_list):
        for index, element in enumerate(token_list):
            if element == "/":
                if index-1 >= 0 and index+1 < len(token_list) \
                        and token_list[index -1].isdigit() and token_list[index+1].isdigit():
                    if index+3 < len(token_list) and token_list[index+2] == "/" \
                            and token_list[index + 3].isdigit():
                        formal_date = [int(token_list[index-1]), int(token_list[index+1]), int(token_list[index+3])]
                        formal_date = "y" + str(formal_date[2]) + "m" + str(formal_date[1]) + "d" + str(formal_date[0])
                        return formal_date, index-1, index+3
                    else:
                        formal_date = [int(token_list[index-1]), int(token_list[index+ 1]), 0]
                        formal_date = "y" + str(formal_date[2]) + "m" + str(formal_date[1]) + "d" + str(formal_date[0])
                        return formal_date, index-1 , index+1

            if element in self.month_dict or element == "سال":
                if index + 1 < len(token_list) and index - 1 > -2:
                    try:
                        formal_date = [int(token_list[index - 1]), int(self.month_dict[token_list[index]]), int(token_list[index + 1])]
                        formal_date = "y" + str(formal_date[2]) + "m" + str(formal_date[1]) + "d" + str(formal_date[0])
                        if token_list[index - 1] and token_list[index + 1]:
                            return formal_date, index-1, index+1
                    except:
                        try:
                            formal_date = [int(token_list[index - 1]), int(self.month_dict[token_list[index]]), 0]
                            formal_date = "y" + str(formal_date[2]) + "m" + str(formal_date[1]) + "d" + str(formal_date[0])
                            return formal_date, index-1, index
                        except:
                            try:
                                if token_list[index] == "سال":
                                    formal_date = [int(token_list[index + 1]),0, 0]
                                    formal_date = "y" + str(formal_date[2]) + "m" + str(formal_date[1]) + "d" + str(formal_date[0])
                                    return formal_date, index+1, index+1
                                else:
                                    print("error")
                            except:
                                pass

    def normalize_dates(self, token_list):
        finded = self.find_date_part(token_list)
        if finded != None:
            date_part = finded[0]
            start_date_index = finded[1]
            end_date_index = finded[2]
            befor_date_part = " ".join(x for x in token_list[:start_date_index])
            after_date_part = [x for x in token_list[end_date_index + 1:]]
            return befor_date_part + " " + date_part + " " + self.normalize_dates(after_date_part)
        else:
            return " ".join(x for x in token_list)

    def list2num(self, numerical_section_list):
        value = 1
        for index, el in enumerate(numerical_section_list):
            if self.is_number(el):
                value *= self.num_dict[el]
            else:
                value *= float(el)
        return value

    def convert2num(self, numerical_section_list):
        value = 0
        tmp_section_list = []
        for index, el in enumerate(numerical_section_list):
            if self.is_number(el) or (el.replace('.', '', 1).isdigit()):
                tmp_section_list.append(el)
            elif el == "و":
                value += self.list2num(tmp_section_list)
                tmp_section_list[:] = []
        if len(tmp_section_list) > 0:
            value += self.list2num(tmp_section_list)
            tmp_section_list[:] = []
        if (value-int(value) == 0):
            return int(value)
        else:
            return value

    def is_number(self, word):
        return word in self.num_dict

    def find_number_location(self, token_list):
        start_index = 0
        number_section =[]
        for i , el in enumerate(token_list):
            if self.is_number(el) or (el.replace('.', '', 1).isdigit()):
                start_index = i
                number_section.append(start_index)
                break

        i = start_index+1
        while(i < len(token_list)):
            if token_list[i] == "و" and (i+1)<len(token_list):
                if self.is_number(token_list[i+1]) or (token_list[i+1].replace('.', '', 1).isdigit()):
                    number_section.append(i)
                    number_section.append(i+1)
                    i += 2
                else:
                    break
            elif self.is_number(token_list[i]) or (token_list[i].replace('.', '', 1).isdigit()):
                number_section.append(i)
                i += 1
            else:
                break
        return number_section

    def normalize_numbers(self, token_list, converted=""):
        for i, el in enumerate(token_list):
            if el.endswith("ین") and self.is_number(el[:-2]):
                token_list[i] = el[:-2]
        finded = self.find_number_location(token_list)
        if len(finded) == 0:
            rest_of_string = " ".join(t for t in token_list)
            return converted + " " + rest_of_string
        else:
            numerical_subsection = [token_list[x] for x in finded]
            numerical_subsection = self.convert2num(numerical_subsection)

            converted = converted + " " + " ".join(x for x in token_list[:finded[0]]) + " " + str(numerical_subsection)

            new_index = finded[-1] + 1
            return self.normalize_numbers(token_list[new_index:], converted)


class PinglishNormalizer():
    def __init__(self):
        self.data_helper = DataHelper()
        self.file_dir = os.path.dirname(os.path.realpath(__file__)) + "/"

        self.en_dict_filename = self.file_dir + "resource/tokenizer/enDict"
        self.en_dict = self.data_helper.load_var(self.en_dict_filename)

        self.fa_dict_filename = self.file_dir + "resource/tokenizer/faDict"
        self.fa_dict = self.data_helper.load_var(self.fa_dict_filename)


    def pingilish2persian(self, pinglish_words_list):

        for i, word in enumerate(pinglish_words_list):
            if word in self.en_dict:
                pinglish_words_list[i] = self.en_dict[word]#.decode("utf-8")
                #inp = inp.replace(word, enDict[word], 1)
            else:
                ch = self.characterize(word)
                pr = self.map_char(ch)
                amir = self.make_word(pr)
                for wd in amir:
                    am = self.escalation(wd)
                    asd = ''.join(am)
                    if asd in self.fa_dict:
                        pinglish_words_list[i] = asd#.decode("utf-8")
                        #inp = inp.replace(word, asd, 1)
        inp = " ".join(x for x in pinglish_words_list)
        return inp

    def characterize(self, word):
        list_of_char = []
        i = 0
        while i < len(word):
            char = word[i]
            sw_out = self.switcher(char)
            if (sw_out == None):
                esp_out = None
                if(i < len(word) - 1):
                    esp_out = self.esp_check(word[i], word[i + 1])
                if(esp_out == None):
                    list_of_char.append(word[i])
                else:
                    list_of_char.append(esp_out)
                    i += 1
            else:
                list_of_char.append(sw_out)
            i += 1
        return list_of_char

    def switcher(self, ch):
        switcher = {
            "c": None,
            "k": None,
            "z": None,
            "s": None,
            "g": None,
            "a": None,
            "u": None,
            "e": None,
            "o": None
        }
        return switcher.get(ch, ch)

    def esp_check(self, char1, char2):
        st = char1 + char2
        if (st == "ch"):
            return "ch"
        elif (st == "kh"):
            return "kh"
        elif (st == "zh"):
            return "zh"
        elif (st == "sh"):
            return "sh"
        elif (st == "gh"):
            return "gh"
        elif (st == "aa"):
            return "aa"
        elif (st == "ee"):
            return "ee"
        elif (st == "oo"):
            return "oo"
        elif (st == "ou"):
            return "ou"
        else:
            return None

    def map_char(self, word):
        listm = []
        sw_out = self.map_switcher(word[0])
        i = 0
        if (sw_out == None):
            listm.append(["ا"])
            i += 1
        if (word[0] == "oo"):
            listm.append(["او"])
            i += 1
        while i < len(word):
            listm.append(self.char_switcher(word[i]))
            i += 1
        if word[len(word) - 1] == "e":
            listm.append(["ه"])
        elif word[len(word) - 1] == "a":
            listm.append(["ا"])
        elif word[len(word) - 1] == "o":
            listm.append(["و"])
        elif word[len(word) - 1] == "u":
            listm.append(["و"])

        return listm

    def map_switcher(self, ch):
        switcher = {
            "a": None,
            "e": None,
            "o": None,
            "u": None,
            "ee": None,

            "ou": None
        }
        return switcher.get(ch, ch)

    def make_word(self, chp):
        word_list = [[]]
        for char in chp:
            word_list_temp = []
            for tmp_word_list in word_list:
                for chch in char:
                    tmp = copy.deepcopy(tmp_word_list)
                    tmp.append(chch)
                    word_list_temp.append(tmp)
            word_list = word_list_temp
        return word_list

    def escalation(self, word):
        tmp = []
        i = 0
        t = len(word)
        while i < t - 1:
            tmp.append(word[i])
            if word[i] == word[i + 1]:
                i += 1
            i += 1
        if i != t:
            tmp.append(word[i])
        return tmp

    def char_switcher(self, ch):
        switcher = {
            'a': ["", "ا"],
            'c': ["ث", "ص", "ص"],
            'h': ["ه", "ح"],
            'b': ["ب"],
            'p': ["پ"],
            't': ["ت", "ط"],
            's': ["س", "ص", "ث"],
            'j': ["ج"],
            'ch': ["چ"],
            'kh': ["خ"],
            'q': ["ق", "غ"],
            'd': ["د"],
            'z': ["ز", "ذ", "ض", "ظ"],
            'r': ["ر"],
            'zh': ["ژ"],
            'sh': ["ش"],
            'gh': [",ق", "غ"],
            'f': ["ف"],
            'k': ["ک"],
            'g': ["گ"],
            'l': ["ل"],
            'm': ["م"],
            'n': ["ن"],
            'v': ["و"],
            'aa': ["ا"],
            'ee': ["ی"],
            'oo': ["و"],
            'ou': ["و"],
            'i': ["ی"],
            'y': ["ی"],
            ' ': [""],
            'w': ["و"],
            'e': ["", "ه"],
            'o': ["", "و"]
        }
        return switcher.get(ch, "")
