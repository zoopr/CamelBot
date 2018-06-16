import discord
import requests
from bs4 import BeautifulSoup
import urllib
import re

import Constants


async def web_search(message, client):
    search_query = message.content[7:].strip(' ')
    print('Searching web for: ' + search_query)
    search_query = search_query.replace(' ', '+')

    #language parameter can be added as first one in GOOGLE_IMGSEARCH_HEAD_URL.
    search_url = Constants.GOOGLE_IMGSEARCH_HEAD_URL + "{}".format(search_query) + "&hl=en_US"# + IMGSEARCH_FOOT_URL
    search_response = requests.get(search_url)
    search_response_text = search_response.text

    soup = BeautifulSoup(search_response_text, "html.parser")
    valid_link = ""
    for link in soup.findAll('a'):
        if link.get('href').startswith('/url?q='):
            candidate = urllib.parse.unquote(link.get('href')[7:])
            if candidate.find("/settings/ads/preferences") != 0: # could just be "/" to filter out all local links to google.com
                valid_link = candidate.split('&')[0]
                break;

    return valid_link

async def image_search(message, client):
    search_query = message.content[3:].strip(' ')
    print('Searching for: ' + search_query)
    search_query = search_query.replace(' ', '+')

    search_url = Constants.GOOGLE_IMGSEARCH_HEAD_URL + search_query + Constants.GOOGLE_IMGSEARCH_FOOT_URL
    search_response = requests.get(search_url)
    search_response_text = search_response.text

    soup = BeautifulSoup(search_response_text, "html.parser")
    valid_links = []
    for link in soup.findAll('a'):
        print('Link:::: ' + str(link))
        if link.get('href').startswith('/imgres?imgurl='):
            valid_links.append(link.get('href')[15:])

    for i in range(0, len(valid_links)):
        print(valid_links[i])

    link_to_send = valid_links[0][:valid_links[0].index('&')]

    return link_to_send
