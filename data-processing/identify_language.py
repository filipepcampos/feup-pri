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

"""
For each quote, identify the language it's written in
"""
def identify_language(json):
    if 'quotes' in json:
        for quote in json['quotes']:
            doc = nlp(quote['text'])
            quote['language'] = doc._.language
    return json

def main():
    #process_json(identify_language)
    x = nlp("Je me apelle")
    print(x._.language)

if __name__ == '__main__':
    main()