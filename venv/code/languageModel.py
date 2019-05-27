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

    def score(self, fourgram, method):
        #print("predict started")
        maximumCount = 0
        maxbi = 0
        maxuni = 0
        bestWord = 'anecdote'
        amountFourgram = max(self.fourgramCounts[fourgram[0], fourgram[1], fourgram[2], fourgram[3]], 1)
        amountTrigram = max(self.trigramCounts[fourgram[1], fourgram[2], fourgram[3]],1)
        amountBigram = max(self.bigramCounts[fourgram[2], fourgram[3]],1)
        amountUnigram = max(self.unigramCounts[fourgram[3]],1)

        for i in self.unigramCounts.keys():
            if i == '<\s>':
                print("Lalalalal", i)
            self.scoreFive[i] = (self.fivegramCounts[fourgram[0], fourgram[1], fourgram[2], fourgram[3], i] / amountFourgram)
            self.scoreFour[i] = (self.fourgramCounts[fourgram[1], fourgram[2], fourgram[3], i] / amountTrigram)
            self.scoreThree[i] = (self.trigramCounts[fourgram[2], fourgram[3], i] / amountBigram)
            self.scoreTwo[i] = (self.bigramCounts[fourgram[3], i] / amountUnigram)
            self.scoreOne[i] = (self.unigramCounts[i]/self.total)
            self.probability[i] = 0.4*self.scoreFive[i] + 0.3*self.scoreFour[i] + 0.2*self.scoreThree[i] + 0.07*self.scoreTwo[i] +0.03*self.scoreOne[i]
        if method == 'greedy':
            return self.greedy()
        elif method == 'sampling':
            return self.sampling()
        else:
            return self.beamSearch(fourgram)

    def greedy(self):
        maximumCount = 0
        for i in self.probability:
            if i == '<\s>':
                print("GAGAGAGAGAGA", i)
            if self.probability[i] > maximumCount:
                maximumCount = self.probability[i]
                bestWord = i
        return bestWord

    def sampling(self):
        totalValue = 0
        for i in self.probability:
            totalValue = totalValue + self.probability[i]
        randomNum = random()*totalValue
        for i in self.probability:
            # print("random:", randomNum)
            #print("word: ", i, self.probability[i])
            randomNum = randomNum - self.probability[i];
            if randomNum <= 0:
                bestWord = i
                break
        return bestWord

    def beamSearch(self, fourgram):
        bestWords = ['anecdote', 'anecdote', 'anecdote']
        phrase1 = [' ', ' ']
        phrase2 = [' ', ' ']
        phrase3 = [' ', ' ']
        scores=[0,0,0]
        for i in self.probability:
            if i == '<\s>':
                print("Yayayaya", i)
            if self.probability[i] > self.probability[bestWords[2]]:
                if self.probability[i] > self.probability[bestWords[1]]:
                    if self.probability[i] > self.probability[bestWords[0]]:
                        bestWords[1] = bestWords[0]
                        bestWords[2] = bestWords[1]
                        bestWords[0] = i
                    else:
                        bestWords[2] = bestWords[1]
                        bestWords[1] = i
                else:
                    bestWords[2] = i
        #evaluate first word
        phrase1[0] = self.score([fourgram[1], fourgram[2], fourgram[3], bestWords[0]], 'greedy')
        phrase1[1] = self.score([fourgram[2], fourgram[3], bestWords[0], phrase1[0]], 'greedy')

        # evaluate second word
        phrase2[0] = self.score([fourgram[1], fourgram[2], fourgram[3], bestWords[1]], 'greedy')
        phrase2[1] = self.score([fourgram[2], fourgram[3], bestWords[1], phrase2[0]], 'greedy')

        # evaluate first word
        phrase3[0] = self.score( [fourgram[1], fourgram[2], fourgram[3], bestWords[2]], 'greedy')
        phrase3[1] = self.score( [fourgram[2], fourgram[3], bestWords[2], phrase3[0]], 'greedy')

        scores[0] = 3*self.fivegramCounts[fourgram[1], fourgram[2], fourgram[3], bestWords[0], phrase1[0]] + 3*self.fivegramCounts[fourgram[2], fourgram[3], bestWords[0], phrase1[0], phrase1[1]] + 2*self.fourgramCounts[fourgram[2], fourgram[3], bestWords[0], phrase1[0]] + 2*self.fourgramCounts[fourgram[3], bestWords[0], phrase1[0], phrase1[1]] + self.trigramCounts[ fourgram[3], bestWords[0], phrase1[0]] + self.trigramCounts[bestWords[0], phrase1[0], phrase1[1]]
        scores[1] = 3*self.fivegramCounts[fourgram[1], fourgram[2], fourgram[3], bestWords[1], phrase2[0]] + 3*self.fivegramCounts[fourgram[2], fourgram[3], bestWords[1], phrase2[0], phrase2[1]] + 2*self.fourgramCounts[fourgram[2], fourgram[3], bestWords[1], phrase2[0]] + 2*self.fourgramCounts[fourgram[3], bestWords[1], phrase2[0], phrase2[1]] + self.trigramCounts[ fourgram[3], bestWords[1], phrase2[0]] + self.trigramCounts[bestWords[1], phrase2[0], phrase2[1]]
        scores[2] = 3*self.fivegramCounts[fourgram[1], fourgram[2], fourgram[3], bestWords[2], phrase3[0]] + 3*self.fivegramCounts[fourgram[2], fourgram[3], bestWords[2], phrase3[0], phrase3[1]] + 2*self.fourgramCounts[fourgram[2], fourgram[3], bestWords[2], phrase3[0]] + 2*self.fourgramCounts[fourgram[3], bestWords[2], phrase3[0], phrase3[1]] + self.trigramCounts[ fourgram[3], bestWords[2], phrase3[0]] + self.trigramCounts[bestWords[2], phrase3[0], phrase3[1]]

        maximum = max(scores[0],scores[1],scores[2])

        if maximum == scores[0]:
            return bestWords[0]
        elif maximum == scores[1]:
            return bestWords[1]
        else: return bestWords[2]

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
