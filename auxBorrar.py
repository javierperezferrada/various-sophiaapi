@csrf_exempt
#@protected_resource()
def searchPage(request,pageNum):
    #This function return a search result
    es = ElasticSearch('http://localhost:9202/')
    if request.method == 'POST':

        #save in variables the post content
        search = json.loads(request.body)
        try:
            index = search['index']
        except Exception as e:
            error = {"error":"the index field is required in a search"}
            print e
            return JsonResponse(error)
        #init query
        dateField = index[0:3]+"_date"
        try:
            sort = search['sort']
            #if sort == 'score':
            #    sort = '_score'
        except:
            sort = dateField
        if sort == '_score':
            query={ 'sort':[{sort:{'order':'desc'}}],"min_score": 0.5,"query": {"bool": {}}}
        else:
            query={ 'sort':[{sort:{'order':'desc'}},{ "_score": { "order": "desc" }}],"min_score": 0.5,"query": {"bool": {}}}
        try:
            #save de fields in the post doc
            fields = search['fields']
        except Exception as e:
            error = {"error":"the fields field is required in a search"}
            print e
            return JsonResponse(error)
        fieldMust = []
        auxAnd = False
        try:
            if search['and']:
                #if search is 'and' make the query part to 'must'
                auxAnd = True
                must = search['and']
                for m in must:
                    for f in fields:
                        key = m.keys()
                        value = m.values()
                        mustDoc = {key[0]:{f:value[0]}}
                        fieldMust.append(mustDoc)
        except:
            pass
        try:
            if search['art_name_press_source']:
                fieldMust.append({"match":{'art_name_press_source':search['art_name_press_source']}})
                auxAnd = True
        except:
            pass
        try:
            if search['pub_username']:
                fieldMust.append({"match":{'pub_username':search['pub_username']}})
                auxAnd = True
        except:
            pass
        try:
            if search['art_category']:
                fieldMust.append({"match":{'art_category':search['art_category']}})
                auxAnd = True
        except:
            pass
        if auxAnd:
            query['query']['bool']['must']=fieldMust
        fieldShould = []
        auxShould = False
        try:
            if search['or']:
                auxShould = True
                #if search is 'or' make the query part to 'should'
                should = search['or']
                for s in should:
                    for f in fields:
                        key = s.keys()
                        value = s.values()
                        shouldDoc = {key[0]:{f:value[0]}}
                        fieldShould.append(shouldDoc)
        except:
            pass
        try:
            if search['idYes']:
                auxShould = True
                #if search is dates beetwen shows
                ids = search['idYes']
                for i in ids:
                    idYesDocument = {"match":{"_id":i}}
                    fieldShould.append(idYesDocument)
        except:
            pass
        if auxShould:
            query['query']['bool']['should']=fieldShould

        fieldMustNot = []
        auxNot = False
        try:
            if search['not_and']:
                auxNot = True
                #if search is 'not_and' make the query part to 'must_not'
                must_not = search['not_and']
                #print must_not
                for mn in must_not:
                    for f in fields:
                        key = mn.keys()
                        value = mn.values()
                        mustNotDoc = {key[0]:{f:value[0]}}
                        fieldMustNot.append(mustNotDoc)
        except Exception as e:
            pass
        try:
            if search['idNot']:
                auxNot = True
                #if search is dates beetwen shows
                ids = search['idNot']
                for i in ids:
                    idNotDocument = {"match":{"_id":i}}
                    fieldMustNot.append(idNotDocument)
        except:
            pass
        if auxNot:
            query['query']['bool']['must_not']=fieldMustNot
        try:
            if search['dates']:
                #if search is dates beetwen shows
                dateField = search["index"][0:3]+"_date"
                dates = search['dates']
                query['filter']={
                                "range": {
                                  dateField: {
                                    "from": dates["startdate"] ,
                                    "to": dates["enddate"]
                                  }}}
        except:
            pass


        try:
            if search['pre_owner']:
                #print 'pre_owner'
                auxQuery = {"query":{"match":{"pre_owner":search['pre_owner'].replace(" ","_")}},"_source":"pre_twitter"}
                twitter = es.search(auxQuery,size=10000,index="pressmedia")
                #print "twitter['hits']['total']"
                #print twitter['hits']['total']
                if sort == '_score':
                    filteredQuery = {'sort':[{sort:{'order':'desc'}}],"min_score": 0.5,"query": {
                              "filtered": {
                                "query": {},
                                "filter": {
                                  "bool": {
                                    "should": []
                                  }
                                }
                              }
                            }
                            }
                else:
                    filteredQuery = {'sort':[{sort:{'order':'desc'}},{ "_score": { "order": "desc" }}],"min_score": 0.5,"query": {
                              "filtered": {
                                "query": {},
                                "filter": {
                                  "bool": {
                                    "should": []
                                  }
                                }
                              }
                            }
                            }
                for t in twitter['hits']['hits']:
                    if index == "articles":
                        filteredQuery['query']['filtered']['filter']['bool']['should'].append({"term": {"art_name_press_source":t['_source']['pre_twitter'].lower()}})
                    if index == "publications":
                       filteredQuery['query']['filtered']['filter']['bool']['should'].append({"term": {"pre_username":t['_source']['pre_twitter'].lower()}})
                filteredQuery['query']['filtered']['query'] = query['query']
                #print 'filteredQuery'
                #print json.dumps(filteredQuery)
                query = filteredQuery

        except Exception as e:
            pass
        #print query
        try:
            if search['repeated'] == 1:
                print 'solicita repetidos'
                query["aggs"] = {
                            "articlesByPressMedia":{
                                "terms":{"field":"art_name_press_source","size":1000},
                                "aggs":{
                                    "repeated":{"sum":{"field":"art_repeated"}}
                                }
                                }
                            }
        except:
            pass
        searchFrom = (int(pageNum)-1) * int(paginationSize)
        #print 'query'
        #print query


        result = es.search(query,size=paginationSize,es_from=searchFrom,index=index)
        totalPages =  math.ceil(result['hits']['total']/float(paginationSize))
        result['totalPages']=totalPages
        result['page'] = pageNum
        return JsonResponse(result)
