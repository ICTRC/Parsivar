import re


class Tokenizer():
    def __init__(self):
        """
        Define Regex Patterns
        """
        self.NUMBER_PATTERN = r"[-+]?\d*\.\d+|\d+"
        self.SENTENCE_DELIMITERS = r'([!\.\?؟]+)[\n]*'
        self.NEWLINE_PATTERNS = [r':\n', r';\n', r'؛\n', r'[\n]+']

    def tokenize_words(self, doc_string):
        """Tokenize the input document into words."""
        if not doc_string:
            return []
        # Remove zero-width non-joiner characters and split into words
        return [word.strip("\u200c") for word in doc_string.strip().split() if word.strip("\u200c")]

    def tokenize_sentences(self, doc_string):
        """Tokenize the input document into sentences."""
        if not doc_string:
            return []

        # Extract and replace numbers with a placeholder
        numbers = re.findall(self.NUMBER_PATTERN, doc_string)
        doc_string = re.sub(self.NUMBER_PATTERN, 'floatingpointnumber', doc_string)

        # Replace sentence delimiters and newline patterns with tabs
        doc_string = re.sub(self.SENTENCE_DELIMITERS, self._add_tab, doc_string)
        for pattern in self.NEWLINE_PATTERNS:
            doc_string = re.sub(pattern, self._add_tab, doc_string)

        # Restore numbers in the document
        for number in numbers:
            doc_string = re.sub('floatingpointnumber', number, doc_string, 1)

        # Split into sentences and filter out empty strings
        return [sentence for sentence in doc_string.split('\t\t') if sentence]

    def _add_tab(self, match):
        """Helper method to format matched delimiters with tabs."""
        matched_text = match.group().strip(' \n')
        return f" {matched_text}\t\t"