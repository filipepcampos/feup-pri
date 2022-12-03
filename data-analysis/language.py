import pandas as pd
import spacy
import json
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
from pathlib import Path

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=Path)
    parser.add_argument('-o', type=Path)
    return parser.parse_args()

p = get_parser()
output_folder = p.o
input_file = p.i

def savefig(name):
    plt.savefig(f'{output_folder}/{name}')

def main():
    df = pd.read_json(input_file)
    quote_df = pd.DataFrame(pd.Series(quote for quote_list in df['quotes'] for quote in quote_list)).rename(columns={0:'json'})

    quote_df['text'] = quote_df['json'].map(lambda x : x['text'])
    quote_df['likes'] = quote_df['json'].map(lambda x : x['likes'])
    quote_df['tags'] = quote_df['json'].map(lambda x : x['tags'])
    quote_df['language'] = quote_df['json'].map(lambda x: x['language']['language'])
    quote_df = quote_df.drop('json', axis=1)
    quote_df.head()

    language_df = quote_df.groupby('language').count().sort_values(by='text', ascending=False).reset_index()
    language_df.head(10).to_csv(f'{output_folder}/top_languages.csv')

    plt.figure(figsize=(12,4))
    g = sns.barplot(data=language_df.head(15), y='text', x='language')
    g.set_yscale("log")
    plt.yticks(rotation = 90)
    plt.xlabel('Language')
    plt.ylabel('Quote Count')
    plt.tight_layout()
    savefig('language_count.pdf')

if __name__ == '__main__':
    main()