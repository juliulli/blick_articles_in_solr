from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

import __3_helpers
import __5_nlp_functions


def get_archive(archive_link_file, article_link_file):
    publicated_articles = []
    with open(archive_link_file) as f:
        lines = f.readlines()
    for line in lines:
        date = line.split("/")[-1]
        archive_day = str((line)[ :-1])
        link = (rf"{archive_day}")
        print(link)

        loop_count = 0
        while loop_count < 10:
            try:
                blick_archiv_request = requests.get(link, allow_redirects=True)
                loop_count = 10
            except Exception as e:
                print("got an exception:", type(e),e)
                time.sleep(5)
                loop_count += 1
                if loop_count == 9:
                    continue

        blick_soup = BeautifulSoup(blick_archiv_request.text, features="lxml")
        for a in blick_soup.find_all(href=True):
            finding = [date, str(a['href'])]
            publicated_articles.append(finding)
    df = pd.DataFrame(publicated_articles, columns = ['date', 'article_links'])
    df.to_csv(article_link_file,index=True)
    return(article_link_file)

def prep_links(archive_links, content_link_file):
    archive_links_blick = pd.read_csv(archive_links)
    archive_links_blick['link_count'] = archive_links_blick.groupby('article_links')['article_links'].transform('count')
    archive_links_blick['date'] = archive_links_blick['date'].str.replace('\n','')
    archive_links_blick = archive_links_blick.loc[archive_links_blick['link_count'] == 1].copy()
    archive_links_blick = archive_links_blick[archive_links_blick["article_links"].str.contains("https://www.blick.ch/services/webarchiv") == False]
    archive_links_blick = archive_links_blick[archive_links_blick["article_links"].str.contains("https://www.blick.ch/webarchiv") == False]
    archive_links_blick = archive_links_blick[archive_links_blick["article_links"].str.contains("/gewinnen/") == False]
    archive_links_blick = archive_links_blick.drop(['link_count'], axis=1)
    archive_links_blick = archive_links_blick.iloc[:, [1,2]]
    archive_links_blick.to_csv(content_link_file,index=False)
    return(content_link_file)

def prep_content(content_links, content_size):
    begin_from = content_size * (-1)
    daily_blick_links = pd.read_csv(content_links)
    ready_content = daily_blick_links[begin_from:]
    return ready_content

def curl_contents(ready_content, output_save_file):
    n = 1
    for index, row in ready_content.iterrows():
        url = 'https://blick.ch' + str(row[1])
        loop_count = 0

        while loop_count < 10:
            try:
                blick_request = requests.get(url, allow_redirects=True)
                loop_count = 10
            except Exception as e:
                print("got an exception:", type(e), e)
                time.sleep(5)
                loop_count += 1
                if loop_count == 9:
                    continue

        blick_soup = BeautifulSoup(blick_request.text, features="lxml")
        try:
            titel = blick_soup.title.text
            titel = __5_nlp_functions.replace_ampersand(titel)
        except AttributeError:
            continue

        if titel == "401 Authorization Required":
            continue

        meta = blick_soup.findAll("meta")
        p_tags = blick_soup.findAll('p')

        id = __3_helpers.get_new_doc_no()
        text_extract = __5_nlp_functions.prep_text(p_tags)
        beschreibung, kategorie, edited = __5_nlp_functions.blick_meta(meta)
        entropy = __5_nlp_functions.prep_entropy(text_extract)
        wstf = __5_nlp_functions.prep_wstf(text_extract)
        sentiment = __5_nlp_functions.prep_sentiment(text_extract)
        english_keywords = __5_nlp_functions.prep_english_kw(text_extract)
        pub_date = __5_nlp_functions.prep_pub_date(row[0])

        if edited == "":
            edited = pub_date

        output_save_file_wn = output_save_file[:-4] + str(id) + output_save_file[-4:]

        ready_for_solr = __3_helpers.write_output_once(output_save_file_wn, id, titel, beschreibung, text_extract, kategorie, edited, entropy, wstf, sentiment, english_keywords, url, pub_date)
        nothing = __3_helpers.solr_add(ready_for_solr)
        n += 1
        print(output_save_file_wn + " " + nothing + ": " + pub_date + ", ", titel)
    return n