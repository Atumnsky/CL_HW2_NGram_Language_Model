"""
Replace this with an explanation of the purpose of this module
"""


class CorpusReader:
    """
    Read the contents of a directory of files, and return the results as
    either a list of sentences or a list of words.

    The pathname of the directory to read should be passed when
    creating the class:
    rdr = CorpusReader(r"path/to/dir")

    Attributes:
        tokenizer: # TODO
        path: TODO
    """

    def __init__(self, directory, tokenizer):
        """
        Initialize a CorpusReader object. This function checks that
        the directory exists and is a directory, but does not read its
        contents.
        @param directory: str: the path to the directory of corpus files
        @param tokenizer: a Tokenizer
        """
        ...


    def raw(self):
        """
        Read in the corpus files and return the results as one long string.
        @return: str
        """
        # TODO
        ...


    def sents(self):
        """
        Read in the corpus files and returns the sentences as a list of lists of tokens.
        Uses the tokenizer's string2sentences method.
        @return: the corpus as a list of lists of strings
        """
        # TODO
        ...

    def words(self):
        """
        Read in the corpus files and returns the words of the corpus as a list of tokens.
        Uses the tokenizer's word_tokenize method.
        @return: the corpus as a list of lists of strings
        """
        # TODO
        ...

class Tokenizer:
    """
    Tokenizes a data point
    """

    def __init__(self):
        pass

    def _clean_word(self, word):
        """
        Clean up one word:
        Remove punctuation from before and after the word.
        e.g. \"Wow!!!\" -> Wow
        e.g. can't -> can't
        """

    def sent_tokenize(self, text):
        """
        Split a text into a list of sentences.
        Split on . ? !
        Discard empty sentences.
        @param text: # TODO
        @return: # TODO
        """
        ...

    def word_tokenize(self, text):
        """
        Split a text into a list of words.
        Split on whitespace.
        use self._clean_word to remove punctuation.
        Discard empty words.
        @param text: # TODO
        @return: # TODO
        """
        ...

    def string2sentences(self, text):
        """
        Split a text into a list of lists of tokens.
        Uses sent_tokenize and word_tokenize.
        @param text: # TODO
        @return: list of lists of strings (tokens).
                    Tokens may contain punctuation internally
                    (e.g. can't, uh-oh) but no other punctuation.
        """
        # TODO
        ...


if __name__ == '__main__':
    # Some testing
    # Feel free to edit, add more testing, etc.
    # this section will not be marked

    c = "Here's my sentence. \"What a nice sentence it is!!!\"   Wow! ...\n"

    tok = Tokenizer()

    words = tok.word_tokenize(c)
    print(words)

    sents = tok.sent_tokenize(c)
    print(sents)

    tokenised_sentences = tok.string2sentences(c)
    print(tokenised_sentences)

    # real data
    path = "train"
    reader = CorpusReader(path, tok)

    corpus = reader.sents()
    for s in corpus[20:30]:
        print(s)
