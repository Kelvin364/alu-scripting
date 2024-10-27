#!/usr/bin/python3
"""Script that fetch 10 hot post for a given subreddit."""
import requests


def top_ten(subreddit):
    """
    Queries the Reddit API and prints the titles of the first 10 hot posts
    for a given subreddit.
    
    Args:
        subreddit: Name of the subreddit to query
    
    Returns:
        None if subreddit is invalid, prints titles otherwise
    """
    # Set a custom User-Agent to avoid Too Many Requests errors
    headers = {
        'User-Agent': 'linux:0:1.0 (by /u/your_username)'
    }
    
    # Use the proper URL format for hot posts
    url = f'https://www.reddit.com/r/{subreddit}/hot.json?limit=10'
    
    try:
        # Allow_redirects=False to handle invalid subreddits
        response = requests.get(url, headers=headers, allow_redirects=False)
        
        # Check if the response was successful and not a redirect
        if response.status_code == 200:
            posts = response.json().get('data', {}).get('children', [])
            
            if posts:
                for post in posts:
                    print(post.get('data', {}).get('title'))
            else:
                print(None)
        else:
            print(None)
            
    except Exception:
        print(None)
