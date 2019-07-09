"""
Created on Tue July 09 11:29:14 2019
@author: nilanshbansal
"""
import json
import csv
import os
import requests


with open('devrel_tweets.csv', 'r') as f:
    reader = csv.reader(f)
    messages = []
    version1_tags = []
    suggested_tags = []
    for row in reader:
        messages.append(row[0])
        version1_tags.append(row[1])
        suggested_tags.append(row[2])

url = 'http://68.183.89.148:9090/trial'
count = 0
all_data = []
for idx, message in enumerate(messages[1:], start=1):
    count += 1
    obj = {}
    r = requests.post(url, data={'sentdata[q]': message})
    res_json = json.loads(r.json()['filters'])
    obj['s.no'] = count
    obj['version2_tags'] = res_json['TOPIC'] + res_json['SUBTOPIC']
    obj['Tweet'] = message
    obj['version1_tags'] = version1_tags[idx]
    obj['suggested_tags'] = suggested_tags[idx]
    all_data.append(obj)


writeHeader = True
if os.path.exists('twitter_devrel_analysis_version2.csv'):
    writeHeader = False

headlines = ['s.no', 'Tweet', 'version1_tags',
             'version2_tags', 'suggested_tags']
with open('twitter_devrel_analysis_version2.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, headlines)
    if writeHeader:
        writer.writeheader()
    for data in all_data:
        writer.writerow(data)
