from process_json import process_json

"""
Group the quotes into arrays with the naming convention "quotes_{language}"
"""
def group_quotes_language(json):
    if 'quotes' in json:
        for quote in json['quotes']:
            quote_copy = {}
            quote_copy['text'] = quote['text']
            quote_copy['tags'] = quote['tags']
            quote_copy['likes'] = quote['likes']
            key = 'quotes_' + quote['language']['language']
            quotes = json.get(key, [])
            quotes.append(quote_copy)
            json[key] = quotes
        del json['quotes']
    return json

def main():
    process_json(group_quotes_language)

if __name__ == "__main__":
    main()