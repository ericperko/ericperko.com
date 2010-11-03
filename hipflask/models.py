from google.appengine.ext import db

class RecentPosts(db.Model):
    postsJson = db.TextProperty(required=True)

class RecentCommits(db.Model):
    commitsJson = db.TextProperty(required=True)
