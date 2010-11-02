from __future__ import with_statement
import collections
import logging
import yaml
import copy
from flask import url_for, render_template

apps = {}
title_lookup = {}
groups = []
page_counts = collections.defaultdict(lambda: 1)

with open('content/site.yaml', 'r') as f:
    yaml_repr = yaml.load(f)

for group_repr in yaml_repr:
    group_name = group_repr.keys()[0]
    group_members = group_repr.values()[0]
    items = []
    for item in group_members:
        if len(item.keys()) > 1:
            num_pages = item['pages']
            del item['pages']
        else:
            num_pages = 1
        item_name = item.keys()[0]
        if '/' in item_name:
            item_name, long_name = item_name.split("/")
        else:
            long_name = item_name
        item_url = item.values()[0]
        items.append({'name': item_name, 'url': item_url})
        apps[item_name] = item_url
        title_lookup[item_url] = long_name
        page_counts[item_url] = num_pages
    
    groups.append({
        'name': group_name,
        'items': items
    })

def parse_groups():
    parsed_groups = [copy.deepcopy(group) for group in groups if group['name'] != 'hidden']
    for group in parsed_groups:
        for item in group['items']:
            if not item['url'].startswith('http'):
                item['url'] = url_for(item['url'])
    return parsed_groups

def render_with_app_lists(template, **kwargs):
    kwargs['groups'] = parse_groups()
    return render_template(template, **kwargs)
