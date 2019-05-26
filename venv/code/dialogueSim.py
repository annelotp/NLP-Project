from languageModel import languageModel
from BigCorpus import BigCorpus
from corpus import corpus
import csv

class dialogueSim:

    #data = pd.read_csv()
    def __init__(data = '../data/movie-dialog-corpus/movie_lines.tsv', self=None):
        self.data = data

def main():

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
    #no capitals!!!
    bigram = ['we', 'have']
    print(bigram[0], bigram[1])
    for i in range(15):
        if "</s>" in bigram:
            nextword = lm.endofSentence
            print(nextword)
            bigram = ["<s>", nextword]
        else:
            nextword = lm.predict(bigram)
            print(nextword)
            bigram = [bigram[1], nextword]
            #print(bigram[0], bigram[1])

if __name__ == "__main__":
    main()