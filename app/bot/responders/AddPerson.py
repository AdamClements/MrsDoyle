import bot.Responder
import bot.conversation
import xmpp

class AddPerson(Responder):
""" Checks for people asking to be left alone """
  def process_message(message, sender):
    global TRIGGER_ADDPERSON
    global ADDPERSON
    
    if re.search(TRIGGER_ADDPERSON, message, re.IGNORECASE):
      emailtoinvite = re.search("("+TRIGGER_ADDPERSON+")", message, re.IGNORECASE).group(0)
      xmpp.send_invite(emailtoinvite)
      send_random(talker.jid, ADDPERSON)
      return True
    else
      return False
