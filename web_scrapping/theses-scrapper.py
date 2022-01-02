import requests
import pandas as pd
import time
from bs4 import BeautifulSoup as bs


def full_scrapper(link):
    """
    Created by Vallian Sayoga
    
    The base function to scrape UMich's theses database.
    
    link: URL used for scrapping from result search for example:
        'https://deepblue.lib.umich.edu/browse?rpp=25&offset=0&etal=-1&sort_by=2&type=dateissued&starts_with=2021&order=DESC'
        with url pattern:
            offset = 0
            offset += 25 for each loop    
    """    
    
    # First URL crawl
    base = 'https://deepblue.lib.umich.edu'
    url = link
    r = requests.get(url)
    c = r.content
    soup = bs(c, 'html.parser')
    
    # Second URL crawl
    metadata = soup.find("a", text="Show full item record", href=True)
    rm = requests.get(base + metadata['href'])
    cm = rm.content
    soupm = bs(cm, 'html.parser')
    
    # There are odd and even table rows
    all_odd = soupm.find_all('tr', {'class': 'ds-table-row odd'})
    all_even = soupm.find_all('tr', {'class': 'ds-table-row even'})
    
    d = {}
    d['author'] = all_odd[0].find_all('td')[1].text
    for i in range(len(all_odd)):
        if all_odd[i].find_all('td', {'class':"label-cell"})[0].text == 'dc.date.issued':
            try:
                d['date_issued'] = all_odd[i].find_all("td", {"class":"word-break"})[0].text
            except:
                d['date_issued'] = None
                
        if all_odd[i].find_all('td', {'class':"label-cell"})[0].text == 'dc.subject.hlbtoplevel':
            try:
                d['subject'] = (all_odd[i].find_all("td", {"class":"word-break"})[0].text)
            except:
                d['subject'] = None
                
        if all_odd[i].find_all('td', {'class':"label-cell"})[0].text == 'dc.contributor.affiliationumcampus':
            try:
                d['campus'] = (all_odd[i].find_all("td", {"class":"word-break"})[0].text)
            except:
                d['campus'] = None
                
        if all_odd[i].find_all('td', {'class':"label-cell"})[0].text == 'dc.owningcollname':
            try:
                d['department'] = (all_odd[i].find_all("td", {"class":"word-break"})[0].text)
            except:
                d['department'] = None
                
        if all_odd[i].find_all('td', {'class':"label-cell"})[0].text == 'dc.title':
            try:
                d['title'] = (all_odd[i].find_all("td", {"class":"word-break"})[0].text)
            except:
                d['title'] = None
                
        if all_odd[i].find_all('td', {'class':"label-cell"})[0].text == 'dc.language.iso':
            try:
                d['language'] = (all_odd[i].find_all("td", {"class":"word-break"})[0].text)
            except:
                d['language'] = None
                
        if all_odd[i].find_all('td', {'class':"label-cell"})[0].text == 'dc.type':
            try:
                d['type'] = (all_odd[i].find_all("td", {"class":"word-break"})[0].text)
            except:
                d['type'] = None
                
        if all_odd[i].find_all('td', {'class':"label-cell"})[0].text == 'dc.description.peerreviewed':
            try:
                d['peerreviewed'] = (all_odd[i].find_all("td", {"class":"word-break"})[0].text)
            except:
                d['peerreviewed'] = None
                
        if all_odd[i].find_all('td', {'class':"label-cell"})[0].text == 'dc.identifier.url':
            try:
                d['url_identifier'] = (all_odd[i].find_all("td", {"class":"word-break"})[0].text)
            except:
                d['url_identifier'] = None
                
        if all_odd[i].find_all('td', {'class':"label-cell"})[0].text == 'dc.identifier.uri':
            try:
                d['url_identifier'] = all_odd[i].find_all("td", {"class":"word-break"})[0].text
            except:
                d['url_identifier'] = None
                
            
    for i in range(len(all_even)):
        if all_even[i].find_all('td', {'class':"label-cell"})[0].text == 'dc.date.issued':
            try:
                d['date_issued'] = all_even[i].find_all("td", {"class":"word-break"})[0].text
            except:
                d['date_issued'] = None
                
        if all_even[i].find_all('td', {'class':"label-cell"})[0].text == 'dc.subject.hlbtoplevel':
            try:
                d['subject'] = (all_even[i].find_all("td", {"class":"word-break"})[0].text)
            except:
                d['subject'] = None
                
        if all_even[i].find_all('td', {'class':"label-cell"})[0].text == 'dc.contributor.affiliationumcampus':
            try:
                d['campus'] = (all_even[i].find_all("td", {"class":"word-break"})[0].text)
            except:
                d['campus'] = None
                
        if all_even[i].find_all('td', {'class':"label-cell"})[0].text == 'dc.owningcollname':
            try:
                d['department'] = (all_even[i].find_all("td", {"class":"word-break"})[0].text)
            except:
                d['department'] = None
                
        if all_even[i].find_all('td', {'class':"label-cell"})[0].text == 'dc.title':
            try:
                d['title'] = (all_even[i].find_all("td", {"class":"word-break"})[0].text)
            except:
                d['title'] = None
                
        if all_even[i].find_all('td', {'class':"label-cell"})[0].text == 'dc.language.iso':
            try:
                d['language'] = (all_even[i].find_all("td", {"class":"word-break"})[0].text)
            except:
                d['language'] = None
                
        if all_even[i].find_all('td', {'class':"label-cell"})[0].text == 'dc.type':
            try:
                d['type'] = (all_even[i].find_all("td", {"class":"word-break"})[0].text)
            except:
                d['type'] = None
                
        if all_even[i].find_all('td', {'class':"label-cell"})[0].text == 'dc.description.peerreviewed':
            try:
                d['peerreviewed'] = (all_even[i].find_all("td", {"class":"word-break"})[0].text)
            except:
                d['peerreviewed'] = None
                
        if all_even[i].find_all('td', {'class':"label-cell"})[0].text == 'dc.identifier.url':
            try:
                d['url_identifier'] = (all_even[i].find_all("td", {"class":"word-break"})[0].text)
            except:
                d['url_identifier'] = None
                
        if all_even[i].find_all('td', {'class':"label-cell"})[0].text == 'dc.identifier.uri':
            try:
                d['url_identifier'] = all_even[i].find_all("td", {"class":"word-break"})[0].text
            except:
                d['url_identifier'] = None
          
    return d

# Testing on 25 titles on a single page
# url = 'https://deepblue.lib.umich.edu/browse?rpp=25&offset=0&etal=-1&sort_by=2&type=dateissued&starts_with=2021&order=DESC'
# r = requests.get(url)
# c = r.content
# soup = bs(c, 'html.parser')
#
# l = list()
# for each_link in soup.find_all('div', {'class':"artifact-title"}):
#   
#     element = each_link.find('a', href=True)
#     full_path = base_url + element['href']
#     l.append(full_scrapper(full_path))
# ---------------------------------------------------------------------------------------------------------------------------------------
# Scrapping 2000 titles
# l = []
# loops = 1
# for offset in range(2025, 25):
#     print(f'Doing the {loops}th loop')
#     loops += 1
#     url = f'https://deepblue.lib.umich.edu/browse?rpp=25&offset={offset}&etal=-1&sort_by=2&type=dateissued&starts_with=2021&order=DESC'
#     r = requests.get(url)
#     c = r.content
#     soup = bs(c, 'html.parser')
# 
#     for each_link in soup.find_all('div', {'class':"artifact-title"}):
#         element = each_link.find('a', href=True)
#         full_path = base_url + element['href']
#         l.append(full_scrapper(full_path))
#  
#     for i in range(3):
#         print(f'Delaying for {i+1} second(s)')
#         time.sleep(1)
#     print('-'*15)
