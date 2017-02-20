from pyelasticsearch import ElasticSearch

es = ElasticSearch('http://localhost:9202/')


paginationSize = 10
index = 'articles'
query = {'query':{
        "match" : {
            "art_content" : "articulo no posee contenido"
        }
    }
}
result = es.search(query,size=paginationSize,index=index)
for r in result['hits']['hits']:
    if r['art_content']=="articulo no posee contenido":
    	print r

print result['hits']['total']
