from __future__ import division
import math, collections
from random import random


class languageModel:

    def __init__(self, corpus):
        self.unigramCounts = collections.defaultdict(lambda: 0)
        self.bigramCounts = collections.defaultdict(lambda: 0)
        self.trigramCounts = collections.defaultdict(lambda: 0)
        self.fourgramCounts = collections.defaultdict(lambda: 0)
        self.fivegramCounts = collections.defaultdict(lambda: 0)
        self.startProb = collections.defaultdict(lambda: 0)
        self.scoreFive = collections.defaultdict(lambda: 0)
        self.scoreFour = collections.defaultdict(lambda: 0)
        self.scoreThree = collections.defaultdict(lambda: 0)
        self.scoreTwo = collections.defaultdict(lambda: 0)
        self.scoreOne = collections.defaultdict(lambda: 0)

        self.total = 0
        self.train(corpus)

    def train(self, corpus):
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

    def score(self, fourgram):
        amountFourgram = max(self.fourgramCounts[fourgram[0], fourgram[1], fourgram[2], fourgram[3]], 1)
        amountTrigram = max(self.trigramCounts[fourgram[1], fourgram[2], fourgram[3]],1)
        amountBigram = max(self.bigramCounts[fourgram[2], fourgram[3]],1)
        amountUnigram = max(self.unigramCounts[fourgram[3]],1)
        probability = collections.defaultdict(lambda: 0)

        for i in self.unigramCounts.keys():
            self.scoreFive[i] = (self.fivegramCounts[fourgram[0], fourgram[1], fourgram[2], fourgram[3], i] / amountFourgram)
            self.scoreFour[i] = (self.fourgramCounts[fourgram[1], fourgram[2], fourgram[3], i] / amountTrigram)
            self.scoreThree[i] = (self.trigramCounts[fourgram[2], fourgram[3], i] / amountBigram)
            self.scoreTwo[i] = (self.bigramCounts[fourgram[3], i] / amountUnigram)
            self.scoreOne[i] = (self.unigramCounts[i]/self.total)
            probability[i] = 0.4*self.scoreFive[i] + 0.3*self.scoreFour[i] + 0.2*self.scoreThree[i] + 0.07*self.scoreTwo[i] +0.03*self.scoreOne[i]
        return probability

    def greedy(self, probability):
        maximumCount = 0
        for i in probability:
            if probability[i] > maximumCount:
                maximumCount = probability[i]
                bestWord = i
        return bestWord

    def sampling(self, probability):
        totalValue = 0
        for i in probability:
            totalValue = totalValue + probability[i]
        randomNum = random()*totalValue
        for i in probability:
            randomNum = randomNum - probability[i];
            if randomNum <= 0:
                bestWord = i
                break
        return bestWord

    def beamSearch(self, fourgram, probability):
        bestWords = self.extendTree(self.score(fourgram))
        nodes = [[0,0,0],[0,0,0],[0,0,0]]
        nodes[0] = self.extendTree(self.score([fourgram[1],fourgram[2],fourgram[3], bestWords[0]]))
        nodes[1] = self.extendTree(self.score([fourgram[1],fourgram[2],fourgram[3], bestWords[1]]))
        nodes[2] = self.extendTree(self.score([fourgram[1],fourgram[2],fourgram[3], bestWords[2]]))
        scores = [0,0,0]

        if bestWords[0] == '</s>' and self.score([fourgram[1],fourgram[2],fourgram[3], bestWords[0]])>0.6:
            return bestWords[0]

        for k in range(3):
            for l in range(3):
                scores[k] = scores[k] + 3*self.fivegramCounts[fourgram[1], fourgram[2], fourgram[3], bestWords[k], nodes[k][l]] + 2*self.fourgramCounts[fourgram[2], fourgram[3], bestWords[k], nodes[k][l]] + self.trigramCounts[fourgram[3], bestWords[k], nodes[k][l]]
                #print("Score: ", k, scores[k])

        maximum = max(scores[0],scores[1],scores[2])

        if maximum == scores[0]:
            return bestWords[0]
        elif maximum == scores[1]:
            return bestWords[1]
        else: return bestWords[2]

    def extendTree(self, probability):
        bestWords = ['anecdote', 'anecdote', 'anecdote']
        for i in probability:
            if probability[i] > probability[bestWords[2]]:
                if probability[i] > probability[bestWords[1]]:
                    if probability[i] > probability[bestWords[0]]:
                        bestWords[2] = bestWords[1]
                        bestWords[1] = bestWords[0]
                        bestWords[0] = i
                    else:
                        bestWords[2] = bestWords[1]
                        bestWords[1] = i
                else:
                    bestWords[2] = i
        return bestWords

    @property
    def endofSentence(self):
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

        return bestWord

    def printTrigram(self):
        for i in range(100):
            print(self.trigramCounts.keys()[i])
