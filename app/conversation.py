
# Trigger words
TRIGGER_HELLO = r"hi|hello|morning|afternoon|evening|hey|sup"
TRIGGER_YES = r"yes|yeh|ya|booyah|ok|please|totally|definitely|absolutely|yeah|yup|affirmative|yarr|yah|please|sure|okay|alright|yep|go on|certainly"
TRIGGER_TEA = r"cuppa|tea|brew|cup|drink|beverage|refreshment"
TRIGGER_GOAWAY = r"go away|busy|from home|not today"
TRIGGER_ADDPERSON = r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b"
TRIGGER_TEAPREFS = r"earl gr[ae]y|peppermint|milk|sugar|white|black|roibos|chai|green tea|ceylon|camomile|herbal tea"
TRIGGER_RUDE = "ZnVja3xzaGl0fGJvbGxvY2tzfGJpdGNofGJhc3RhcmR8cGVuaXN8Y29ja3xoZWxsIHxwaXNzfHJl\ndGFyZHxjdW50fGNvZmZlZQ=="
#(If you decode this and are offended, it's your own fault. It is a list of things mrs doyle will shout at you for saying...)

# Responses
NEWBIE_GREETING = "Well hello dear, my name is Mrs Doyle. If you ever want tea, just ask me and I'll see what I can do! Of course if you're busy and don't want me bugging you, just say so and I'll back off."

ADDPERSON = [
  "Oh, I'll go introduce myself then!",
  "Another potential tea drinker? Perfect!"]

GREETING = [
  "Well hello dear", 
  "Top o' the mornin' to ya", 
  "Hello", 
  "Hi", 
  "Good morning father", 
  "Beautiful day outside isn't it?", 
  "How do?",
  "I'm feeling fat, and sassy"]
  
WANT_TEA = [
  "Will you have a cup of tea?", 
  "Will you have a cup of tea father?", 
  "We were just about to have a cup of tea, will you join us?", 
  "Join us in a cup of tea?", 
  "Tea perchance?", 
  "Could I interest you in a brew?", 
  "Hot beverage?",
  "Take time for tea?",
  "You look thirsty dear, tea?",
  "You know what I fancy, a cuppa. Will you be joining us?", 
  "Will you have a cup of tea? I *probably* won't choose you to make it..."
  "Tea for two, two for tea... will you join us?",
  "What would you say to a cup father?",
  "If a man has no tea in him, he is incapable of understanding truth and beauty. Won't you have a cup?",
  "Fancy a cup o' the hot stuff?"]
  
NOBACKOUT = [
  "I heard you already, tea's coming up",
  "Your fate is secured, back out now and the whole system crumbles. You *will* have tea.", 
  "You are already in the list of tea drinkers. There's no getting out of it now.", 
  "Too late for that, you know you want tea really.",
  "I can't hear you, I'm on my way to the kitchen"]
  
AHGRAND = [
  "Ah, grand! I'll wait a couple of minutes and see if anyone else wants one", 
  "Champion.", 
  "You won't regret it!", 
  "Wonderful!", 
  "I'm so glad!", 
  "Oh I _am_ pleased!",
  "Perfect!",
  "Lovely",
  "Absolutely splendiferous",
  "Marvellous!", 
  "Oh good, I do like a cup of tea!", 
  "Fabulous!"]
  
AH_GO_ON = [
  "Ah, go on! Won't you just have a cup", 
  "There's childers in Africa who can't even have tea. Won't you just have a cup", 
  "Ah go on go on go on", 
  "Go on, go on, go on", 
  "It's no bother, really", 
  "It would make me so happy if you'd just have a cup", 
  "A cup of tea a day keeps the doctor away.", 
  "Go on, it'll do you a world of good.",
  "If a man has no tea in him, he is incapable of understanding truth and beauty.",
  "Are you sure, Father? There's cocaine in it! "]
  
GOOD_IDEA = [
  "Fantastic idea, I'll see who else wants one and get back to you in a couple of minutes", 
  "Yay, tea!"
  "I was just about to suggest the same thing. I'll see who else wants one", 
  "Coming right up... in a couple of minutes", 
  "What a delightful idea! I'll let you know who else is in",
  "Oh yes, let's! I'll ask around",
  "Tea you say? What a wonderful thought, I'll see who else agrees",
  "You do have the best ideas, I'll see who else will join us"]
  
ON_YOUR_OWN = [
  "You're on your own I'm afraid, nobody else wants one!", 
  "What? Well, this is embarrassing... nobody else seems to want tea :(", 
  "Well, this is practically unheard of, I could convince *nobody* to have a cup", 
  "Sad times indeed, tea for one today",
  "There was nobody... nobody at all, I'm so sorry!",
  "Not _one_ other person, can you believe it?",
  ":( I'm sorry, looks like you'll have to make it yourself"]
  
WELL_VOLUNTEERED = [
  "Well volunteered! The following other people want tea!",
  "Be a love and put the kettle on would you?",
  "Well, somebody has to make the tea, this time it's you",
  "Your time has come... Go make the tea.",
  "You know it's a wonderful thing you're about to do...",
  "You know what, I think it's your turn to make the tea now I think about it.",
  "Polly put the kettle on, kettle on, kettle on. You are Polly in this game.",
  "Why not stretch those weary legs and have a wander over to the kitchen. Say, while you're there...."]
  
OTHEROFFERED = [
  " has been kind enough to make the tea, I'd do it myself only I don't have arms",
  " has been kind enough to make the tea",
  " has been awarded the honour of providing you with tea",
  " is going to make tea for you, isn't that nice?",
  " will be bringing you some tea, don't forget to say thanks",
  " kindly offered to make the tea",
  " is about to selflessly put the kettle on",
  " is today's lucky tea lady",
  " will soon bring you a warm fuzzy feeling in a cup"]
  
HUH = [
  "I don't understand what you're saying...",
  "If it's not about tea, I'm afraid I'm not really interested...",
  "Pardon?",
  "Beg pardon?",
  "Hm?",
  "Umm.....",
  "Pancakes.",
  "I fail to see the relevance...",
  "Is there something I can do for you?",
  "Are you sure you're speaking English?",
  "Now really, whatever does that mean?",
  "I'm afraid I'm just not familiar with this new slang you young people use.",
  "You always say that!"]
  
RUDE = [
  "Now that's no way to talk to a lady",
  "Wash your mouth out with soap and water!",
  "Well that's not very polite is it?",
  "You won't get any tea talking like that!",
  "Ah, it's a bit much for me, father. 'Feck' this and 'feck' that. 'You big bastard'. Oh, dreadful language! 'You big hairy arse', 'You big fecker'. Fierce stuff! And of course, the f-word, father, the bad f-word, worse than 'feck' - you know the one I mean.",
  "'Eff you'. 'Eff your 'effin' wife'. Oh, I don't know why they have to use language like that. 'I'll stick this 'effin' pitchfork up your hole', oh, that was another one, oh, yes!"]
  
HOW_TO_TAKE_IT = [
  "How do you take your tea?",
  "And how do you take it?",
  "How do you like it?",
  "Milk? Sugar? Lemon? Shaken? Stirred anticlockwise?"]
  
NO_TEA_TODAY = [
  ":( Alright, I won't bother you again. Say hello if you change your mind",
  "Oh... I'm sorry, I'll leave you alone. Let me know if you change your mind though"]
  
JUST_MISSED = [
  "Sorry dear, too late!",
  "I'm afraid that ship has sailed...",
  "Too slow I'm afraid",
  "Snooze you lose, we already had tea.",
  "You'll have to pay closer attention next time, this round's been and gone"]

