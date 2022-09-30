import argparse
import ijson

def parse_args():
    parser = argparse.ArgumentParser(description='An interesting description')
    parser.add_argument('file', type=str, help='Json file with data')
    return parser.parse_args()

def main():
    args = parse_args()

    with open(args.file, "r") as file:
        objects = ijson.items(file, 'item')
        for o in objects:
            print(o['title'])
            break

if __name__ == '__main__':
    main()