#example code to request oauth in python
import requests
import requests.auth
import simplejson as json
from collections import OrderedDict
from urllib import urlencode
import base64

URL_BASE_API = "http://localhost:8000/"
#URL_BASE_API = "http://api.sophia-project.info/"
PARAM_LOGIN_URL = URL_BASE_API + "accounts/login"
TOKEN_URL = URL_BASE_API + "o/token/"
#client = requests.session()
#client.get(PARAM_LOGIN_URL)
#csrftoken = client.cookies['csrftoken']
#leer token desde un archivo para que no este en GIT
#token = "T5mYRgebeMDBxO8EGgiBLyytczMPot"

#headers = {"Authorization":"Bearer "+token}
#headers["X-CSRFToken"] = csrftoken

#r = client.get(url, headers=headers)
#print r.content


#client.get(login_url)
#csrftoken = client.cookies['csrftoken']
#headers["X-CSRFToken"] = csrftoken
#data = {}
#r = client.post(url,data=data, headers=headers)
#print r.content
print 'obteniendo un nuevo token-----------------------------------------------'
#information generated in /o/applications
client_id = "rbClH5YE3XGbKaz9r3vnIi8CVa0KTdK7eCsN5ajo"
client_secret = "1J67W55UjD85BLq9byszdbpJ2bQ015sZe6KM6VMjvMHXrZOUV7GPQ5zK4FXTUyBeMsPsctALiTFlhS6FGuEeizNcULg4HxfOmUByyjUbScv6NJN50wp7BwGS6J6bkcAk"
redirect_uri = "http://localhost:8000/test/"

#build an authorization link for your provider
#using the client_id and authorization_url

authorization_url = "http://localhost:8000/o/authorize/"

#authenticate requests
client = requests.session()
client.get(PARAM_LOGIN_URL)
csrftoken = client.cookies['csrftoken']
#print csrftoken
login_data = {"username":"javier","password":"PODsatelite","csrfmiddlewaretoken":csrftoken}
r1 = client.post(PARAM_LOGIN_URL,data=login_data)
#print 'first r1----------------------------------------------------------------'
#print r1.content
client.get(redirect_uri)
csrftoken = client.cookies['csrftoken']

params = OrderedDict([('client_id', client_id), ('response_type', "code"), ('state', "random_state_string"),("redirect_uri",redirect_uri)])
r3 = client.get(authorization_url, params=urlencode(params))
#print r3.content

headers = {}
headers["X-CSRFToken"] = csrftoken
data = {"client_id":client_id,"redirect_uri":redirect_uri,"csrfmiddlewaretoken":csrftoken ,"response_type":"code","scope":"read write","state":"random_state_string","allow":"Authorize"}
r4 = client.post(authorization_url,data=data,headers=headers)
print r4.content
jsonResponse = json.loads(r4.content)
CODE = jsonResponse['code']

try:
    data = {
        'code': CODE,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    headers = {
        'Authorization': 'Basic %s' % base64.b64encode('%s:%s' % (client_id, client_secret))
    }
    r = requests.post(TOKEN_URL, data=data, headers=headers)
    print r.content
except Exception as e:
    print e
    pass
