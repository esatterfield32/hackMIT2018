import requests
import json

#r = requests.get('http://127.0.0.1:5000/')
#print(r.json())

r = requests.post('http://127.0.0.1:5000/', data = {'id':'60326553'})
print(r.json())   
