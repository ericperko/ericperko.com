import logging

import base64
import simplejson
from datetime import datetime
import urllib2
from urllib import urlencode
from github2.client import Github

import xmlwizardry

from settings import GITHUB_USER, GITHUB_API_KEY, POSTEROUS_USER

encode_xml = base64.encodestring
decode_xml = base64.decodestring
encode_commits = simplejson.dumps
decode_commits = simplejson.loads

from models import *

def update_github():
    logging.info("updating github")
    github = Github(username=GITHUB_USER, api_token=GITHUB_API_KEY)
    commits = []
    for r in github.repos.list(for_user='irskep'):
        new_commits = github.commits.list("irskep/%s" % r.name, 'master')
        for c in new_commits:
            c.repo = r
        commits.extend(new_commits)
    commits = reversed(sorted(commits, key=lambda c: c.committed_date)[-10:])
    recent_commits = []
    for c in commits:
        minute = str(c.committed_date.minute)
        if len(minute) < 2:
            minute = "0" + minute
        recent_commits.append({
            'repo_name': c.repo.name,
            'repo_url': c.repo.url,
            'time': {
                'day': c.committed_date.day,
                'month': c.committed_date.month,
                'year': c.committed_date.year,
                'hour': c.committed_date.hour,
                'minute': minute
            },
            'message': c.message,
            'url': c.url
        })
    return recent_commits

def update_posterous():
    logging.info("updating posterous")
    response = urllib2.urlopen("http://posterous.com/api/readposts", urlencode((
        ('hostname', POSTEROUS_USER),
        ('num_posts', '3'),
    ))).read()
    return response
#
def _read_posterous_response(response):
    posts = xmlwizardry.xmltodict(response)['post']
    if not isinstance(posts, list):
        posts = [posts]
    return posts

def get_posts_commits():
    should_update = False
    try:
        update_time = UpdateTime.all()[0]
        logging.info(str(update_time))
        delta = (datetime.now() - update_time.time)
        logging.info(str(delta))
        if delta.days >= 1:
            logging.info('yes, updating')
            should_update = True
            update_time.time = datetime.now()
            logging.info(str(update_time))
            update_time.put()
    except IndexError:
        logging.info("couldn't get UpdateTime object")
        db.put(UpdateTime(time=datetime.now()))
        should_update = True
    
    updated = False
    if should_update:
        logging.info('updating everything')
        posts_response = update_posterous()
        commits = update_github()
        updated = True
    else:
        try:
            logging.info('trying to read posts')
            posts_object = RecentPostsXML.all()[0]
            posts = _read_posterous_response(decode_xml(posts_object.posts))
            commits = decode_commits(posts_object.commits)
            logging.info('succeeded in doing so')
        except IndexError:
            logging.info("couldn't read posts")
            posts_response = update_posterous()
            commits = update_github()
            updated = True
    
    if updated:
        try:
            posts_object = RecentPostsXML.all()[0]
            posts_object.posts = encode_xml(posts_response)
            posts_object.commits = encode_commits(commits)
            posts_object.put()
        except IndexError:
            db.put(RecentPostsXML(posts=encode_xml(posts_response), commits=encode_commits(commits)))
        posts = _read_posterous_response(posts_response)
    
    return posts, commits

def force_updates():
    UpdateTime.all()[0].delete()
    get_posts_commits()
