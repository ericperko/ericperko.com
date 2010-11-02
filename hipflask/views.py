# -*- coding: utf-8 -*-
from __future__ import with_statement

import logging
import functools
import markdown

from hipflask import app

from flask import render_template, flash, url_for, redirect, Markup, abort

import web2point0
from site import render_with_app_lists, reverse_apps, paged_apps

# ==============
# = Front page =
# ==============

@app.route('/')
def index():
    """Display front page with recent blog posts and Github commits"""
    posts, commits = web2point0.get_posts_commits()
    context = {
        'posts': posts,
        'commits': commits,
        'title': "Home",
    }
    return render_with_app_lists('index.html', **context)

@app.route('/run_updates')
def run_updates():
    """Update posts/commits cache"""
    web2point0.force_updates()
    return 'Updated.'

# =========
# = Pages =
# =========

def apps(app_name):
    if app_name in paged_apps.keys():
        return paged_app(app_name, page=1)
    with open('content/%s.markdown' % app_name, 'r') as f:
        html = Markup(markdown.markdown(f.read()))
    context = {
        'title': reverse_apps[app_name],
        'html': html
    }
    return render_with_app_lists('app.html', **context)

@app.route('/<app_name>/<int:page>')
def paged_app(app_name, page=1):
    total_pages = paged_apps[app_name]
    if page > total_pages:
        abort(404)
    pages = range(1, int(total_pages)+1)
    this_page=int(page)
    context = {'title': reverse_apps[app_name]}
    if this_page > 1:
        context['previous_page'] = url_for('paged_app', app_name=app_name, page=this_page-1)
    if this_page < total_pages:
        context['next_page'] = url_for('paged_app', app_name=app_name, page=this_page+1)
    
    with open('content/%s_%s.markdown' % (app_name, page)) as f:
        context['html'] = Markup(markdown.markdown(f.read()))
    return render_with_app_lists('multipage.html', **context)

for item in reverse_apps.keys():
    app.add_url_rule('/%s' % item, item, functools.partial(apps, item))
