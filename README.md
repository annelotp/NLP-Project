# NLP-Project: Dialogue Generation

The dialogue simulator will produce a text word by word. When selecting the next word in a sentence, various strategies can be applied. The strategies implemented are "Sampling" which chooses a next word according to its probability, "Greedy" which always chooses the word with the highest probability and "BeamSearch" which creates a shortlist of the most probable words and then recalculates the probability once a few more words have been added and chooses the optimal one. The question to be answered is which of these approaches generates the best dialogues according to the following criteria: correct grammar, understandability and sentence diversity.

## Score
```bash
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
```
## Greedy
```bash
    def greedy(self, probability):
        maximumCount = 0
        for i in probability:
            if probability[i] > maximumCount:
                maximumCount = probability[i]
                bestWord = i
        return bestWord
```
### Output example 1:
```bash
Starting from "i want to get"
Speaker 1: i want to get out of here 
Speaker 2: i dont know 
Speaker 1: i dont know 
Speaker 2: i dont know 
Speaker 1: i dont know 
Speaker 2: i dont know 
```
### Output example 2:
```bash
Starting from "i love you and"
Speaker 1: i love you and i want to be a good one
Speaker 2: shut up
Speaker 1: you know what i mean
Speaker 2: the only thing i know is that i cant go to the bathroom
Speaker 1: did you see that
Speaker 2: i dont know
Speaker 1: you know what i mean
Speaker 2: hey
Speaker 1: yes
Speaker 2: big deal
Speaker 1: i don’t know
Speaker 2: im not sure i can do this
Speaker 1: what
Speaker 2: we have to get out of here
Speaker 1: and you know what i mean
Speaker 2: id like to see you
Speaker 1: thanks
```
## Sampling
```bash
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
```
### Output:
```bash
Starting from "i want to get"
Speaker 1: i want to get too much attention theres you and youre entitled to worry
Speaker 2: him wid one fierce flash of me eyes mister can you visit part and an audience - theres no company no fortune you owe me uri one last push
Speaker 1:
Speaker 2: the bellboy looks puzzled
Speaker 1: chance of the old days the sand pit in back of the south latrine 
Speaker 2: pain on this his office back of st mikes hes our psychiatric type of your business thats for sure
Speaker 1: i you okay
Speaker 2: because that is what
Speaker 1: to get out
```

## Beam Search
![Beam Search](https://github.com/annelotp/NLP-Project/blob/master/venv/report%20%2B%20pitch/beamSearch-2.png)
```bash
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
```
### Output example 1:
```bash
Starting from "how are you doing"
Speaker 1: how are you doing
Speaker 2: take it easy now dont want me to go back to the hospital
Speaker 1: sure i dont know
Speaker 2: gustafsons what do you think
Speaker 1: umm i dont know what youre talking to me
Speaker 2: he is a good idea 
Speaker 1: no no no no i dont want you to be happy 
Speaker 2: thank god for you faith i think i know what you mean
Speaker 1: you know what i want to talk about it 
```
### Output example 2:
```bash
Starting from "i wonder how the"
Speaker 1: i wonder how the wars going
Speaker 2: have to do is get in my bed and then the big papa bear he roared and somebodys been sleeping in my bed and then the big papa bear he roared and somebodys been sleeping in my bed and then the big papa bear he
```
## Conclusion
The greedy algorithm, when given a first word decided by sampling selection, produces well understandable conversations. However it lacks diversity and falls into repetitiveness after a certain while. The sampling strategy performs poorly because of its struggle to produce grammatically sound sentences. Although the beam search algorithm performs the best overall; when considering grammar, uniqueness and consistency; it performs worse than initially expected. Further improvements to the program could be implementing seq2seq, however given the time restrictions this was not possible.
