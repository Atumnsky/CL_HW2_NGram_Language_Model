import random
from model import START, END


random.seed(42)

def generate_one(model, max_length):
    """
    Generate one sentence (list of strings) or word (string) from the model.
    Uses probabilities from the model
    """
    context = [START]*(model.n-1)
    result = []

    for _ in range(max_length):
        succ = model.get_successors(context)

        tokens = [t for t, in succ]

        Probabilities = [model.probability((model.hashable_prefix(context)), t, 0) for t in tokens]

        

def demonstrate(model):
    """
    
    """


