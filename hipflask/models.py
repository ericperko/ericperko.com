from google.appengine.ext import db

class UpdateTime(db.Model):
    time = db.DateTimeProperty(required=True)

class RecentPostsXML(db.Model):
    posts = db.TextProperty(required=True)
    commits = db.TextProperty(required=True)
        
