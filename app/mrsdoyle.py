import datetime
import random
import re
import wsgiref.handlers
import cgi
from google.appengine.api import xmpp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.ereporter import report_generator
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import xmpp_handlers
from google.appengine.api.taskqueue import Task

from conversation import *
from stats import *

drinkers = set([])
settingprefs = set([])
teacountdown = False
doublejeopardy = ""

def send_random(recipient, choices, prefix=""):
  xmpp.send_message(recipient, prefix + random.sample(choices, 1)[0])
  
class Roster(db.Model):
  jid = db.StringProperty(required=True)
  teaprefs = db.StringProperty(required=False, default="")
  askme = db.BooleanProperty(required=False, default=True)

def get_roster():
  return Roster.all().fetch(limit=999)
  
def howTheyLikeItClause(message, talker):
  global TRIGGER_TEAPREFS
  global HOW_TO_TAKE_IT
  
  fromaddr = talker.jid
  
  # Try to work out if this includes a how they like it clause
  clauses = message.split(",")
  if len(clauses) > 1:
    del clauses[0]
    secondSentence = " ".join(clauses)
    if re.search(TRIGGER_TEAPREFS, secondSentence, re.IGNORECASE):
      talker.teaprefs = secondSentence
      talker.put()
      return
      
  # If they haven't given any preferences before
  if talker.teaprefs == "":
    send_random(fromaddr, HOW_TO_TAKE_IT)
    settingprefs.add(fromaddr)
    return   
      
def selectByMadeVsDrunkRatio(drinkers):
  # Build a dictionary mapping the contents of drinkers onto their made drunk ratio
  probs = dict()
  probTotal = 0.0
  
  for person in drinkers:
    ratio = getMadeDrunkRatio(person)
    probs[person] = ratio
    probTotal += ratio
    
  # Now if we generate a random point between 0 and the total probs, then iterate through
  # the dictionary of listeners, summing the probabilities as we go, as soon as the probs
  # tip over the total, that person has been randomly selected with a weight.
  goalNumber = probTotal * random.random()
  probSum = 0.0
  for person in probs.keys():
    probSum += probs[person]
    if probSum >= goalNumber:
      return person
      
  # We probably had a floating point rounding error. Randomly select the first person in the list :P    
  return drinkers[0]

class XmppHandler(xmpp_handlers.CommandHandler):
  """Handler class for all XMPP activity."""

  def unhandled_command(self, message=None):
    message.reply("I don't have any secret easter egg commands.....")
        
  def debug_command(self, message=None):
    message.reply("In order to save your soul, the temptation to game the system has been removed and Mrs Doyle is now inscrutable")
    
  def testDist_command(self, message=None):
    global drinkers
    
    drinkers = set(["amanda@touchtype-online.com", "george@touchtype-online.com", "paul@paulbutcher.com", "alex@touchtype-online.com"])
    results = dict(zip(drinkers, [0,0,0,0]))
    
    for x in range(100):
      choice = selectByMadeVsDrunkRatio(drinkers)
      results[choice] = results[choice] + 1
      
    for x in results.keys():
      message.reply(x + ": " + str(results[x]) + " given a made drunk ratio of " + str(getMadeDrunkRatio(x)))
      

  def text_message(self, message=None):
    global NOBACKOUT
    global GREETING
    global AHGRAND
    global GOOD_IDEA
    global HUH
    global RUDE
    global NO_TEA_TODAY
    
    global TRIGGER_HELLO
    global TRIGGER_YES
    global TRIGGER_TEA
    global TRIGGER_RUDE
    global TRIGGER_GOAWAY
    
    global teacountdown
    global drinkers
    global settingprefs
    
    fromaddr = self.request.get('from').split("/")[0]    
    talker = Roster.get_or_insert(key_name=fromaddr, jid=fromaddr)
    talker.askme=True
    talker.put()
    
    # Mrs Doyle takes no crap
    if re.search(TRIGGER_RUDE, message.body, re.IGNORECASE):
      send_random(fromaddr, RUDE)
      return
      
    # See if we're expecting an answer as regards tea preferences
    if fromaddr in settingprefs:
      talker.teaprefs = message.body
      talker.put()
      settingprefs.remove(fromaddr)
      return
    
    if teacountdown:    
      if fromaddr in drinkers:
        send_random(fromaddr, NOBACKOUT)
        return
        
      if re.search(TRIGGER_GOAWAY, message.body, re.IGNORECASE):
        talker.askme=False
        talker.put()
        send_random(fromaddr, NO_TEA_TODAY)
        return
    
      if re.search(TRIGGER_YES, message.body, re.IGNORECASE):
        drinkers.add(fromaddr)
        send_random(fromaddr, AHGRAND)        
        howTheyLikeItClause(message.body, talker)       
        
      else:
        send_random(fromaddr, AH_GO_ON)
    elif re.search(TRIGGER_TEA, message.body, re.IGNORECASE):
      send_random(fromaddr, GOOD_IDEA)
      howTheyLikeItClause(message.body, talker)
      
      drinkers.add(fromaddr)
      
      for person in get_roster():
        if person.askme and not person.jid == fromaddr:
          xmpp.send_presence(jid=person.jid, presence_type = xmpp.PRESENCE_TYPE_PROBE)
          
      doittask = Task(countdown="120", url="/maketea")
      doittask.add()
      teacountdown = True
      
    elif re.search(TRIGGER_HELLO, message.body, re.IGNORECASE):
      send_random(fromaddr, GREETING)
    else:
      send_random(fromaddr, HUH)
    
class DoThis(webapp.RequestHandler):
    def post(self):
      global ON_YOUR_OWN
      global WELL_VOLUNTEERED
      global OTHEROFFERED
      
      global drinkers
      global teacountdown
      global doublejeopardy      
      
      if len(drinkers) == 1:
        for n in drinkers:
          send_random(n, ON_YOUR_OWN)
      elif len(drinkers) > 0:        
        # Select someone who wasn't the last person to make the tea 
        doublejeopardy = teamaker = selectByMadeVsDrunkRatio(filter(lambda n : n != doublejeopardy, drinkers))
        
        for person in drinkers:
          if person == teamaker:
            send_random(person, WELL_VOLUNTEERED)
            statDrinker(person, len(drinkers))
            statRound  (person, len(drinkers))
            
            for drinker in drinkers:
              if drinker != person:
                temp = Roster.get_by_key_name(drinker)
                teapref = temp.teaprefs
                xmpp.send_message(person, drinker.split("@")[0].title() + "("+teapref+")")
          else:
            send_random(person, OTHEROFFERED, teamaker.split("@")[0].title())
            statDrinker(person)
        
      teacountdown = False     
      drinkers = set([])
      settingprefs = set([])

class Register(webapp.RequestHandler):
    def post(self):
      global WANT_TEA
      global teacountdown
      
      fromaddr = self.request.get('from').split("/")[0]    
      Roster.get_or_insert(key_name=fromaddr, jid=fromaddr)
      
      if(teacountdown):
        send_random(fromaddr, WANT_TEA)
      
def main():
  app = webapp.WSGIApplication([
      ('/maketea', DoThis),
      ('/_ah/xmpp/message/chat/', XmppHandler),
      ('/_ah/xmpp/presence/available/', Register),
      ('/_ah/xmpp/subscription/subscribe/', Register),
      ], debug=True)
  wsgiref.handlers.CGIHandler().run(app)


if __name__ == '__main__':
  main()
