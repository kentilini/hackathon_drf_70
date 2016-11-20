# -*- coding: utf-8 -*-
import urllib
from lxml import html


def get_prep_list(name):
    url = "http://wikimipt.org/index.php?fulltext=Search&search=" + urllib.quote(name.encode('utf8'))
    str = urllib.urlopen(url).read()
    page = html.fromstring(str)
    xpath_str = "//div[@class='searchresults']/ul[1]//div[@class='mw-search-result-heading']/a" 

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
    xpath_prop_value = "//*[@class = 'starrating-avg']"
    print len(page.xpath(xpath_prop_value))
    if len(page.xpath(xpath_prop_value)) == 5:
#        print page.xpath(xpath_prop_value)[0].xpath('/text()')
        for prop in page.xpath(xpath_prop_value):
            property_list.append(prop.text) 
    return property_list

def get_prep_by_path(link, name):
    prep = {}
    prep['name'] = name
    prep['link'] = link

    additional_props = get_prep_property(link)
    print additional_props
    if len(additional_props) > 4:
        prep['knowledge'] = additional_props[0]
        prep['teaching_skills'] = additional_props[1]
        prep['in_person'] = additional_props[2]
        prep['how_easy'] = additional_props[3]
        prep['total'] = additional_props[4]
    return prep

def get_prep_property_list(prep_name):
    list = get_prep_list(prep_name)
    result = []
    for i in range(0, len(list)):
        prep = {}
        prep['name'] = list[i][0]
        prep['link'] = list[i][1]

        additional_props = get_prep_property(list[i][1])
        #print additional_props
        if len(additional_props) > 4:
            prep['knowledge'] = additional_props[0]
            prep['teaching_skills'] = additional_props[1]
            prep['in_person'] = additional_props[2]
            prep['how_easy'] = additional_props[3]
            prep['total'] = additional_props[4]

        result.append(prep)
    return result


