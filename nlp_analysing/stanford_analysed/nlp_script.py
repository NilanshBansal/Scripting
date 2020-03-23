import requests
import time
import csv
import os
import json

input_csv = "slack_chats_stanford"
output_csv = input_csv + "_bert"

with open(input_csv + ".csv", 'r') as f:
    reader = csv.reader(f)
    messages = []
    stanford_sentiments = []
    stanford_qas = []
    for row in reader:
        messages.append(row[1])
        stanford_sentiments.append(row[2])
        stanford_qas.append(row[3])

## STANFORD ANALYSIS
url = 'http://3.135.227.133:8080/api/getnlpscore'

start = time.time()

count = 0 
all_data = []

for idx, message in enumerate(messages[1:], start=1):
    obj = {}
    count += 1
    print(count)
    obj['s.no'] = count
    obj['text'] = message
    obj['stanford_sentiment'] = stanford_sentiments[idx]
    obj['stanford_qa'] = stanford_qas[idx]
    try:
        senti_params = {"type": "plain", "TextToAnalyse": str(message)}
        senti_res = requests.post(url, data=senti_params)
        jsn = json.loads(json.loads(senti_res.text))
        obj['combine_sentiment'] = jsn['sentiment']
        if jsn['type']:
            obj['combine_qa'] = jsn['type']
        else:
            obj['combine_qa'] = 'unpredcitable'
    except Exception as e:
        print(str(e))

    all_data.append(obj)

headlines = ['s.no','text','stanford_sentiment','stanford_qa','combine_sentiment','combine_qa']
with open(output_csv + ".csv",'w',encoding='utf-8-sig',newline='') as f:
    writer = csv.DictWriter(f,headlines)
    writer.writeheader()
    for data in all_data:
        writer.writerow(data)

print(time.time()-start)