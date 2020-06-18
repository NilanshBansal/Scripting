import json
import csv
import os
from nltk_q_prediction_model import predict_question_bool

with open('stack_qs_analysed.csv', 'r') as f:
    reader = csv.reader(f)
    messages = []
    platforms = []
    text_types_stanford = []
    for row in reader:
        platforms.append(row[1])
        messages.append(row[2])
        text_types_stanford.append(row[3])


count = 0
all_data = []

for idx, msg in enumerate(messages[1:], start=1):
    count += 1
    obj = {}
    obj['s.no'] = count
    obj['platform'] = platforms[idx]
    obj['msg'] = msg
    obj['text_type_stanford'] = text_types_stanford[idx]

    try:
        obj['text_type_nltk'] = predict_question_bool(msg)
    except Exception as e:
        obj['text_type_nltk'] = str(e)

    print(count)
    all_data.append(obj)
print("Out of loop")

headlines = ['s.no','platform','msg','text_type_stanford','text_type_nltk']
with open('nltk_qs_analysed.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, headlines)
    writer.writeheader()
    for data in all_data:
        writer.writerow(data) 
