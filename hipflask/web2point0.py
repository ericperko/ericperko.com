import logging

import simplejson
from datetime import datetime
import urllib2
from urllib import urlencode
from github2.client import Github
import posterous

import xmlwizardry
import settings

encode_posts = simplejson.dumps
decode_posts = simplejson.loads
encode_commits = simplejson.dumps
decode_commits = simplejson.loads

from models import *

def delete_all(ModelClass):
    objs = ModelClass.all()
    for obj in objs:
        obj.delete()

def update_github():
    logging.info("updating github")
    github = Github(username=settings.GITHUB_USER, api_token=settings.GITHUB_API_KEY)
    commits = []
    for r in github.repos.list(for_user=settings.GITHUB_USER):
        new_commits = github.commits.list("%s/%s" % (settings.GITHUB_USER, r.name), 'master')
        for c in new_commits:
            c.repo = r
        commits.extend(new_commits)
    all_commits = sorted(commits, key=lambda c: c.committed_date)
    commits = reversed(all_commits[-settings.NUM_GITHUB_COMMITS:])
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
    
    delete_all(RecentCommits)
    RecentCommits(commitsJson=encode_commits(recent_commits)).put()
    
    return recent_commits

def update_posterous():
    logging.info("updating posterous")
    primary_site = None
    try:
        api = posterous.API(settings.POSTEROUS_USER, settings.POSTEROUS_PASSWORD)
        sites = api.get_sites()
    except Exception, e:
        logging.error('Posterous user information incorrect')
        sites = []
        return {}
    for site in sites:
        if site.primary:
            primary_site = site
    if primary_site:
        posts_repr = primary_site.read_posts()[:settings.NUM_POSTEROUS_POSTS]
        posts = [{
            'title': post.title,
            'link': post.link
        } for post in posts_repr]
        logging.info(str(posts))
        
        delete_all(RecentPosts)
        RecentPosts(postsJson=encode_posts(posts)).put()
        
        return posts
    else:
        logging.info('No primary posterous site')
        return {}

def get_posts_commits():
    try:
        posts = decode_posts(RecentPosts.all()[0].postsJson)
    except IndexError:
        posts = update_posterous()
    
    try:
        commits = decode_commits(RecentCommits.all()[0].commitsJson)
    except IndexError:
        commits = update_github()
    
    return posts, commits
