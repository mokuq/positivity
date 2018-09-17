import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        self.words_pos = set() #set() - тип даних множина 
        self.words_neg = set()

        file1 = open(positives, "r") #file changed to file1 (for clarifying that it is not a second "file" - see below)
        for line in file1:
            if line [0]!=";":
                self.words_pos.add(line.rstrip("\n")) 

                
        file1.close()

        file2 = open(negatives, "r")
        for line in file2:
            if line [0]!=";":
                self.words_neg.add(line.rstrip("\n"))

        file2.close()   

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""

        if text.lower() in self.words_pos:
            return 1
        
        elif text.lower() in self.words_neg:
            return -1
            
        else:
            return 0
