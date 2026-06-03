"""
Defines functions to use a trained model generatively.
Demonstrates several models with a script.
"""

import argparse
import random
import corpus_reader
from model import START, END, NGramModel

random.seed(42)

def generate_one(model, max_length=100):
    """
    Generates one sentence or word, depending on the mode, using the probabilities
    defined in the model. Starts with start token(s), and uses random.choices
    or a similar function to choose probabilistically from the possible successors to
    the words generated so far.
    """
    context = [START] * (model.n - 1)
    result = []

    for _ in range(max_length):
        succ = model.get_successors(context)
        if not succ:
            break

        tokens = [token for token, count in succ]
        probabilities = [model.probability(model.hashable_prefix(context), token, 0) for token in tokens]

        next_token = random.choices(tokens, weights=probabilities, k=1)[0]
        if next_token == END:
            break
        result.append(next_token)

        context = (context + [next_token])[-(model.n - 1):]

    if model.mode == "word":
        return "".join(result)
    return result
        

def demonstrate(model):
    """
    Demonstrates one model as follows:
    1. Print the models’ string representation using e.g. print(my_model)
    2. Generate 5 words/sentences using your function generate_one and print
    them out nicely.
    3. Calculate and print the raw perplexity of the 6 test words/sentences below
    using the model’s corpus_perplexity method on EACH word/sentence.
    4. Similarly, Calculate and print the LaPlace-smoothed perplexity with
    smoothing_constant=1 for the 6 words/sentences
    """

    print(model)

    print("\nGenerated items:")
    for _ in range(5):
        item = generate_one(model)
        if model.mode == "word":
            print(f"  {item}")
        elif model.mode == "sentence":
            print(f"  {' '.join(item)}")

    if model.mode == "word":
        test_strings = ["swicky", "these", "devils", "foonch", "FAQ", "isn't"]
    elif model.mode == "sentence":
        test_strings = ["\"Don't make too much noise,\" said Father Brown.","Don't go there!","Father Brown laughed.","make noise too much don't Father said Brown.","The men left.","The swicky men left."]

    print("\nPerplexities:")
    for s in test_strings:
        raw = model.corpus_perplexity(s, smoothing_constant=0)
        smoothed = model.corpus_perplexity(s, smoothing_constant=1)
        raw_val = raw[0] if raw else float('inf')
        smooth_val = smoothed[0] if smoothed else float('inf')

        print(f"\n{s}")
        print(f"\tRaw:\t\t{raw_val}")
        print(f"\tSmoothed:\t{smooth_val}")


#Script
if __name__ == "__main__":
    """
    command: python generate.py data: folder n: 2
    instructions: python generate.py -h
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("data: ", required=True, help="Path to data")
    parser.add_argument("n: ", type = int, default = 2, help = "N-gram size")
    parser.add_argument("mode: ", choices = ["sentence", "word"], help = "sentence mode for word generation, word mode for character generation")
    parser.add_argument("tokenizer: ", choices = ["basic", "NLTK"], help = "select tokenizer: basic, NLTK")

    args = parser.parse_args()

    if args.tokenizer == "NLTK":
        tok = corpus_reader.TokenizerNLTK()
    else:
        tok = corpus_reader.Tokenizer()
    
    reader = corpus_reader.CorpusReader(args.data, tok)

    if args.mode == "sentence":
        data = reader.sents()
    else:
        data = reader.words()
    
    model = NGramModel(data, args.n, tok, mode = args.mode)

    demonstrate(model)




