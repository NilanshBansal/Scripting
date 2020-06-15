import json
import csv
import os
import requests
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'copernicus_api.settings')
#import django
#django.setup()


with open('stack_qs.csv', 'r') as f:
    reader = csv.reader(f)
    titles = []
    for row in reader:
        titles.append(row[0])

ml_url = 'http://3.135.227.133:8000/api/getnlpscore'

count = 0
all_data = []

for idx, title in enumerate(titles[1:2], start=1):
    count += 1
    obj = {}
    obj['s.no'] = count
    obj['title'] = title
    senti_params = {"type": "plain", "TextToAnalyse": title}
    try:
        senti_res = requests.post(ml_url, data=senti_params)
        jsn = json.loads(senti_res.text)
        obj['text_type'] = jsn['type']
    except Exception as e:
        print(str(e))
        obj['text_type'] = str(e)
    all_data.append(obj)

writeHeader = True
if os.path.exists('stack_qs_analysed.csv'):
    writeHeader = False

headlines = ['s.no', 'title', 'text_type']
with open('stack_qs_analysed.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, headlines)
    if writeHeader:
        writer.writeheader()
    for data in all_data:
        writer.writerow(data)
