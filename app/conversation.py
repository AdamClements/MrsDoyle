
# Trigger words
TRIGGER_HELLO = r"hi|hello|morning|afternoon|evening|hey|sup"
TRIGGER_YES = r"yes|yeh|ya|booyah|ok|please|totally|definitely|absolutely|yeah|yup|affirmative|yarr|yah|please|sure|okay|alright|yep|go on|certainly"
TRIGGER_TEA = r"cuppa|tea|brew|cup|drink|beverage|refreshment"
TRIGGER_GOAWAY = r"go away|busy|from home|not today"
TRIGGER_TEAPREFS = r"milk|sugar|white|black|roibos"
TRIGGER_RUDE = r"fuck|shit|bollocks|bitch|bastard|penis|cock|hell |piss|retard|cunt|swype|coffee|nuance"
#(I apologise for any offence caused, but we had to be comprehensive in order to rebuke the foul mouthed)

# Responses
GREETING = set([
  "Well hello dear", 
  "Top o' the mornin' to ya", 
  "Hello", 
  "Hi", 
  "Good morning father", 
  "Beautiful day outside isn't it?", 
  "I'm feeling fat, and sassy"])
  
WANT_TEA = set ([
  "Will you have a cup of tea?", 
  "Will you have a cup of tea father?", 
  "We were just about to have a cup of tea, will you join us?", 
  "Join us in a cup of tea?", 
  "Tea perchance?", 
  "Could I interest you in a brew?", 
  "Hot beverage?", 
  "Tea for two, two for tea... will you join us?",
  "What would you say to a cup father?",
  "There's always time for a nice cup of tea. Sure, didn't the Lord himself pause for a nice cup of tea before giving himself up for the world. ",
  "Fancy a cup o' the hot stuff?"])
  
NOBACKOUT = set([
  "I heard you already, tea's coming up",
  "Your fate is secured, back out now and the whole system crumbles. You *will* have tea.", 
  "You are already in the list of tea drinkers. There's no getting out of it now.", 
  "Too late for that, you know you want tea really.",
  "I can't hear you, I'm on my way to the kitchen"])
  
AHGRAND = set([
  "Ah, grand! I'll wait a couple of minutes and see if anyone else wants one", 
  "Champion.", 
  "You won't regret it!", 
  "Wonderful!", 
  "I'm so glad!", 
  "Marvellous!", 
  "Oh good, I do like a cup of tea!", 
  "Fabulous!"])
  
AH_GO_ON = set([
  "Ah, go on! Won't you just have a cup", 
  "There's childers in Africa who can't even have tea. Won't you just have a cup", 
  "Ah go on go on go on", 
  "Go on, go on, go on", 
  "It's no bother, really", 
  "It would make me so happy if you'd just have a cup", 
  "A cup of tea a day keeps the doctor away.", 
  "Go on, it'll do you a world of good.",
  "Are you sure, Father? There's cocaine in it! "])
  
GOOD_IDEA = set([
  "Fantastic idea, I'll see who else wants one and get back to you in a couple of minutes", 
  "I was just about to suggest the same thing. I'll see who else wants one", 
  "Coming right up... in a couple of minutes", 
  "You do have the best ideas, I'll see who else will join us"])
  
ON_YOUR_OWN = set([
  "You're on your own I'm afraid, nobody else wants one!", 
  "What? Well, this is embarrassing... nobody else seems to want tea :(", 
  "Well, this is practically unheard of, I could convince *nobody* to have a cup", 
  "Sad times indeed, tea for one today"])
  
WELL_VOLUNTEERED = set([
  "Well volunteered! The following other people want tea!",
  "Be a love and put the kettle on would you?",
  "You know what, I think it's your turn to make the tea now I think about it.",
  "Polly put the kettle on, kettle on, kettle on. You are Polly in this game.",
  "Why not stretch those weary legs and have a wander over to the kitchen. Say, while you're there...."])
  
OTHEROFFERED = set([
  " has been kind enough to make the tea, I'd do it myself only I don't have arms",
  " has been kind enough to make the tea",
  " kindly offered to make the tea",
  " is about to selflessly put the kettle on",
  " is today's lucky tea lady",
  " will soon bring you a warm fuzzy feeling in a cup"])
  
HUH = set([
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
  "Oh, no, not cocaine. God, what am I on about? No, what d'you call them. Raisins. ",
  "Football, football, football, football, football, football, football, football, football... what you men see in it, I don't know. ",
  "You always say that!"])
  
RUDE = set([
  "Now that's no way to talk to a lady",
  "Wash your mouth out with soap and water!",
  "Well that's not very polite is it?",
  "You won't get any tea talking like that!",
  "Ah, it's a bit much for me, father. 'Feck' this and 'feck' that. 'You big bastard'. Oh, dreadful language! 'You big hairy arse', 'You big fecker'. Fierce stuff! And of course, the f-word, father, the bad f-word, worse than 'feck' - you know the one I mean.",
  "'Eff you'. 'Eff your 'effin' wife'. Oh, I don't know why they have to use language like that. 'I'll stick this 'effin' pitchfork up your hole', oh, that was another one, oh, yes!",
  "'Ride me sideways' was another one!"])
  
HOW_TO_TAKE_IT = set([
  "How do you take your tea?",
  "And how do you take it?",
  "How do you like it?"])
  
NO_TEA_TODAY = set([
  ":( Alright, I won't bother you again. Say hello if you change your mind",
  "Oh... I'm sorry, I'll leave you alone. Let me know if you change your mind though"])

