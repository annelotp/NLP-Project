from __future__ import division
import math, collections
from random import seed
from random import random


class languageModel:

    def __init__(self, corpus):
        """Initialize your data structures in the constructor."""
        self.unigramCounts = collections.defaultdict(lambda: 1)
        self.bigramCounts = collections.defaultdict(lambda: 0)
        self.trigramCounts = collections.defaultdict(lambda: 0)
        self.startProb = collections.defaultdict(lambda: 0);
        self.total = 0
        self.train(corpus)
        #self.printTrigram()

    def train(self, corpus):
        """ Takes a corpus and trains your language model.
            Compute any counts or other corpus statistics in this function.
        """
        for sentence in corpus.sentences:
            i = 0
            while i < len(sentence):
                x = sentence[i]
                self.unigramCounts[x] = self.unigramCounts[x] + 1
                if i > 0:
                    y = sentence[i - 1]
                    self.bigramCounts[y,x] = self.bigramCounts[y,x] + 1
                if i > 1:
                    z = sentence[i - 2]
                    self.trigramCounts[z,y,x] = self.trigramCounts[z,y,x] + 1
                self.total += 1
                i = i + 1

    def predict(self, bigram):
        maximumCount = 0
        maxbi = 0
        maxuni = 0
        bestWord = 'anecdote'
        amountBigram = self.bigramCounts[bigram[0], bigram[1]]

        for i in self.unigramCounts.keys():
            self.startProb[i] = (self.trigramCounts[bigram[0], bigram[1], i] / amountBigram)
        randomNum = random()
        print("random:", randomNum)
        for i in self.startProb:
            # print("random:", randomNum)
            # print("word: ", i, self.startProb[i])
            randomNum = randomNum - self.startProb[i];
            # print("random after:", randomNum)
            if randomNum <= 0:
                bestWord = i
                break


        #for i in self.unigramCounts.keys():
          #  if self.trigramCounts[bigram[0],bigram[1],i] > maximumCount:
           #     maximumCount = self.trigramCounts[bigram[0],bigram[1],i]
           #     bestWord = i
                #print(maximumCount)
                #print("best word", i)
            elif self.bigramCounts[bigram[1],i] > 0 and self.bigramCounts[bigram[1],i] > maxbi and maximumCount == 0:
                maxbi = self.bigramCounts[bigram[1], i]
                bestWord = i
            elif self.unigramCounts[i] > maximumCount and maximumCount == 0 and maxbi == 0:
                maxuni = self.unigramCounts[bigram[1], i]
                bestWord = i
        if maximumCount > 0:
            return bestWord
        elif maxbi > 0:
            return maxbi
        else:
            return maxuni

    @property
    def endofSentence(self):
        maximumCount = 0
        bestWord = 'anecdote'
        totalSentences = self.unigramCounts["<s>"]
        for i in self.unigramCounts.keys():
            self.startProb[i] = (self.bigramCounts["<s>", i]/totalSentences)
            #if self.startProb[i] > 0:
                #print("Probability: ", i, self.startProb[i])
        randomNum = random()
        print("random:", randomNum)
        for i in self.startProb:
           # print("random:", randomNum)
            #print("word: ", i, self.startProb[i])
            randomNum = randomNum - self.startProb[i];
            #print("random after:", randomNum)
            if randomNum <= 0:
                bestWord = i
                break


        #for i in self.unigramCounts.keys():
        #    if self.bigramCounts["<s>", i] > maximumCount:
        #        maximumCount = self.bigramCounts["<s>", i]
         #       bestWord = i
                #print(maximumCount)
                #print("best word", i)
        return bestWord

    def printTrigram(self):
        for i in range(100):
            print(self.trigramCounts.keys()[i])
