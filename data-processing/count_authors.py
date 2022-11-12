from process_json import process_json

"""
Count number of authors
"""

def count_authors(json):    
    json['authorsCount'] = len(json['authors'])
    return json

def main():
    process_json(count_authors)

if __name__ == '__main__':
    main()