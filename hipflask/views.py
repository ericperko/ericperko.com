# -*- coding: utf-8 -*-
from __future__ import with_statement

import logging
import functools
import markdown

from hipflask import app

from flask import render_template, flash, url_for, redirect, Markup

import web2point0
import site
from util import *

@app.route('/')
def index():
    posts, commits = web2point0.get_posts_commits()
    context = {
        'posts': posts,
        'commits': commits,
        'title': "Home",
    }
    return render_with_app_lists('index.html', **context)

@app.route('/pyglettutorial/')
def pyglettutorial_index():
    return redirect(url_for('pyglettutorial', page=1))

@app.route('/pyglettutorial/<int:page>')
def pyglettutorial(page=1, total_pages=6):
    pages = range(1, int(total_pages)+1)
    this_page=int(page)
    context = {'title': 'Python Game Programming Tutorial'}
    if this_page > 1:
        context['previous_page'] = url_for('pyglettutorial', page=this_page-1)
    if this_page < total_pages:
        context['next_page'] = url_for('pyglettutorial', page=this_page+1)
    
    with open('content/tutorial_%s.markdown' % page) as f:
        context['html'] = Markup(markdown.markdown(f.read()))
    logging.info(context['html'])
    return render_with_app_lists('multipage.html', **context)

@app.route('/run_updates')
def run_updates():
    web2point0.force_updates()
    return 'Updated.'

def apps(app):
    with open('content/%s.markdown' % app) as f:
        html = Markup(markdown.markdown(f.read()))
    context = {
        'title': site.reverse_apps[app],
        'html': html
    }
    return render_with_app_lists('app.html', **context)

for item in site.apps.values():
    app.add_url_rule('/%s' % item, item, functools.partial(apps, item))
