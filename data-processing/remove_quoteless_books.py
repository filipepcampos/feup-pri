from process_json import process_json

def remove_quoteless_books(json):
    # Remove if there's no field 'quotes'
    if 'quotes' not in json:
        return None
    return json

def main():
    process_json(remove_quoteless_books)

if __name__ == '__main__':
    main()