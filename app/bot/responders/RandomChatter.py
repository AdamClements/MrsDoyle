import bot.Responder
import bot.conversation

class RandomChatter(Responder):
""" Checks for people asking to be left alone """
  def process_message(message, sender):
    global TRIGGER_HELLO
    global GREETING
    global HUH
    
    if re.search(TRIGGER_HELLO, message, re.IGNORECASE):
      send_random(talker.jid, GREETING)
    else:
      send_random(talker.jid, HUH)
      
    return True
