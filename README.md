What does Mrs Doyle do?
=======================

Mrs Doyle is a tool to solve a problem which has plagued offices for centuries, “Whose turn is it to make the tea?”

Now usually it’s down to the newest member of the team, or perhaps somebody that nobody really likes, but here everybody is equal. It is Mrs Doyle's responsibility to stay in touch with everybody throughout the day to make sure that they are sufficiently hydrated. As soon as one person hints – however subtly – that they may be in need of a beverage, Mrs Doyle asks the whole office whether they might be persuaded to have a cup of tea.

Once she has surveyed everybody in the office about their imminent desire to imbibe, she fairly and equitably appoints one of the tea drinking cohort and delegates to them the responsibility of providing for their fellow consumers. Her ways are mysterious and oftentimes people get the impression that they are being victimised in some way, but over time they come to find that Mrs Doyle really does know best. What’s more it adds a touch of adrenaline into an otherwise sedentary pursuit. It really is quite a rush not being chosen!


Setting Up:
===========

Mrs Doyle uses the Google App Engine (www.appspot.com) and works best within hosted google services. It’s fairly simple and written in Python. You can simply modify and add a range of different responses for different situations by editing conversation.py

To get started, you should download the google app engine SDK and register an appspot.com account. If you then download the code upload it using the google sdk tools (how to do this depends on whether you are using linux or windows, the documentation is available online but basically involves pointing a tool at the app folder and typing in your email address/password). *Firstly however* you will need to edit app.yaml to reflect the app name you registered on _your_ google appspot account. 

Once she has been successfully deployed, go to your google talk client (or the chat window in your gmail) and add <youruploadedappname>@appspot.com to your contacts (I’m afraid the app name mrsdoyle is already taken). 

You should now be able to talk to her, and if you mention tea, she will ask everyone who is online whether they want tea. They then have 120 seconds to answer yes or no, after which Mrs Doyle will select somebody at random who has to make the tea (weighted for fairness towards people who have drunk more than they’ve made). They will receive a list of all the people they have to brew for.

Obviously this is just a bit of fun and so there are no real licensing terms, but it would be nice to know if you do make use of it in your office. If you add any cool functionality and are in a sharing mood, that would be great too!

Usage tips:
=============
* Any mention of tea, brew, cuppa etc will start a round, so be careful what you say to her if you don't actually want tea!
* The first time you say yes (or "please" or "sure" etc.) to a cup of tea, she will ask you how you like it. If you answer her, she will tell whoever has to make the tea how you like it. She will also remember and use this for next time too.
* If you want to change how you take your tea, simply tell her by saying something like "yes, milk no sugar please" (the comma is the important bit) in response to her asking you whether you want a cup of tea. Again she will remember this until you tell her other wise.
* Once you have said yes, there is no backing out.
* If you are busy and do not wish to be disturbed, simply say so and she will leave you alone for the rest of the day.
* Once you have had a few cups of tea, go to <yourappname>.appspot.com/stats to see some interesting statistics about how many cups of tea have been drunk as well as who's been luckiest in terms of cups made vs drunk!

Finally
============
I'd absolutely love it if you let me know when this app gets used! Heck, I might even fix issues/take feature requests if I'm feeling kindly.