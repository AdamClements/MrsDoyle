from google.appengine.ext import db

class Registry(db.Model):
	user_email = db.StringProperty(required=True) # email address
	ignore_status = db.StringProperty(required=True, choices = set(["ask", "ignore"])) # default should be maybe 'ignore' to make it work on an opt-in basis (set to 'ask' for now)
	tea_pref = db.StringProperty()

def checkUserExists(useremail):
  query = db.GqlQuery("SELECT * FROM Registry WHERE user_email='" + useremail + "'")
  for result in query:
    return True
  return False

def getTeaPreference(useremail):
  userExists = checkUserExists(useremail)
  if not userExists:
	  # user does not exist so need to add
	  registry = Registry(user_email = useremail, ignore_status = 'ask', tea_pref = 'no tea preference')
	  registry.put()
	  return registry.tea_pref
  else:
	  registryKey = db.Key.from_path('Registry', useremail)
	  registry = db.get(registryKey)
	  return registry.tea_pref

def setTeaPreference(useremail, preference):
  registry = Registry(user_email = useremail, ignore_status = 'ask', tea_pref = 'no tea preference')
  registry.put()

def clearTeaPreference(useremail):
  registryKey = db.Key.from_path('Registry', useremail)
  registry = db.get(registryKey)
  registry.tea_pref = 'no tea preference'
  registry.put()
