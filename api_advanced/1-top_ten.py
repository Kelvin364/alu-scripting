#!/usr/bin/python3
"""
Module for recursively querying the Reddit API to get hot posts
"""
import requests


def recurse(subreddit, hot_list=[], after=None):
    """
    Returns a list of titles of all hot posts on a given subreddit.
    Args:
        subreddit: subreddit to search
        hot_list: list to store results
        after: token for pagination
    Returns:
        List of titles or None if invalid subreddit
    """
    # Set custom User-Agent to avoid Too Many Requests error
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    
    # Add after parameter for pagination if it exists
    params = {'after': after} if after else {}

    try:
        # Make GET request to Reddit API
        response = requests.get(url, 
                              headers=headers,
                              params=params,
                              allow_redirects=False)

        # Check if subreddit is invalid
        if response.status_code == 404:
            return None

        # Parse response data
        data = response.json()
        posts = data['data']['children']
        
        # Base case: no more posts
        if not posts:
            return hot_list
        
        # Add titles to hot_list
        for post in posts:
            hot_list.append(post['data']['title'])
        
        # Get "after" token for next page
        after = data['data']['after']
        
        # Base case: no more pages
        if not after:
            return hot_list
            
        # Recursive case: get next page
        return recurse(subreddit, hot_list, after)

    except Exception:
        return None
