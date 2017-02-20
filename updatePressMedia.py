# -*- coding: utf-8 -*-
import tweepy
import time
import requests
import simplejson as json

#credenciales de sophiaproject4
consumer_key = 'wHpPsl5nuZXEyJU6fgqPzvs3V'
consumer_secret = 'zqDiIsAMGaCvuQpwYFZCawLGjRWHH9UNW6iPq9lXdY3PEvmYTk'
access_token = '822060303907176448-YYFVabdPAF8Fw8JbB7bM2out2RUFTvn'
access_token_secret = 'ctFi2JCDuI80e6lYCZDzKu3OYTBhvzAXeS1bCfO7aKMtn'

#credenciales en produccion
#consumer_key = 'ac1yMlhXpxDAjzJWwmzagg'
#consumer_secret = 'wpMMIXxkZ3ChqANkdVkzMH0wMdb8nKMqIVaztIEwtw'
#access_token = '2177040169-5aVazrfgCpjhDOgemcIw1PvZXb3nbHtglUuAOcf'
#access_token_secret = 'iCVFeVZkhSC3hsJfISbLDbpZZAyUS2Grn6ZJUNABaWmrt'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

leer = json.loads(open('dataMedios.json').read())
#URL_API = 'http://localhost:8000/v2/'
URL_API = 'http://api.sophia-project.info/v2/'

for l in leer:
    doc = {}
    #print l['twitter']
    tweet = l
    print tweet
    l['pre_country'] = 'Chile'
    try:
        user = api.get_user(l['pre_twitter'])
        l['pre_date'] = str(user.created_at)
    except:
        l['pre_date'] = '2016-01-01 00:00:00'
    l['pre_language'] = 'Español'
    name_owner = l['pre_owner']
    name_owner = name_owner.replace(" ","_")
    name_owner = name_owner.replace("(","_")
    name_owner = name_owner.replace(")","_")
    name_owner = name_owner.replace("-","_")
    name_owner = name_owner.replace(". ","_")
    name_owner = name_owner.replace(",","_")
    l['pre_owner'] = name_owner
    print requests.post(URL_API+'pressmedia/',json.dumps(l))
