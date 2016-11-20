# -*- coding: utf-8 -*-
import urllib
from lxml import html


def get_prep_list(name):
    url = "http://wikimipt.org/index.php?search=" + urllib.quote(name)
    str = urllib.urlopen(url).read()
    page = html.fromstring(str)
    xpath_str = "            // * [ @ id = 'mw-content-text'] / div / ul[1] / li[1] / div[1] / a"

    prep_list = []
    for link in page.xpath(xpath_str):
        prep_name = link.get('title')
        prep_list.append([prep_name, "http://wikimipt.org" + link.get("href")])
    return prep_list

def get_prep_property(path):
    str = urllib.urlopen(path).read()
    page = html.fromstring(str)
    property_list = []
    for i in range(1, 6):
        xpath_prop_name = "//*[@id='mw-content-text']/table/tr[8]/td/table/tr[" + `i` + "]/td[1]"
        xpath_prop_value = "//*[@id='mw-content-text']/table/tr[8]/td/table/tr[" + `i` + "]/td[2]/div/span[contains(@class, 'starrating-avg')]"

        property_list.append( [page.xpath(xpath_prop_name)[0].text, page.xpath(xpath_prop_value)[0].text] )
    return property_list


def get_prep_property_list(prep_name):
    list = get_prep_list(prep_name)
    result = []
    for i in range(0, len(list)):
        prep = []
        prep.append(['name', list[i][0]])
        prep.append(['link', list[i][1]])

        additional_props = get_prep_property(list[i][1])
        print additional_props
        prep.append(['knowledge', additional_props[0][1]])
        prep.append(['teaching_skills', additional_props[1][1]])
        prep.append(['in_person', additional_props[2][1]])
        prep.append(['how_easy', additional_props[3][1]])
        prep.append(['total', additional_props[4][1]])

        result.append(prep)
    return result


