from process_json import process_json

"""
Fill missing attributes according to book_attributes and quote_attributes default values
"""

book_attributes = {
    'title': None,
    'author': None,
    'rating': None,
    'pageCount': None,
    'ISBN': None,
    'genres': [],
    'quotes': None
}

quote_attributes = {
    'text': None,
    'tags': [],
    'likes': None
}

def fill_missing(json, attribute, null_value):
    json[attribute] = null_value if json.get(attribute) is None else json[attribute]

def transform_fill_missing_fields(json):
    for key, value in book_attributes.items():
        fill_missing(json, key, value)
    
    if 'quotes' in json:
        for quote in json['quotes']:
            for key, value in quote_attributes.items():
                fill_missing(quote, key, value)
    return json

def main():
    process_json(transform_fill_missing_fields)

if __name__ == '__main__':
    main()