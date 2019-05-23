class corpus:
    sentences = []


    def processLine(self, line):
        #delete all the punctuation marks
        line = line.strip()
        line = line.lower()
        line = line.replace('"', '')
        line = line.replace('?', '')
        line = line.replace(',', '')
        line = line.replace('.', '')
        line = line.replace('!', '')
        line = line.replace("'", '')
        line = line.replace(":", '')
        line = line.replace(";", '')
        if line == '':
            return None
        self.words = []
        tokens = line.split()
        if (type(tokens) == type([])):
            self.words.append("<s>")
            for i in tokens:
                self.words.append(i)
            self.words.append("</s>")

            self.sentences.append(self.words)



    def read_corpus(self, corpus):
        self.corpus = corpus
        for line in corpus:
            self.processLine(line)