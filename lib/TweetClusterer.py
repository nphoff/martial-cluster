import sys
import os
import json
import TwitterScraper

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
        print len(self.bulk_corpus)
        print self.bulk_corpus[1]

    def cleanBulkCorpus(self):
        self.bulk_text = [self.bulk_corpus[i]['text'] for i in range(len(self.bulk_corpus))]
        
    def stripUsers(self):
        for i in range(len(self.bulk_text)):
            

if __name__ == '__main__':
    tc = TweetClusterer()
    tc.getBulkCorpus()
