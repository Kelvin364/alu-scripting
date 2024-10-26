#!/usr/bin/python3
"""function that fetches from reddit"""
import requests


def number_of_subscribers(subreddit):
    """function that fetches data """
    headers = {'User-Agent': 'MyAPI/0.1'}
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    fetched_data = requests.get(url, headers=headers, allow_redirects=False)
    status = fetched_data.status_code
    if status == 200:
        results = fetched_data.json()
        subscribers = results['data']['subscribers']
    else:
        subscribers = 0
    return subscribers
