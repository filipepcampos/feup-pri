from process_json import process_json

"""
Convert pageCount attribute from "N pages" to just N
If the attribute is non-numeric the attribute will be set as None
"""

def transform_number_pages(json):
    if 'pageCount' in json:
        try:
            json['pageCount'] = int(json['pageCount'].split(" ")[0])
        except ValueError:
            json['pageCount'] = None
    return json

def main():
    process_json(transform_number_pages)

if __name__ == '__main__':
    main()