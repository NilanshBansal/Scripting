import requests
import os
import csv 
import json

with open('tweets.csv','r') as f:
	reader = csv.reader(f)
	messages = []
	old_tags = []
	for row in reader:
		messages.append(row[1])

url = 'http://68.183.89.148:9090/trial'
count = 0 
all_data = []
for idx,message in enumerate(messages[1:],start=1):
	count += 1
	obj = {}
	r = requests.post(url,data={'sentdata[q]':message})
	res_json = json.loads(r.json()['filters'])
	obj['s.no'] = count
	obj['tags'] = res_json['parents'] + res_json['children']
	obj['tweets'] = message
	all_data.append(obj)


writeHeader=True
if os.path.exists('devrel_tweets.csv') :
	writeHeader=False

headlines = ['s.no','tweets','tags']
with open('devrel_tweets.csv', 'w',encoding='utf-8-sig',newline='') as f:
	writer = csv.DictWriter(f,headlines)
	if writeHeader:
		writer.writeheader()
	for data in all_data:
		writer.writerow(data)

