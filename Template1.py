#
# Simple template for minimalist derivational search function
# with set-theoretical bare phrase structure as a basis,
# for illustration
#

import itertools    #   module for simple combinatorial operations

# Lexicon will be a simple dictionary with lexical features provided as sets (currently empty)
lexicon = {'a': set(),
           'b': set(),
           'c': set(),
           'd': set()}

# Class which defines the phrase structure formalism
class PhraseStructure:
    def __init__(self, X=None, Y=None):
        self.constituents = {X, Y}      # Daughter constituents
        self.phon = ''                  # Name
        self.features = None            # Set of features, generated from lexical items

    # Standard Merge
    def Merge(X, Y):
        return PhraseStructure(X, Y)

    # A zero-level category is one that lacks at least one daughter constituent
    def zero_level(self):
        return self.constituents & {None}

    # Auxiliary function which maps phrase structure objects into symbolic printouts
    def __str__(self):
        str = ''
        if self.zero_level():
            str = self.phon
        else:
            str += '{'
            for const in self.constituents:
                str = str + f' {const} '
            str += '}'
        return str

# Speaker model performs most calculations
class SpeakerModel:
    def __init__(self):
        self.syntactic_operations = [PhraseStructure.Merge]     # List of all syntactic operations available
        self.n_derivations = 0                                  # Counts the number of derivations

    # Retrieves lexical items from the dictionary and constructs zero-level phrase structure objects
    def LexicalRetrieval(self, name):
        ps = PhraseStructure()
        ps.features = lexicon[name]     # Stream lexical features from the lexical items into the constituent
        ps.phon = name                  # Create artificial name
        return ps

    # A wrapper function for the derivational search function
    # which performs auxiliary tasks and initializes the derivation
    def derive(self, sentence):
        self.n_derivations = 0
        self.derivational_search_function({self.LexicalRetrieval(item) for item in sentence.split(' ')})

    # Searches through all derivations defined by the grammar (here, Merge)
    def derivational_search_function(self, sWM):
        if len(sWM) == 1:                               #   If there is only one phrase structure object in the working memory
            self.final_output(next(iter(sWM)))          #   stop the derivation and consider it a finished derivation,
        else:                                           #   else continue the derivation:
            for pair in itertools.combinations(sWM, 2): #   (1) get all combinations of two objects in the working memory
                for OP in self.syntactic_operations:    #   (2) consider all syntactic operations available in the grammar
                    # Apply (2) to (1) and continue the derivation (recursive branching)
                    self.derivational_search_function({SO for SO in sWM if SO not in {pair[0], pair[1]}} | {OP(pair[0], pair[1])})

    # Processes all complete derivations, in this case prints them out
    def final_output(self, solution):
        self.n_derivations += 1
        print(f'\t{self.n_derivations}. {solution}')  # print the output


sm = SpeakerModel()     # Creates the speaker model
sm.derive('a b c d')    # Calls the wrapper function with a sentence, from which we construct
                        # the initial numeration

