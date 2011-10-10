from google.appengine.ext import db

class PerUserTotals(db.Model):
  cupsMade = db.IntegerProperty(default=0)
  cupsDrunk = db.IntegerProperty(default=0)
  
class PerUserStats(db.Model):
  date = db.DateTimeProperty(auto_now_add=True)
  drinker = db.StringProperty(required=True)  
  
class PerRoundStats(db.Model):
  date = db.DateTimeProperty(auto_now_add=True)
  maker = db.StringProperty(required=True)
  cups = db.IntegerProperty(required=True)
  
def statDrinker(name, maker=False):
  totals = PerUserTotals.get_or_insert(key_name=name)
  totals.cupsDrunk = totals.cupsDrunk + 1
  if maker:
    totals.cupsMade = totals.cupsMade + 1  
  totals.put()
  
  drinkerStats = PerUserStats(drinker=name)
  drinkerStats.put()
  
  
def statMaker(name):
  statDrinker(name, True)  
  
def statRound(pName, pCups):
  newRound = PerRoundStats(maker=pName, cups=pCups)
  newRound.put()