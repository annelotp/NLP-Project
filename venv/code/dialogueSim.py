from languageModel import languageModel
from BigCorpus import BigCorpus
import csv

class dialogueSim:

    #data = pd.read_csv()
    def __init__(data = '../data/movie-dialog-corpus/movie_lines.tsv', self=None):
        self.data = data

def main():

    with open('../data/movie-dialog-corpus/movie_lines.tsv') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        sentences = []
        for row in reader:
            sentences.append(row[-1])

    #data = '../data/movie-dialog-corpus/movie_lines.tsv'
    #corpus = BigCorpus(data)

    lm = languageModel(sentences)
    bigram = ['i', 'am']
    print(bigram[0], bigram[1])
    for i in range(10):
        nextword = lm.predict(bigram)
        print(nextword)
        bigram = [bigram[1], nextword]
        print(bigram[0], bigram[1])

if __name__ == "__main__":
    main()