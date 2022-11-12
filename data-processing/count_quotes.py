from process_json import process_json

"""
Count number of quotes
"""

def count_quotes(json):    
    json['quotesCount'] = len(json['quotes'])
    return json

def main():
    process_json(count_quotes)

if __name__ == '__main__':
    main()