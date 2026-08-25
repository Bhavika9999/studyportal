"""
YouTube Educational Video Search Service
Integrates with YouTube Data API v3 with graceful fallback handling.
"""

import requests
from django.conf import settings


def search_youtube(query):
    """
    Search YouTube for educational videos matching the given query.
    
    Returns a dictionary:
    {
        'configured': bool,
        'videos': list of dicts,
        'error': str or None
    }
    """
    api_key = getattr(settings, 'YOUTUBE_API_KEY', '') or ''
    api_key = api_key.strip()

    if not api_key:
        return {
            'configured': False,
            'videos': [],
            'error': 'YouTube search is currently unavailable because the API key has not been configured in .env.'
        }

    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'maxResults': 12,
        'key': api_key,
        'videoEmbeddable': 'true',
        'safeSearch': 'moderate',
    }

    try:
        response = requests.get(url, params=params, timeout=8)
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            videos = []
            for item in items:
                video_id = item.get('id', {}).get('videoId')
                snippet = item.get('snippet', {})
                if video_id and snippet:
                    thumbnails = snippet.get('thumbnails', {})
                    thumb_url = (
                        thumbnails.get('high', {}).get('url') or
                        thumbnails.get('medium', {}).get('url') or
                        thumbnails.get('default', {}).get('url') or
                        ''
                    )
                    videos.append({
                        'id': video_id,
                        'title': snippet.get('title', 'Untitled Video'),
                        'description': snippet.get('description', ''),
                        'thumbnail': thumb_url,
                        'channel_title': snippet.get('channelTitle', 'Unknown Channel'),
                        'published_at': snippet.get('publishedAt', '')[:10],
                        'url': f"https://www.youtube.com/watch?v={video_id}",
                    })
            return {
                'configured': True,
                'videos': videos,
                'error': None if videos else 'No educational videos found for this search term.'
            }
        elif response.status_code == 403:
            return {
                'configured': True,
                'videos': [],
                'error': 'YouTube API quota exceeded or invalid API key. Please check your Google Cloud Console.'
            }
        else:
            return {
                'configured': True,
                'videos': [],
                'error': f"YouTube API returned status code {response.status_code}."
            }
    except requests.RequestException as e:
        return {
            'configured': True,
            'videos': [],
            'error': 'Unable to connect to YouTube. Please check your internet connection.'
        }
