import os
import csv
os.environ.setdefault('DJANGO_SETTINGS_MODULE','copernicus_api.settings')

import django
django.setup()

from users.models import User,Member,UserEvent

def get_user_info(user_email):
    user = User.objects.get(email=user_email)
    obj = user.__dict__
    del obj['_state']

    with open('user_info.csv','w',encoding='utf-8-sig',newline='') as f:
        writer = csv.DictWriter(f,obj.keys())
        writer.writeheader()
        writer.writerow(obj)
    
def get_all_members_info(user_email):
    members = Member.objects.filter(user__email = user_email).values('member_email','first_name','last_name')
    print(members[0])
    
    with open('member_info.csv','w',encoding='utf-8-sig',newline='') as f:
        writer = csv.DictWriter(f,members[0].keys())
        writer.writeheader()
        for member in members:
            writer.writerow(member)

def get_user_events_info(user_email):
    events = UserEvent.objects.filter(user_email = user_email).values('event_name','about_event','from_date','to_date','member','event_url','event_type','meetup_event_selection','user_attending_count')

    with open('user_events_info.csv','w',encoding='utf-8-sig',newline='') as f:
        writer = csv.DictWriter(f,events[0].keys())
        writer.writeheader()
        for event in events:
            writer.writerow(event)

if __name__ == '__main__':
    # get_user_info('bansalnilansh@gmail.com')
    # get_all_members_info('bansalnilansh@gmail.com')
    # get_user_events_info('bansalnilansh@gmail.com')