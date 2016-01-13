##
## feedmgr.py
## ljheidel@noozjunkie.com
##
import requests
import json
import collector_config
import os
import sys
import logging
from .restcall import RestCall
from noozjunkie_collector import rest,log,stats

## 
## Manage feeds
##
class FeedMgr:

    def __init__(self):
        self.initFeeds()

    ## 
    ## Read feeds from a local json file, check to see if each feed exists
    ## if it doesn't, add it.
    ##
    def initFeeds(this):
        log.info('Reading feeds file %s' % (collector_config.FEEDS_FILE))
        with open(collector_config.FEEDS_FILE) as feeds_file:
            feeds = json.load(feeds_file)
            for feed in feeds:
                this.addFeed(feed['title'], feed['source'], "", feed['type'], feed['interval'], feed['active'])

    ##
    ## Check the API to see if the feed exists, if not, add it.
    ##
    def addFeed(this, title, source, description="", type=2, interval=300, active=0):
        if this.feedExists(title) == False:
            log.warn("Adding type %s feed %s to be retrieved from %s to API server." % (type, title, source))
            data = { 'title': title, 'source': source, 'type': type, 'interval': interval, 'active': active }
            response = None
            try:
                response = rest.doPost("feed", data)
                return response
            except:
                log.error("Error adding feed %s to API server." % (feed))
                raise Exception()
                return False

    ##
    ## Check to see if a feed exists on the API server.
    ##
    def feedExists(this, title):
        log.debug("Checking to see if feed %s exists on API server." % (title)) 
        filters = [dict(name='title', op='equals', val=title)]
        try: 
            response = rest.doGet("feed", filters)
            if response.json()['num_results'] != 0:
                return True
            else:
                return False
        except:
            log.error("Error checking to see if feed %s exists on API server." % (title))
            raise Exception()
            return True

    ## 
    ## Get the list of feeds from the API server
    ##
    def getFeeds(this):
        log.info("Retreiving list of feeds from API server.")
        response = ""
        try:
            response = rest.doGet("feed")
            return response.json()['objects']
        except:
            log.error("Error retreiving list of feeds from API server.")
            raise Exception() 
            return False
