"""
Created on Thu Aug 01 14:00 2019
@author: nilanshbansal
"""
import json
import csv
import os
import requests


with open('comments.csv', 'r') as f:
    reader = csv.reader(f)
    messages = []
    for row in reader:
        messages.append(row[1])


url = 'http://139.59.35.166:9090/trial'
count = 0
all_data = []
for idx, message in enumerate(messages[1:], start=1):
    count += 1
    obj = {}
    r = requests.post(url, data={'sentdata[q]': message})
    res_json = json.loads(r.json()['filters'])
    obj['s.no'] = count
    try:
        obj['tags'] = res_json['TOPIC'] 
    except:
        obj['tags'] = ''
    obj['comment'] = message
    all_data.append(obj)


writeHeader = True
if os.path.exists('github_comment_analysis_v3.csv'):
    writeHeader = False

headlines = ['s.no', 'comment','tags']
with open('github_comment_analysis_v3.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, headlines)
    if writeHeader:
        writer.writeheader()
    for data in all_data:
        writer.writerow(data)
