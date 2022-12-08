import os
import requests
import time
from process_json import process_json

WIKIMEDIA_BEARER = os.getenv('WIKIMEDIA_BEARER')
WIKIMEDIA_ACCESS_TOKEN = os.getenv('WIKIMEDIA_ACCESS_TOKEN')
LANGUAGE_CODE = 'en'
HEADERS = {
    'Authorization': f'{WIKIMEDIA_BEARER} {WIKIMEDIA_ACCESS_TOKEN}',
}
BASE_URL = 'https://api.wikimedia.org/core/v1/wikipedia/'

def search_for_title(book_title):
    search_query = book_title + " book"
    number_of_results = 1
    endpoint = '/search/page'
    url = BASE_URL + LANGUAGE_CODE + endpoint
    parameters = {'q': search_query, 'limit': number_of_results}
    response = requests.get(url, headers=HEADERS, params=parameters)
    data = response.json()["pages"][0]
    return data["title"]

def get_description(page_title):
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts%7Cinfo&titles={page_title}&formatversion=2&exintro=1&explaintext=1&inlinkcontext=Main%20Page"
    response = requests.get(url, headers=HEADERS)
    data = response.json()

    return data["query"]["pages"][0]["extract"]

"""
Get the wikipedia description for each book
"""
def get_wikipedia_description(json):
    if not "wikipedia_description" in json:
        try:
            title = search_for_title(json["title"] + " book")
            description = get_description(title)
            json["wikipedia_description"] = description
        except Exception:
            pass
        time.sleep(2)
    return json

def main():
    process_json(get_wikipedia_description)

if __name__ == '__main__':
    main()