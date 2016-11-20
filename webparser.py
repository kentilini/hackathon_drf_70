# -*- coding: utf-8 -*-
import urllib
from lxml import html


def get_prep_list(name):
    url = "http://wikimipt.org/index.php?search=" + urllib.quote(name.encode('utf8'))
    str = urllib.urlopen(url).read()
    page = html.fromstring(str)
    xpath_str = "//*[@id= 'mw-content-text']//li/div[@class='mw-search-result-heading']/a" 

    indx = 0
    prep_list = []
    for link in page.xpath(xpath_str):
        prep_name = link.get('title')
        prep_list.append([prep_name, "http://wikimipt.org" + link.get("href")])
        indx += 1
        if indx > 3:
            return prep_list
    return prep_list

def get_prep_property(path):
    str = urllib.urlopen(path).read()
    page = html.fromstring(str)
    property_list = []
    for i in range(1, 6):
        xpath_prop_name = "//*[@id='mw-content-text']/table/tr[8]/td/table/tr[" + `i` + "]/td[1]"
        xpath_prop_value = "//*[@id='mw-content-text']/table/tr[8]/td/table/tr[" + `i` + "]/td[2]/div/span[contains(@class, 'starrating-avg')]"
        if len(page.xpath(xpath_prop_name)) > i:
            property_list.append( [page.xpath(xpath_prop_name)[i].text, page.xpath(xpath_prop_value)[i].text] )
    return property_list

def get_prep_by_path(link, name):
    prep = {}
    prep['name'] = name
    prep['link'] = link

    additional_props = get_prep_property(link)
    # print additional_props
    prep['knowledge'] = additional_props[0][1]
    prep['teaching_skills'] = additional_props[1][1]
    prep['in_person'] = additional_props[2][1]
    prep['how_easy'] = additional_props[3][1]
    prep['total'] = additional_props[4][1]

def get_prep_property_list(prep_name):
    list = get_prep_list(prep_name)
    result = []
    for i in range(0, len(list)):
        prep = {}
        prep['name'] = list[i][0]
        prep['link'] = list[i][1]

        additional_props = get_prep_property(list[i][1])
        #print additional_props
        if len(additional_props) > 0:
            prep['knowledge'] = additional_props[0][1]
            prep['teaching_skills'] = additional_props[1][1]
            prep['in_person'] = additional_props[2][1]
            prep['how_easy'] = additional_props[3][1]
            prep['total'] = additional_props[4][1]

        result.append(prep)
    return result


