#!/usr/bin/python3

"""
Displays the titles of 10 hot posts listed for a subreddit
"""

from requests import get
import subprocess


def top_ten(subreddit):
    """
    The Function that fethces the Reddit API
    """
    user_agent = {'User-agent': 'Google Chrome Version 81.0.4044.129'}
    params = {'limit': 10}
    url = 'https://www.reddit.com/r/{}/hot/.json'.format(subreddit)

    response = get(url, headers=user_agent, params=params)
    if response.status_code != 200:
        print("None")
        return

    try:
        results = response.json()
        my_data = results.get('data').get('children')

        for i in my_data:
            print(i.get('data').get('title'))

    except Exception:
        print("None")
