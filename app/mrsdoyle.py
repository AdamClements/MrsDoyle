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
    global someone
    global roster
    global teacountdown
    global drinkers
    
    fromaddr = self.request.get('from').split("/")[0]
    roster.add(fromaddr)
    
    if teacountdown:
      if fromaddr in drinkers:
        message.reply("You are already in the list of tea drinkers. there's no getting out of it now.")
        return
    
      if re.search(r"yes|yeh|ya|booyah|ok|please|totally|definitely|absolutely|yeah|yup|affirmative|yarr|yah|please|sure", message.body, re.IGNORECASE):
        drinkers.add(fromaddr)
        message.reply("Ah, grand! I'll wait a couple of minutes and see if anyone else wants one")
      else:
        message.reply("Ah, go on! Won't you just have a cup")
    elif re.search(r"cuppa|tea|brew", message.body, re.IGNORECASE):
      message.reply("Fantastic idea, I'll see who else wants one and get back to you in a couple of minutes")
      drinkers.add(fromaddr)
      
      for person in roster:
        if not person == fromaddr:
          xmpp.send_presence(jid=person, presence_type = xmpp.PRESENCE_TYPE_PROBE)
          
      doittask = Task(countdown="120", url="/maketea")
      doittask.add()
      teacountdown = True
      
    elif re.search(r"hi|hello|morning|afternoon|evening", message.body, re.IGNORECASE):
      message.reply("Top o' the morning to ya")
    else:
      message.reply("I don't understand what you're saying.... ")
    
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
      global drinkers
      global teacountdown
      teamaker = random.sample(drinkers, 1)[0]
      
      if drinkers == set([teamaker]):
        xmpp.send_message(teamaker, "Nobody else wants one, you're on your own I'm afraid!")
      else:      
        for person in drinkers:
          if person == teamaker:
            xmpp.send_message(person, "Well volunteered! The following other people want tea:")
            for drinker in drinkers:
              if drinker != person:
                xmpp.send_message(person, drinker.split("@")[0].title())
          else:
            xmpp.send_message(person, teamaker.split("@")[0].title() + " has been kind enough to offer to make the tea, I'd do it myself only I don't have arms.")
        
      teacountdown = False     
      drinkers = set([])

class Register(webapp.RequestHandler):
    def post(self):
      global roster
			global teacountdown
      person = self.request.get('from').split("/")[0]
      roster.add(person)
			
			if(teacountdown):
				xmpp.send_message(person, "Will you have a cup of tea??")  
      
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
