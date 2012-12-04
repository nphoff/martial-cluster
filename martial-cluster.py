from lib.TwitterScraper import TwitterScraper
from lib.TweetClusterer import TweetClusterer
import pylab
import sys
import IPython

#Master list of martial arts used.  Add things here if curious.
martial_arts = ['karate', 'taekwondo', 'haidonggumdo', 'dambe', 'jitsu', 'capoeira', 'kenpo', 'kickboxing', 'jeetkunedo', 'kungfu', 'taichi', 'aikido', 'judo', 'kendo', 'ninjutsu', 'hapkido', 'muaythai']


def fullScrape():
    ts = TwitterScraper()
    for ma in martial_arts:
        print("Scraping Twitter for hashtags of %s" % ma)
        ts.scrapeSearch(ma)
        ts.saveScrape()
        ts.data = []

def userList():
    ts = TwitterScraper()
    for ma in martial_arts:
        print("Generating user lists for %s" % ma)
        ts.generateUserList(ma)
        ts.saveUserList(ma)
        print("Found %d users for %s" % (len(ts.userList), ma))
        ts.userList = []

def getAllUserTweets():
    ts = TwitterScraper()
    for ma in martial_arts:
        ts.getBroadUserTweets(ma)
        ts.saveBroadUserTweets(ma)

def compareWordPopularity():
    bulk = TweetClusterer()
    bulk.getBulkCorpus()
    bulk.cleanCorpus()
    bulk_words = bulk.makeWordCountTuples()
    comparison_vectors = []
    legend = []
    for ma in martial_arts:
        tmp = TweetClusterer()
        tmp.getCorpus(ma)
        tmp.cleanCorpus()
        tmp_words = tmp.makeWordCountTuples()
        sim = bulk.compareWordCountTuples(bulk_words, tmp_words)
        comparison_vectors.append(sim)
        legend.append(ma)
    #plotting
    for vec in comparison_vectors:
        if vec == []:
            continue
        else:
            a = pylab.plot(vec)
            pylab.hold(True)
            pylab.legend([a], [ma])
    IPython.embed()
    pylab.show()
if __name__ == '__main__':
    if len(sys.argv) > 2:
        sys.exit("Error, received too many input arguments.")
    elif len(sys.argv) < 2:
        sys.exit("""Error, usage is: python martial-cluster.py command
where command is one of the following:
    s or scrape (scrape of Twitter data for all martial arts)
    u or userlist (generate user lists)
    a or allusertweets (collects all tweets from all users found)""")

    options = {'s' : fullScrape,
               'scrape': fullScrape,
               'u': userList,
               'userlist': userList,
               'a': getAllUserTweets,
               'allusertweets': getAllUserTweets,
               'c': compareWordPopularity,
               'compare': compareWordPopularity}

    if sys.argv[1] in options:
        options[sys.argv[1]]()
    
