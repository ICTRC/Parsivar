import nltk
from nltk.chunk import conlltags2tree, tree2conlltags
#from sklearn.model_selection import train_test_split
from collections import Iterable
from nltk import ChunkParserI, ClassifierBasedTagger


class ClassifierChunkParser(ChunkParserI):
    def __init__(self):
        self.tagger = None
        pass

    def parse(self, tagged_sent):
        chunks = self.tagger.tag(tagged_sent)
        iob_triplets = [(w, t, c) for ((w, t), c) in chunks]

        # Transform the list of triplets to nltk.Tree format
        return conlltags2tree(iob_triplets)

    def train_merger(self, train_file_path, test_split=0.1):
        print("Loading Data...")
        file = open(train_file_path, "r", encoding='utf-8')
        file_content = file.read()
        file_content = file_content.split("\n\n")

        data_list = []
        for line in file_content:
            line = nltk.chunk.util.conllstr2tree(line, chunk_types=('NP',), root_label='S')
            if (len(line) > 0):
                data_list.append(line)

        # train_sents, test_sents = train_test_split(data_list, test_size=test_split, random_state=91)
        train_sents = data_list
        test_sents = []

        print("Training the model ...")

        # Transform the trees in IOB annotated sentences [(word, pos, chunk), ...]
        chunked_sents = [tree2conlltags(sent) for sent in train_sents]

        # Transform the triplets in pairs, make it compatible with the tagger interface [((word, pos), chunk), ...]
        def triplets2tagged_pairs(iob_sent):
            return [((word, pos), chunk) for word, pos, chunk in iob_sent]

        chunked_sents = [triplets2tagged_pairs(sent) for sent in chunked_sents]

        self.feature_detector = self.features
        self.tagger = ClassifierBasedTagger(
            train=chunked_sents,
            feature_detector=self.features)

        token_merger_model = self.tagger

        if len(test_sents) > 0:
            print("evaluating...")
            print(token_merger_model.evaluate(test_sents))

        return token_merger_model

    def nestedtree_to_list(self, tree, separator_char, d=0):
        s = ''
        for item in tree:
            if isinstance(item, tuple):
                s += item[0] + separator_char
            elif d >= 1:
                news = self.nestedtree_to_list(item, separator_char, d + 1)
                s += news + separator_char
            else:
                news = self.nestedtree_to_list(item, separator_char, d + 1) + '\t'
                s += news + separator_char
        return s.strip(separator_char)

    def merg_tokens(self, token_list, token_merger_model, separator_char):
        # gets a string line as input and returns a list of tokens
        tmp_list = []
        for word in token_list:
            tmp_list.append((word, 'N'))

        self.tagger = token_merger_model

        res = self.parse(tmp_list)
        res = self.nestedtree_to_list(res, separator_char=separator_char)
        res = res.strip('\t').split('\t')
        res = [x.strip(separator_char).strip() for x in res]
        return res

    def features(self, tokens, index, history):
        """
        `tokens`  = a POS-tagged sentence [(w1, t1), ...]
        `index`   = the index of the token we want to extract features for
        `history` = the previous predicted IOB tags
        """

        # Pad the sequence with placeholders
        tokens = [('__START2__', '__START2__'), ('__START1__', '__START1__')] + list(tokens) + [
            ('__END1__', '__END1__'),
            ('__END2__', '__END2__')]
        history = ['__START3__', '__START2__', '__START1__'] + list(history)

        # shift the index with 2, to accommodate the padding
        index += 2

        word, pos = tokens[index]
        prevword, prevpos = tokens[index - 1]
        prevprevword, prevprevpos = tokens[index - 2]
        nextword, nextpos = tokens[index + 1]
        nextnextword, nextnextpos = tokens[index + 2]
        previob = history[index - 1].split("-")[0]
        prevpreviob = history[index - 2].split("-")[0]
        prevprevpreviob = history[index - 3].split("-")[0]

        return {
            'word': word,

            'prev-iob': previob,
            # 'prev-prev-iob' : prevpreviob,
            # 'prev_prev-prev-iob' : prevprevpreviob,

            'next-word': nextword,
            # 'next-next-word': nextnextword,

            'prev-word': prevword,
            # 'prev-prev-word': prevprevword,
        }