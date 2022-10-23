import os
import pandas as pd
import configparser

import __2_variables


# prepare new save file

def start_new(filename):
    save = open(filename, "a", encoding="ISO-8859-1")
    save_header = ("original => derivation" + "\n")
    save.write(save_header)
    save.close()

# save results in file

def save_result(filename, line):
    save = open(filename, "a", encoding="ISO-8859-1")
    line = str(line.encode('utf-8').strip())
    save.write(line)
    save.close()

def save_result_en(filename, line):
    save = open(filename, "a", encoding="ISO-8859-1")
    line = str(line.strip()) + "\n"
    save.write(line)
    save.close()

def start_output(output_save_file):
    save = open(output_save_file, "w")
    save.write("<add>" + "\n")
    save.close()


def write_output(output_save_file, id_number, titel, beschreibung, text_extract, kategorie, edited, entropy, wstf,
                 sentiment, english_keywords, url, pub_date):
    file = open(output_save_file, "w")
    file.write("  <doc>" + "\n")
    file.write('    <field name="id">' + str(id_number) + '</field>' + "\n")

    try:
        file.write('    <field name="titel">' + titel + '</field>' + "\n")
    except UnicodeEncodeError:
        file.write('    <field name="titel">' + '</field>' + "\n")

    try:
        file.write('    <field name="beschreibung">' + beschreibung + '</field>' + "\n")
    except UnicodeEncodeError:
        file.write('    <field name="beschreibung">' + '</field>' + "\n")

    try:
        file.write('    <field name="text_extract">' + text_extract + '</field>' + "\n")
    except UnicodeEncodeError:
        file.write('    <field name="text_extract">' + '</field>' + "\n")

    try:
        file.write('    <field name="kategorie">' + kategorie + '</field>' + "\n")
    except UnicodeEncodeError:
        file.write('    <field name="kategorie">' + '</field>' + "\n")

    try:
        file.write('    <field name="geändert">' + edited + '</field>' + "\n")
    except UnicodeEncodeError:
        file.write('    <field name="geändert">' + '</field>' + "\n")

    file.write('    <field name="entropy">' + str(entropy) + '</field>' + "\n")
    file.write('    <field name="wstf">' + str(wstf) + '</field>' + "\n")
    file.write('    <field name="senti">' + str(sentiment) + '</field>' + "\n")
    file.write('    <field name="english_kw">' + english_keywords + '</field>' + "\n")
    file.write('    <field name="link">' + url + '</field>' + "\n")
    file.write('    <field name="archiv-datum">' + pub_date + '</field>' + "\n")
    file.write("  </doc>" + "\n")
    file.close()
    return


def write_output_once(output_save_file_wn, id_number, titel, beschreibung, text_extract, kategorie, edited, entropy, wstf,
                      sentiment, english_keywords, url, pub_date):
    file = open(output_save_file_wn, "w")
    file.write("<add>" + "\n")
    file.write("  <doc>" + "\n")
    file.write('    <field name="id">' + str(id_number) + '</field>' + "\n")

    try:
        file.write('    <field name="titel">' + titel + '</field>' + "\n")
    except UnicodeEncodeError:
        file.write('    <field name="titel">' + '</field>' + "\n")

    try:
        file.write('    <field name="beschreibung">' + beschreibung + '</field>' + "\n")
    except UnicodeEncodeError:
        file.write('    <field name="beschreibung">' + '</field>' + "\n")

    try:
        file.write('    <field name="text_extract">' + text_extract + '</field>' + "\n")
    except UnicodeEncodeError:
        file.write('    <field name="text_extract">' + '</field>' + "\n")

    try:
        file.write('    <field name="kategorie">' + kategorie + '</field>' + "\n")
    except UnicodeEncodeError:
        file.write('    <field name="kategorie">' + '</field>' + "\n")

    try:
        file.write('    <field name="geändert">' + edited + '</field>' + "\n")
    except UnicodeEncodeError:
        file.write('    <field name="geändert">' + '</field>' + "\n")

    file.write('    <field name="entropy">' + str(entropy) + '</field>' + "\n")
    file.write('    <field name="wstf">' + str(wstf) + '</field>' + "\n")
    file.write('    <field name="senti">' + str(sentiment) + '</field>' + "\n")
    file.write('    <field name="english_kw">' + english_keywords + '</field>' + "\n")
    file.write('    <field name="link">' + url + '</field>' + "\n")
    file.write('    <field name="archiv-datum">' + pub_date + '</field>' + "\n")
    file.write("  </doc>" + "\n")
    file.write("</add>" + "\n")
    file.close()
    return output_save_file_wn


def stop_output(output_save_file):
    save = open(output_save_file, "w")
    save.write("</add>" + "\n")
    save.close()


dictionary = pd.read_csv('0_deu_eng_dictionary.txt', sep="|", encoding="cp1252")


def kw_translate(german_kw):
    zw_erg = dictionary.loc[dictionary['deutsch'] == german_kw]
    if len(zw_erg) > 0:
        english_words = zw_erg['english'].unique()
        transl = ""
        for word in english_words:
            transl = transl + str(word) + ", "
        transl = transl[:-2]
    else:
        transl = ""
    return transl


def tuple_to_stringalizer(toople):
    to_str = ''
    for item in toople:
        if item == 'NN':
            continue
        to_str = to_str + item + ", "
    to_str = to_str[:-2]
    return to_str


def transform_to_xml(content_doc, solr_doc_file):
    with open(content_doc, 'rb') as source_file:
        with open(solr_doc_file, 'w+b') as dest_file:
            contents = source_file.read()
            dest_file.write(contents.decode('cp1252').encode('utf-8'))
    return solr_doc_file


def get_new_doc_no():
    config = configparser.ConfigParser()
    config.read('__0_config.ini')
    cur_doc = config['BLICK_PARAMS']['current_doc_no']
    cur_doc = str(int(cur_doc) + 1)
    config.set('BLICK_PARAMS', 'current_doc_no', cur_doc)
    with open('__0_config.ini', 'w') as configfile:
        config.write(configfile)
    return cur_doc


def post_to_solr(content_docum):
    for i in content_docum:
        docnum = get_new_doc_no()
        fill = 10 - len(docnum)
        filename = __2_variables.collection + "_" + docnum.rjust(fill, '0')
        solr_doc_file = transform_to_xml(i, filename)
        solr_add(solr_doc_file)
        print("Document ", filename, " passed to solr.")
        os.remove(i)


def solr_add(doc):
    command = "/opt/solr/bin/post -c " + __2_variables.collection + " ./" + doc
    os.system(command)
    return "Extraktion und Beladung durchgeführt."





















