from google.appengine.ext import db

class Roster(db.Model):
  jid               = db.StringProperty (required=True)
  teaprefs          = db.StringProperty (required=True, default="")
  askme             = db.BooleanProperty(required=True, default=True)
  newbie            = db.BooleanProperty(required=True, default=True)
  hasDoubleJeopardy = db.BooleanProperty(required=True, default=False)
  isSettingPrefs    = db.BooreanProperty(required=True, default=False)
