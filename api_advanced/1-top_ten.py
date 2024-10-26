#!/usr/bin/python3
"""
1-main
"""

import requests


def top_ten(subreddit):
    """
    Prints the titles of the first 10 hot posts listed for a given subreddit.
    Args:
        subreddit: subreddit to search
    """
    # Set custom User-Agent to avoid Too Many Requests error
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    
    # Limit to 10 posts in query parameters
    params = {'limit': 10}

    try:
        # Make GET request to Reddit API
        response = requests.get(url,
                              headers=headers,
                              params=params,
                              allow_redirects=False)
        
        # Check if subreddit is invalid
        if response.status_code == 404:
            print("None")
            return

        # Parse response data
        data = response.json()
        posts = data['data']['children']
        
        # Print first 10 post titles
        for post in posts:
            print(post['data']['title'])

    except Exception:
        print("None")
