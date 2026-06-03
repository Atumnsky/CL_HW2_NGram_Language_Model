"""
Demonstrates the code by training and demonstrating 24 different models.
12 models with train.zip
12 models using Gutenberg Corpus
"""
from nltk.corpus import gutenberg
import corpus_reader
import model
import generate

train_path = r"./train"

tok_plain = corpus_reader.Tokenizer()
tok_nltk = corpus_reader.TokenizerNLTK()

reader_plain = corpus_reader.CorpusReader(train_path, tok_plain)
reader_nltk = corpus_reader.CorpusReader(train_path, tok_nltk)

"""
12 N-gram models from train.zip
"""
print("---N-gram models trained from ./train---")
for n in [1,2,3]:
    for mode in ["sentence", "word"]:
        for tok, reader in [(tok_plain, reader_plain),(tok_nltk, reader_nltk)]:
            if mode == "sentence":
                data1 = reader.sents()
            else:
                data1 = reader.words()

            ngram_model1 = model.NGramModel(data1, n, tok, mode = mode)

            generate.demonstrate(ngram_model1)


"""
12 N-gram models from gutenberg
"""

print("---N-gram models trained from Gutenberg---")
for n in [1,2,3]:
    for mode in ["sentence", "word"]:
        for tok in [(tok_plain),(tok_nltk)]:
            if mode == "sentence":
                data2 = gutenberg.sents()
            else:
                data2 = gutenberg.words()

            ngram_model2 = model.NGramModel(data2, n, tok, mode = mode)

            generate.demonstrate(ngram_model2)