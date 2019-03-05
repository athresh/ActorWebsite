# -*- coding: utf-8 -*-

import json
import urllib

api_key = "AIzaSyDs-V4WEf0oDt70mqowVBHqa3IqQsLD0DI"
query = 'Taylor Swift'
service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
params = {
    'query': query,
    'limit': 10,
    'indent': True,
    'key': api_key,
}
url = service_url + '?' + urllib.parse.urlencode(params)
print(url)
response = json.loads(urllib.request.urlopen(url).read())
for element in response['itemListElement']:
    print (element['result']['name'] + ' (' + str(element['resultScore']) + ')')