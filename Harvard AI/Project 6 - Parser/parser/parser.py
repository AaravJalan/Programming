import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | VP | S Conj S
NP -> N | Det N | Det AP N
VP -> V | V NP | Adv VP | VP Adv | VP PP

PP -> P NP
AP -> Adj | Adj AP
"""

# | AP NP | Adv NP | Conj NP |
grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():
    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Returning all words in sentence, if they contain at least one alphabet.
    return [x.lower() for x in nltk.word_tokenize(sentence) if alphabet(x)]


# Helper function to check if a word contains an alphabet.
def alphabet(word):
    for char in word:
        if char.isalpha():
            return True
    return False


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # List of all noun chunks.
    chunks = []

    for chunk in tree.subtrees():
        # Checks if the chunk is a noun phrase.
        if chunk.label() == 'NP':
            # Checks if an NP chunk doesn't contain any other nested NP chunks.
            if check(chunk):
                # Adds noun phrase to the chunks list.
                chunks.append(chunk)
    return chunks


# Helper function which checks if one NP chunk contains any others.
def check(noun_phrase):
    for chunk in noun_phrase.subtrees():
        # If the subtree is a NP chunk, and not the same as the parent...
        if chunk.label() == 'NP' and chunk != noun_phrase:
            # ...Parent contains another NP chunk, returning False.
            return False
    return True


if __name__ == "__main__":
    main()
