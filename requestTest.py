# -*- coding: utf-8 -*-
__author__ = 'RicardoMoya'

from bs4 import BeautifulSoup
import requests

url = "https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending"

# Realizamos la petición a la web
user_agent = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept_encoding':'gzip,deflate,br','Accept_language':'en-US.en;q=0.5','Referer':'https://www.google.com/','Upgrade_insecure_requests':'1'}
req = requests.get(url, headers=user_agent)
print req.content
