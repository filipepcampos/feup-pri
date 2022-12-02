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
Identify the language of the description of the book
"""
def identify_language(json):
    if 'description' in json:
        if json['description'] != None:
            doc = nlp(json['description'], disable=["tok2vec", "tagger", "attribute_ruler", "ner", "senter", "lemmatizer"])
            json['description_' + doc._.language['language']] = json['description']
        del json['description']
    return json

def main():
    process_json(identify_language)

if __name__ == '__main__':
    main()