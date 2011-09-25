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

roster = set([])
drinkers = set([])
teacountdown = False

# Trigger words
TRIGGER_HELLO = r"hi|hello|morning|afternoon|evening"
TRIGGER_YES = r"yes|yeh|ya|booyah|ok|please|totally|definitely|absolutely|yeah|yup|affirmative|yarr|yah|please|sure"
TRIGGER_TEA = r"cuppa|tea|brew"

# Responses
GREETING = set(["Well hello dear", "Top o' the mornin' to ya", "Hello", "Hi", "Good morning father", "Beautiful day outside isn't it?", "I'm feeling fat, and sassy"])
WANT_TEA = set (["Will you have a cup of tea?", "Will you have a cup of tea father?", "We were just about to have a cup of tea, will you join us?", "Join us in a cup of tea?", "Tea perchance?", "Could I interest you in a brew?", "Hot beverage?"])
NOBACKOUT = set(["Your fate is secured, back out now and the whole system crumbles. You *will* have tea.", "You are already in the list of tea drinkers. There's no getting out of it now."])
AHGRAND = set(["Ah, grand! I'll wait a couple of minutes and see if anyone else wants one", "Champion.", "You won't regret it!", "Wonderful!", "I'm so glad!"])
AH_GO_ON = set(["Ah, go on! Won't you just have a cup", "There's childers in Africa who can't even have tea. Won't you just have a cup", "Ah go on go on go on", "Go on, go on, go on", "It's no bother, really", "It would make me so happy if you'd just have a cup"])
GOOD_IDEA = set(["Fantastic idea, I'll see who else wants one and get back to you in a couple of minutes", "I was just about to suggest the same thing. I'll see who else wants one", "Coming right up... in a couple of minutes"])
ON_YOUR_OWN = set(["You're on your own I'm afraid, nobody else wants one!", "What? Well, this is embarrassing... nobody else seems to want tea :(", "Well, this is practically unheard of, I could convince *nobody* to have a cup", "Sad times indeed, tea for one today"])
WELL_VOLUNTEERED = set(["Well volunteered! The following other people want tea!", "Be a love and put the kettle on would you?", "You know what, I think it's your turn to make the tea now I think about it.", "Polly put the kettle on, kettle on, kettle on. You are Polly in this game.", "The tea was a lie, you'll have to make it for yourself", "Why not stretch those weary legs and have a wander over to the kitchen. Say, while you're there...."])
OTHEROFFERED = set([" has been kind enough to make the tea, I'd do it myself only I don't have arms", " has been kind enough to make the tea", " kindly offered to make the tea", " is about to selflessly put the kettle on", " is today's lucky tea lady", " will soon bring you a warm fuzzy feeling in a cup"])
HUH = set(["I don't understand what you're saying...", "If it's not about tea, I'm afraid I'm not really interested...", "Pardon?", "Beg pardon?", "Hm?", "Umm.....", "Pancakes.", "I fail to see the relevance...", "Is there something I can do for you?"])


def send_random(recipient, choices, prefix=""):
  xmpp.send_message(recipient, prefix + random.sample(choices, 1)[0])

class XmppHandler(xmpp_handlers.CommandHandler):
  """Handler class for all XMPP activity."""

  def unhandled_command(self, message=None):
    # Show help text
    message.reply("I don't have any secret easter egg commands.....")
        
  def debug_command(self, message=None):
    global roster
    global drinkers
    global teacountdown
    message.reply("Roster: " + ", ".join(roster))
    message.reply("Drinkers: " + ", ".join(drinkers))
    message.reply("CountingDown " + str(teacountdown))

  def text_message(self, message=None):
    global NOBACKOUT
    global GREETING
    global AHGRAND
    global GOOD_IDEA
    global HUH
    
    global TRIGGER_HELLO
    global TRIGGER_YES
    global TRIGGER_TEA
    
    global roster
    global teacountdown
    global drinkers
    
    fromaddr = self.request.get('from').split("/")[0]
    roster.add(fromaddr)
    
    if teacountdown:
      if fromaddr in drinkers:
        send_random(fromaddr, NOBACKOUT)
        return
    
      if re.search(TRIGGER_YES, message.body, re.IGNORECASE):
        drinkers.add(fromaddr)
        send_random(fromaddr, AH_GRAND)
      else:
        send_random(fromaddr, AH_GO_ON)
    elif re.search(TRIGGER_TEA, message.body, re.IGNORECASE):
      send_random(fromaddr, GOOD_IDEA)
      drinkers.add(fromaddr)
      
      for person in roster:
        if not person == fromaddr:
          xmpp.send_presence(jid=person, presence_type = xmpp.PRESENCE_TYPE_PROBE)
          
      doittask = Task(countdown="120", url="/maketea")
      doittask.add()
      teacountdown = True
      
    elif re.search(TRIGGER_HELLO, message.body, re.IGNORECASE):
      send_random(fromaddr, GREETING)
    else:
      send_random(fromaddr, HUH)
    
  def attemptsend_command(self, message=None):    
    global teacountdown
    global roster
    for person in roster:
      xmpp.send_presence(jid=person, presence_type = xmpp.PRESENCE_TYPE_PROBE)
    
    doittask = Task(countdown="15", url="/maketea")
    doittask.add()
    teacountdown = True
    
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
                xmpp.send_message(person, drinker.split("@")[0].title())
          else:
            send_random(person, OTHEROFFERED, teamaker.split("@")[0].title())
        
      teacountdown = False     
      drinkers = set([])

class Register(webapp.RequestHandler):
    def post(self):
      global WANT_TEA
      global roster
      global teacountdown
      
      person = self.request.get('from').split("/")[0]
      roster.add(person)
      
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
