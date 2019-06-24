import os
import csv
os.environ.setdefault('DJANGO_SETTINGS_MODULE','copernicus_api.settings')

import django
django.setup()

from stackoverflow.models import StackoverflowUserQuestions



def get_stack_qs():
    count = 1
    res = StackoverflowUserQuestions.objects.values('tagnames','title')
    all_data = []
    for r in res:
        obj = {}
        obj['s.no'] = count
        obj['old_tags'] = r['tagnames']
        obj['msg'] = r['title']
        count += 1 
        all_data.append(obj)

    headlines = ['s.no','msg','old_tags']
    with open('stack_tag_analysis.csv','w',encoding='utf-8-sig',newline='') as f:
        writer = csv.DictWriter(f,headlines)
        writer.writeheader()
        for data in all_data:
            writer.writerow(data)




if __name__ == '__main__':
    print("Storing data !")
    get_stack_qs()
    print("Done !")