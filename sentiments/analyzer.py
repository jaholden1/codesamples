import nltk

class Analyzer():
    """Implements sentiment analysis."""


    def __init__(self, positives, negatives):
        """Initialize Analyzer."""

        # create lists and open files for reading
        self.positives = []
        with open("positive-words.txt") as positive:
            # iterate over each line, skipping comments that start with ;
            for line in positive:
                if not line.startswith((";", " ")):
                    self.positives.append(line.strip())
        
        self.negatives = []
        with open("negative-words.txt") as negative:
            # iterate over each line, skipping comments that start with ;
            for line in negative:
                if not line.startswith((";", " ")):
                    self.negatives.append(line.strip())



    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""

        # split words into single tokens (containing single words)
        tokenizer = nltk.tokenize.TweetTokenizer()
        # instantiate tokenizer
        tokens = tokenizer.tokenize(text)
        score = 0
        
        # iterate over tokens
        for token in tokens:
            # check if token is positive or negative word
            if token.lower() in self.positives:
                score += 1
            elif token.lower() in self.negatives:
                score -= 1
                
        # return final score        
        return score
