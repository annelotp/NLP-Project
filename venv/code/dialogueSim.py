from languageModel import languageModel
from BigCorpus import BigCorpus
from corpus import corpus
import csv

class dialogueSim:

    #data = pd.read_csv()
    def __init__(data = '../data/movie-dialog-corpus/movie_lines.tsv', self=None):
        self.data = data

def main():
    print("main started")
    with open('../data/movie-dialog-corpus/movie_lines.tsv') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        dialogues = []
        for row in reader:
            dialogues.append(row[-1])

    #data = '../data/movie-dialog-corpus/movie_lines.tsv'
    #corpus = BigCorpus(data)
    corp = corpus()
    corp.read_corpus(dialogues)

    lm = languageModel(corp)

    #methods = ['greedy', 'sampling', 'beamSearch']
    methods = ['beamSearch']
    for method in methods:
        print("Method: ", method)
        conversation = []
        sentence = []
        #no capital letters!
        fourgram = ['how', 'are', 'you', 'doing']
        for i in fourgram:
            sentence.append(i)
        print(sentence)
        n = 1
        while n < 10:
            if fourgram[3] == "</s>" :
                n = n+1
                conversation.append(sentence)
                sentence = []
                nextword = lm.endofSentence
                sentence.append(nextword)
                #print("New senctence: ", nextword)
                #fourgram = [fourgram[3], "</s>", "<s>", nextword]
                fourgram = [fourgram[1], fourgram[2], fourgram[3], nextword]

            else:
                nextword = lm.score(fourgram, method)
                sentence.append(nextword)
                #print(nextword)
                fourgram = [fourgram[1], fourgram[2],fourgram[3],nextword]
        conversation.append(sentence)
        #print("hi there we should print the full convo now", conversation.__len__())
        speaker = ["Speaker 1:", "Speaker 2:"]
        for q, sent in enumerate(conversation):
            #print(q)
            #print(sent)
            speak(speaker[q%2], sent)


def speak(speaker, sentence):
    sentence.insert(0,speaker)
    text= " ".join(sentence)
    print(text)

if __name__ == "__main__":
    main()