from datetime import datetime, timedelta
import random
import re
import wsgiref.handlers
import cgi
import base64
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
informed = set([])
settingprefs = set([])
teacountdown = False
doublejeopardy = ""
lastround = datetime.now()
  
class Roster(db.Model):
  jid = db.StringProperty(required=True)
  teaprefs = db.StringProperty(required=False, default="")
  askme = db.BooleanProperty(required=False, default=True)
  newbie = db.BooleanProperty(required=False, default=True)

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

def getSalutation(jid):
  return jid.split("@")[0].replace(".", " ").title() 

def buildWellVolunteeredMessage(person):
  finalMessage = random.sample(WELL_VOLUNTEERED, 1)[0] + '\n'
 
  for drinker in drinkers:
    if drinker != person:
      temp = Roster.get_by_key_name(drinker)
      teapref = temp.teaprefs
      finalMessage += " * " + getSalutation(drinker) + " ("+teapref+")" + '\n'
 
  return finalMessage

class XmppHandler(xmpp_handlers.CommandHandler):
  """Handler class for all XMPP activity."""

  def unhandled_command(self, message=None):
    message.reply("I don't have any secret easter egg commands.....")

  def text_message(self, message=None):
    global NOBACKOUT
    global GREETING
    global AHGRAND
    global GOOD_IDEA
    global NO_TEA_TODAY
    global JUST_MISSED
    global WANT_TEA
    
    global TRIGGER_YES
    global TRIGGER_TEA
    global TRIGGER_TEAPREFS
    
    global teacountdown
    global drinkers
    global settingprefs
    global lastround
    
    fromaddr = self.request.get('from').split("/")[0]    
    talker = Roster.get_or_insert(key_name=fromaddr, jid=fromaddr)
    
    # If they showed up in the middle of a round, ask them if they want tea in
    # the normal way after we've responded to this message
    if(talker.askme == False and teacountdown):
      send_random(fromaddr, WANT_TEA)
      informed.add(fromaddr)

    talker.askme=True
    talker.put()
    
    if SwearFilter.send_message(message.body, talker) return
    if GoAwayCheck.send_message(message.body, talker) return
              
    xmpp.send_presence(fromaddr, status="", presence_type=xmpp.PRESENCE_TYPE_AVAILABLE)

    # See if we're expecting an answer as regards tea preferences
    if fromaddr in settingprefs:
      talker.teaprefs = message.body
      talker.put()
      settingprefs.remove(fromaddr)
      xmpp.send_message(fromaddr, "Okay!")
      return
    
    if teacountdown:    
      if fromaddr in drinkers:
        if re.search(TRIGGER_TEAPREFS, message.body, re.IGNORECASE):
          xmpp.send_message(fromaddr, "So you like your tea '" + message.body + "'?")
          talker.teaprefs = message.body
          talker.put()
        elif re.search(TRIGGER_YES, message.body, re.IGNORECASE):
          xmpp.send_message(fromaddr, "Okay!")
        else:
          send_random(fromaddr, NOBACKOUT)
        return        
    
      if re.search(TRIGGER_YES, message.body, re.IGNORECASE):
        drinkers.add(fromaddr)
        send_random(fromaddr, AHGRAND)        
        howTheyLikeItClause(message.body, talker)       
        
      else:
        send_random(fromaddr, AH_GO_ON)
        
      return
    
    if AddPerson.send_message(message.body, talker) return

    if re.search(TRIGGER_TEA, message.body, re.IGNORECASE):
      send_random(fromaddr, GOOD_IDEA)
      howTheyLikeItClause(message.body, talker)
      
      drinkers.add(fromaddr)
      
      for person in get_roster():
        if person.askme and not person.jid == fromaddr:
          xmpp.send_presence(jid=person.jid, presence_type = xmpp.PRESENCE_TYPE_PROBE)
          
      doittask = Task(countdown="120", url="/maketea")
      doittask.add()
      teacountdown = True
      return      
      
    if re.search(TRIGGER_YES, message.body, re.IGNORECASE) and (datetime.now() - lastround) < timedelta(seconds=120):
      send_random(fromaddr, JUST_MISSED)
      return
      
    if RandomChatter.send_message(message.body, talker) return
    
class ProcessTeaRound(webapp.RequestHandler):
    def post(self):
      global ON_YOUR_OWN
      global WELL_VOLUNTEERED
      global OTHEROFFERED
      
      global drinkers
      global teacountdown
      global doublejeopardy    
      global lastround  
      global informed
      
      if len(drinkers) == 1:
        for n in drinkers:
          send_random(n, ON_YOUR_OWN)
      elif len(drinkers) > 0:        
        # Select someone who wasn't the last person to make the tea 
        doublejeopardy = teamaker = selectByMadeVsDrunkRatio(filter(lambda n : n != doublejeopardy, drinkers))
        
        for person in drinkers:
          if person == teamaker:
            statDrinker(person, len(drinkers))
            statRound  (person, len(drinkers))
            
            xmpp.send_message(person, buildWellVolunteeredMessage(person))
          else:
            send_random(person, OTHEROFFERED, getSalutation(teamaker))
            statDrinker(person)
        
      teacountdown = False     
      drinkers = set([])
      settingprefs = set([])
      informed = set([])
      lastround = datetime.now()
    

class Register(webapp.RequestHandler):
    def post(self):
      global WANT_TEA
      global NEWBIE_GREETING
      global teacountdown
      global informed
      
      fromaddr = self.request.get('from').split("/")[0]    
      person = Roster.get_or_insert(key_name=fromaddr, jid=fromaddr)
      
      if(person.newbie):
        xmpp.send_message(fromaddr, NEWBIE_GREETING)
        person.newbie = False
        person.put()

      if(not person.askme):
        xmpp.send_presence(fromaddr, status=":( Haven't heard from " + getSalutation(fromaddr) + " in a while...", presence_type=xmpp.PRESENCE_TYPE_AVAILABLE)
      else:
        xmpp.send_presence(fromaddr, status="", presence_type=xmpp.PRESENCE_TYPE_AVAILABLE)

      if(teacountdown and person.askme and fromaddr not in informed):
        send_random(fromaddr, WANT_TEA)
        informed.add(fromaddr)
      
def main():
  app = webapp.WSGIApplication([
      ('/maketea', ProcessTeaRound),
      ('/_ah/xmpp/message/chat/', XmppHandler),
      ('/_ah/xmpp/presence/available/', Register),
      ('/_ah/xmpp/subscription/subscribe/', Register),
      ], debug=True)
  wsgiref.handlers.CGIHandler().run(app)


if __name__ == '__main__':
  main()
