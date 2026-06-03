"""
The objective of this model is to read in text and turn it into usable tokens
"""
import re
import os
import nltk

class CorpusReader:
    """
    Read the contents of a directory of files, and return the results as
    either a list of sentences or a list of words.

    The pathname of the directory to read should be passed when
    creating the class:
    rdr = CorpusReader(r"path/to/dir")

    Attributes:
        tokenizer: a Tokenizer
        path: The path to the directory of corpus files
    """

    def __init__(self, directory, tokenizer):
        """
        Initialize a CorpusReader object. This function checks that
        the directory exists and is a directory, but does not read its
        contents.
        @param directory: str: the path to the directory of corpus files
        @param tokenizer: a Tokenizer
        """
        self.path = directory
        self.tokenizer = tokenizer
        
        if not os.path.isdir(directory):
            raise ValueError(directory + " does not exist or is not a directory")


    def raw(self):
        """
        Read in the corpus files and return the results as one long string.
        @return: str
        """
        text = ""

        for filename in os.listdir(self.path):
            if filename.endswith(".txt"):
                full_file_path = os.path.join(self.path, filename)
                with open(full_file_path) as conn:
                    text += conn.read()
        return text


    def sents(self):
        """
        Read in the corpus files and returns the sentences as a list of lists of tokens.
        Uses the tokenizer's string2sentences method.
        @return: the corpus as a list of lists of strings
        """
        text = ""

        for filename in os.listdir(self.path):
            if filename.endswith(".txt"):
                full_file_path = os.path.join(self.path, filename)
                with open(full_file_path) as conn:
                    text += conn.read()

        return self.tokenizer.string2sentences(text)

    def words(self):
        """
        Read in the corpus files and returns the words of the corpus as a list of tokens.
        Uses the tokenizer's word_tokenize method.
        @return: the corpus as a list of lists of strings
        """
        text = ""

        for filename in os.listdir(self.path):
            if filename.endswith(".txt"):
                full_file_path = os.path.join(self.path, filename)
                with open(full_file_path) as conn:
                    text += conn.read()
                    
        return self.tokenizer.word_tokenize(text)

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
        clean_word = re.sub(r"^\W+|\W+$", "", word)
        return clean_word
               


    def sent_tokenize(self, text):
        """
        Split a text into a list of sentences.
        Split on . ? !
        Discard empty sentences.
        @param text: string
        @return: list of strings
        """
        sentences = re.split(r"(?<=[.?!])\s+", text)
        return [sent for sent in sentences if sent!=""]


    def word_tokenize(self, text):
        """
        Split a text into a list of words.
        Split on whitespace.
        use self._clean_word to remove punctuation.
        Discard empty words.
        @param text: string
        @return: list of strings
        """
        words = text.split()
        cleaned_words = [self._clean_word(w) for w in words]
        return [w for w in cleaned_words if w!=""]

    def string2sentences(self, text):
        """
        Split a text into a list of lists of tokens.
        Uses sent_tokenize and word_tokenize.
        @param text: string
        @return: list of lists of strings (tokens).
                    Tokens may contain punctuation internally
                    (e.g. can't, uh-oh) but no other punctuation.
        """
        tok_sents = self.sent_tokenize(text)
        tok_list = []
        for sent in tok_sents:
            tok_list.append(self.word_tokenize(sent))
        return tok_list

class TokenizerNLTK(Tokenizer):
    """
    A tokenizer that uses nltk's tokenizers.
    """

    def __init__(self):
        
        self.nltk = nltk

    def sent_tokenize(self, text):
        return self.nltk.sent_tokenize(text)

    def word_tokenize(self, text):
        return self.nltk.word_tokenize(text)



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
