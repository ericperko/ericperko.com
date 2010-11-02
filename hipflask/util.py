import logging
from flask import render_template, flash, url_for, redirect, Markup

import site

def _parse_app_list(item_list):
    items = []
    for a, b in item_list:
        if b.startswith('http'):
            items.append({'name':a, 'url': b})
        else:
            items.append({'name':a.split('/')[0], 'url': '/%s' % b})
    items.sort(key=lambda x: x['name'].lower())
    return items

def _parse_simple_list(item_list):
    items = []
    for a, b in item_list:
        if b.startswith('http'):
            items.append({'name':a, 'url': b})
        else:
            items.append({'name':a, 'url': url_for(b)})
    return items

def render_with_app_lists(template, **kwargs):
    code = _parse_app_list(site.code.iteritems())
    toys = _parse_app_list(site.toys.iteritems())
    default = _parse_simple_list(site.default)
    kwargs.update(locals())
    return render_template(template, **kwargs)
