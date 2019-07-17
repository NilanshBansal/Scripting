import os
import csv
os.environ.setdefault('DJANGO_SETTINGS_MODULE','copernicus_api.settings')

import django
django.setup()

import datetime

from users.models import User,Member,UserEvent
from twitter.models import TwitterUserToken,UserTimeline

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

def get_twitter_token_info(user_email):
    user_token = TwitterUserToken.objects.get(email=user_email)
    obj = {
        "id":user_token.id,
        "user_email":user_token.email,
        "twitter_id":user_token.twitter_id,
        "access_token":user_token.access_token,
        "access_token_secret":user_token.access_token_secret,
        "screen_name":user_token.screen_name,
        "member_id":user_token.member.id,
        "member_email":user_token.member.member_email,
        "member_name":user_token.member.first_name + ' ' + user_token.member.last_name
    }

    with open('twitter_token_info.csv','w',encoding='utf-8-sig',newline='') as f:
        writer = csv.DictWriter(f,obj.keys())
        writer.writeheader()
        writer.writerow(obj)

def get_twitter_user_timeline_info(user_email):
    members = Member.objects.filter(user__email=user_email)
    for member in members:
        member_email = member.member_email
        member_tweets = UserTimeline.objects.filter(user_email=user_email, member__member_email=member_email)
        twitter_user_token = TwitterUserToken.objects.get(email=user_email,member__member_email=member_email)
        
        tweets_info = []
        for tweet in member_tweets:
            tweet_obj = {
                "id":tweet.id,
                "status_id":tweet.status_id,
                "posted_by_user_name":tweet.posted_by_user_name,
                "posted_by_user_screen_name":tweet.posted_by_user_screen_name,
                "created_at_time":tweet.created_at_time,
                "created_at_date":tweet.created_at_date,
                "text":tweet.text,
                
                "user_email":user_email,
                "member_email":member_email,
                "member_id":tweet.member.id,
                "member_name":tweet.member.first_name + ' ' + tweet.member.last_name,
                "member_user_twitter_id": twitter_user_token.twitter_id,
                "member_user_screen_name":twitter_user_token.screen_name,

                "devrel_choices" : tweet.get_devrel_choices_display(),
                "text_type" : tweet.text_type,
                "sentiment_positive" : tweet.sentiment_positive,
                "sentiment_negative" : tweet.sentiment_negative,
                "sentiment_neutral": tweet.sentiment_neutral,
                "tags":tweet.tags,
                "location":tweet.location
            }

            tweets_info.append(tweet_obj)

        with open(member_email +'_twitter_timeline_info.csv','w',encoding='utf-8-sig',newline='') as f:
            writer = csv.DictWriter(f,tweets_info[0].keys())
            writer.writeheader()
            for row in tweets_info:
                writer.writerow(row)

if __name__ == '__main__':
    # get_user_info('bansalnilansh@gmail.com')
    # get_all_members_info('bansalnilansh@gmail.com')
    # get_user_events_info('bansalnilansh@gmail.com')
    # get_twitter_token_info('bansalnilansh@gmail.com')
    get_twitter_user_timeline_info('bansalnilansh@gmail.com')