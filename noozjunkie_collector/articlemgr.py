##
## articlemgr.py 
## ljheidel@noozjunkie.com
##
## Handle injecting articles into the webapp via its REST API
##
import requests
import json
import collector_config
from noozjunkie_collector import rest, log

##
## This class provides functions that add articles and keywords
##
class ArticleMgr():

    ##
    ## Process articles that are passed in as a list of
    ## ArticleData objects.
    ##
    def processArticles(self, articles):
        for a in articles:
            self.addArticle(a)

    ##
    ## Add an article from an ArticleData object, checking
    ## its hash first to make sure that it's unique.  Add any
    ## keywords to the Keywords table, and add the relationships
    ## to the ArticleKeyword table.
    ##
#   def addArticle(self, article):
#       if self.articleExists(article) == False:
#           logging.info("adding article %s" % (article.title))
#           data = { "title": article.title, "link": article.link, "keywords": article.keywords, "description": article.description, "content": article.content, "contenthash": article.contenthash, "retrieved": article.retrieved, "published": article.published }
#           headers = {'Content-Type': 'application/json', 'user-agent': collector_config.USER_AGENT }
#           url = "%s/api/article" % (collector_config.API_BASE_URL)
#           response = None
#           try:
#               response = requests.post(url, headers=headers, data=json.dumps(data))
#               assert response.status_code == 201
#           except AssertionError as e:
#               logging.error(e)
#           for word in article.keywords:
#               keywordid = self.addKeyword(word)
#               self.addArticleKeyword(response.json()['id'], keywordid)
#               
#       else:
#           return False

    def addArticle(self, article):
            if self.articleExists(article) == False:
                log.info("adding article %s" % (article.title))
                data = { "title": article.title, "link": article.link, "keywords": article.keywords, "description": article.description, "content": article.content, "contenthash": article.contenthash, "retrieved": article.retrieved, "published": article.published }
                try: 
                    response = rest.doPost("article", data)
                    for word in article.keywords:
                        keywordid = self.addKeyword(word)
                        self.addArticleKeyword(response.json()['id'], keywordid)
                except Exception as e:
                    log.exception(e)
                    return None
            else:
                return False
    ##
    ## Create records in the ArticleKeyword table that tie records in
    ## the Article table to records in the Keywords table.
    ##
#   def addArticleKeyword(self, articleid, keywordid):
#       data = { "articleid": articleid, "keywordid": keywordid }
#       headers = {'Content-Type': 'application/json', 'user-agent': collector_config.USER_AGENT }
#       url = url = "%s/api/articlekeyword" % (collector_config.API_BASE_URL)
#       response = None
#       try:
#           response = requests.post(url, headers=headers, data=json.dumps(data))
#           assert response.status_code == 201
#           return(response.json()['id'])
#       except AssertionError as e:
#           logging.error(e)

    def addArticleKeyword(self, articleid, keywordid):
        data = { "articleid": articleid, "keywordid": keywordid } 
        response = None
        try:
            response = rest.doPost("articlekeyword", data)
            return(response.json()['id'])
        except Exception as e:
            log.exception(e)
            return None
            
    ##
    ## Add a keyword to the Keywords table if it doesn't exist.  If it doesn't,
    ## create the keyword record and return its id, if not
    ## return the id of the existing record in the table.
    ##
#   def addKeyword(self, word):
#       ke = self.keywordExists(word)
#       if ke == False:
#           logging.debug("adding keyword %s" % (word))
#           data = { "word": word }
#           headers = {'Content-Type': 'application/json', 'user-agent': collector_config.USER_AGENT }
#           url = "%s/api/keyword" % (collector_config.API_BASE_URL)
#           response = None
#           try:
#               response = requests.post(url, headers=headers, data=json.dumps(data))
#               assert response.status_code == 201
#           except AssertionError as e:
#               logging.error(e)
#           return(response.json()['id'])
#       else:
#           return ke
    def addKeyword(self, word):
        ke = self.keywordExists(word)
        if ke == False:
            log.debug("adding keyword %s" % (word))
            data = { "word": word }
            response = None
            try:
                response = rest.doPost("keyword", data)
            except Exception as e: 
                log.exception(e)
                return None
            return(response.json()['id'])
        else:
            return ke
            
    ##
    ## Check to see if a keyword exists, if it doesn't, False, otherwise
    ## return the ID of the keyword in the table
    ##
#   def keywordExists(this, word):
#       filters = [dict(name='word', op='equals', val=word)]
#       params = dict(q=json.dumps(dict(filters=filters)))
#       headers = {'Content-Type': 'application/json', 'user-agent': collector_config.USER_AGENT }
#       url = "%s/api/keyword" % (collector_config.API_BASE_URL)
#       response = None
#       try:
#           response = requests.get(url, headers=headers, params=params)
#           assert response.status_code == 200
#       except AssertionError as e:
#           logging.error(e)
#       if response.json()['num_results'] != 0:
#           r = response.json()['objects'].pop()
#           return r['id']
#       else:
#           return False
    def keywordExists(this, word):
        filters = [dict(name='word', op='equals', val=word)]
        response = None
        try:
            response = rest.doGet("keyword", filters)
            if response.json()['num_results'] != 0:
                return response.json()['objects'].pop()['id']
            else:
                return False
        except Exception as e:
            log.exception(e)
            return None
    ##
    ## Check to see if an article exists.
    ##
#   def articleExists(this, article):
#       filters = [dict(name='contenthash', op='equals', val=article.contenthash)]
#       params = dict(q=json.dumps(dict(filters=filters)))
#       headers = {'Content-Type': 'application/json', 'user-agent': collector_config.USER_AGENT }
#       url = "%s/api/article" % (collector_config.API_BASE_URL)
#       response = None
#       try:
#           response = requests.get(url, headers=headers, params=params)
#           assert response.status_code == 200
#       except AssertionError as e:
#           logging.error(e)
#       if response.json()['num_results'] != 0:
#           return True
#       else:
#           return False
    def articleExists(this, article):
        filters = [dict(name='contenthash', op='equals', val=article.contenthash)]
        response = None
        try:
            response = rest.doGet("article", filters)
            if response.json()['num_results'] != 0:
                return True;
            else:
                return False;
        except Exception as e:
            log.exception(e)
            return None
