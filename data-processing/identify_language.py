from process_json import process_json
import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector

def get_lang_detector(nlp, name):
    return LanguageDetector()

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

# Setup language detector
Language.factory("language_detector", func=get_lang_detector)
nlp.add_pipe('language_detector', last=True)

def gen_quote_text(json):
    if 'quotes' in json:
        for quote in json['quotes']:
            yield (quote['text'], quote) # (text that will be used by nlp, context)

"""
For each quote, identify the language it's written in
"""
def identify_language(json):
    for doc, quote in nlp.pipe(gen_quote_text(json), disable=["tok2vec", "tagger", "attribute_ruler", "ner", "senter", "lemmatizer"], as_tuples=True):
        quote['language'] = doc._.language
    return json

def main():
    process_json(identify_language)

if __name__ == '__main__':
    main()