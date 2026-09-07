"""
Google Books Search Service
Integrates with Google Books API to search academic books, textbooks, and references.
"""

import requests


def _search_open_library(query):
    """Use Open Library when Google Books is unavailable or rate-limited."""
    url = "https://openlibrary.org/search.json"
    params = {
        'q': query,
        'limit': 16,
        'fields': 'title,subtitle,author_name,publisher,first_publish_year,number_of_pages_median,subject,cover_i,key',
    }

    response = requests.get(url, params=params, timeout=8)
    if response.status_code != 200:
        return []

    books = []
    for item in response.json().get('docs', []):
        cover_id = item.get('cover_i')
        work_key = item.get('key', '')
        books.append({
            'title': item.get('title', 'Untitled'),
            'subtitle': item.get('subtitle', ''),
            'authors': ', '.join(item.get('author_name', [])) or 'Unknown Author',
            'publisher': (item.get('publisher') or ['Unknown Publisher'])[0],
            'published_date': item.get('first_publish_year', 'N/A'),
            'description': 'Open Library book record.',
            'page_count': item.get('number_of_pages_median', 'N/A'),
            'categories': ', '.join((item.get('subject') or [])[:3]),
            'thumbnail': f'https://covers.openlibrary.org/b/id/{cover_id}-M.jpg' if cover_id else '',
            'preview_link': f'https://openlibrary.org{work_key}' if work_key else '#',
        })

    return books


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
            books = _search_open_library(query)
            return {
                'books': books,
                'total': len(books),
                'error': None if books else 'Book search services are temporarily unavailable. Please try again shortly.'
            }
    except requests.RequestException:
        try:
            books = _search_open_library(query)
        except requests.RequestException:
            books = []
        return {
            'books': books,
            'total': len(books),
            'error': None if books else 'Unable to connect to the book search services. Please check your internet connection.'
        }
