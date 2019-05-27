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
    #no capitals!!!
    conversation = []
    sentence = []
    fourgram = ['i', 'love', 'you', 'and']
    for i in fourgram:
        sentence.append(i)
    for i in range(200):
        if fourgram[3] == "</s>" :
            conversation.append(sentence)
            sentence = []
            nextword = lm.endofSentence
            sentence.append(nextword)
            #print("New senctence: ", nextword)
            fourgram = [fourgram[3], "</s>", "<s>", nextword]
        else:
            nextword = lm.predict(fourgram)
            sentence.append(nextword)
           # print(nextword)
            fourgram = [fourgram[1], fourgram[2],fourgram[3],nextword]
            #print(bigram[0], bigram[1])

    speaker = ["Speaker 1:", "Speaker 2:"]
    for i,sent in enumerate(conversation):
        speak(speaker[i%2], sent)
    print("finished main")
    return

def speak(speaker, sentence):
    ("speak started")
    sentence.insert(0,speaker)
    text= " ".join(sentence)
    ("finished speak")
    return text

if __name__ == "__main__":
    main()