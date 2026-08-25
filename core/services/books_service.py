"""
Google Books Search Service
Integrates with Google Books API to search academic books, textbooks, and references.
"""

import requests


def search_books(query):
    """
    Search Google Books API for academic books matching the query.
    
    Returns a dictionary:
    {
        'books': list of dicts,
        'total': int,
        'error': str or None
    }
    """
    query = query.strip()
    if not query:
        return {
            'books': [],
            'total': 0,
            'error': 'Please enter a book title, author, or subject to search.'
        }

    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        'q': query,
        'maxResults': 16,
        'printType': 'books',
    }

    try:
        response = requests.get(url, params=params, timeout=8)
        if response.status_code == 200:
            data = response.json()
            total_items = data.get('totalItems', 0)
            items = data.get('items', [])
            
            books = []
            for item in items:
                vinfo = item.get('volumeInfo', {})
                
                # Image thumbnail (replace http with https)
                image_links = vinfo.get('imageLinks', {})
                thumbnail = image_links.get('thumbnail') or image_links.get('smallThumbnail') or ''
                if thumbnail.startswith('http://'):
                    thumbnail = 'https://' + thumbnail[7:]

                authors = vinfo.get('authors', [])
                authors_str = ", ".join(authors) if authors else 'Unknown Author'

                books.append({
                    'title': vinfo.get('title', 'Untitled'),
                    'subtitle': vinfo.get('subtitle', ''),
                    'authors': authors_str,
                    'publisher': vinfo.get('publisher', 'Unknown Publisher'),
                    'published_date': vinfo.get('publishedDate', 'N/A'),
                    'description': vinfo.get('description', 'No description available for this book.'),
                    'page_count': vinfo.get('pageCount', 'N/A'),
                    'categories': ", ".join(vinfo.get('categories', [])) if vinfo.get('categories') else '',
                    'thumbnail': thumbnail,
                    'preview_link': vinfo.get('previewLink') or vinfo.get('infoLink') or '#',
                })

            return {
                'books': books,
                'total': total_items,
                'error': None if books else f"No academic books found for '{query}'."
            }
        else:
            return {
                'books': [],
                'total': 0,
                'error': f"Google Books API returned status code {response.status_code}."
            }
    except requests.RequestException:
        return {
            'books': [],
            'total': 0,
            'error': 'Unable to connect to Google Books. Please check your internet connection.'
        }
