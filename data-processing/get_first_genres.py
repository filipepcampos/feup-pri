from process_json import process_json

"""
Get the first three genres
"""

def get_first_genres(json):
    for i in range(0, min(3, len(json['genres']))):
        json[f'genre{i+1}'] = json['genres'][i]
    return json

def main():
    process_json(get_first_genres)

if __name__ == '__main__':
    main()