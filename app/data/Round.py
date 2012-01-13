from google.appengine.ext import db

class Round(db.Model):
  office = db.StringProperty(required=True)
  drinkers = db.StringProperty(required=True)

  jid = db.StringProperty(required=True)
  teaprefs = db.StringProperty(required=False, default="")
  askme = db.BooleanProperty(required=False, default=True)
  newbie = db.BooleanProperty(required=False, default=True)
