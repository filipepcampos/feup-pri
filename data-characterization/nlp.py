import argparse
from pathlib import Path 
import pandas as pd
import spacy
import json
from tqdm import tqdm

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=Path)
    parser.add_argument('-o', type=Path)
    return parser.parse_args()

p = get_parser()
output_folder = p.o
input_file = p.i

def main():
    df = pd.read_csv(input_file)

    quote_df = pd.DataFrame(pd.Series(quote for quote_list in df['quotes'] for quote in quote_list)).rename(columns={0:'json'})
    quote_df['text'] = quote_df['json'].map(lambda x : x['text'])
    quote_df['likes'] = quote_df['json'].map(lambda x : x['likes'])
    quote_df['tags'] = quote_df['json'].map(lambda x : x['tags'])
    quote_df = quote_df.drop('json', axis=1)
    
    nlp = spacy.load("en_core_web_sm")

    # TODO



if __name__ == '__main__':
    main()