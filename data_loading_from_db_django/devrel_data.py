import os
import csv
os.environ.setdefault('DJANGO_SETTINGS_MODULE','copernicus_api.settings')

import django
django.setup()

import datetime

from users.models import User,Member,UserEvent
from twitter.models import TwitterUserToken,UserTimeline
from github.models import GithubToken, GithubUser, UserIssue, IssueComment

"""

****** USER ******

"""

def get_user_info(user_email):
    user = User.objects.get(email=user_email)
    obj = user.__dict__
    del obj['_state']

    filename = user_email + "/user/user_info.csv"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'w',encoding='utf-8-sig',newline='') as f:
        writer = csv.DictWriter(f,obj.keys())
        writer.writeheader()
        writer.writerow(obj)
    
def get_all_members_info(user_email):
    members = Member.objects.filter(user__email = user_email).values('member_email','first_name','last_name')
    if members.exists():
        filename = user_email + '/user/member_info.csv'
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

            filename = user_email + '/user/' + member_email + '_user_events_info.csv'
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

        filename = user_email + '/twitter/' + member_email + '_twitter_token_info.csv'
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
            
            filename = user_email + '/twitter/' + member_email +'_twitter_timeline_info.csv'
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

def get_github_token_info(user_email):
    members = Member.objects.filter(user__email=user_email)
    if not members.exists():
        return print('No member exists !')
    
    for member in members:
        member_email = member.member_email

        try:
            user_token = GithubToken.objects.get(email=user_email, member__member_email=member_email)
        except:
            continue
            
        obj = {
            "id":user_token.id,
            "user_email":user_token.email,
            "github_user_id":user_token.user_id,
            "access_token":user_token.access_token,
            "github_user_name":user_token.user_name,
            "member_id":user_token.member.id,
            "member_email":user_token.member.member_email,
            "member_name":user_token.member.first_name + ' ' + user_token.member.last_name
        }

        filename = user_email + '/github/' + member_email + '_github_token_info.csv'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w',encoding='utf-8-sig',newline='') as f:
            writer = csv.DictWriter(f,obj.keys())
            writer.writeheader()
            writer.writerow(obj)


def get_github_user_issues(user_email):
    members = Member.objects.filter(user__email=user_email)
    if not members.exists():
        return print('No member exists !')
    
    for member in members:
        member_email = member.member_email
        
        try:
            user_token = GithubToken.objects.get(email=user_email, member__member_email=member_email)
            owner_user_id = user_token.user_id
        except:
            continue

        member_issues = UserIssue.objects.filter(owner_user_id=owner_user_id, member__member_email=member_email)
        if not member_issues.exists():
            continue
        
        issues_info = []
        
        for issue in member_issues:
            issue_obj = {
                "id":issue.id,
                "github_issue_id":issue.issue_id,
                "issue_title":issue.issue_title,
                "issue_body":issue.issue_body,
                "text_type" : issue.text_type,
                "sentiment_positive" : issue.sentiment_positive,
                "sentiment_negative" : issue.sentiment_negative,
                "sentiment_neutral": issue.sentiment_neutral,

                "repo_name":issue.repo_name,
                "tags":issue.tags,
                "created_at_time":issue.created_at_time,
                "created_at_date":issue.created_at_date,
                
                "issue_creator_user_github_id":issue.user_id,

                "user_email":user_email,
                "member_email":member_email,
                "member_id":issue.member.id,
                "member_name":issue.member.first_name + ' ' + issue.member.last_name,
                "member_user_github_id":issue.owner_user_id,

                "devrel_choices" : issue.get_devrel_choices_display(),
            }
            try:
                issue_creator_user_obj=GithubUser.objects.filter(user_id=issue_obj['issue_creator_user_github_id'])[0]
                issue_obj['issue_creator_user_github_username'] = issue_creator_user_obj.username
                issue_obj['issue_creator_user_github_location'] = issue_creator_user_obj.location
            except:
                continue

            try:
                issue_member_user_obj=GithubUser.objects.filter(user_id=issue_obj['member_user_github_id'])[0]
                issue_obj["member_user_github_username"] = issue_member_user_obj.username
                issue_obj["member_user_github_location"] = issue_member_user_obj.location
            except:
                continue

            issues_info.append(issue_obj)
        
        filename = user_email + '/github/' + member_email +'_github_issues_info.csv'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        if len(issues_info) > 0: 
            with open(filename, 'w',encoding='utf-8-sig',newline='') as f:
                writer = csv.DictWriter(f,issues_info[0].keys())
                writer.writeheader()
                for row in issues_info:
                    writer.writerow(row)


def get_github_user_info(user_email):
    members = Member.objects.filter(user__email=user_email)
    if not members.exists():
        return print('No member exists !')
    
    for member in members:
        member_email = member.member_email

        users = GithubUser.objects.filter(member__member_email=member_email).values('username','repos','avatar_url','email','user_id','location')

        if not users.exists():
            continue
        
        filename = user_email + '/github/' + member_email + '_github_user_info.csv'
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w',encoding='utf-8-sig',newline='') as f:
            writer = csv.DictWriter(f,users[0].keys())
            writer.writeheader()
            for user in users:
                writer.writerow(user)


def get_github_user_issue_comments(user_email):
    
    members = Member.objects.filter(user__email=user_email)
    if not members.exists():
        return print('No member exists !')
    
    for member in members:
        member_email = member.member_email
        
        try:
            user_token = GithubToken.objects.get(email=user_email, member__member_email=member_email)
            owner_user_id = user_token.user_id
        except:
            continue

        member_issue_comments = IssueComment.objects.filter(owner_user_id=owner_user_id, member__member_email=member_email)
        if not member_issue_comments.exists():
            continue
        
        issue_comments_info = []
        
        for issue_comment in member_issue_comments:
            issue_comment_obj = {
                "id":issue_comment.id,
                "issue_id":issue_comment.issue_id,
                "comment_id":issue_comment.comment_id,
                "comment":issue_comment.comment,
                "text_type" : issue_comment.text_type,
                "sentiment_positive" : issue_comment.sentiment_positive,
                "sentiment_negative" : issue_comment.sentiment_negative,
                "sentiment_neutral": issue_comment.sentiment_neutral,
                "tags":issue_comment.tags,
                "created_at_time":issue_comment.created_at_time,
                "created_at_date":issue_comment.created_at_date,
                "issue_comment_creator_user_github_id":issue_comment.user_id,

                "user_email":user_email,
                "member_email":member_email,
                "member_id":issue_comment.member.id,
                "member_name":issue_comment.member.first_name + ' ' + issue_comment.member.last_name,
                "member_user_github_id":issue_comment.owner_user_id,

                "devrel_choices" : issue_comment.get_devrel_choices_display(),
            }
            try:
                issue_comment_creator_user_obj=GithubUser.objects.filter(user_id=issue_comment_obj['issue_comment_creator_user_github_id'])[0]
                issue_comment_obj['issue_comment_creator_user_github_username'] = issue_comment_creator_user_obj.username
                issue_comment_obj['issue_comment_creator_user_github_location'] = issue_comment_creator_user_obj.location
            except:
                continue

            try:
                issue_comment_member_user_obj=GithubUser.objects.filter(user_id=issue_comment_obj['member_user_github_id'])[0]
                issue_comment_obj["member_user_github_username"] = issue_comment_member_user_obj.username
                issue_comment_obj["member_user_github_location"] = issue_comment_member_user_obj.location
            except:
                continue

            issue_comments_info.append(issue_comment_obj)
        
        filename = user_email + '/github/' + member_email +'_github_issue_comments_info.csv'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        if len(issue_comments_info) > 0: 
            with open(filename, 'w',encoding='utf-8-sig',newline='') as f:
                writer = csv.DictWriter(f,issue_comments_info[0].keys())
                writer.writeheader()
                for row in issue_comments_info:
                    writer.writerow(row)




if __name__ == '__main__':
    user_email = 'mhall119@gmail.com'
    get_user_info(user_email)
    get_all_members_info(user_email)
    get_user_events_info(user_email)
    get_twitter_token_info(user_email)
    get_twitter_user_timeline_info(user_email)
    get_github_token_info(user_email)
    get_github_user_issues(user_email)
    get_github_user_info(user_email)
    get_github_user_issue_comments(user_email)