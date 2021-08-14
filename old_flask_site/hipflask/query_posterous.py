import logging
import simplejson
import posterous

import settings

encode_posts = simplejson.dumps
decode_posts = simplejson.loads

from models import RecentPosts

def delete_all(ModelClass):
    objs = ModelClass.all()
    for obj in objs:
        obj.delete()

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

def get_posts():
    try:
        posts = decode_posts(RecentPosts.all()[0].postsJson)
    except IndexError:
        posts = update_posterous()
    
    return posts
