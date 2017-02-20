#!/bin/bash

java -cp SophiaCollector/SophiaCollectorArticlesPast_v07022017.jar:\
SophiaCollector/lib/commons-codec-1.10.jar:\
SophiaCollector/lib/commons-io-2.4.jar:\
SophiaCollector/lib/commons-logging-1.2.jar:\
SophiaCollector/lib/httpasyncclient-4.1.1.jar:\
SophiaCollector/lib/httpclient-4.5.2.jar:\
SophiaCollector/lib/httpcore-4.4.4.jar:\
SophiaCollector/lib/httpcore-nio-4.4.4.jar:\
SophiaCollector/lib/httpmime-4.5.2.jar:\
SophiaCollector/lib/jackson-core-asl-1.9.13.jar:\
SophiaCollector/lib/jackson-mapper-asl-1.9.13.jar:\
SophiaCollector/lib/json-20160212.jar:\
SophiaCollector/lib/jsoup-1.8.3.jar:\
SophiaCollector/lib/mongo-java-driver-3.2.2.jar:\
SophiaCollector/lib/signpost-commonshttp4-1.2.1.2.jar:\
SophiaCollector/lib/signpost-core-1.2.1.2.jar:\
SophiaCollector/lib/unirest-java-1.4.9.jar \
cl.uach.inf.sophia.datacollection.SophiaCollector
                                                         
