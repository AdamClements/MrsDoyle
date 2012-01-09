import re

class Responder():
""" This is a module which accepts a message and chooses whether to handle it or not """
  
  def __send_random(recipient, choices, substitutions):
    """ Chooses a random response from a given list, optionally with substitutions 
        (which may or may not be provided or used)
    """
    message = random.sample(choices, 1)[0]    
    for item in substitutions:
      message = message.replace('{%s}' % item, substitutions[item])
      
    xmpp.send_message(recipient, message)
    
  def __matches(message, regex):
    """ Checks if the given regex matches the message, case insensitively """
    return re.search(regex, message, re.IGNORECASE)
    
  def process_message(message, sender):
    """ Processes a message from the user and decides whether to act on it.
        If this should be the last action and end the chain of delegation, 
        return True, otherwise return False 
        
        message: String text of the message
        sender:  Roster object containing the details of the person who
                 sent the message
    """
    return False
