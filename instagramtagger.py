""" 
This program retrieves the top trending Instagram hashtags for the past 24 hours or live hashtags. 
It uses the Instagram API to search for hashtags based on media count and time frame.
The program requires a valid access token to function properly.
"""

import datetime
import requests
from dateutil import tz

INSTAGRAM_API_BASE_URL = 'https://graph.instagram.com'
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN_HERE' #replace this with your GRAPH API token
NUM_HASHTAGS_TO_DISPLAY = 10

def get_top_trending_hashtags(timeframe):
    if timeframe == '24_hours':
        now = datetime.datetime.utcnow()
        twenty_four_hours_ago = now - datetime.timedelta(hours=24)

        now_str = now.replace(tzinfo=datetime.timezone.utc).isoformat()
        twenty_four_hours_ago_str = twenty_four_hours_ago.replace(tzinfo=datetime.timezone.utc).isoformat()

        params = {
            'fields': 'id,name,media_count',
            'access_token': ACCESS_TOKEN,
            'q': f'explore/topical_explore?timezone_offset=0&count={NUM_HASHTAGS_TO_DISPLAY}&'
                 f'max_timestamp={now_str}&min_timestamp={twenty_four_hours_ago_str}'
        }
        response = requests.get(f'{INSTAGRAM_API_BASE_URL}/v12/ig_hashtag_search', params=params, timeout=10)

    elif timeframe == 'live':
        params = {
            'fields': 'id,name,media_count',
            'access_token': ACCESS_TOKEN,
            'q': f'explore/topical_explore?timezone_offset=0&count={NUM_HASHTAGS_TO_DISPLAY}'
        }
        response = requests.get(f'{INSTAGRAM_API_BASE_URL}/v12/ig_hashtag_search', params=params, timeout=10)

    else:
        raise ValueError('Invalid timeframe. Must be "24_hours" or "live".')

    try:
        data = response.json()['data']
    except (ValueError, KeyError):
        return []


    return [d['name'] for d in data]

if __name__ == '__main__':

    top_hashtags_24_hours = get_top_trending_hashtags('24_hours')
    print(f'Top {NUM_HASHTAGS_TO_DISPLAY} hashtags on Instagram in the past 24 hours:')
    for hashtag in top_hashtags_24_hours:
        print(hashtag)

    print()

    top_live_hashtags = get_top_trending_hashtags('live')
    print(f'Top {NUM_HASHTAGS_TO_DISPLAY} live hashtags on Instagram:')
    for hashtag in top_live_hashtags:
        print(hashtag)
