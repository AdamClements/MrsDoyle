import bot.Responder
import bot.conversation
import xmpp

class GoAwayCheck(Responder):
""" Checks for people asking to be left alone """
  def process_message(message, sender):
    global TRIGGER_GOAWAY
    global NO_TEA_TODAY
    
    if re.search(TRIGGER_GOAWAY, message, re.IGNORECASE):
      sender.askme=False
      sender.put()
      send_random(sender.jid, NO_TEA_TODAY)
      xmpp.send_presence(sender.jid, status=":( Leaving " + getSalutation(sender.jid) + " alone. So alone...", presence_type=xmpp.PRESENCE_TYPE_AVAILABLE)
      return True
    else
      return False
