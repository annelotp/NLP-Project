from languageModel import languageModel
from BigCorpus import BigCorpus
class dialogueSim:

    #data = pd.read_csv()
    def __init__(data = '../data/tagged-train2.dat'):
        self.data = data

def main():
    data = '../data/tagged-train2.dat'
    corpus = BigCorpus(data)

    lm = languageModel(corpus)
    bigram = ['i', 'am']
    print(bigram[0], bigram[1])
    for i in range(10):
        nextword = lm.predict(bigram)
        print(nextword)
        bigram = [bigram[1], nextword]
        print(bigram[0], bigram[1])

if __name__ == "__main__":
    main()