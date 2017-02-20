# -*- coding: utf-8 -*-
__author__ = 'RicardoMoya'

from bs4 import BeautifulSoup
import requests

url = "http://ellibero.cl/opinion/mama-parece-que-me-comi-un-sapo/"

# Realizamos la petición a la web
user_agent = {'User-agent': 'Mozilla/5.0'}
req = requests.get(url, headers=user_agent)

# Comprobamos que la petición nos devuelve un Status Code = 200
statusCode = req.status_code
if statusCode == 200:

    # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
    html = BeautifulSoup(req.text,"html.parser")

    # Obtenemos todos los divs donde estan las entradas
    entradas = html.find_all('p')
    print entradas
    for i in entradas:
        print i.get_text()
        print html.title.get_text()
    # Recorremos todas las entradas para extraer el título, autor y fecha

else:
    print "Status Code %d" %statusCode
