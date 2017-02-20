# -*- coding: utf-8 -*-
import time
import pymongo
from pymongo import MongoClient
import json
import requests
import subprocess import Popen
import os


client = MongoClient('localhost', 27017)
db = client['SophiaCollectorNew']
collection = db['Tweets']

auxTweets = 0
auxArticles = 0
firstCount = collection.find({'to_download': 1}).count()

while(1):
    #wait a minute
    time.sleep(60)
    currentCount = collection.find({'to_download': 1}).count()
    print "Time : %s" % time.ctime()
    if firstCount < currentCount:
        print 'Tweets Collector working correctly'
        auxTweets = 0
    else:
        if auxTweets > 5:
            print '----------------Failed Tweets Collector---------------------'
            #run de script to both TweetsCollector
            try:
                #subprocess.call(['./start_sophiacollectorTweets.sh'])
                os.system('pkill -f SophiaCollector/SophiaCollectorTweets_v27012017.jar')
                p = Popen(['./start_sophiacollectorTweets.sh'])
            except Exception as e:
                print e
        else:
            auxTweets += 1
    if firstCount > currentCount:
        print 'Articles Collector working correctly'
        auxArticles = 0
    else:
        if auxArticles > 4:
            print '----------------Failed Articles Collector-------------------'
            ##run de script to both ArticlesCollector
            try:
                #subprocess.call(['./start_sophiacollector.sh'])
                os.system('pkill -f SophiaCollector/SophiaCollectorArticles_v27012017.jar')
                p = Popen(['./start_sophiacollector.sh'])
            except Exception as e:
                print e
        else:
            auxArticles += 1
    firstCount = currentCount
