"""
Wikipedia Search Service
Queries Wikipedia REST API for page summaries, thumbnails, and article links.
"""

import requests
import urllib.parse


def search_wikipedia(query):
    """
    Search Wikipedia for the given query and retrieve a structured summary.
    
    Returns a dictionary:
    {
        'found': bool,
        'title': str,
        'summary': str,
        'thumbnail': str or None,
        'url': str,
        'error': str or None
    }
    """
    query = query.strip()
    if not query:
        return {
            'found': False,
            'title': '',
            'summary': '',
            'thumbnail': None,
            'url': '',
            'error': 'Please enter a search topic.'
        }

    headers = {
        'User-Agent': 'StudentStudyPortal/1.0 (Educational College Project; contact: student@example.com)'
    }

    # First, try Wikipedia REST summary endpoint
    encoded_title = urllib.parse.quote(query.replace(' ', '_'))
    summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_title}"

    try:
        response = requests.get(summary_url, headers=headers, timeout=8)
        
        if response.status_code == 200:
            data = response.json()
            extract = data.get('extract')
            
            # If the extract exists and is not a disambiguation error
            if extract and data.get('type') != 'disambiguation':
                thumbnail_url = data.get('thumbnail', {}).get('source') if data.get('thumbnail') else None
                page_url = data.get('content_urls', {}).get('desktop', {}).get('page') or f"https://en.wikipedia.org/wiki/{encoded_title}"
                return {
                    'found': True,
                    'title': data.get('title', query.title()),
                    'summary': extract,
                    'thumbnail': thumbnail_url,
                    'url': page_url,
                    'error': None
                }

        # If direct page not found or disambiguation, search via Opensearch API
        search_url = "https://en.wikipedia.org/w/api.php"
        search_params = {
            'action': 'opensearch',
            'search': query,
            'limit': 5,
            'namespace': 0,
            'format': 'json'
        }
        search_res = requests.get(search_url, params=search_params, headers=headers, timeout=8)
        
        if search_res.status_code == 200:
            search_data = search_res.json()
            # OpenSearch returns [query, [titles], [descriptions], [urls]]
            if len(search_data) >= 4 and len(search_data[1]) > 0:
                best_title = search_data[1][0]
                best_url = search_data[3][0]
                
                # Fetch summary for the best title
                encoded_best = urllib.parse.quote(best_title.replace(' ', '_'))
                best_summary_res = requests.get(
                    f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_best}",
                    headers=headers,
                    timeout=8
                )
                if best_summary_res.status_code == 200:
                    best_data = best_summary_res.json()
                    return {
                        'found': True,
                        'title': best_data.get('title', best_title),
                        'summary': best_data.get('extract', search_data[2][0] if search_data[2] else 'No detailed summary available.'),
                        'thumbnail': best_data.get('thumbnail', {}).get('source') if best_data.get('thumbnail') else None,
                        'url': best_data.get('content_urls', {}).get('desktop', {}).get('page') or best_url,
                        'error': None
                    }
                else:
                    return {
                        'found': True,
                        'title': best_title,
                        'summary': search_data[2][0] if search_data[2] and search_data[2][0] else 'Click the article link below to view full information on Wikipedia.',
                        'thumbnail': None,
                        'url': best_url,
                        'error': None
                    }

        return {
            'found': False,
            'title': query,
            'summary': '',
            'thumbnail': None,
            'url': '',
            'error': f"No Wikipedia article found for '{query}'. Please check the topic name or try different keywords."
        }

    except requests.RequestException:
        return {
            'found': False,
            'title': query,
            'summary': '',
            'thumbnail': None,
            'url': '',
            'error': 'Unable to connect to Wikipedia. Please check your internet connection.'
        }
