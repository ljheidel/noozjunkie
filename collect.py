#!flask/bin/python3
## 
## This is the data collector for noozjunkie.  It interacts with
## the REST API in the webapp to get the feeds and store the
## articles.
##
from noozjunkie_collector import log, stats
log.warning("NoozJunkie Collector trying to score...")

from noozjunkie_collector import FeedMgr, Collector, ArticleMgr

if __name__ == '__main__':
    f = FeedMgr()
    c = Collector()
    a = ArticleMgr()
    feeds = f.getFeeds()
    c.processFeeds(feeds)
    articles = c.getArticles()
    a.processArticles(articles)
    log.warning("%s feeds available, %s feeds processed, %s articles retrieved, %s articles added" % (stats.feeds_total, stats.feeds_processed, stats.articles_retreived, stats.articles_added))
    log.warning("NoozJunkie Collector is holding.  Shutting down.  Bye bye.")
