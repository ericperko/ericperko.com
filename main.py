from google.appengine.ext.webapp.util import run_wsgi_app
from jinja2 import FileSystemLoader
import os
from hipflask import app

if len(app.jinja_loader.searchpath) == 1:
    # Add more options for loading templates, since we don't
    # actually want templates to be stored in hipflask/ but
    # rather in content/
    import os
    app.jinja_loader.searchpath.append(os.path.join(app.root_path, '..', 'content', 'templates'))

run_wsgi_app(app)
