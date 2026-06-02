import random
from model import START, END

random.seed(42)

def generate_one(model, max_length=100):
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
        test_strings = [
            "\"Don't make too much noise,\" said Father Brown.",
            "Don't go there!",
            "Father Brown laughed.",
            "make noise too much don't Father said Brown.",
            "The men left.",
            "The swicky men left."
        ]

    print("\nPerplexities:")
    for s in test_strings:
        raw = model.corpus_perplexity(s, smoothing_constant=0)
        smoothed = model.corpus_perplexity(s, smoothing_constant=1)
        raw_val = raw[0] if raw else float('inf')
        smooth_val = smoothed[0] if smoothed else float('inf')

        print(f"\n{s}")
        print(f"\tRaw:\t\t{raw_val:.2f}")
        print(f"\tSmoothed:\t{smooth_val:.2f}")
    print("\n" + "-" * 40)

#Script