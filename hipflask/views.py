# -*- coding: utf-8 -*-
from __future__ import with_statement

import logging
import functools
import markdown

from hipflask import app

from flask import render_template, flash, url_for, redirect, Markup, abort

import web2point0
from site import *

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

@app.route('/<app_name>/<int:page>')
def apps(app_name, page=1):
    context = {'title': reverse_apps[app_name]}
    total_pages = page_counts[app_name]
    if page > total_pages:
        abort(404)
    if total_pages == 1:
        template_name = 'content/%s.markdown' % app_name
    else:
        pages = range(1, int(total_pages)+1)
        this_page=int(page)
        if this_page > 1:
            context['previous_page'] = url_for('paged_app', app_name=app_name, page=this_page-1)
        if this_page < total_pages:
            context['next_page'] = url_for('paged_app', app_name=app_name, page=this_page+1)
        template_name = 'content/%s_%s.markdown' % (app_name, page)
    
    with open(template_name, 'r') as f:
        context['html'] = Markup(markdown.markdown(f.read()))
    return render_with_app_lists('page.html', **context)

for item in reverse_apps.keys():
    app.add_url_rule('/%s' % item, item, functools.partial(apps, item))
