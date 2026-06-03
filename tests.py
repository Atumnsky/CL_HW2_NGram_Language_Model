"""
Tests the tokenizers, n-gram table and probability_zero in the model
"""

from corpus_reader import Tokenizer, TokenizerNLTK
from model import START, END , NGramModel


expected_output_plain = [
    ["Hello", "this", "is", "our", "tiny", "corpus", "to", "test", "if", "our", "program", "works", "or", "if", "it", "didn't"],
    ["n't", "to", "worry", "it", "will", "definitely", "work"],
    ["But", "anyway", "let's", "just", "continue", "the", "assignment", "now", "and", "not", "get", "hung", "up", "on", "a", "simple", "file"]
]

expected_output_NLTK = [
    ["Hello", ",", "this", "is", "our", "tiny", "corpus", "to", "test", "if", "our", "program", "works", "or", "if", "it", "didn't…", "."], 
    ["n't", "to", "worry", ",", "it", "will", "definitely", "work", "!"], 
    ["But", "anyway", ",", "let", "'s", "just", "continue", "the", "assignment", "now", "and", "not", "get", "hung", "up", "on", "a", "simple", "file", "."]
]

def test_tokenizer_plain(text):
    """
    Test the plain tokenizer with a given text file.
    """
    with open(text, 'r', encoding='mac_roman') as f:
        all_text = f.read()

    my_tokenizer = Tokenizer()
    test_tokenized = my_tokenizer.string2sentences(all_text)
    same_output = True

    if test_tokenized != expected_output_plain:
        same_output = False
        print("TEST FAILED: Tokenizer output does not match expected output.")
    else:
        print("TEST PASSED: Tokenizer output matches expected output.")

    return same_output

def test_tokenizer_nltk(text):
    """
    Test the NLTK tokenizer with a given text file.
    """
    with open(text, 'r', encoding='mac_roman') as f:
        all_text = f.read()

    my_tokenizer = TokenizerNLTK()
    test_tokenized = my_tokenizer.string2sentences(all_text)
    same_output = True

    if test_tokenized != expected_output_NLTK:
        same_output = False
        print("TEST FAILED: NLTK Tokenizer output does not match expected output.")
    else:
        print("TEST PASSED: NLTK Tokenizer output matches expected output.")

    return same_output



def test_ngram_table():
    """
    Tests the N-gram table with a tiny corpus of words and a tiny corpus of sentences
    """
    tok = Tokenizer()

    sentence_data = [['the','cat','jumped'],['the','dog','barked']]
    ngram_s = NGramModel(sentence_data, n = 3, tokenizer = tok, mode="sentence")

    expected_ngram_s = {
        ("<s>", "<s>"): {"the": 2},
        ("<s>", "the"):  {"cat": 1, "dog": 1},
        ("the", "cat"):  {"jumped": 1},
        ("cat", "jumped"):  {"</s>": 1},
        ("the", "dog"):  {"barked": 1},
        ("dog", "barked"):  {"</s>": 1}
    }

    if ngram_s.ngram_table != expected_ngram_s:
        print("TEST FAILED: N-gram table -sentence mode")
    else:
        print("TEST PASSED: N-gram table -sentence mode")

    
    word_data = ['cat', 'dog']
    ngram_w = NGramModel(word_data, n=3, tokenizer=tok, mode="word")

    expected_ngram_w = {
        ("<s>", "<s>"): {"c": 1, "d": 1},
        ("<s>", "c"):   {"a": 1},
        ("c", "a"):     {"t": 1},
        ("a", "t"):     {"</s>": 1},
        ("<s>", "d"):   {"o": 1},
        ("d", "o"):     {"g": 1},
        ("o", "g"):     {"</s>": 1}
    }

    if ngram_w.ngram_table != expected_ngram_w:
        print("TEST FAILED: N-gram table -word mode")
    else:
        print("TEST PASSED: N-gram table -word mode")




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
    tok = Tokenizer()

    sentence_data = [['the','cat','jumped'],['the','dog','barked']]
    model = NGramModel(sentence_data, n=3, tokenizer=tok, mode="sentence")
    test_passed = True

    k = 1

    raw1 = model.probability(('x','y'), 'zzz', 0)
    smooth1 = model.probability(('x','y'),'zzz',k)
    if not (raw1 == 0 and smooth1 > 0):
        print("TEST FAILED: unknown prefix + unknown successors")
        print(f"raw={raw1}, smooted={smooth1}")
        test_passed = False
    

    raw2 = model.probability(('x','y'), 'the', 0)
    smooth2 = model.probability(('x','y'),'the',k)
    if not (raw2 == 0 and smooth2 > 0):
        print("TEST FAILED: unknown prefix + known successors")
        print(f"raw={raw2}, smooted={smooth2}")
        test_passed = False


    raw3 = model.probability(('the','cat'), 'zzz', 0)
    smooth3 = model.probability(('the','cat'),'zzz',k)
    if not (raw3 == 0 and smooth3 > 0):
        print("TEST FAILED: known prefix + unknown successors")
        print(f"raw={raw3}, smooted={smooth3}")
        test_passed = False
    

    raw4 = model.probability(('<s>','the'), 'barked', 0)
    smooth4 = model.probability(('<s>','the'),'jumped',k)
    if not (raw4 == 0 and smooth4 > 0):
        print("TEST FAILED: known prefix + known successors")
        print(f"raw={raw4}, smooted={smooth4}")
        test_passed = False
    

    if test_passed:
        print("TEST PASSED: probablity_zero")


    



if __name__ == "__main__":
    print("--- STARTING TOKENIZER TESTS ---")
    test_tokenizer_plain("tiny_corpus.txt")
    test_tokenizer_nltk("tiny_corpus.txt")

    print("---STARTING MODEL TESTS---")
    test_ngram_table()
    test_probability_zero()
