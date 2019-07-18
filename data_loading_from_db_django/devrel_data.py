import os
import csv
os.environ.setdefault('DJANGO_SETTINGS_MODULE','copernicus_api.settings')

import django
django.setup()

import datetime

from users.models import User,Member,UserEvent
from twitter.models import TwitterUserToken,UserTimeline
from github.models import GithubToken

"""

****** USER ******

"""

def get_user_info(user_email):
    user = User.objects.get(email=user_email)
    obj = user.__dict__
    del obj['_state']

    filename = "scraped_data/user_info.csv"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'w',encoding='utf-8-sig',newline='') as f:
        writer = csv.DictWriter(f,obj.keys())
        writer.writeheader()
        writer.writerow(obj)
    
def get_all_members_info(user_email):
    members = Member.objects.filter(user__email = user_email).values('member_email','first_name','last_name')
    if members.exists():
        filename = 'scraped_data/member_info.csv'
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w',encoding='utf-8-sig',newline='') as f:
            writer = csv.DictWriter(f,members[0].keys())
            writer.writeheader()
            for member in members:
                writer.writerow(member)
    else:
        print('No member exists !')


def get_user_events_info(user_email):
    members = Member.objects.filter(user__email=user_email)
    if members.exists():
        for member in members:
            member_email = member.member_email
            events = UserEvent.objects.filter(user_email=user_email, member__member_email=member_email)
            if not events.exists():
                continue

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

            filename = 'scraped_data/' + member_email + '_user_events_info.csv'
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            with open(filename, 'w',encoding='utf-8-sig',newline='') as f:
                writer = csv.DictWriter(f,all_events[0].keys())
                writer.writeheader()
                for event in all_events:
                    writer.writerow(event)
    else:
        print('No member exists !')

"""

****** TWITTER ******

"""

def get_twitter_token_info(user_email):
    members = Member.objects.filter(user__email=user_email)
    if not members.exists():
        return print('No member exists !')
    
    for member in members:
        member_email = member.member_email
        try:
            user_token = TwitterUserToken.objects.get(email=user_email,member__member_email=member_email)
        except:
            continue
        
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

        filename = 'scraped_data/' + member_email + '_twitter_token_info.csv'
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w',encoding='utf-8-sig',newline='') as f:
            writer = csv.DictWriter(f,obj.keys())
            writer.writeheader()
            writer.writerow(obj)


def get_twitter_user_timeline_info(user_email):
    members = Member.objects.filter(user__email=user_email)
    if members.exists():
        for member in members:
            member_email = member.member_email
            member_tweets = UserTimeline.objects.filter(user_email=user_email, member__member_email=member_email)
            
            if not member_tweets.exists():
                continue

            try:
                twitter_user_token = TwitterUserToken.objects.get(email=user_email,member__member_email=member_email)
            except:
                continue

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
            
            filename = 'scraped_data/' + member_email +'_twitter_timeline_info.csv'
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            with open(filename, 'w',encoding='utf-8-sig',newline='') as f:
                writer = csv.DictWriter(f,tweets_info[0].keys())
                writer.writeheader()
                for row in tweets_info:
                    writer.writerow(row)
    else:
        print('No member exists !')



"""

****** GITHUB ******

"""
# BASED ON MEMBERS TOO ?

def get_github_token_info(user_email):
    try:
        user_token = GithubToken.objects.get(email=user_email)
    except:
        return print('Twitter not connected !')
        
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

    filename = 'scraped_data/twitter_token_info.csv'
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename,'w',encoding='utf-8-sig',newline='') as f:
        writer = csv.DictWriter(f,obj.keys())
        writer.writeheader()
        writer.writerow(obj)

if __name__ == '__main__':
    user_email = 'mhall119@gmail.com'
    get_user_info(user_email)
    get_all_members_info(user_email)
    get_user_events_info(user_email)
    get_twitter_token_info(user_email)
    get_twitter_user_timeline_info(user_email)