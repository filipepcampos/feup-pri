from process_json import process_json

def strip_quotes(json):
    # Stop if there's no field 'quotes'
    if 'quotes' not in json:
        return json
    
    quotes = json['quotes']

    for quote in quotes:
        text = quote['text']

        # Replace '\n' and '\t' by empty space
        new_text = text.replace('\\n', ' ')
        new_text = text.replace('\\t', ' ')

        # Remove unecessary white spaces
        new_text = ' '.join(new_text.split())

        # Modify value
        quote['text'] = new_text
    
    return json

def main():
    process_json(strip_quotes)

if __name__ == '__main__':
    main()