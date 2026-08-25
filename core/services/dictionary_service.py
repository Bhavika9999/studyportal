"""
Dictionary Service
Integrates with the Free Dictionary API to retrieve word meanings, parts of speech, phonetics, and examples.
"""

import requests


def lookup_word(word):
    """
    Look up definitions, pronunciation, and examples for an English word.
    
    Returns a dictionary:
    {
        'found': bool,
        'word': str,
        'phonetic': str,
        'audio': str or None,
        'meanings': list of dicts: [
            {
                'part_of_speech': str,
                'definitions': [
                    {'definition': str, 'example': str or None, 'synonyms': list}
                ]
            }
        ],
        'error': str or None
    }
    """
    word = word.strip().lower()
    if not word:
        return {
            'found': False,
            'word': '',
            'phonetic': '',
            'audio': None,
            'meanings': [],
            'error': 'Please enter a word to search.'
        }

    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    try:
        response = requests.get(url, timeout=8)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                entry = data[0]
                
                # Extract phonetic text
                phonetic_text = entry.get('phonetic', '')
                audio_url = None
                
                for p in entry.get('phonetics', []):
                    if not phonetic_text and p.get('text'):
                        phonetic_text = p.get('text')
                    if p.get('audio') and not audio_url:
                        audio_url = p.get('audio')

                # Extract meanings
                meanings_list = []
                for m in entry.get('meanings', []):
                    pos = m.get('partOfSpeech', 'general')
                    defs_list = []
                    for d in m.get('definitions', []):
                        defs_list.append({
                            'definition': d.get('definition', ''),
                            'example': d.get('example', None),
                            'synonyms': d.get('synonyms', [])[:5],
                        })
                    
                    meanings_list.append({
                        'part_of_speech': pos,
                        'definitions': defs_list,
                    })

                return {
                    'found': True,
                    'word': entry.get('word', word),
                    'phonetic': phonetic_text,
                    'audio': audio_url,
                    'meanings': meanings_list,
                    'error': None
                }

        # 404 or word not found
        return {
            'found': False,
            'word': word,
            'phonetic': '',
            'audio': None,
            'meanings': [],
            'error': f"Word '{word}' not found. Please check the spelling or try another word."
        }

    except requests.RequestException:
        return {
            'found': False,
            'word': word,
            'phonetic': '',
            'audio': None,
            'meanings': [],
            'error': 'Unable to connect to Dictionary service. Please check your internet connection.'
        }
