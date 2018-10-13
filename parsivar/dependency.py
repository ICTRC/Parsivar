# coding=utf-8
from nltk.parse.dependencygraph import DependencyGraph
from nltk.parse import malt
from nltk.parse.malt import MaltParser
import os
import codecs
import tempfile
import postagger
import tokenizer
import normalizer
import stemmer


class MyMaltParser(MaltParser):
    def __init__(self, parser_dirname, model_filename, tagger, stemmer):
        """
        An interface for parsing with the Malt Parser.
        :param parser_dirname: The path to the maltparser directory that
        contains the maltparser-1.x.jar
        :type parser_dirname: str
        :param model_filename: The name of the pre-trained model with .mco file
        extension. If provided, training will not be required.
        (see http://www.maltparser.org/mco/mco.html and
        see http://www.patful.com/chalk/node/185)
        :type model_filename: str
        :param tagger: The tagger used to POS tag the raw string before
        formatting to CONLL format. It should behave like `nltk.pos_tag`
        :type tagger: function
        :param stemmer: a function which returns stem of the word
        :type function
        """
        self.working_dir = parser_dirname
        self.mco = model_filename
        self.pos_tagger = tagger
        self._malt_bin = os.path.join(parser_dirname, 'maltparser-1.9.1.jar')
        self.stemmer = stemmer.convert_to_stem if stemmer else lambda w, t: '_'

    def parse_tagged_sent(self, sentence, verbose=False, top_relation_label='null'):
        tmp_file_address = tempfile.gettempdir()
        input_file = tempfile.NamedTemporaryFile(prefix='malt_input.conll', dir=tmp_file_address, delete=False)
        output_file = tempfile.NamedTemporaryFile(prefix='malt_output.conll', dir=tmp_file_address, delete=False)

        for i, (word, tag) in enumerate(sentence, start=1):
            word = word.strip()
            if not word:
                word = '_'
            input_file.write(('\t'.join([str(i), word.replace(' ', '_'), self.stemmer(word, tag).replace(' ', '_'), tag, tag, '_', '0', 'ROOT', '_', '_', '\n'])).encode('utf8'))
        input_file.write('\n\n'.encode('utf8'))
        input_file.close()

        cmd = ['java', '-jar', self._malt_bin, '-w', self.working_dir, '-c', self.mco, '-i', input_file.name, '-o', output_file.name, '-m', 'parse']
        if self._execute(cmd, verbose) != 0:
            raise Exception("MaltParser parsing failed: %s" % (' '.join(cmd)))

        dependency_graph = None
        with codecs.open(output_file.name, encoding='utf-8') as infile:
            content = infile.read().strip()
            if len(content) > 0:
                dependency_graph = DependencyGraph(content)

        input_file.close()
        output_file.close()
        os.remove(input_file.name)
        os.remove(output_file.name)
        return dependency_graph


class DependencyParser:
    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"
        self.my_normalizer = normalizer.Normalizer()
        self.my_tokenizer = tokenizer.Tokenizer()
        self.my_stemmer = stemmer.FindStems()
        self.my_tagger = postagger.POSTagger(tagging_model="wapiti").parse

        self.parser = MyMaltParser(parser_dirname=self.dir_path + 'resource/dependency_parser',
                                   model_filename='total_dep_parser.mco',
                                   tagger=self.my_tagger,
                                   stemmer=self.my_stemmer)

    def make_trainable_corpus(self, path, tagger=None):
        if tagger is None:
            tagger = self.my_tagger
        with open(path, 'r') as infile:
            content = infile.read().strip().split('\n\n')
            for i, sent in enumerate(content):
                if len(sent) == 0:
                    continue
                lines = sent.split('\n')
                sent_tokens = [x.split('\t')[1].decode('utf-8') for x in lines]
                tagged_sent = tagger(sent_tokens)
                tages = [x[1].encode('utf-8') for x in tagged_sent]
                for j, line in enumerate(lines):
                    line = line.split('\t')
                    line[3] = tages[j]
                    line[4] = tages[j]
                    line = '\t'.join(line)
                    lines[j] = line
                sent = '\n'.join(lines)
                content[i] = sent
        content = '\n\n'.join(content)
        with open("train_file.conll", 'w') as outfile:
            outfile.write(content)
        return content

    def parse_sent(self, sent, tagger=None, verbose=False):
        if tagger is None:
            tagger = self.my_tagger
        tokens = self.my_tokenizer.tokenize_words(sent)
        tagged_sent = tagger(tokens)
        return self.parser.parse_tagged_sent(tagged_sent, verbose)