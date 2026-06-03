"""
This module defines a class NGramModel that builds an ngram table from the
sentences or words of a corpus. It can also calculate the perplexity of a given
string, and generate sample strings from the model.
"""


from corpus_reader import Tokenizer
import math

# global start and end tokens
START = "<s>"
END = "</s>"

class NGramModel:
    """
    YUEPENG Describe the class -
    An n-gram language model that extimates probabilities of words (or characters) based on the previous n - 1 tokens

    Attributes:
        n : int: size of ngrams
        mode : str : # YUEPENG describe -   'sentence' for word generation in a sentence
                                            'word' for character generatoion in a word
        ngram_table : dict # YUEPENG describe - mapping prefixes to a dict of successors with their counts
        successors : set # YUEPENG describe - all tokens that ever appear as successors
        V : int: # YUEPENG describe - size of the successor vocab, len(successors)
    """

    def __init__(self, data, n, tokenizer: Tokenizer, mode="sentence"):
        """
        @param data: list of strings or list of lists of strings
        @param n: size of ngrams (e.g. 2 for bigrams)
        @param mode: if sentence: use ngrams of words to make sentences (default)
                     if word: use ngrams of letters to make words
        """
        # Mode: Whether we're making sentences from words or words from characters
        # YUEPENG raise an informative ValueError if mode is neither "sentence" nor "word"
        if mode != "sentence":
            raise ValueError ('Mode of the NGramModel is incorrect, please use mode="sentence" or mode="word"')
        elif mode != "word":
            raise ValueError ('Mode of the NGramModel is incorrect, please use mode="sentence" or mode="word"')
        
        # YUEPENG otherwise, store mode in self.mode
        # YUEPENG define self.n
        # YUEPENG define self.tokenizer
        else:
            self.mode = mode
            self.n = n
            self.tokenizer = tokenizer

        # YUEPENG use the data to create self.ngram_table (dict), self.successors (set), and self.V (int)
        self.ngram_table = {}
        self.successors = set()

        for item in data:
            tokens = self.preprocess(item) #lowercase and add START, END (list of strings)

            for i in range(len(tokens) - n+1):
                prefix_list = tokens[i : i + n-1]
                successor = tokens[i + n-1]
                prefix = self.hashable_prefix(prefix_list)

                if prefix not in self.ngram_table:
                    self.ngram_table[prefix] = {}
                self.ngram_table[prefix][successor] = self.ngram_table[prefix].get(successor, 0)+1

                self.successors.add(END)
                self.V = len(self.successors)



    # PROVIDED
    def __str__(self):
        """
        A string representation of the model.
        """
        ret = "-------------------"
        ret += f"\n{self.n}-gram model for {self.mode}s"
        ret += f"\nTokenizer class: {type(self.tokenizer).__name__}"
        ret += f"\nV = {self.V}"
        ret += f"\nNumber of prefixes: {len(self.ngram_table)}"
        ret += "\n-------------------"

        return ret
################################################################################################
    # OPTIONAL
    def get_ith_ngram(self, clean_item, i):
        """
        Helper function to get a single ngram
            from a cleaned list of words or characters.
        Optional -- delete if not wanted.
        Applies self.hashable_prefix so the prefix can be a key in self.ngram_table.
        @param clean_item: list of strings
        @param i: int
        @return: pair (prefix as str or Tuple, successor str)
        """
        prefix_sublist = ...  # TODO
        prefix = self.hashable_prefix(prefix_sublist)
        successor = ... # TODO
        return prefix, successor

    # OPTIONAL
    def number_of_ngrams(self, clean_item):
        """
        Helper function (optional -- delete if unwanted)
        """
        ...
################################################################################################

    # REQUIRED
    def preprocess(self, item):
        """
        Preprocesses a single data point:
            - make all characters lowercase
            - if in word mode, make item into a list of its characters
            - #YUEPENG Add n-1 START tokens and 1 END tokens

        @param item: string (word mode) or list of strings (sentence mode)
        @return list of strings
        """
        if self.mode == 'word':
            item = item.lower()
            token = list(item)
        elif self.mode == 'sentence':
            tokens = [word.lower() for word in item]
        
        start_tokens = [START] * (self.n - 1)
        return start_tokens + tokens + [END]

    # REQUIRED
    def probability(self, prefix, w_n, smoothing_constant=0):
        """
        Compute the probability that the prefix is followed by w_n, using LaPlace smoothing (default no smoothing)
        @param prefix: the same type as the keys of self.ngram_table. (str or Tuple)
        @param w_n: string: successor to prefix
        @param smoothing_constant: for LaPlace smoothing. Default 0 (no smoothing)
        Usage: e.g. to calculate the probability of the trigram "we love linguistics" without smoothing:
            probablility(("we", "love"), "linguistics")
        Returns 0 for unknown words and unknown prefixes.
        @return YUEPENG float probability
        """
        succ_dict = self.ngram_table.get(prefix, {})
        prefix_count = sum(succ_dict.values())
        ngram_count = succ_dict.get(w_n, 0)

        if smoothing_constant == 0:
            if prefix_count == 0:
                return 0.0
            return ngram_count/prefix_count
        else:
            return (ngram_count + smoothing_constant) / (prefix_count + smoothing_constant * self.V)

    # REQUIRED
    def corpus_perplexity(self, corpus: str, smoothing_constant=0):
        """
        Calculates the total complexity of a corpus, given as a single string.
        Applies the appropriate tokenisation and calls the perplexity method on each word or sentence.
        @param corpus: one or more words or sentences as a single string
        @param smoothing_constant: for LaPlace smoothing. Default 0 (no smoothing)
        @return: YUEPENG perplexity for each sentence/word (list of float)
        """
        if self.mode == 'sentence':
            items = self.tokenizer.string2sentences(corpus)
        elif self.mode == 'word':
            items = self.tokenizer.word_tokenize(corpus)
        
        return [self.perplexity(item,smoothing_constant) for item in items]
 
    # REQUIRED
    def perplexity(self, item, smoothing_constant=0):
        """
        Given a datapoint, apply self.preprocess,
            then calculate the perplexity of the processed data point.
        This is for a single word as a string (word mode) or a list of strings (sentence mode).
            Use corpus_perplexity for untokenised items.
        @param item: str: a word (word mode) or a sentence as a single string (sentence mode)
        @param smoothing_constant: for LaPlace smoothing. Default 0 (no smoothing)
        @return: YUEPENG perplexity of the item (float)

        ### LOWER PERPLEXITY == BETTER MODEL
        """ 
        # Recommendation: work in log space
        # to avoid floating point errors due to very small probabilities.
        tokens = self.preprocess(item)
        total_log_prob = 0.0
        N = 0

        for i in range(len(tokens) - self.n+1):
            prefix_list = tokens[i : i + self.n-1]
            successors = tokens[i + self.n-1]
            prefix = self.hashable_prefix(prefix_list)
            P = self.probability(prefix, successors, smoothing_constant)

            if P == 0:
                return float('inf') #log(0) = inf
            
            total_log_prob += math.log(P)
            N += 1
        
        avg_log_prob = total_log_prob/N
        return math.exp(-avg_log_prob)



    # REQUIRED
    def get_successors(self, prefix):
        """
        Get all successors of prefix
        @param prefix: same type as self.ngram_table
        @return: sorted list of (str, int) pairs
        """
        # make the prefix hashable if it's not already
        prefix = self.hashable_prefix(prefix)
        # find all successors of the prefix, and their counts
        inner_dict = self.ngram_table.get(prefix,{})
        successor_count_pairs = inner_dict.items()  # YUEPENG
        # return the successors and counts, most common first.
        return sorted(successor_count_pairs, key=lambda x: x[1], reverse=True)

    # PROVIDED
    def hashable_prefix(self, prefix):
        """
        Convenience function to get a hashable key for the ngram table,
            since lists cannot be keys in dicts.
        """
        if self.n == 2:
            # bigrams can just use the string
            if (isinstance(prefix, list) or isinstance(prefix, tuple)) and len(prefix) == 1:
                return prefix[0]
            elif isinstance(prefix, str):
                return prefix
            else:
                print(prefix, type(prefix))
                raise ValueError("Are you sure you've got a bigram?")
        else:
            # for higher n, just make a tuple
            return tuple(prefix)

    # PROVIDED
    def print_successors(self, prefix, k=None):
        """
        Prints the top k successors of prefix, and their counts,
            sorted by frequency.
        @param prefix: same type as self.ngram_table.
        @param k: how many successors to print. Default prints all.
        """
        # pretty-print the prefix
        if self.n < 3:
            print(prefix, ":")
        else:
            print(" ".join(prefix), ":")

        to_print = self.get_successors(prefix)
        if k is not None:
            print(f"Top {k} successors:")
            to_print = to_print[:k]
        for successor, count in to_print:
            print(f"\t{successor} -- {count}")

    # PROVIDED
    def print_model(self, k=None):
        """
        Prints out the model parameters and some statistics.
        """
        print("-----------------------")
        print(f"Model {self.n}-grams:\n")
        for prefix in self.ngram_table:
            self.print_successors(prefix, k)
        print("------------------------")
        print("Statistics")
        print(f"n = {self.n}")
        print("V =", self.V)
        print("Number of prefixes: ", len(self.ngram_table))
        print("------------------------")


if __name__ == "__main__":
    # Some testing
    # Feel free to edit, add more testing, etc.
    # this section will not be graded.

    from corpus_reader import Tokenizer

    toy = "\"Hi !there friend!\" !??? Can't you help me? There aren't so many..."

    tok = Tokenizer()

    # test string2sentences
    sents = tok.string2sentences(toy)
    # print(sents)
    gold_sents = [['Hi', 'there', 'friend'], ["Can't", 'you', 'help', 'me'], ['There', "aren't", 'so', 'many']]
    print(sents == gold_sents)


    model = NGramModel(sents, 4, tok)
    model.print_model()
    test_sentence = "Hi there, friend"
    test_tokens = tok.word_tokenize(test_sentence)
    print(model.perplexity(test_tokens, 1))


