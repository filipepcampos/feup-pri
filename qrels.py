import json
import sys
from collections import Counter

def main():

    qrels = {}

    for line in sys.stdin:
        if len(line) <= 2:
            continue
        
        doc = json.loads(line[:-2] if line[-2] == ',' else line[:-1])

        rel_genres = [
            "Horror", 
            "Psychological Horror", 
            "Halloween",
            "Ghosts",
            "Paranormal",
            "Gothic Horror",
            "Suspense",
            "Supernatural",
        ]

        horror_genre = any([genre in doc['genres'] for genre in rel_genres])

        quotes = doc['quotes']
        likes = 0
        count = 0

        for i in range(len(quotes)):
            if quotes[i]['language']['language'] == "pt":
                likes += quotes[i]['likes']
                count += 1

        if horror_genre and count > 0:
            qrels[doc['title']] = (count, likes, len(quotes))

    for title in sorted(qrels, key=qrels.get, reverse=True):
        print(title, qrels[title])

if __name__ == "__main__":
    main()