from languageModel import languageModel
from corpus import corpus
import csv

class dialogueSim:


    def __init__(data = '../data/movie-dialog-corpus/movie_lines.tsv', self=None):
        self.data = data

def main():
    print("main started")
    with open('../data/movie-dialog-corpus/movie_lines.tsv') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        dialogues = []
        for row in reader:
            dialogues.append(row[-1])

    corp = corpus()
    corp.read_corpus(dialogues)

    lm = languageModel(corp)

    methods = ['greedy', 'sampling', 'beamSearch']
    for method in methods:
        print("Method: ", method)
        conversation = []
        sentence = []
        #no capital letters!
        fourgram = ['how', 'much', 'do', 'we']
        for i in fourgram:
            sentence.append(i)
        print(sentence)
        n = 1
        while n < 6:
            if fourgram[3] == "</s>" :
                n = n+1
                conversation.append(sentence)
                sentence = []
                nextword = lm.endofSentence
                sentence.append(nextword)
                print("New senctence: ", nextword)
                fourgram = [fourgram[1], fourgram[2], fourgram[3], nextword]

            else:
                if method == 'greedy':
                     nextword = lm.greedy(lm.score(fourgram))
                elif method == 'sampling':
                    nextword = lm.sampling(lm.score(fourgram))
                else:
                    nextword = lm.beamSearch(fourgram, lm.score(fourgram))
                sentence.append(nextword)
                print(nextword)
                fourgram = [fourgram[1], fourgram[2],fourgram[3],nextword]
        conversation.append(sentence)
        speaker = ["Speaker 1:", "Speaker 2:"]
        for q, sent in enumerate(conversation):
            speak(speaker[q%2], sent)


def speak(speaker, sentence):
    sentence.insert(0,speaker)
    text= " ".join(sentence)
    print(text)

if __name__ == "__main__":
    main()