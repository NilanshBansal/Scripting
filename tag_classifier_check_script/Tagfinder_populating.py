import requests
import os
import csv 
import json
import utils.tagEx as tagFind

with open('tweets.csv','r') as f:
	reader = csv.reader(f)
	messages = []
	for row in reader:
		messages.append(row[1])

url = 'http://68.183.89.148:9090/trial'

count = 0 
all_data = []
for idx,message in enumerate(messages[1:],start=1):
    count += 1
    obj = {}
    obj['s.no'] = count
    obj['old_tags'] = tagFind.tagEx(message)
    obj['msg'] = message

    r = requests.post(url,data={'sentdata[q]':message})
    res_json = json.loads(r.json()['filters'])
    obj['new_tags'] = res_json['parents'] + res_json['children']
    
    all_data.append(obj)


writeHeader=True
if os.path.exists('devrel_tweets_comaprison.csv') :
	writeHeader=False

headlines = ['s.no','msg','old_tags','new_tags']
with open('devrel_tweets_comaprison.csv', 'w',encoding='utf-8-sig',newline='') as f:
	writer = csv.DictWriter(f,headlines)
	if writeHeader:
		writer.writeheader()
	for data in all_data:
		writer.writerow(data)

