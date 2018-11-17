import os
from nltk.tag.stanford import StanfordPOSTagger
import re

class POSTagger():
    def __init__(self,
                 stanford_postagger_model=None,
                 wapiti_postagger_model=None,
                 jar_tagger_path=None,
                 jdk_variable_path="C:/Program Files/Java/jdk1.8.0_121/bin/java.exe",
                 tagging_model="wapiti"):

        import platform
        if platform.system() == "Windows":
            self.tagging_model = "stanford"
        else:
            self.tagging_model = tagging_model

        self.dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"

        if stanford_postagger_model is None:
            self.stanford_postagger_model = self.dir_path + "resource/postagger/NC_model"
        else:
            self.stanford_postagger_model = stanford_postagger_model

        if jar_tagger_path is None:
            self.jar_tagger_path = self.dir_path + 'resource/postagger/stanford-postagger.jar'
        else:
            self.jar_tagger_path = jar_tagger_path

        if wapiti_postagger_model is None:
            self.wapiti_postagger_model = self.dir_path + "resource/postagger/UPC_full_model_wapiti"
        else:
            self.wapiti_postagger_model = wapiti_postagger_model

        if self.tagging_model == "stanford":
            java_path = jdk_variable_path
            os.environ['JAVAHOME'] = java_path

            self.tagger = StanfordPOSTagger(model_filename=self.stanford_postagger_model,
                                            path_to_jar=self.jar_tagger_path,
                                            encoding='utf-8',
                                            java_options='-mx5000m')
        elif self.tagging_model == "wapiti":
            from wapiti import Model
            self.tagger = Model(model=self.wapiti_postagger_model)

    def is_all_latin(self, word):
        pattern = '[a-zA-Z]*'
        w = re.sub(pattern, '', word)
        if len(w) == 0:
            return True
        else:
            return False

    def parse(self, token_list):
        tagged_tuples = []
        if self.tagging_model == "stanford":
            postags = self.tagger.tag(token_list)
            for element in postags:
                tmp = '_'.join(t for t in element)
                tmp = tmp.strip("_")
                tmp = tmp.split('/')
                tag = tmp[-1]
                tmp = tmp[:-1]
                tmp = '/'.join(i for i in tmp)
                tmp = tmp.strip('/')
                if self.is_all_latin(tmp):
                    tagged_tuples.append((tmp, "FW"))
                else:
                    tagged_tuples.append((tmp, tag))

        elif self.tagging_model == "wapiti":
            sent_line = "\n".join(x for x in token_list)
            postags = self.tagger.label_sequence(sent_line).decode('utf-8')
            postags = postags.strip().split('\n')
            for i, el in enumerate(token_list):
                if self.is_all_latin(el):
                    tagged_tuples.append((el, u"FW"))
                else:
                    tagged_tuples.append((el, postags[i]))
        return tagged_tuples
