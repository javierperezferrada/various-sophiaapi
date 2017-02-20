# -*- coding: utf-8 -*-
import time
from subprocess import Popen
import os
import requests
import simplejson as json

response = requests.get("http://api.sophia-project.info/past/count/")
jresponse = json.loads(response.content)
print jresponse['docs']
pastDocs = jresponse['docs']
while(1):
    #wait five minutes
    time.sleep(300)
    response = requests.get("http://api.sophia-project.info/past/count/")
    jresponse = json.loads(response.content)
    print jresponse['docs']
    currentDocs = jresponse['docs']
    if currentDocs < pastDocs:
        pastDocs = currentDocs
    else:
        try:
        	os.system('pkill -f SophiaCollector/SophiaCollectorArticlesPast_v08022017.jar')
        except Exception as e:
    	       print e
        try:
        	p = Popen(['./start_sophiacollector.sh'])
        except Exception as e:
    	       print e
