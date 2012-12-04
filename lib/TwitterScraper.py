import sys
import json
import requests
from keys import *

# ********** IMPORTANT **********
# - If you want to use this class, you will have to create a keys.py file
#   with the same fields with your own twitter API keys, set as globals shown
#   in the __init__ method

class TwitterScraper(object):
    """This class will allow a user to input a RESTful query, to twitter, and return the response."""

    def __init__(self):
        #importhing values from keys.py file
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.request_token_URL = request_token_URL
        self.authorize_URL = authorize_URL
        self.access_token_URL = access_token_URL
        self.callback_URL = callback_URL
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.access_level = access_level

        #other variables
        self.basic_search_URL = 'http://search.twitter.com/search.json?q='

    def basicSearch(self,query,limits = None):
        params = query
        if limits is None:
            query += '&rpp=100'
        self.response = requests.get(self.basic_search_URL + params)
        
    def scrapeSearch(self,query):
        self.query = query
        params = '%23' + self.query + '%20-rt' + '&rpp=100' + '&lang=en'
        print("Scraping data")
        self.data = []
        for i in range(1,16):
            print(".")
            r = requests.get(self.basic_search_URL + params + '&page=' + str(i))
            if (r.ok == True):
                if (r.json['results'] == []):
                    print("Reached end of input.")
                    break
                else:
                    self.data = self.data + r.json['results']

    def saveScrape(self):
        #save data into the data directory
        with open('data/raw/' + self.query + '.json', 'wb') as outfile:
            json.dump(self.data, outfile)

    def openScrape(self, query):
        with open('data/raw/' + self.query + '.json', 'rb') as infile:
            self.data = json.load(infile)

    def generateUserList(self, query):
        self.query = query
        self.openScrape(query)
        self.userList = []
        for i in range(len(self.data)):
            self.userList.append(self.data[i]['from_user'])
        temp = set(self.userList)
        self.userList = list(temp)

    def saveUserList(self,query):
        self.query = query
        with open('data/users/' + self.query + '.json', 'wb') as outfile:
            json.dump(self.userList, outfile)

    def loadUserList(self, query):
        self.query = query
        with open('data/users/' + self.query + '.json', 'rb') as infile:
            self.userList = json.load(infile)

    def getBroadUserTweets(self,query):
        self.query = query
        print("Scraping data for %s" % query)
        self.broad_data = []
        self.loadUserList(self.query)
        i = 0
        for user in self.userList:
            i = i + 1
            print("Processing user %d of %d" % (i, min(len(self.userList),100)))
            if i >= 100:
                break
            params = 'from%3A' + user + '%20-rt' + '&rpp=100' + '&lang=en'
            r = requests.get(self.basic_search_URL + params)
            if(r.ok == True):
                if(r.json['results'] == []):
                    print("No tweets for that user :(.")
                else:
                    self.broad_data = self.broad_data + r.json['results']

    def saveBroadUserTweets(self, query):
        self.query = query
        with open('data/alltweets/' + self.query + '.json', 'wb') as outfile:
            json.dump(self.broad_data, outfile)
        


if __name__ == '__main__':
    ts = TwitterScraper()
