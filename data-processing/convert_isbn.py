from process_json import process_json

"""
Use ISBN-13 standard in all books, some of them use ISBN-10 so we need to
convert those cases.
"""

def convert_isbn(json):
    if 'ISBN' in json:
        old_isbn = json['ISBN'][:-1]
        try:
            int(old_isbn)
        except ValueError:
            del json['ISBN']                # Remove outliers such as BO7FRW1CKJ
            return json
        if len(old_isbn) == 9:              # ISBN-10
            new_isbn = "978" + old_isbn
            check = 38
            for i, d in enumerate(old_isbn):
                check += int(d) * 3 if i % 2 == 0 else int(d)
            check = check % 10
            json['ISBN'] = new_isbn + "0" if check == 0 else new_isbn + str(10 - check)

    return json

def main():
    process_json(convert_isbn)

if __name__ == '__main__':
    main()