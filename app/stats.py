from google.appengine.ext import db

class PerUserStats(db.Model):
  date = db.DateTimeProperty(auto_now_add=True)
  cupsMade = db.IntegerProperty(default=0)
  cupsDrunk = db.IntegerProperty(default=0)
  
class PerRoundStats(db.Model):
  date = db.DateTimeProperty(auto_now_add=True)
  maker = db.StringProperty(required=True)
  cups = db.IntegerProperty(required=True)
  
def statDrinker(name):
  drinkerStats = PerUserStats.get_or_insert(key_name=name)
  drinkerStats.cupsDrunk = drinkerStats.cupsDrunk + 1
  drinkerStats.put()
  
def statMaker(name):
  drinkerStats = PerUserStats.get_or_insert(key_name=name)
  drinkerStats.cupsDrunk = drinkerStats.cupsDrunk + 1
  drinkerStats.cupsMade = drinkerStats.cupsMade + 1
  drinkerStats.put()
  
def statRound(pName, pCups):
  newRound = PerRoundStats(maker=pName, cups=pCups)
  newRound.put()