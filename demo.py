"""
Demonstrates the code by training and demonstrating 24 different models.
12 models with train.zip
12 models using Gutenberg Corpus
"""
import nltk
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
for n in [1,2,3]:
    for mode in ["sentence", "word"]:
        for tok, reader in [(tok_plain, reader_plain),(tok_nltk, reader_nltk)]:
            if mode == "sentence":
                data = reader.sents()
            else:
                data = reader.words()

            ngram_model = model.NGramModel(data, n, tok, mode = mode)

            generate.demonstrate(ngram_model)


"""
12 N-gram models from gutenberg
"""