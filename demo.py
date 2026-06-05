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
for n in [2,3,4]:
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

tok_gutenberg = corpus_reader.TokenizerNLTK()

print("---N-gram models trained from Gutenberg---")
for n in [2,3,4]:
    for mode in ["sentence", "word"]:
        if mode == "sentence":
            data_gut = gutenberg.sents()
        else:
            data_gut = gutenberg.words()
            
        model_gut = model.NGramModel(data_gut, n, tok_gutenberg, mode=mode)
        
        print("Gutenberg's own sents() and words()")
        generate.demonstrate(model_gut)

        gut_text = gutenberg.raw()
        if mode == "sentence":
            data_raw = tok_gutenberg.string2sentences(gut_text)
        else:
            data_raw = tok_gutenberg.word_tokenize(gut_text)
        
        model_raw = model.NGramModel(data_raw, n, tok_gutenberg, mode = mode)

        print("Gutenberg raw with own tokenizer")
        generate.demonstrate(model_raw)