import json
import csv
import os
import requests
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'copernicus_api.settings')
import django
django.setup()
from bs4 import BeautifulSoup

from users.models import KeywordLibrary


with open('keyword_test_analysed_woprob.csv', 'r') as f:
    reader = csv.reader(f)
    messages = []
    tags = []
    tfidf_tags = []
    for row in reader:
        messages.append(row[1])
        tags.append(row[2])
        tfidf_tags.append(row[3])

count = 0
all_data = []

for idx, msg in enumerate(messages[1:], start=1):
    count += 1
    obj = {}
    obj['s.no'] = count
    obj['msg'] = msg
    obj['tags'] = tags[idx]
    obj['tfidf_tags'] = tfidf_tags[idx]

    tfidf_tag_list = tfidf_tags[idx].split('\n')
    tfidf_tagginglib_output = []
    for tftag in tfidf_tag_list:
        tftag = tftag.lower().strip()
        if KeywordLibrary.objects.filter(keyword=tftag).exists():
            tfidf_tagginglib_output.append(tftag)
    
    obj['tfidx_tagging_lib_passed'] = tfidf_tagginglib_output
    all_data.append(obj)

headlines = ['s.no','msg','tags','tfidf_tags','tfidx_tagging_lib_passed']
with open('keyword_test_analysed_woprob_tagex.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, headlines)
    writer.writeheader()
    for data in all_data:
        writer.writerow(data) 