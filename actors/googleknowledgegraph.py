# coding=UTF-8

"""Example of Python client calling Knowledge Graph Search API."""
import json
import urllib.request
import urllib.parse

class GoogleKnowledgeGraph():
    def getUrl(self,query,limit=10,result_len=3):
        api_key = open('actors/api_key.txt').read()
        service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
        params = {
            'query': query,
            'limit': limit,
            'indent': True,
            'key': api_key,
        }
        result=[]
        url = service_url + '?' + urllib.parse.urlencode(params)
        response = json.loads(urllib.request.urlopen(url).read())
        for element in response['itemListElement']:
            key='detailedDescription'
            key2='url'
            if(key2 in element['result']):
                if(len(result)<result_len):
                    result.append(element['result'][key2])
            if key in element['result']:
                if key2 in element['result'][key]:
                    if(len(result)<result_len):
                        result.append(element['result'][key][key2])
                    else:
                        break
        return result