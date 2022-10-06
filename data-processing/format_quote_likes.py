from process_json import process_json

"""
For each quote convert likes attribute from "N likes" to just N
If the attribute is non-numeric the attribute will be set as None
"""

def transform_number_likes(json):
    if 'quotes' in json:
        for quote in json['quotes']:
            if 'likes' in quote:
                try:
                    quote['likes'] = int(quote['likes'].split(" ")[0])
                except ValueError:
                    quote['likes'] = None        
    return json

def main():
    process_json(transform_number_likes)

if __name__ == '__main__':
    main()