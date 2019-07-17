import os
import csv
os.environ.setdefault('DJANGO_SETTINGS_MODULE','copernicus_api.settings')

import django
django.setup()

import datetime
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
    
    with open('member_info.csv','w',encoding='utf-8-sig',newline='') as f:
        writer = csv.DictWriter(f,members[0].keys())
        writer.writeheader()
        for member in members:
            writer.writerow(member)

def get_user_events_info(user_email):
    events = UserEvent.objects.filter(user_email = user_email)

    all_events = []
    for event in events:
        obj = {
            "id": event.id,
            "user_email":event.user_email,
            "member_id":event.member.id,
            "member_email":event.member.member_email,
            "member_name":event.member.first_name + ' ' + event.member.last_name,

            "event_name":event.event_name,
            "about_event":event.about_event,
            "from_date":event.from_date.strftime("%Y-%m-%d"),
            "to_date":event.to_date.strftime("%Y-%m-%d"),
            "event_url":event.event_url,
            "event_type":event.get_event_type_display(),

            "meetup_event_id": None if not event.meetup_event_selection else event.meetup_event_selection.id,
            "meetup_event_name":None if not event.meetup_event_selection else event.meetup_event_selection.name,
            "meetup_yes_rsvp_count":None if not event.meetup_event_selection else event.meetup_event_selection.yes_rsvp_count,
            "meetup_event_id":None if not event.meetup_event_selection else event.meetup_event_selection.event_id,
            "meetup_event_link":None if not event.meetup_event_selection else event.meetup_event_selection.link,

            "user_attending_count":event.user_attending_count
        }
        all_events.append(obj)


    with open('user_events_info.csv','w',encoding='utf-8-sig',newline='') as f:
        writer = csv.DictWriter(f,all_events[0].keys())
        writer.writeheader()
        for event in all_events:
            writer.writerow(event)

if __name__ == '__main__':
    # get_user_info('bansalnilansh@gmail.com')
    # get_all_members_info('bansalnilansh@gmail.com')
    get_user_events_info('bansalnilansh@gmail.com')