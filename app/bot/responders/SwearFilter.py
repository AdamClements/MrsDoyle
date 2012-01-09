import bot.Responder
import bot.conversation

class SwearFilter(Responder):
""" Checks for people using naughty words and rebukes them """
  def process_message(message, sender):
    global TRIGGER_RUDE
    global RUDE
    
    if re.search(base64.b64decode(TRIGGER_RUDE), message, re.IGNORECASE):
      send_random(sender.jid, RUDE)
      return True
    else:
      return False
