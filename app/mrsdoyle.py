import datetime
import logging
import random
import os
import re
import wsgiref.handlers
import cgi
from registry import *
from google.appengine.api import xmpp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.ereporter import report_generator
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import xmpp_handlers
from google.appengine.api.taskqueue import Task
from pprint import pprint 

drinkers = set([])
settingprefs = set([])
teacountdown = False

# Trigger words
TRIGGER_HELLO = r"hi|hello|morning|afternoon|evening"
TRIGGER_YES = r"yes|yeh|ya|booyah|ok|please|totally|definitely|absolutely|yeah|yup|affirmative|yarr|yah|please|sure|okay|alright|yep|go on"
TRIGGER_TEA = r"cuppa|tea|brew|cup|drink|beverage|refreshment"
TRIGGER_GOAWAY = r"go away|busy|from home|not today"
TRIGGER_TEAPREFS = r"milk|sugar|white|black|roibos"
TRIGGER_RUDE = r"fuck|shit|bollocks|bitch|bastard|penis|cock|hell |piss|retard|cunt|swype|coffee"
#(I apologise for any offence caused, but we had to be comprehensive in order to rebuke the foul mouthed)

# Responses
GREETING = set(["Well hello dear", "Top o' the mornin' to ya", "Hello", "Hi", "Good morning father", "Beautiful day outside isn't it?", "I'm feeling fat, and sassy"])
WANT_TEA = set (["Will you have a cup of tea?", "Will you have a cup of tea father?", "We were just about to have a cup of tea, will you join us?", "Join us in a cup of tea?", "Tea perchance?", "Could I interest you in a brew?", "Hot beverage?", "Tea for two, two for tea... will you join us?"])
NOBACKOUT = set(["I heard you already, tea's coming up","Your fate is secured, back out now and the whole system crumbles. You *will* have tea.", "You are already in the list of tea drinkers. There's no getting out of it now.", "Too late for that, you know you want tea really."])
AHGRAND = set(["Ah, grand! I'll wait a couple of minutes and see if anyone else wants one", "Champion.", "You won't regret it!", "Wonderful!", "I'm so glad!", "Marvellous!", "Oh good, I do like a cup of tea!", "Fabulous!"])
AH_GO_ON = set(["Ah, go on! Won't you just have a cup", "There's childers in Africa who can't even have tea. Won't you just have a cup", "Ah go on go on go on", "Go on, go on, go on", "It's no bother, really", "It would make me so happy if you'd just have a cup", "A cup of tea a day keeps the doctor away.", "Go on, it'll do you a world of good."])
GOOD_IDEA = set(["Fantastic idea, I'll see who else wants one and get back to you in a couple of minutes", "I was just about to suggest the same thing. I'll see who else wants one", "Coming right up... in a couple of minutes", "You do have the best ideas, I'll see who else will join us"])
ON_YOUR_OWN = set(["You're on your own I'm afraid, nobody else wants one!", "What? Well, this is embarrassing... nobody else seems to want tea :(", "Well, this is practically unheard of, I could convince *nobody* to have a cup", "Sad times indeed, tea for one today"])
WELL_VOLUNTEERED = set(["Well volunteered! The following other people want tea!", "Be a love and put the kettle on would you?", "You know what, I think it's your turn to make the tea now I think about it.", "Polly put the kettle on, kettle on, kettle on. You are Polly in this game.", "Why not stretch those weary legs and have a wander over to the kitchen. Say, while you're there...."])
OTHEROFFERED = set([" has been kind enough to make the tea, I'd do it myself only I don't have arms", " has been kind enough to make the tea", " kindly offered to make the tea", " is about to selflessly put the kettle on", " is today's lucky tea lady", " will soon bring you a warm fuzzy feeling in a cup"])
HUH = set(["I don't understand what you're saying...", "If it's not about tea, I'm afraid I'm not really interested...", "Pardon?", "Beg pardon?", "Hm?", "Umm.....", "Pancakes.", "I fail to see the relevance...", "Is there something I can do for you?", "Are you sure you're speaking English?", "Now really, whatever does that mean?", "I'm afraid I'm just not familiar with this new slang you young people use."])
RUDE = set(["Now that's no way to talk to a lady", "Wash your mouth out with soap and water!", "Well that's not very polite is it?", "You won't get any tea talking like that!"])
HOW_TO_TAKE_IT = set(["How do you take your tea?", "And how do you take it?", "How do you like it?"])
NO_TEA_TODAY = set([":( Alright, I won't bother you again. Say hello if you change your mind", "Oh... I'm sorry, I'll leave you alone. Let me know if you change your mind though"])

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
      
class XmppHandler(xmpp_handlers.CommandHandler):
  """Handler class for all XMPP activity."""

  def unhandled_command(self, message=None):
    # Show help text
    message.reply("I don't have any secret easter egg commands.....")
    
        
  def debug_command(self, message=None):
    global drinkers
    global teacountdown
    message.reply("Drinkers: " + ", ".join(drinkers))
    message.reply("CountingDown " + str(teacountdown))

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
      teamaker = random.sample(drinkers, 1)[0]
      
      if drinkers == set([teamaker]):
        send_random(teamaker, ON_YOUR_OWN)
      else:      
        for person in drinkers:
          if person == teamaker:
            send_random(person, WELL_VOLUNTEERED)
            for drinker in drinkers:
              if drinker != person:
                teapref = Roster.get(drinker).teaprefs
                xmpp.send_message(person, drinker.split("@")[0].title() + "("+teapref+")")
          else:
            send_random(person, OTHEROFFERED, teamaker.split("@")[0].title())
        
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
        send_random(person, WANT_TEA)
      
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
