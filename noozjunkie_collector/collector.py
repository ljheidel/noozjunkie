##
## collector.py
## ljheidel@noozjunkie.com
##
import collector_config
import feedparser
import praw
import newspaper
import nltk
import datetime
import hashlib
import requests
import json
import dateutil
from noozjunkie_collector import rest,log,stats

nltk.download('punkt')

##
## Create an object that serves as the data collector.  It will
## hold all of the article data.
##
class Collector:

    articles = []

    ##
    ## Process the feeds that come in as JSON.  Dole them out
    ## to various functions for processing based on the type field 
    ## of the record.
    ##
    def processFeeds(self, feeds):
        stats.feeds_total=len(feeds)
        for feed in feeds:
            do_it_again = 0
            try:
                do_it_again = int(dateutil.parser.parse(feed['retrieved']).strftime("%s")) + int(feed['interval'])
            except: 
                do_it_again = 0
            if feed['active'] == 1 and do_it_again < datetime.datetime.utcnow().timestamp():
                ##
                ## Time update needs to happen at the beginning of the run to minimize 
                ## the possibility race condition when muliple collector jobs
                ## are scheduled.
                ##
                self.setFeedRetrieved(feed['id'], str(datetime.datetime.utcnow()))
                log.info("processing feed %s" % (feed['title']))
                if feed['type'] == 0:
                    self.processRSS(feed['id'], feed['source'])
                elif feed['type'] == 1:
                    self.processReddit(feed['id'], feed['source'])
                else:
                    self.processGeneric(feed['id'], feed['source'])
                stats.feeds_processed += 1

    ##
    ## Process an RSS feed append the articles to the articles array 
    ## as ArticleData objects.
    ##
    def processRSS(self, feedid, url):
        d = feedparser.parse(url)
        for item in d['items']:
            log.info('retreiving %s' % item.title)
            self.articles.append(ArticleData(feedid, item.title, item.link, item.description, item.published))

    ## 
    ## Process a reddit feed (subreddit)
    ##
    def processReddit(self, feedid, subreddit):
        r = praw.Reddit(collector_config.USER_AGENT)
        sr = r.get_subreddit(subreddit)
    
        for item in sr.get_new():
            log.info('retreiving %s' % item.title)
            self.articles.append(ArticleData(feedid, item.title, item.url, item.selftext, str(datetime.datetime.utcfromtimestamp(item.created))))
        
        for item in sr.get_hot():
            log.info('retreiving %s' % item.title)
            self.articles.append(ArticleData(feedid, item.title, item.url, item.selftext, str(datetime.datetime.utcfromtimestamp(item.created))))

        for item in sr.get_top():
            log.info('retreiving %s' % item.title)
            self.articles.append(ArticleData(feedid, item.title, item.url, item.selftext, str(datetime.datetime.utcfromtimestamp(item.created))))

    ## 
    ## Process a generic feed (web page)
    ##
    def processGeneric(self, feedid, url):
        p = newspaper.build(url)
        for a in p.articles:
            a.download()
            log.info('retreiving %s' % a.title)
            self.articles.append(ArticleData(feedid, a.title, a.url, "", str(datetime.datetime.utcnow())))
    ##
    ## Return the 'retrieved' field from the feed record indicating the last time
    ## the feed was processed.
    ##
#   def getFeedRetrieved(self, feedid):
#       filters = [dict(name='id', op='equals', val=feedid)]
#       params = dict(q=json.dumps(dict(filters=filters)))
#       headers = {'Content-Type': 'application/json', 'user-agent': collector_config.USER_AGENT }
#       url = "%s/api/feed" % (collector_config.API_BASE_URL)
#       response = None
#       try:
#           response = requests.get(url, headers=headers, params=params)
#           assert response.status_code == 200
#       except AssertionError as e:
#           logging.error(e)
#       if response.json()['num_results'] != 0:
#           r = response.json()['objects'].pop()
#           return r['retrieved']
#       else:
#
#           return False

    def getFeedRetrieved(self, feedid):
        log.debug("Checking when feed %s last retreived." % (feedid))
        filters = [dict(name='id', op='equals', val=feedid)]
        response = None
        try: 
            response = rest.doGet(filters)
            if response.json()['num_results'] != 0:
                r = response.json()['objects'].pop()
                log.info("Feed %s last retreived %s" % (feedid, r['retrieved']))
                return r['retrieved'] 
            else:
                log.info("No retreived timestamp for %s" % (feedid))
                return False
        except Exception as e:
            log.exception(e)
            raise Exception()
            return None

    ## 
    ## Set the 'retrieved' field of the feed record
    ##
#   def setFeedRetrieved(self, feedid, retrieved):
#       filters = [dict(name='id', op='equals', val=feedid)]
#       data = json.dumps(dict(q=dict(filters=filters), retrieved=retrieved))
#       headers = {'Content-Type': 'application/json', 'user-agent': collector_config.USER_AGENT }
#       url = "%s/api/feed" % (collector_config.API_BASE_URL)
#       response = None
#       try:
#           response = requests.put(url, headers=headers, data=data)
#           assert response.status_code == 200
#       except AssertionError as e:
#           logging.error(e)
#       if response.json()['num_modified'] != 0:
#           return True
#       else:
#           return False

    def setFeedRetrieved(self, feedid, retrieved):
        log.debug("Updating feed %s with last retrieved time of %s." % (feedid, retrieved))
        filters = [dict(name='id', op='equals', val=feedid)]
        data = dict(retrieved=retrieved)
        print("doput(feed, %s, %s)" % (filters, data))
        response = None
        try:
            response = rest.doPut("feed", filters, data)
        except Exception as e:
            log.error("Failed to updaste feed %s with last retrieved time of %s." % (feedid, retrieved))
            log.exception(e)
            raise Exception()
            return None
        if response.json()['num_modified'] != 0:
            log.info("Updating feed %s with last retrieved time of %s." % (feedid, retrieved))
            return True
        else:
            log.error("Failed to updaste feed %s with last retrieved time of %s." % (feedid, retrieved))
            return False
        
    ##
    ## Return the articles collected as a list
    ##
    def getArticles(self):
        return self.articles

##
## This class stores data (both content and metadata) for an article
## In addition to storage, there are functions in here which actually down-
## load the data.
##
class ArticleData:
    title = ""
    content = ""
    contenthash = ""
    keywords = ""
    feedid = ""
    link = ""
    description = ""
    published = ""
    retrieved = ""

    def __init__(self, feedid, title, link, description, published):
        self.feedid = feedid
        self.title = title
        self.link = link
        self.description = description
        self.published = published
        self.content = self.retrieveContent(self.link)
        if self.content != None:
            self.contenthash = hashlib.md5(self.content.encode('utf-8')).hexdigest()   

    ## 
    ## Use the newspaper module to grab the content from a web page
    ##
    def retrieveContent(self, link):
        try:
            a = newspaper.Article(link)
            a.download()
            a.parse()
            text = a.text
            a.nlp()
            self.keywords = a.keywords
            self.retrieved = str(datetime.datetime.utcnow())
            return a.text
        except Exception as e:
            log.error("Exception retrieving %s" % (link))
            log.exception(e)
