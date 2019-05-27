from __future__ import division
import math, collections
from random import seed
from random import random


class languageModel:

    def __init__(self, corpus):
        """Initialize your data structures in the constructor."""
        self.unigramCounts = collections.defaultdict(lambda: 0)
        self.bigramCounts = collections.defaultdict(lambda: 0)
        self.trigramCounts = collections.defaultdict(lambda: 0)
        self.fourgramCounts = collections.defaultdict(lambda: 0)
        self.fivegramCounts = collections.defaultdict(lambda: 0)

        self.scoreFive = collections.defaultdict(lambda: 0)
        self.scoreFour = collections.defaultdict(lambda: 0)
        self.scoreThree = collections.defaultdict(lambda: 0)
        self.scoreTwo = collections.defaultdict(lambda: 0)
        self.scoreOne = collections.defaultdict(lambda: 0)
        self.probability = collections.defaultdict(lambda: 0)

        self.startProb = collections.defaultdict(lambda: 0);
        self.total = 0
        self.train(corpus)
        #self.printTrigram()

    def train(self, corpus):
        """ Takes a corpus and trains your language model.
            Compute any counts or other corpus statistics in this function.
        """
        print("train started")
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
                if i > 2:
                    w = sentence[i-3]
                    self.fourgramCounts[w,z,y,x] = self.fourgramCounts[w,z,y,x] + 1
                if i > 3:
                    v = sentence[i-4]
                    self.fivegramCounts[v,w,z,y,x] = self.fivegramCounts[v,w,z,y,x] + 1
                self.total += 1
                i = i + 1
        print("train finished")

    def predict(self, fourgram):
        print("predict started")
        maximumCount = 0
        maxbi = 0
        maxuni = 0
        bestWord = 'anecdote'
        amountFourgram = max(self.fourgramCounts[fourgram[0], fourgram[1], fourgram[2], fourgram[3]], 1)
        amountTrigram = max(self.trigramCounts[fourgram[1], fourgram[2], fourgram[3]],1)
        amountBigram = max(self.bigramCounts[fourgram[2], fourgram[3]],1)
        amountUnigram = max(self.unigramCounts[fourgram[3]],1)

        for i in self.unigramCounts.keys():
            self.scoreFive[i] = (self.fivegramCounts[fourgram[0], fourgram[1], fourgram[2], fourgram[3], i] / amountFourgram)
            self.scoreFour[i] = (self.fourgramCounts[fourgram[1], fourgram[2], fourgram[3], i] / amountTrigram)
            self.scoreThree[i] = (self.trigramCounts[fourgram[2], fourgram[3], i] / amountBigram)
            self.scoreTwo[i] = (self.bigramCounts[fourgram[3], i] / amountUnigram)
            self.scoreOne[i] = (self.unigramCounts[i]/self.total)
            self.probability[i] = 0.4*self.scoreFive[i] + 0.3*self.scoreFour[i] + 0.2*self.scoreThree[i] + 0.07*self.scoreTwo[i] +0.03*self.scoreOne[i]
        #print("random:", randomNum)
        totalValue = 0
        maximumCount = 0
        for i in self.probability:
            #totalValue = totalValue + self.probability[i]
            if self.probability[i] > maximumCount:
                maximumCount = self.probability[i]
                bestWord = i
       # randomNum = random()*totalValue


        # for i in self.probability:
        #     # print("random:", randomNum)
        #     #print("word: ", i, self.probability[i])
        #     randomNum = randomNum - self.probability[i];
        #     #print("random after:", randomNum)
        #     if randomNum <= 0:
        #         bestWord = i
        #         break
        print("predict finished")
        return bestWord

        #for i in self.unigramCounts.keys():
          #  if self.trigramCounts[bigram[0],bigram[1],i] > maximumCount:
           #     maximumCount = self.trigramCounts[bigram[0],bigram[1],i]
           #     bestWord = i
                #print(maximumCount)
                #print("best word", i)
           # elif self.bigramCounts[bigram[1],i] > 0 and self.bigramCounts[bigram[1],i] > maxbi and maximumCount == 0:
           #     maxbi = self.bigramCounts[bigram[1], i]
           #     bestWord = i
           # elif self.unigramCounts[i] > maximumCount and maximumCount == 0 and maxbi == 0:
           #     maxuni = self.unigramCounts[bigram[1], i]
            #    bestWord = i
       # if maximumCount > 0:
       #     return bestWord
       # elif maxbi > 0:
       #     return maxbi
       # else:
        #    return maxuni

    @property
    def endofSentence(self):
        print("started endofSentence")
        maximumCount = 0
        bestWord = 'anecdote'
        totalSentences = self.unigramCounts["<s>"]
        for i in self.unigramCounts.keys():
            self.startProb[i] = (self.bigramCounts["<s>", i]/totalSentences)
        randomNum = random()
        for i in self.startProb:
            randomNum = randomNum - self.startProb[i];
            if randomNum <= 0:
                bestWord = i
                break


        #for i in self.unigramCounts.keys():
        #    if self.bigramCounts["<s>", i] > maximumCount:
        #        maximumCount = self.bigramCounts["<s>", i]
         #       bestWord = i
                #print(maximumCount)
                #print("best word", i)
        print("finished endofSentence")
        return bestWord

    def printTrigram(self):
        for i in range(100):
            print(self.trigramCounts.keys()[i])
