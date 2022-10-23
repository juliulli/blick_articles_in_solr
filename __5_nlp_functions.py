import textacy
import textacy.text_stats
from re import search
import pytz

import dateutil.parser
format = '%Y-%m-%dT%H:%M:%S.%f%z'

from textblob_de import TextBlobDE as TextBlob

import textstat
textstat.set_lang('de')

from nltk.corpus import stopwords
german_stop_words = stopwords.words('german')

import spacy
nlp = spacy.load("de_core_news_lg")

import yake

kw_extractor = yake.KeywordExtractor()
language = "ger"
max_ngram_size = 1
deduplication_threshold = 0.3
numOfKeywords = 100
custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)

from HanTa import HanoverTagger as ht
hannover = ht.HanoverTagger('morphmodel_ger.pgz')

import __2_variables
import __3_helpers


def get_lemma(to_lemmatize):
    lemmatized = hannover.analyze(to_lemmatize)
    return lemmatized

def replace_ampersand(text):
    text = text.replace('&', '&amp;')
    return text

def stop_word_removal(x):
    x = x.replace(",","").replace(".", "")
    x = x.lower()
    token = x.split()
    return ' '.join([w for w in token if not w in german_stop_words])

# text cleanser
alphabet = "abcdefghijklmnopqrstuvwxyz =>,öäü"
def letters_only(source):
    result = ""
    for i in source.lower():
        if i in alphabet:
            result += i
    return result

def prep_pub_date(unformatted_pub_date):
    pub_date = str(unformatted_pub_date)
    pub_date = pub_date.replace("_", ".") \
        .replace("januar", "01") \
        .replace("februar", "02") \
        .replace("maerz", "03") \
        .replace("april", "04") \
        .replace("mai", "05") \
        .replace("juni", "06") \
        .replace("juli", "07") \
        .replace("august", "08") \
        .replace("september", "09") \
        .replace("oktober", "10") \
        .replace("november", "11") \
        .replace("dezember", "12")
    pub_date = pub_date[-4:] + "-" + pub_date[3:5] + "-" + pub_date[:2] + "T00:00:00Z"
    return(pub_date)

def blick_meta(meta):
    beschreibung = ""
    kategorie = ""
    edited = ""
    for i in meta:
        if search('property="og:description"', str(i)):
            beschreibung_text = str(i).split('"')
            beschreibung = str(beschreibung_text[1])
            beschreibung = replace_ampersand(beschreibung)
        if search('property="article:section"', str(i)):
            kategorie_text = str(i).split('"')
            kategorie = kategorie_text[1]
        if search('og:updated_time', str(i)):
            edited_text = str(i).split('"')
            edited_text = edited_text[1]
            edited_text = dateutil.parser.parse(edited_text)
            edited_text = edited_text.replace(tzinfo=pytz.UTC) - edited_text.utcoffset()
            edited = str(edited_text.strftime("%Y-%m-%dT%H:%M:%SZ"))
    return beschreibung, kategorie, edited

def prep_text(p_tags):
    try:
        text_1 = p_tags[0].text
    except IndexError:
        text_1 = ""
    try:
        text_2 = p_tags[1].text
    except IndexError:
        text_2 = ""
    try:
        text_3 = p_tags[2].text
    except IndexError:
        text_3 = ""
    text_extract = text_1 + " " + text_2 + " " + text_3
    text_extract = replace_ampersand(text_extract)
    return(text_extract)

def prep_entropy(text_extract):
    tdoc = textacy.make_spacy_doc(text_extract, lang="de_core_news_lg")
    entropy = round(textacy.text_stats.basics.entropy(tdoc), 4)
    return(entropy)

def prep_wstf(text_extract):
    try:
        wstf = round(textstat.wiener_sachtextformel(text_extract, 4), 4)
    except ZeroDivisionError:
        wstf = 0.0000
    return(wstf)

def prep_sentiment(text_extract):
    sentiment = round(TextBlob(text_extract).sentiment[0], 4)
    return sentiment


def prep_english_kw(text_extract):
    text_w_stopw = stop_word_removal(text_extract)
    keywords = custom_kw_extractor.extract_keywords(text_w_stopw)

    english_keywords = ""
    for keyword in keywords:
        lemma_kw = get_lemma(keyword[0])
        if len(lemma_kw) > 0:
            lemma_kw = __3_helpers.tuple_to_stringalizer(lemma_kw)
            lemma_kw = lemma_kw.split(", ")[0]
            lemma_kw = lemma_kw.lower()
            lemma_kw = letters_only(lemma_kw)
        else:
            lemma_kw = ""

        transl_keyw = __3_helpers.kw_translate(lemma_kw)
        try:
            if len(transl_keyw) != "":
                transl_keyw = letters_only(transl_keyw)
                trans_line = str(lemma_kw) + "=>" + str(transl_keyw) + "\n"
                __3_helpers.save_result_en(__2_variables.translation_save, trans_line)
                english_keywords = english_keywords + str(transl_keyw) + " "
            else:
                pass
        except TypeError:
            pass

    english_keywords = " ".join(english_keywords.split())
    english_keywords = english_keywords.replace(", ", " ")
    return(english_keywords)
