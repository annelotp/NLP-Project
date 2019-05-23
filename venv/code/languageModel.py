import math, collections


class languageModel:

    def __init__(self, corpus):
        """Initialize your data structures in the constructor."""
        self.unigramCounts = collections.defaultdict(lambda: 0)
        self.bigramCounts = collections.defaultdict(lambda: 0)
        self.trigramCounts = collections.defaultdict(lambda: 0)
        self.total = 0
        self.train(corpus)

    def train(self, sentences):
        """ Takes a corpus and trains your language model.
            Compute any counts or other corpus statistics in this function.
        """
        for sentence in sentences:
            i = 0
            while i < len(sentence.data):
                x = sentence.data[i].word
                self.unigramCounts[x] = self.unigramCounts[x] + 1
                if i > 0:
                    y = sentence.data[i - 1].word
                    self.bigramCounts[x, y] = self.bigramCounts[x, y] + 1
                if i > 1:
                    z = sentence.data[i - 2].word
                    self.trigramCounts[x, y, z] = self.trigramCounts[x, y, z] + 1
                self.total += 1
                i = i + 1

    def predict(self, bigram):
        maximumCount = -1
        bestWord = 'anecdote'
        for i in range(10):
            print(self.trigramCounts.keys()[i])
        for i in self.unigramCounts.keys():
            if self.trigramCounts[bigram[0],bigram[1],i] > maximumCount:
                maximumCount = self.trigramCounts[bigram[0],bigram[1],i]
                bestWord = i
        return bestWord


    def score(self, sentence):
        """ Takes a list of strings as argument and returns the log-probability of the
            sentence using your language model. Use whatever data you computed in train() here.
        """
        uniscore = 0.0
        biscore = 0.0
        triscore = 0.0
        i = 0
        while i < len(sentence):
            x = sentence[i]
            countUNI = self.unigramCounts[x] + 1
            if countUNI > 0:
                uniscore += math.log(countUNI)
                uniscore -= math.log(self.total + len(self.unigramCounts))
            else:
                uniscore = float('-inf')  # not smoothed

            if i > 0:
                y = sentence[i - 1]
                countBI = self.bigramCounts[x, y] + 1
                if countBI > 0:
                    biscore += math.log(countBI)
                    biscore -= math.log(self.unigramCounts[y] + len(self.unigramCounts))
                else:
                    biscore = float('-inf')  # not smoothed
            if i > 1:
                z = sentence[i - 2]
                countTRI = self.trigramCounts[x, y, z] + 1
                if countTRI > 0:
                    biscore += math.log(countTRI)
                    biscore -= math.log(self.bigramCounts[x, y] + len(self.bigramCounts))
                else:
                    biscore = float('-inf')  # not smoothed
            i = i + 1
        return 0.7 * triscore + 0.2 * biscore + 0.1 * uniscore