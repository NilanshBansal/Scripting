import requests
import os
import csv 
import json

with open('twitter_timeline.csv','r') as f:
	reader = csv.reader(f)
	messages = []
	old_tags = []
	for row in reader:
		messages.append(row[1])
		old_tags.append(row[2])

url = 'http://68.183.89.148:9090/trial'
count = 0 
all_data = []
for idx,message in enumerate(messages[1:1500],start=1):
	count += 1
	obj = {}
	r = requests.post(url,data={'sentdata[q]':message})
	res_json = json.loads(r.json()['filters'])
	obj['s.no'] = count
	obj['new_tags'] = res_json['parents'] + res_json['children']
	print(obj['new_tags'])
	obj['msg'] = message
	obj['old_tags'] = old_tags[idx]
	all_data.append(obj)


writeHeader=True
if os.path.exists('twitter_dataset_1500.csv') :
	writeHeader=False

headlines = ['s.no','msg','old_tags','new_tags']
with open('twitter_dataset_1500.csv', 'w',encoding='utf-8-sig',newline='') as f:
	writer = csv.DictWriter(f,headlines)
	if writeHeader:
		writer.writeheader()
	for data in all_data:
		writer.writerow(data)

