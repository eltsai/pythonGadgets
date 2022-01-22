#!/usr/bin/env python3
# coding=utf-8
# author=eltsai

years = [str(year) for year in range(2015, 2022)]
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
name='' # put your name here

import urllib.request
from html_table_parser.parser import HTMLTableParser
from bs4 import BeautifulSoup


def containsDay(string):
    if any([day in string for day in days]):
        return True
    return False

def containsName(string):
    return name in string

starter_week = "https://secure.math.ucla.edu/seminars/weekly_list.php?t=1642287527"
cur = starter_week
count = 0
while count <= 500:
    # print(count)
    count += 1
    # try:
    f = urllib.request.urlopen(cur)
    webpage = f.read().decode('utf-8')
    cur_year = 2022
    for year in years:
        if year in webpage:
            cur_year = year
    p = HTMLTableParser()
    p.feed(webpage)
    # print(year)
    date = None
    # print(p.tables[0][1:])
    for line_list in p.tables[0][1:]:
        for line in line_list:
            if containsDay(line):
                date = line
            if containsName(line):
                print(date, cur_year, line, line_list[line_list.index(line)+1])
                
    bsObj = BeautifulSoup(webpage, 'html.parser')

    links = bsObj.findAll('a')
    finalLinks = set()
    found = False
    link_list = []
    for link in links:
        #print(link.attrs)
        # if 'title' in link.attrs and link.attrs['title'] == 'Previous Week':
        #     print(link.attrs['href'])
        if 'href' in link.attrs and '/seminars/weekly_list.php?t=' in link.attrs['href']:
            found =True
            link_list.append('https://secure.math.ucla.edu' + link.attrs['href'])
            # break
            # print(link.attrs)
        
    if len(link_list) <= 2:
        print("No previous week!")
        break

    cur = link_list[1]

# except:
#     print(f"failed to open {starter_week}")