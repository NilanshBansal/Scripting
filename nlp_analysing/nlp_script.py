import requests
import time
import csv
import os
import json

input_csv = "twitter_corpus"
output_csv = input_csv + "_stanford"

with open(input_csv + ".csv", 'r') as f:
    reader = csv.reader(f)
    messages = []
    labelled_sentiments = []
    for row in reader:
        messages.append(row[0])
        labelled_sentiments.append(row[1])

## STANFORD ANALYSIS
url = 'http://3.135.227.133:8000/api/getnlpscore'

start = time.time()

count = 0 
all_data = []

for idx, message in enumerate(messages[1:], start=1):
    obj = {}
    count += 1
    obj['s.no'] = count
    obj['text'] = message
    obj['labelled_sentiment'] = labelled_sentiments[idx]
    try:
        senti_params = {"type": "plain", "TextToAnalyse": str(message)}
        senti_res = requests.post(url, data=senti_params)
        jsn = json.loads(senti_res.text)
        obj['stanford_sentiment'] = jsn['sentiment']
        if jsn['type']:
            obj['stanford_qa'] = jsn['type']
        else:
            obj['stanford_qa'] = 'unpredcitable'
    except Exception as e:
        print(str(e))

    all_data.append(obj)

headlines = ['s.no','text','labelled_sentiment','stanford_sentiment','stanford_qa']
with open(output_csv + ".csv",'w',encoding='utf-8-sig',newline='') as f:
    writer = csv.DictWriter(f,headlines)
    writer.writeheader()
    for data in all_data:
        writer.writerow(data)

print(time.time()-start)