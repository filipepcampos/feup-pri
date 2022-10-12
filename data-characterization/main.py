import os
import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

def get_quote_df(df):
    quote_df = pd.DataFrame(pd.Series(quote for quote_list in df['quotes'] for quote in quote_list)).rename(columns={0:'json'})
    quote_df['text'] = quote_df['json'].map(lambda x : x['text'])
    quote_df['likes'] = quote_df['json'].map(lambda x : x['likes'])
    quote_df['tags'] = quote_df['json'].map(lambda x : x['tags'])
    quote_df = quote_df.drop('json', axis=1)
    return quote_df

def get_genre_df(df):
    genre_df = pd.DataFrame(pd.Series(genre for genres_list in df['genres'] for genre in genres_list).value_counts()).rename(columns={0: 'count'})
    genre_df = genre_df.reset_index().rename(columns={'index': 'genre'})
    return genre_df

def get_tag_df(quote_df):
    tag_df = pd.DataFrame(pd.Series(tag for tags_list in quote_df['tags'] for tag in tags_list).value_counts()).rename(columns={0: 'count'})
    tag_df = tag_df.reset_index().rename(columns={'index': 'tag'})

def get_author_df(df):
    author_df = df.groupby(['author']) \
        .agg({'title': 'count', 'rating': 'mean'}) \
        .rename(columns={'title': 'nBooks', 'rating': 'avgRating'}) \
        .sort_values('nBooks', ascending=False) \
        .reset_index()
    return author_df

def main():
    ## Setup 

    df = pd.read_json(input_file)
    df['nQuotes'] = df['quotes'].apply(lambda x: len(x))
    df.describe().to_csv(f'{output_folder}/book_describe.csv')

    genre_df = get_genre_df(df)
    quote_df = get_quote_df(df)
    tag_df = get_tag_df(quote_df)
    author_df = get_author_df(df)
    author_df.head(10).to_csv(f'{output_folder}/top_authors.csv')

    data = [
        ["Raw data size", f"{os.path.getsize('data/goodreads.json') >> 20} MB"],
        ["Processed data size", f"{os.path.getsize(input_file) >> 20} MB"],
        ["Total number of books", f"{df['title'].count()} books"],
        ["Total number of quotes", f"{df['nQuotes'].sum()} quotes"],
        ["Average number of quotes per book", f"{df['nQuotes'].mean():.2f} quotes"],
        ["Median number of quotes per book", f"{int(df['nQuotes'].median())} quotes"],
        ["Number of authors", f"{len(author_df['author'].unique())} authors"],
        ["Number of genres", f"{len(genre_df['genre'].unique())} unique genres"],
        ["Number of tags", f"{len(tag_df['tag'].unique())} unique tags"]
    ]

    volume_df = pd.DataFrame(data, columns=['Attribute', 'Value'])
    volume_df = volume_df.set_index('Attribute')
    volume_df.head(10).to_csv(f'{output_folder}/data_volume.csv')

    sns.displot(df, x="rating", bins=80, kde=True, kind='hist')
    plt.xlabel('Rating')
    plt.savefig(f'{output_folder}/rating_distribution.png')

    sns.boxplot(author_df.rename(columns={'nBooks': 'Book Count', 'avgRating': 'Average Rating'}), showfliers=False)
    plt.ylabel('Number of books')
    plt.tight_layout()
    savefig('book_rating_distribution.png')

    sns.barplot(data=genre_df.reset_index().head(15), x='genre', y='count')
    plt.xticks(rotation = 90)
    plt.xlabel('Genre')
    plt.ylabel('Count')
    plt.tight_layout()
    savefig('genre_count.png')

    sns.barplot(data=tag_df.reset_index().head(15), x='tag', y='count')
    plt.xticks(rotation = 90)
    plt.xlabel('Tag')
    plt.ylabel('Count')
    plt.tight_layout()
    savefig('tag_count.png')

    sns.displot(data=genre_df, x='count', kind='hist')
    savefig('genre_count.png')

    sns.lmplot(data=author_df, x='nBooks', y='avgRating')
    plt.ylabel('Average rating')
    plt.xlabel('Number of books')
    savefig('n_books_over_avgrating.png')

if __name__ == '__main__':
    main()