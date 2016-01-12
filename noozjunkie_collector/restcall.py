##
## collector.py
## ljheidel@noozjunkie.com
##
import collector_config
import requests
import json
from noozjunkie_collector import log

class RestCall:

    token = False

    def __init__(self):
        self.token = self.requestToken()

    def requestToken(self):
        headers = {'Content-Type': 'application/json', 'user-agent': collector_config.USER_AGENT }
        url = "%s/auth" % (collector_config.API_BASE_URL)
        data = { 'username': collector_config.API_USERNAME, 'password': collector_config.API_PASSWORD }
        response = ""
        log.info("Requesting JWT token from %s for %s" % (url, data['username']))
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            newtoken = response.json()['access_token']
            log.info("Retreived JWT token from %s for %s" % (url, data['username']))
            return newtoken
        except requests.exceptions.HTTPError as e:
            log.error("Error requesting token from %s: %s %s (%s)" % (url, response.json()['status_code'], response.json()['error'], response.json()['description']))
            raise Exception()
            return False
        except Exception as e:
            log.exception(e)
            raise Exception()
            return False

    def doGet(self, endpoint, filters = ""):
        headers = {'Content-Type': 'application/json', 'user-agent': collector_config.USER_AGENT, 'Authorization': "JWT %s" % self.token}
        url = "%s/api/%s" % (collector_config.API_BASE_URL, endpoint)
        params = ""
        response = ""
        log.debug("GET request to %s" % (url))
        try:
            if filters != "":
                params = dict(q=json.dumps(dict(filters=filters)))
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
            else:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
            log.debug("Retrieved GET data from %s" % (url))
            return response
        except requests.exceptions.HTTPError as e:
            log.warning("Error GETting data from %s: %s %s (%s)" % (url, response.json()['status_code'], response.json()['error'], response.json()['description']))
            return False

    def doPost(self, endpoint, data = ""):
        headers = {'Content-Type': 'application/json', 'user-agent': collector_config.USER_AGENT, 'Authorization': "JWT %s" % self.token}
        url = "%s/api/%s" % (collector_config.API_BASE_URL, endpoint)
        params = ""
        response = ""
        log.debug("POST request to %s" % (url))
        try:
            if data != "":
                response = requests.post(url, headers=headers, data=json.dumps(data))
                response.raise_for_status()
            else:
                response = requests.post(url, headers=headers)
                response.raise_for_status()
            log.debug("Retrieved POST data from %s" % (url))
            return response
        except requests.exceptions.HTTPError as e:
            log.warning("Error POSTing data to %s: %s %s (%s)" % (url, response.json()['status_code'], response.json()['error'], response.json()['description']))
            return False

    def doPut(self, endpoint, filters = "", data = dict()):
        putdata = dict()
        if filters != "":
            putdata.update(dict(q=dict(filters=filters)))
        putdata.update(data)

        headers = {'Content-Type': 'application/json', 'user-agent': collector_config.USER_AGENT, 'Authorization': "JWT %s" % self.token}
        url = "%s/api/%s" % (collector_config.API_BASE_URL, endpoint)
        params = ""
        response = ""
        log.debug("PUT request to %s" % (url))
        try:
            if putdata != "":
                response = requests.put(url, headers=headers, data=json.dumps(putdata))
                response.raise_for_status()
            else:
                response = requests.post(url, headers=headers)
                response.raise_for_status()
            log.debug("Retrieved put data from %s" % (url))
            return response
        except requests.exceptions.HTTPError as e:
            log.warning("Error PUTting data to %s: %s %s (%s)" % (url, response.json()['status_code'], response.json()['error'], response.json()['description']))
            return False
