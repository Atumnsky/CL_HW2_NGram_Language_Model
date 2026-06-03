"""

"""

import corpus_reader
import model
import generate

expected_output_plain = [
    ['Hello', 'this', 'is', 'our', 'tiny', 'corpus', 'to', 'test', 'if', 'our', 'program', 'works', 'or', 'if', 'it', "didn’t"],
    ['n’t', 'to', 'worry', 'it', 'will', 'definitely', 'work'], 
    ['But', 'anyway', 'let’s', 'just', 'continue', 'the', 'assignment', 'now', 'and', 'not', 'get', 'hung', 'up', 'on', 'a', 'simple', 'file']
]

expected_output_NLTK = [
    ['Hello', ',', 'this', 'is', 'our', 'tiny', 'corpus', 'to', 'test', 'if', 'our', 'program', 'works', 'or', 'if', 'it', 'didn','’','t…', '.'], 
    ['n','’','t', 'to', 'worry', ',', 'it', 'will', 'definitely', 'work', '!'], 
    ['But', 'anyway', ',', 'let', '’', 's', 'just', 'continue', 'the', 'assignment', 'now', 'and', 'not', 'get', 'hung', 'up', 'on', 'a', 'simple', 'file', '.']
]

def test_tokenizer_plain(text):
    """
    Test the plain tokenizer with a given text file.
    """
    with open(text, 'r', encoding='mac_roman') as f:
        all_text = f.read()

    my_tokenizer = corpus_reader.Tokenizer()
    test_tokenized = my_tokenizer.string2sentences(all_text)
    same_output = True

    if test_tokenized != expected_output_plain:
        same_output = False
        print("Test failed: Tokenizer output does not match expected output.")
    else:
        print("Test passed: Tokenizer output matches expected output.")

    return same_output

def test_tokenizer_nltk(text):
    """
    Test the NLTK tokenizer with a given text file.
    """
    with open(text, 'r', encoding='mac_roman') as f:
        all_text = f.read()

    my_tokenizer = corpus_reader.TokenizerNLTK()
    test_tokenized = my_tokenizer.string2sentences(all_text)
    same_output = True

    if test_tokenized != expected_output_NLTK:
        same_output = False
        print("Test failed: NLTK Tokenizer output does not match expected output.")
    else:
        print("Test passed: NLTK Tokenizer output matches expected output.")

    return same_output

if __name__ == "__main__":
    print("--- STARTING TOKENIZER TESTS ---")
    test_tokenizer_plain("tiny_corpus.txt")
    test_tokenizer_nltk("tiny_corpus.txt")

def test_ngram_table():
    """
    Tests the N-gram table with a tiny corpus of words and a tiny corpus of sentences
    """
    


def test_probability_zero():
    """
    Using your tiny model from test_ngram_table, test
    that you get the following:
    1. 4 parts: Raw AND smoothed probability 0 for a prefix OR successor not
    in the model at all
    2. For a prefix in the model and a successor that is in the model but not in
    that prefix’s successors:
    1. 0 raw prob
    2. non-zero smoothed prob
    """
