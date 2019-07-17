import requests
import os
import unicodedata
from bs4 import BeautifulSoup
import pandas as pd

LETTER_CODES = {'A','B','C','D','G','H','J','L','M','N','P','R','S','V'}
COLUMN_NAMES = ['First Level', 'Second Level', 'Third Level', 'Fourth Level'
                , 'Fifth Level', 'ATC', 'Name', 'DDD', 'Unit', 'Adm.R', 'Note']
collected_parse = []

def recursive_scrape(url=''):
#   Gets site, ensures site is available
    html = requests.get(url)
    if not html:
        raise Exception('Error accessing site, response code {} for site {}'
                    .format(html.status_code, html.url ))
   
    soup = BeautifulSoup(html.text, 'lxml')
    
#    All relevant data is contained within <div id="content"> tags
#    Specifically, followed links are only found in <b> tags inside <p> tags,
#    Drug group information is found in <b> tags NOT inside <p> tags, and
#    inividual drug information is in tables at the end
    content = soup.find(id='content')
    b_tags = soup.find_all('b')

#    If it has ul's, then we're at the end, otherwise keep going
    if(content.find('ul') is not None):

        info_path = []
        for txt in b_tags:
            if not txt.parent.name == 'p':
                info_path.append(txt.text)
        
        while len(info_path) < 5:
            info_path.append('')
        
        split_list=[]
        tmp_list=[]
#        Automatically chunks based on rows
        for row in content.find_all('tr'):
            for td in row.children:
                tmp_list.append(unicodedata.normalize("NFKD", td.text))
            split_list.append(tmp_list)
            tmp_list=[]

        for item in split_list[1:]:
            collected_parse.append(info_path + item)
        
    else:
        for b in b_tags:
            if b.parent.name == 'p':
            
                #URLS provided are relative with a '.' at beginning that needs to be trimmed
                recursive_scrape(url= "https://www.whocc.no/atc_ddd_index{}"
                                     .format(b.find('a')["href"][1:]))        
#                Reference: b.find('a').text gives name, ["href"] gives follow link w/o beginning
#                print(b.find('a').text , " | {}", b.find('a')["href"])
        
if __name__ == "__main__":
    collected_parse.append(COLUMN_NAMES)

#    Iterates through all ATC letter codes
    for c in LETTER_CODES:
        base_url = "https://www.whocc.no/atc_ddd_index/?code={}&showdescription=no".format(c.upper())
        recursive_scrape(url=base_url)
    df= pd.DataFrame(collected_parse[1:], columns=collected_parse[0])
    
#    Overrides past scrape file
    if os.path.exists("scrape.csv"):
        os.remove("scrape.csv")
    df.to_csv('scrape.csv')
