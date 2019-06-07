# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

taglist = ['li', 'p']
attrlist= ['text','subtext','href','id','class']
test_ret = 'text'
#Currently: specific scrape for Isaac names on Wikipedia
def scrape_li(filt=None, html=None, columns=None, subtag=''):
    tmp = []
    txt,subtxt,href,id_,class_= parse_filt(filt)
    
    txt_filt   = re.compile(txt)
    subtxt_filt= re.compile(subtxt)
    href_filt  = re.compile(href)
    id_filt    = re.compile(id_)
    class_filt = re.compile(class_)
     
    #Replaces out 'null' for 'False' manually
    #TODO: replace entire compile/ if null->false with function
    if txt == 'null':
        txt_filt = False
    
    if subtxt == 'null':
        subtxt_filt = False
    
    if href == 'null':
        href_filt = False
        
    if id_ == 'null':
        id_filt = False
    
    if class_ == 'null':
        class_filt = False
    
    
    #All 'li' tags with proper id, class, and text filter
    for li in html.find_all('li',
                            id   = id_filt,
                            class_= class_filt,
                            text = txt_filt):

        #Currently only manual subtag; if has matching filtered subtag, add to list
        if subtag == 'a':
            if li.find(subtag, 
                       href = href_filt,
                       text = subtxt_filt):
                tmp.append(determine_ret(li))
        else:
            if li.find(subtag,
                       text = subtxt_filt):
                tmp.append(determine_ret(li))
                
    df = pd.DataFrame(tmp, columns=columns.split(sep=','))
#    df.to_csv(path_or_buf='testdf.csv')
    return df

def scrape_p(filt=None, html=None):
    
    return

#Does error checking and actual calling of scrape function
def perform_scrape(tag=None, filt=None, html=None, columns=None, subtag=''):
    #Ensure not trying to use a tag that hasn't been coded yet
    if tag is None or tag not in taglist:
        raise Exception('Parameter \'tag\' is required to be one of the '
                        'following: {}.'.format(', '.join(taglist)))
    
    if not html:
        raise Exception('Error accessing site, response code {} for site {}'
                        .format(html.status_code, html.url ))
    
    html_soup = BeautifulSoup(html.text, 'lxml')
    
    return determine_scrape(tag=tag, filt=filt, html=html_soup, 
                            columns=columns,subtag=subtag)
    

#Separates out filter, replaces 
def parse_filt(filt):
    tmp = filt.split('#')
                     
#   Removes all filter attributes, leaving only filters themselves
    for n,i in enumerate(tmp):
        if i in attrlist:
            del tmp[n]
    #Replaces empty with wildcard regex
    ret_list = [x if not x == '' else '.*' for x in tmp]
            
    return ret_list[0], ret_list[1], ret_list[2], ret_list[3], ret_list[4]

# POC: Could return href's links instead of text, or return subtext, etc
def determine_ret(navstr):
    if test_ret == 'text':
        return navstr.text
    else:
        return None
##Determines which scrape based on tag
def determine_scrape(tag=None, filt=None, html=None, columns=None, subtag=''):
    if not tag:
        return None
    elif tag not in taglist:
        return None
    elif tag == 'li':
        return scrape_li(filt=filt, html=html, columns=columns, subtag=subtag)
    

if __name__ == "__main__":
#    Tag explanation:
#    URL = site to scrape
#    TAG = highest-level tag to check down from
#    SUBTAG = Tag nested within higher-level tag
#    FILT= Filter for tag, with separate inputs separated by # (Would be generated)
#       text = filter for TAG
#       subtext = filter for SUBTAG
#       href = filter for 'a href' link
#       id = filter for TAG id
#       class = filter for TAG class
    
    #Test 1: Get names of Isaacs from Wikipedia
    test_url1   = "https://en.wikipedia.org/wiki/Isaac_(name)"
    test_tag1   = 'li'
    test_filt1  = 'text#null#subtext#(Isaa)#href##id#null#class#null'
    test_cols1  = 'Name'
    test_subtag1= 'a'
    
    #Test 2: Get names of mathematicians
    test_url2   = "https://www.famousmathematicians.net/"
    test_tag2   = 'li'
    test_filt2  = 'text##subtext##href##id#null#class#(page_item\spage-item)'
    test_cols2  = 'Name'
    test_subtag2= 'a'
    
    #Test 3: Test for href crash
    test_url3   = "https://www.mensaforkids.org/teach/lesson-plans/classifying-animals/"
    test_tag3   = 'li'
    test_filt3  = 'text#(Kingdom)#subtext##null#href#null#id#null#class#null'
    test_cols3  = 'List'
    test_subtag3= ''
    
    response = requests.get(test_url2)
    print(perform_scrape(tag=test_tag2
                   ,filt=test_filt2
                   ,html=response
                   ,columns=test_cols2
                   ,subtag=test_subtag2))
