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

    def convert_nested_tree_to_raw_string(self, tree, depth=0):
        """Convert a nested tree structure into a raw string representation."""
        result = []
        for item in tree:
            if isinstance(item, tuple):
                result.append(item[0])
            elif depth >= 1:
                result.append(self.convert_nested_tree_to_raw_string(item, depth + 1))
            else:
                tag = item._label
                nested_string = self.convert_nested_tree_to_raw_string(item, depth + 1)
                result.append(f"[{nested_string} {tag}]")
        return ' '.join(result)

    def chunk_sentence(self, pos_taged_tuples):
        """Chunk a sentence based on the defined grammar."""
        return self.cp.parse(pos_taged_tuples)