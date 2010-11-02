# -*- coding: utf-8 -*-
default = [
    ('Blog', r'http://stevejohnson.posterous.com/'),
    ('tim|steve', r'http://timunionsteve.posterous.com/'),
    ('Music', r'music'),
    ('CWRU Hacker Society', r'http://goto.case.edu/'),
    ('Python game tutorial', r'pyglettutorial_index'),
    ('Start making games', r'http://stevejohnson.posterous.com/a-starting-point-for-making-games'),
]

toys = {
    'gw0rp': 'gw0rp',
    'Artack': 'artack',
    'Bungie Chopper/Elite Bungie Chopper Squadron': 'bungie_chopper',
    'Escort Wing': 'escort_wing',
    'Splatterboard': 'splatterboard',
    'Art Project 1': 'art_project_1',
}

code = {
    'T-Reg': r'http://www.github.com/irskep/T-Reg',
    'Regex compiler': r'http://www.github.com/irskep/regex_compiler',
    'JTrie': r'http://www.github.com/irskep/jtrie',
    'MRJob Py3k port': r'http://www.github.com/irskep/mrjob/tree/py3k',
}

more = {
    u'Music': 'music',
    u'Résumé': 'resume',
    u'Hacker Résumé': 'hacker_resume',
}

apps = {}
apps.update(toys)
apps.update(code)
apps.update(more)

def reverse_dict(d):
    rd = {}
    for k, v in d.iteritems():
        rd[v] = k
    return rd

reverse_apps = reverse_dict(apps)