import re
import base64
import random

from google.appengine.api import xmpp

from bot.conversation import *

class Responder():
  """ This is a module which accepts a message and chooses whether to handle it or not """
  
  def send_random(self, recipient, choices, substitutions=dict()):
    """ Chooses a random response from a given list, optionally with substitutions 
        (which may or may not be provided or used)
    """
    message = random.sample(choices, 1)[0]    
    for item in substitutions:
      message = message.replace('{%s}' % item, substitutions[item])
      
    xmpp.send_message(recipient, message)
    
  def __matches(self, message, regex):
    """ Checks if the given regex matches the message, case insensitively """
    return re.search(regex, message, re.IGNORECASE)
    
  def process_message(self, message, sender):
    """ Processes a message from the user and decides whether to act on it.
        If this should be the last action and end the chain of delegation, 
        return True, otherwise return False 
        
        message: String text of the message
        sender:  Roster object containing the details of the person who
                 sent the message
    """
    return False


class AddPerson(Responder):
  """ Scans the message for email addresses, assumes that you want to add
      them to the current tea group
  """
  def process_message(self, message, sender):
    global TRIGGER_ADDPERSON
    global ADDPERSON
    
    if re.search(TRIGGER_ADDPERSON, message, re.IGNORECASE):
      emailtoinvite = re.search("("+TRIGGER_ADDPERSON+")", message, re.IGNORECASE).group(0)
      xmpp.send_invite(emailtoinvite)
      self.send_random(sender.jid, ADDPERSON)
      return True
    else:
      return False


class GoAwayCheck(Responder):
  """ Checks for people asking to be left alone """
  def process_message(self, message, sender):
    global TRIGGER_GOAWAY
    global NO_TEA_TODAY
    
    if re.search(TRIGGER_GOAWAY, message, re.IGNORECASE):
      sender.askme=False
      sender.put()
      self.send_random(sender.jid, NO_TEA_TODAY)
      xmpp.send_presence(sender.jid, status=":( Leaving " + getSalutation(sender.jid) + " alone. So alone...", presence_type=xmpp.PRESENCE_TYPE_AVAILABLE)
      return True
    else:
      return False


class RandomChatter(Responder):
  """ Generic responses to inconsequential chatter """
  def process_message(self, message, sender):
    global TRIGGER_HELLO
    global GREETING
    global HUH
    
    if re.search(TRIGGER_HELLO, message, re.IGNORECASE):
      self.send_random(sender.jid, GREETING)
    else:
      self.send_random(sender.jid, HUH)
      
    return True


class SwearFilter(Responder):
  """ Checks for people using naughty words and rebukes them """
  def process_message(self, message, sender):
    global TRIGGER_RUDE
    global RUDE
    
    if re.search(base64.b64decode(TRIGGER_RUDE), message, re.IGNORECASE):
      self.send_random(sender.jid, RUDE)
      return True
    else:
      return False
