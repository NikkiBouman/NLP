import unicodedata
import string
import re

SOS_token = 0
EOS_token = 1

class Language:
    def __init__(self):
        self.word2index = {'SOS': 0, 'EOS': 1}
        self.word2count = {}
        self.index2word = {0: 'SOS', 1: 'EOS'}
        self.n_words = 2  # Count SOS and EOS

    def addSentence(self, sentence):
        for word in sentence.split(' '):
            self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1

    def readLang(self, s):
        for index, value in s.items():
            value = normalizeString(value)
            self.addSentence(value)

    def showLang(self):
        print("Word 2 indices: ", self.index2word)
        print("Word counts: ", self.word2count)
        # print("self.word2index)

class MRLanguage:
    def __init__(self):
        self.word2index = {'sos': 0, 'eos': 1}
        self.word2count = {}
        self.index2word = {0: 'sos', 1: 'eos'}
        self.n_words = 2  # Count SOS and EOS

    def addSentence(self, sentence):
        for word in sentence.split(', '):
            self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1

    def readLang(self, s):
        for index, value in s.items():
            value = normalizeMRString(value)
            self.addSentence(value)

    def showLang(self):
        # print("Word indices: ", self.index2word)
        print("Word counts: ", self.word2count)
        print(self.word2index)



def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

def normalizeString(s):
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?_]+", r" ", s)
    return s

def normalizeMRString(s):
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r'\[[^]]*\]', r"", s) # TODO: Data in de square brackets is lost!!
    # s = re.sub(r"[\[*\]]+", r" ", s)
    return s