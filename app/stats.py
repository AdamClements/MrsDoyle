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
  
def statDrinker(name, made=0):
  totals = PerUserTotals.get_or_insert(key_name=name)
  totals.cupsDrunk = totals.cupsDrunk + 1
  totals.cupsMade  = totals.cupsMade + made  
  totals.put()
  
  drinkerStats = PerUserStats(drinker=name)
  drinkerStats.put()
    
def statRound(pName, pCups):
  newRound = PerRoundStats(maker=pName, cups=pCups)
  newRound.put()

def getMadeDrunkRatio(pName):
  totals = PerUserTotals.get_by_key_name(key_names=pName)
  if totals == None or totals.cupsDrunk == 0:
    return 1
  
  # Avoid a divide by zero. Also bias it a bit so newbies think
  # they're getting free tea for a while and get hooked.
  if totals.cupsMade == 0:
    return totals.cupsDrunk / 1
    
  return totals.cupsDrunk / float(totals.cupsMade)
