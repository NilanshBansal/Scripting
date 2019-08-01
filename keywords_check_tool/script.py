"""
Created on Tue July 31 10:40:14 2019
@author: nilanshbansal
"""
import json
import requests
import time

with open('keywords') as f:
    old_keywords_list = f.readlines()

old_keywords_list = [x.strip() for x in old_keywords_list]

url = 'http://139.59.35.166:9090/trial'


useful_words = []
useless_words = []

start = time.time()

for idx,word in enumerate(old_keywords_list[30000:]):
    print(idx,word)
    try:
        r = requests.post(url, data={'sentdata[q]': word})
        res_json = json.loads(r.json()['filters'])
        if "TOPIC" in res_json and res_json['TOPIC']:
            useful_words.append(word)
        else:
            print("USELESS: ",word)
            useless_words.append(word)
    except Exception as e:
        print("Exception at Word: ",word)
        print(str)


with open('useful_words.txt', 'a') as f:
    for word in useful_words:
        f.write("%s\n" % word)


with open('useless_words.txt', 'a') as f:
    for word in useless_words:
        f.write("%s\n" % word)

print(time.time()-start)