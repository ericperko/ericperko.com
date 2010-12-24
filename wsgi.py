from jinja2 import FileSystemLoader
import os
from hipflask import app as application

if len(application.jinja_loader.searchpath) == 1:
    # Add more options for loading templates, since we don't
    # actually want templates to be stored in hipflask/ but
    # rather in content/
    import os
    application.jinja_loader.searchpath.append(os.path.join(application.root_path, '..', 'content', 'templates'))

if __name__ == "__main__":
    application.run()
