import json

import requests
from twython import Twython, endpoints


def pretty_print(d):
    print(json.dumps(d, indent=4, sort_keys=True))


def main():
    APP_KEY = '3bW9nlsI1KFNGemyKABIExJvw'
    APP_SECRET = 'BIFXOGX6gRPQZ38KAgaH49cZSxVsIV0TXJcd2gRPA1XQvgiD0w'

    twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
    # ACCESS_TOKEN = twitter.obtain_access_token()
    ACCESS_TOKEN = 'AAAAAAAAAAAAAAAAAAAAADBcAQEAAAAACmObvD8B4MwW4Bk%2B%2FvMcs75QuvA%3DV6QxfukBXCbsrDBykrZiNklTnjr2tY3A9AubSFDw1T19kh9OJY'
    print(ACCESS_TOKEN)

    twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
    print(twitter)

    api_url = 'https://api.twitter.com/1.1/tweets/search/30day/production.json'
    constructed_url = twitter.construct_api_url(api_url, query='brexit from:borisjohnson', maxResults=10)
    print(constructed_url)
    response = requests.get(constructed_url, headers={
        'Authorization': 'Bearer %s' % ACCESS_TOKEN
    })
    print(response.json())
    print(response.status_code)
    results = response.json()
    # results = twitter.search(q='brexit from:BorisJohnson', include_entities=1, lang='en', count=100, result_type='popular')
    # # results = twitter.search(q='q="to:$tweeterusername", sinceId = $tweetId', include_entities=1, lang='en', since_id=, count=100)
    # # results = twitter.search(q='from:borisjohnson', include_entities=1, lang='en', count=100)
    # # results = twitter.search(q='from:aa, brexit', result_type='popular', max_id=1183041795334250496, include_entities=1, )
    print(pretty_print(results))
    print(len(results['results']))
    print(results.keys())
    print(results['requestParameters'])

if __name__ == '__main__':
    main()