from pyelasticsearch import ElasticSearch
import datetime
import simplejson as json
from django.http import QueryDict

es = ElasticSearch('http://localhost:9202/')


paginationSize = 10000
index = 'articles'

beginDate = "2016-07-01 00:00:00"
endDate = "2017-01-30 23:59:59"
#print beginDate
#print endDate
dateBeginDate = datetime.datetime.strptime(beginDate, "%Y-%m-%d %H:%M:%S")
dateEndDate = datetime.datetime.strptime(endDate, "%Y-%m-%d %H:%M:%S")
delta = dateEndDate - dateBeginDate
#print delta.days
for i in range(int(delta.days)):
    auxStartDate = dateBeginDate + datetime.timedelta(days=i)
    auxEndDate = dateBeginDate + datetime.timedelta(days=i+1)
    #print str(auxStartDate)
    #print str(auxEndDate)
    query = {'query':{
            "range" : {
                "art_date" : {"gte":str(auxStartDate),
                            "lte":str(auxEndDate) }
            }
        }
    }
    #print query
    result = es.search(query,size=10000,index=index)
    for r in result['hits']['hits']:
        #print r['_source']['pub_content']
        query2 = {'query':{
                "bool":{
                    "must":[
                        {"match_phrase" : {"art_content":r['_source']['art_content']}}
                    ],
                    "must_not":{
                        "match" : {"_id":r['_id']}
                    }
                }
            }
        }
        partialResult = es.search(query2,size=paginationSize,index=index)
        print partialResult['hits']['total']
        if partialResult['hits']['total'] > 0:
            doc = {}
            doc['art_repeated'] = 1
            es.update(index,index,r['_id'],doc=doc)
        else:
            doc = {}
            doc['art_repeated'] = 0
            es.update(index,index,r['_id'],doc=doc)
        #for pr in partialResult['hits']['hits']:
            #print pr['_source']['art_content']
