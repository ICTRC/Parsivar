import nltk

class FindChunks():
    def __init__(self):
        self.grammar = r"""
                        VP: {<ADJ_SIM><V_PRS>}
                        VP: {<ADJ_INO><V.*>}
                        VP: {<V_PRS><N_SING><V_SUB>}
                        NP: {<N_SING><ADJ.*><N_SING>}
                        NP: {<N.*><PRO>}
                        VP: {<N_SING><V_.*>}
                        VP: {<V.*>+}
                        NP: {<ADJ.*>?<N.*>+ <ADJ.*>?}
                        DNP: {<DET><NP>}
                        PP: {<ADJ_CMPR><P>}
                        PP: {<ADJ_SIM><P>}
                        PP: {<P><N_SING>}
                        PP: {<P>*}
                        DDNP: {<NP><DNP>}
                        NPP: {<PP><NP>+}
                        """

        self.cp = nltk.RegexpParser(self.grammar)

    def convert_nestedtree2rawstring(self, tree, d=0):
        s = ''
        for item in tree:
            if isinstance(item, tuple):
                s += item[0] + ' '
            elif d >= 1:
                news = self.convert_nestedtree2rawstring(item, d + 1)
                s += news + ' '
            else:
                tag = item._label
                news = '[' + self.convert_nestedtree2rawstring(item, d + 1) + ' ' + tag + ']'
                s += news + ' '
        return s.strip()

    def chunk_sentence(self, pos_taged_tuples):
        return self.cp.parse(pos_taged_tuples)