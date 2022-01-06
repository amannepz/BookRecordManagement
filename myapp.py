import requests
import json
URL = "http://127.0.0.1:8000/brmapp/aman"
data={
'title': 'Python Programming',
'price': 777,
'author': 'Saurabh Shukla',
'publisher': 'Aman Nepali',
}
json_data = json.dumps(data)
r = requests.post(url= URL ,data = json_data)
data = r.json()
print(data)
