import sys
import os
import json
import re
import operator
import TwitterScraper
import IPython

class TweetClusterer(object):
    """This class will allow manipulation of aggregated tweets."""

    def __init__(self):
        pass


    def getBulkCorpus(self):
        file_list =  os.listdir("./data/alltweets/")
        self.bulk_corpus = []
        for i in range(len(file_list)):
            if file_list[i].endswith('.json'):
                self.bulk_corpus += json.load(open('data/alltweets/' + file_list[i], 'rb'))
        self.corpus = self.bulk_corpus

    def getCorpus(self,corpus_name):
        self.corpus = json.load(open('data/alltweets/' + corpus_name + '.json', 'rb'))

    def cleanCorpus(self):
        self.corpus_text = [self.corpus[i]['text'] for i in range(len(self.corpus))]
        self.stripUsers()


    def makeWordCountTuples(self):
        self.splitCorpusToWords()
        self.words_tuple = sorted(self.word_dict.iteritems(), key=operator.itemgetter(1))
        self.words_tuple.reverse()
        return self.words_tuple


    def stripUsers(self):
        pattern = re.compile('@[\w]+')
        for i in range(len(self.corpus_text)):
            self.corpus_text[i] = re.sub(pattern,"",self.corpus_text[i])


    def splitCorpusToWords(self):
        self.word_dict = {}
        for i in range(len(self.corpus)):
            word_list = self.corpus_text[i].split()
            for word in word_list:
                word = word.strip('#/\.-!?')
                if word not in self.word_dict:
                    self.word_dict[word] = 1
                else:
                    self.word_dict[word] += 1

    def compareWordCountTuples(self, wc1, wc2):
        similarity = []
        for i in range(min(20,len(wc2))):
            similarity.append([x[0] for x in wc1].index(wc2[i][0]))
        return similarity

if __name__ == '__main__':
    tc = TweetClusterer()
    tc.getBulkCorpus()
    tc.cleanCorpus()
    a = tc.makeWordCountTuples()
    k = TweetClusterer()
    k.getCorpus('karate')
    k.cleanCorpus()
    b = k.makeWordCountTuples()
    sim = tc.compareWordCountTuples(a,b)
    print tc.words_tuple[:20]
    print k.words_tuple[:20]
    print sim
