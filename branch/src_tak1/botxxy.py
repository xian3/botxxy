# https://en.wikipedia.org/wiki/List_of_Internet_Relay_Chat_commands
# http://wiki.shellium.org/w/Writing_an_IRC_bot_in_Python
# http://forum.codecall.net/topic/59608-developing-a-basic-irc-bot-with-python/
# http://docs.python.org/2/library/ssl.html
# http://docs.python.org/2/library/hashlib.html
# https://www.hackthissite.org/articles/read/1050
# http://stackoverflow.com/questions/4719438/editing-specific-line-in-text-file-in-python

# Import the necessary libraries.
import socket
import ssl
#import hashlib
import time
import random

# Some basic variables used to configure the bot				
server = "boxxybabee.catiechat.net" # server
port = 6667 # default port
ssl_port = 6697 # ssl port
chans = ["#test", "#boxxy"] #default channels
botnick = "testbot" # bot nick
botuser = "I"
bothost = "m.botxxy.you.see"
botserver = "testserver"
botname = "testname"
botpassword = "bawksy"

# Global vars

lastcommand = ''
nicks = []
taggers = []
#alreadyPinged = False
tagged = ''
isTagOn = False
tmpstr = '' # General purpose temporary string

#============BASIC FUNCTIONS TO MAKE THIS A BIT EASIER===============

def ping(reply): # This is our first function! It will respond to server Pings.
		ircsock.send("PONG :Botxyy Pong\n")
		'''
	else: # The NICKSERV operation is here so we can identify the bots nick before joining the default channels
		ircsock.send("PONG :" + reply + "\n") # In some IRCds it is mandatory to reply to PING the same message we recieve
		print ("PONG :" + reply)
		time.sleep(3)
		ircsock.send("NICKSERV IDENTIFY " + botpassword + "\n") # Identifies the bot's nickname with nickserv
		time.sleep(3)
		joinChans(chans) # Joins the default channels
		'''

def sendChanMsg(chan, msg): # This sends a message to the channel 'chan'
	ircsock.send("PRIVMSG " + chan + " :" + msg + "\n")
	
def sendUserMsg(nick, msg): # This sends a notice to the nickname 'nick'
	ircsock.send("NOTICE " + nick + " :" + msg + "\n")
	
def getNick(msg): # Returns the nickname of whoever requested a command from a RAW irc privmsg. Example in commentary below.
	# ":b0nk!LoC@fake.dimension PRIVMSG #test :lolmessage"
	return msg.split('!')[0].replace(':','')

def getUser(msg): # Returns the user and host of whoever requested a command from a RAW irc privmsg. Example in commentary below.
	# ":b0nk!LoC@fake.dimension PRIVMSG #test :lolmessage"
	return msg.split(" PRIVMSG ")[0].translate(None, ':')

def getChannel(msg): # Returns the channel from whereever a command was requested from a RAW irc PRIVMSG. Example in commentary below.
	# ":b0nk!LoC@fake.dimension PRIVMSG #test :lolmessage"
	return msg.split(' PRIVMSG ')[-1].split(' :')[0]

def joinChan(chan): # This function is used to join channels.
	ircsock.send("JOIN " + chan + '\n')

def joinChans(chans): # This is used to join all the channels in the array 'chans'
	for i in chans:
		ircsock.send("JOIN " + i + '\n')

def hello(msg): # This function responds to a user that inputs "Hello testbot"
	nick = getNick(msg)
	chan = getChannel(msg)
	print(nick + " said hi in " + chan)
	ircsock.send("PRIVMSG " + chan + " :Hello " + nick + "! Type !help for more information.\n")

#========================END OF BASIC FUNCTIONS=====================

					#AUTHENTICATION
'''
# TODO: finish this
def authCmd(msg): # Authenticates a nick with the bot
	nick = getNick(msg)
	if '#' in msg.split(':')[1]:
		chan = getChannel(msg)
		sendChanMsg(chan, nick + " MADE A MISTAKE! LET'S ALL PRETENDE WE DIDN'T SEE THAT OK?")
		sendUserMsg(nick, "DO NOT DO THAT IN THE CHANNEL!!!")
	else:
		# ":b0nk!LoC@fake.dimension PRIVMSG :!pass password"
		password = msg.split("!pass")[1].translate(None, " ") # RAW password
		if (not password):
			sendUserMsg(nick, "Bad arguments. Usage: !pass <password>")
		else:
			print ("RAW: " + password)
			password = hashlib.sha256(password).hexdigest() # A HEX representation of the SHA-256 encrypted password
			print ("ENC: " + password)
			success = False
			f = open("auth.txt", 'r') # Opens auth.txt with 'r'ead-only permissions
			for line in f:
				print (line) # debugging
				if (line.split("|!|")[0] == nick) and (line.split("|!|")[1] == password):
					print(nick + " has authenticated successfully")
					success = True
					sendUserMsg(nick, "Correct password! You are now authenticated.")
			if not success:
				print(nick + " mistyped the password")
				sendUserMsg(nick, "Incorrect password!")
			f.close()
'''
					#INVITE

def inviteCmd(msg): # Parses the message to extract NICK and CHANNEL
	# ":b0nk!LoC@fake.dimension PRIVMSG #test :!invite "
	nick = getNick(msg)
	if '#' not in msg.split(':')[1]:
		print(nick + " sent !invite outside of a channel")
		sendUserMsg(nick, "You are not in a channel")
	else:
		chan = getChannel(msg)
		target = msg.split("!invite")[1].lstrip(' ')
		if target.__len__() <= 1: # Checks if user inserted a nickname to invite
			sendChanMsg(chan,"Bad arguments. Usage: !invite <nick>")
		else: # Success
			print ("Inviting " + target + " to channel " + chan)
			sendChanMsg(chan, "Inviting " + target + " here...")
			invite(target,chan)
	
def invite(nick,chan): # Invites given nickname to present channel
	ircsock.send("INVITE " + nick + " " + chan + "\n")

					#VOICE

def voiceCmd(msg):
	nick = getNick(msg)
	if '#' not in msg.split(':')[1]:
		print(nick + " sent !voice outside of a channel")
		sendUserMsg(nick, "You are not in a channel")
	else:
		chan = getChannel(msg)
		target = msg.split("!voice")[1].lstrip(' ')
		if target.__len__() <= 1: # Checks if user inserted a nickname to voice
			sendChanMsg(chan,"Bad arguments. Usage: !voice <nick>")
		else: # Success
			print ("Voicing " + target + " on channel " + chan)
			voice(target,chan)

def voice(nick,chan):
	ircsock.send("MODE " + chan + " +v " + nick + "\n")

					#DEVOICE

def devoiceCmd(msg):
	nick = getNick(msg)
	if '#' not in msg.split(':')[1]:
		print(nick + " sent !devoice outside of a channel")
		sendUserMsg(nick, "You are not in a channel")
	else:
		chan = getChannel(msg)
		target = msg.split("!devoice")[1].lstrip(' ')
		if target.__len__() <= 1: # Checks if user inserted a nickname to devoice
			sendChanMsg(chan,"Bad arguments. Usage: !devoice <nick>")
		elif target != botnick: # Success
			print ("Devoicing " + target + " on channel " + chan)
			devoice(target,chan)
		else:
			sendChanMsg(chan, "Don't you dare make me demote myself.")

def devoice(nick,chan):
	ircsock.send("MODE " + chan + " -v " + nick + "\n")

					#OP

def opCmd(msg):
	nick = getNick(msg)
	if '#' not in msg.split(':')[1]:
		print(nick + " sent !op outside of a channel")
		sendUserMsg(nick, "You are not in a channel")
	else:
		chan = getChannel(msg)
		target = msg.split("!op")[1].lstrip(' ')
		if target.__len__() <= 1: # Checks if user inserted a nickname to op
			sendChanMsg(chan,"Bad arguments. Usage: !op <nick>")
		else: # Success
			print ("Giving op to " + target + " on channel " + chan)
			op(target,chan)

def op(nick,chan):
	ircsock.send("MODE " + chan + " +o " + nick + "\n")

					#DEOP

def deopCmd(msg):
	nick = getNick(msg)
	if '#' not in msg.split(':')[1]:
		print(nick + " sent !deop outside of a channel")
		sendUserMsg(nick, "You are not in a channel")
	else:
		chan = getChannel(msg)
		target = msg.split("!deop")[1].lstrip(' ')
		if target.__len__() <= 1: # Checks if user inserted a nickname to deop
			sendChanMsg(chan,"Bad arguments. Usage: !deop <nick>")
		elif target != botnick: # Success
			print ("Taking op from " + target + " on channel " + chan)
			deop(target,chan)
		else:
			sendChanMsg(chan, "Don't you dare make me demote myself.")

def deop(nick,chan):
	ircsock.send("MODE " + chan + " -o " + nick + "\n")

					#HOP

def hopCmd(msg):
	nick = getNick(msg)
	if '#' not in msg.split(':')[1]:
		print(nick + " sent !hop outside of a channel")
		sendUserMsg(nick, "You are not in a channel")
	else:
		chan = getChannel(msg)
		target = msg.split("!hop")[1].lstrip(' ')
		if target.__len__() <= 1: # Checks if user inserted a nickname to hop
			sendChanMsg(chan,"Bad arguments. Usage: !hop <nick>")
		else: # Success
			print ("Giving hop to " + target + " on channel " + chan)
			hop(target,chan)

def hop(nick,chan):
	ircsock.send("MODE " + chan + " +h " + nick + "\n")

					#DEHOP

def dehopCmd(msg):
	nick = getNick(msg)
	if '#' not in msg.split(':')[1]:
		print(nick + " sent !dehop outside of a channel")
		sendUserMsg(nick, "You are not in a channel")
	else:
		chan = getChannel(msg)
		target = msg.split("!dehop")[1].lstrip(' ')
		if target.__len__() <= 1: # Checks if user inserted a nickname to dehop
			sendChanMsg(chan,"Bad arguments. Usage: !dehop <nick>")
		elif target != botnick: # Success
			print ("Taking hop from " + target + " on channel " + chan)
			dehop(target,chan)
		else:
			sendChanMsg(chan, "Don't you dare make me demote myself.")

def dehop(nick,chan):
	ircsock.send("MODE " + chan + " -h " + nick + "\n")

					#TOPIC

def topicCmd(msg):
	nick = getNick(msg)
	if '#' not in msg.split(':')[1]:
		print(nick + " sent !topic outside of a channel")
		sendUserMsg(nick, "You are not in a channel")
	else:
		chan = getChannel(msg)
		# ":b0nk!LoC@fake.dimension PRIVMSG #test :!topic 1 2 3 test"
		topic = msg.split("!topic")[1].lstrip(' ')
		if topic.__len__() <= 1:
			print ("New topic is empty")
			sendChanMsg(chan, "Bad arguments. Usage: !topic [<new topic>]")
		else:
			print(nick + " changed " + chan + " 's topic to '" + topic + "'")
			changeTopic(chan, topic)

def changeTopic(chan, topic):
	ircsock.send("TOPIC " + chan + " :" + topic + "\n")

					#KICK

def kickCmd(msg):
	nick = getNick(msg)
	if '#' not in msg.split(':')[1]:
		print(nick + " sent !kick outside of a channel")
		sendUserMsg(nick, "You are not in a channel")
	else:
		chan = getChannel(msg)
		target = msg.split("!kick")[1].lstrip(' ')
		if target.__len__() <= 1: # Checks if user inserted a nickname to kick
			sendChanMsg(chan,"Bad arguments. Usage: !kick <nick>")
		elif target == botnick:
			print (nick + " tried to kick the bot!")
			sendChanMsg(chan, "Don't make me kick myself out " + nick + "!")
		else:
			print ("Kicking " + target + " from " + chan)
			kick(target,chan,0)

def kick(nick,chan,isRand):
	if isRand:
		sendChanMsg(chan, "Randomly kicking " + nick + " from " + chan)
		ircsock.send("KICK " + chan + " " + nick + " lol butthurt\n")
	else:
		sendChanMsg(chan, "Kicking " + nick + " from " + chan)
		ircsock.send("KICK " + chan + " " + nick + " lol butthurt\n")

					#RANDOM KICK

def randKick(nicks,chan):
	size = len(nicks) - 1 # Correcting offset (this means if we have an array with 5 elements we should pick a random number between 0 and 4)
	rand = random.randint(0,size) # Picks a random number
	if botnick not in nicks[rand]: # Prevents bot from being kicked by !randkick
		print ("Randomly kicking " + nicks[rand].__str__() + " from channel " + chan)
		kick (nicks[rand],chan,1)
	else:
		print ("Bot will not be kicked. Picking another one...")
		randKick(nicks,chan)

					#DICE

def dice(msg):
	nick = getNick(msg)
	chan = getChannel(msg)
	dice = random.randint(1,6).__str__() # converts the integer dice to a string to be concatenated in the final output
	print (nick + " rolled the dice and got a " + dice)
	sendChanMsg(chan, nick + " rolled a " + dice)

					#QUOTES

def quoteCmd(msg): #TODO: quote IDs
	nick = getNick(msg)
	if '#' not in msg.split(':')[1]:
		print(nick + " sent !quote outside of a channel")
		sendUserMsg(nick, "You are not in a channel")
	else:
		chan = getChannel(msg)
		# ":b0nk!LoC@fake.dimension PRIVMSG #test :!quote random"
		'''
		if not msg.split("!quote")[1] or not msg.split("!quote ")[1]:
			sendChanMsg(chan,"Bad arguments. Usage: !quote num/random")
		else:
			quoteNum = msg.split("!quote ")[1]
			if quoteNum == "random":
		'''
		with open("quotes.txt", 'r') as f:# Opens quotes.txt with 'r'ead-only permissions
			line = random.choice(list(f)) # Picks a random line from the text file
		f.closed # Closes the file to save resources
		if line:
			author = line.split ("|!|")[0]
			quote = line.split ("|!|")[1]
			print (author + "\n" + quote) #debugging
			sendChanMsg(chan, "[Quote] " + quote)
		else:
			print("File quotes.txt is empty")
			sendChanMsg(chan, "There are no quotes on the DB. Could something be wrong???")

def addQuote(msg):
	nick = getNick(msg)
	if '#' not in msg.split(':')[1]: # Checks if quote was sent outside of a channel
		print(nick + " sent !addquote outside of a channel")
		sendUserMsg(nick, "You are not in a channel")
	else:
		chan = getChannel(msg)
		# ":b0nk!LoC@fake.dimension PRIVMSG #test :!quote random"
		newQuote = msg.split("!addquote")[1].lstrip(' ')
		if newQuote.__len__() <= 1: # Checks for empty quote
			sendChanMsg(chan,"Bad arguments. Usage: !addquote [<quote>]")
		else:
			print(nick + " added '" + newQuote + "'\n")
			with open("quotes.txt", 'a') as f:
				f.write(nick + "|!|" + newQuote + '\n') # Adds the quote and the nickname of who inserted it
			f.closed
			sendChanMsg(chan, "Quote added!")

					#BLUEBERRYFOX

def bbfquotes(msg): # blueberryfoxes private fuction
	nick = getNick(msg)
	if '#' not in msg.split(':')[1]:
		print(nick + " sent !blueberry outside of a channel")
		sendUserMsg(nick, "You are not in a channel")
	else:
		print ("Sending blueberryfoxes fav quotes to " + nick)
		chan = getChannel(msg)
		sendChanMsg (chan, "Blueberryfoxes favorite Quotes: One, two, three, four, i declare a thumb war, five, six, seven, eight i use this hand to masturbate")
		time.sleep(1)
		sendChanMsg (chan, "I was like ohho!")
		time.sleep(1)
		sendChanMsg (chan, "I love your hair")

					#GREET MESSAGES

def setGreetCmd(msg):
	nick = getNick(msg)
	if '#' in msg.split(':')[1]: #let's make sure people use this privately so that people won't see the welcoming message until they join a channel
		chan = getChannel(msg)
		print(nick + " sent !setjoinmsg in " + chan + ". Sending warning...")
		sendChanMsg(chan, "Don't do that in the channel " + nick)
		sendUserMsg(nick, "Send it as a notice or query(pvt)")
	else:
		newMsg = msg.split(":!setjoinmsg")[1] # Retrieves the entry message
		if newMsg.__len__() <= 1: # Checks if entry message is empty
			setGreet(nick, newMsg, False) # if empty we send False to setGreet so the bot knows the user wants to unset his greet
		else:
			setGreet(nick, newMsg, True) # in this case the user wants to change or create an entry message so we send True

def setGreet(nick, newMsg, toSet):
	data = []
	with open("greet.txt", 'r') as f:
		for line in f:
			data.append(line) # Saves greet messages in a temporary array. This way we can change whatever we want without touching the file
	f.closed # Closes the file to save resources
	changed = False
	for idx, content in enumerate(data): # Here we start scanning the array
		if nick + "|!|" in content.__str__(): # In this case th user already has a greet message
			if toSet: # This will happen if there is a new entry message and not an empty one
				data[idx] = nick + "|!|" + newMsg.lstrip(' ') + '\n' # Changes the entry message to the new one
				print "Resetting " + nick + "'s greet message to '" + newMsg + "'"
				sendUserMsg(nick, "Entry message re-set!")
				changed = True
				break # We've found the nickname we can get out of the loop
			else: # This will happen if there is an empty entry message on an existing nick
				data[idx] = '' # Completely erases the content
				print "Unsetting " + nick + "'s greet message"
				sendUserMsg(nick, "Entry message unset!")
				changed = True
				break # We've found the nickname we can get out of the loop
	if toSet and not changed: # this will happen if there is a message and we didn't find a nickname in the file which means it's the 1st time being used or it was erased previously
				data.append(nick + "|!|" + newMsg.lstrip(' ') + '\n') # Adds the nick and corresponding greet message
				print "Setting " + nick + "'s greet message to '" + newMsg + "'"
				sendUserMsg(nick, "Entry message set!")
	with open("greet.txt", 'w') as f: # Now that we've changed what we needed we need to write the contents of our temporary array (data) in the file again
		for i in data:
			f.write("%s" % i)
	f.closed # Closes the file to save resources
	
def sendGreet(msg):
	nick = getNick(msg)
	# ":b0nk!LoC@fake.dimension JOIN #test"
	chan = msg.split(" JOIN ")[1]
	with open("greet.txt", 'r') as f: # Looks for a greeting in the file
		greet = ''
		for line in f:
			if nick + "|!|" in line:
				greet = line.split("|!|")[1]
				print("Greeting " + nick + " in " + chan)
				break
	f.closed
	if greet: # If found then greet :D
		sendChanMsg(chan, greet)
	
					#PART MESSAGES
	
def setPartCmd(msg):
	nick = getNick(msg)
	if '#' in msg.split(':')[1]: #let's make sure people use this privately so that people won't see the part message until they leave a channel
		chan = getChannel(msg)
		print(nick + " sent !setquitmsg in " + chan + ". Sending warning...")
		sendChanMsg(chan, "Don't do that in the channel " + nick)
		sendUserMsg(nick, "Send it as a notice or query(pvt)")
	else:
		newMsg = msg.split(":!setquitmsg")[1] # Retrieves the part message
		if newMsg.__len__() <= 1: # Checks if part message is empty
			setPart(nick, newMsg, False) # if empty we send False to setPart so the bot knows the user wants to unset his part message
		else:
			setPart(nick, newMsg, True) # in this case the user wants to change or create an entry message so we send True

def setPart(nick, newMsg, toSet):
	data = []
	with open("part.txt", 'r') as f:
		for line in f:
			data.append(line) # Saves part messages in a temporary array. This way we can change whatever we want without touching the file
	f.closed # Closes the file to save resources
	changed = False
	for idx, content in enumerate(data): # Here we start scanning the array
		if nick + "|!|" in content.__str__(): # In this case the user already has a part message
			if toSet: # This will happen if there is a new part message and not an empty one
				data[idx] = nick + "|!|" + newMsg.lstrip(' ') + '\n' # Changes the part message to the new one
				print "Resetting " + nick + "'s part message to '" + newMsg + "'"
				sendUserMsg(nick, "Part message re-set!")
				changed = True
				break # We've found the nickname we can get out of the loop
			else: # This will happen if there is an empty entry message on an existing nick
				data[idx] = '' # Completely erases the content
				print "Unsetting " + nick + "'s part message"
				sendUserMsg(nick, "Part message unset!")
				changed = True
				break # We've found the nickname we can get out of the loop
	if toSet and not changed: # this will happen if there is a message and we didn't find a nickname in the file which means it's the 1st time being used or it was erased previously
				data.append(nick + "|!|" + newMsg.lstrip(' ') + '\n') # Adds the nick and corresponding part message
				print "Setting " + nick + "'s part message to '" + newMsg + "'"
				sendUserMsg(nick, "Part message set!")
	with open("part.txt", 'w') as f: # Now that we've changed what we needed we need to write the contents of our temporary array (data) in the file again
		for i in data:
			f.write("%s" % i)
	f.closed # Closes the file to save resources
	
def sendPart(msg, isQuit):
	nick = getNick(msg)
	# ":b0nk!~LoC@fake.dimension PART #test :FGSFDS"
	# ":steurun!~androirc@r3if800ykeveolu-mmuluxhgxm QUIT :Ping timeout: 260 seconds"
	with open("part.txt", 'r') as f: # Opens the file with the goodbye messages
		part = ''
		for line in f:
			if nick + "|!|" in line: # Found the message
				part = line.split("|!|")[1]
				print("Saying goodbye to " + nick + "...")
				break
	f.closed # Closes the file to save resources
	if part and isQuit: # Bot says goodbye when the user leaves the network
		sendChanMsg("#boxxy", part)
	elif part and not isQuit: # Bot says goodbye when the user leaves the channel
		chan = msg.split(" PART ")[1].split(' ')[0]
		sendChanMsg(chan, part)
		
	
					#TAG (play catch)
					
def startTag(msg):
	nick = getNick(msg) # Checks who sent the command
	if '#' not in msg.split(':')[1]: # Checks of command was sent in a channel
		print(nick + " sent !starttag outside of a channel") #debugging
		sendUserMsg(nick, "You are not in a channel") # Warned the nickname
	else:
		global isTagOn, tagged
		chan = getChannel(msg) # Get the channel where the game is taking place
		if not isTagOn: # Checks if a game is in progress
			tagged = nick # Whoever starts the game is it
			isTagOn = True # Set game start
			sendChanMsg(chan, "The game starts and " + nick + " is it!")
		else: # Warns if game is on progress
			sendChanMsg(chan, "A game is already in progress.")
		
def endTag(msg):
	nick = getNick(msg)
	if '#' not in msg.split(':')[1]:
		print(nick + " sent !endtag outside of a channel")
		sendUserMsg(nick, "You are not in a channel")
	else:
		global isTagOn, tagged
		chan = getChannel(msg)
		if isTagOn:
			isTagOn = False
			tagged = ''
			sendChanMsg(chan, "The fun is over people :( it's raining...")
		else:
			sendChanMsg(chan, "There is no game in progress!")
					
def tag(msg):
	nick = getNick(msg)
	if '#' not in msg.split(':')[1]:
		print(nick + " sent !tag outside of a channel")
		sendUserMsg(nick, "You are not in a channel")
	else:
		chan = getChannel(msg)
		global isTagOn, tagged
		if isTagOn:
			target = msg.split("!tag")[1].lstrip(' ')
			if target.__len__() <= 1: # Checks if the nick tagged nothing
				sendChanMsg(chan , "Tag who??? Usage: !tag <nick>")
			else:
				target = target.rstrip(' ') # Removes trailing spaces left by some clients auto-complete
				if target in list(taggers): # Target must exist in the list of players
					if nick == tagged: # Checks if the player is it
						if nick == target: # Checks if player is tagging himself
							print(nick + " tagged himself")
							sendChanMsg(chan, "Don't tag yourself " + nick)
						elif target == botnick: # Checks if the bot gets tagged
							print(nick + " tagged the bot!")
							sendChanMsg(chan, nick + " tagged me!")
							target = random.choice(list(taggers)) # Bot picks a random player to tag
							print("Tagging " + target + "...")
							tagged = target
							sendChanMsg(chan, target + " Tag! You're it!")
						else: # Player tags someone other than himself or the bot
							print(tagged + " tagged " + target)
							tagged = target
							sendChanMsg(chan, nick + " tagged you " + target + " you're it!")
					else:
						sendChanMsg(chan, nick + " you are not it!")
				else:
					sendChanMsg(chan, "Who are you tagging " + nick + "?")
		else:
			sendChanMsg(chan, nick + " we're not playing tag now...")
			
					#ROSE
					
def rose(msg):
	nick = getNick(msg)
	if '#' not in msg.split(':')[1]:
		print(nick + " sent !rose outside of a channel")
		sendUserMsg(nick, "You are not in a channel")
	else:
		chan = getChannel(msg)
		target = msg.split("!rose")[1].lstrip(' ')
		if target.__len__() <= 1: # Checks for a target to send a rose to
			sendChanMsg(chan , nick + " don't keep the roses to yourself. Usage: !rose <nick>")
		else:
			rose = "3---<-<-{4@"
			target = target.rstrip(' ')
			if nick == target: # Checks if nick is sending a rose to himself
				print(nick + " is being selfish with the roses")
				sendChanMsg(chan, "Don't be selfish " + nick + " give that rose someone else")
			elif target == botnick:
				print (nick + " sent a rose to the bot.")
				sendChanMsg(chan, nick + " gave me a rose!")
				sendChanMsg(chan, "[" + nick + "]" + " " + rose + " " + "[" + target + "]")
				sendChanMsg(chan, ":3 thanks 4<3")
			else: # Success (normal case)
				print (nick + " sent a rose to " + target)
				sendChanMsg(chan, nick + " gives a rose to " + target)
				sendChanMsg(chan, "[" + nick + "]" + " " + rose + " " + "[" + target + "]")

					#QUIT

def quitIRC(): #This kills the bot!
	print("Killing the bot...")
	ircsock.send("QUIT oh_noes!_why_daddy_whyyyy..._*ded*_X(_(Exited_normally!)\n")

			#HELP (THE WALL OF TEXT) keep this on the bottom

def helpcmd(msg): #Here is the help message to be sent as a private message to the user
	nick = getNick(ircmsg)
	print("Help requested by " + nick)
	sendUserMsg(nick, "You have requested help.")
	time.sleep(0.5) # 0.5 seconds to avoid flooding
	sendUserMsg(nick, "You can say \'Hello " + botnick + "\' in a channel and I will respond.")
	time.sleep(0.5)
	sendUserMsg(nick, "You can also invite me to a channel and I'll thank you for inviting me there.")
	time.sleep(0.5)
	sendUserMsg(nick, "General commands: !help !invite !rtd !quote !addquote !setjoinmsg !setquitmsg !starttag !endtag !tag !rose")
	time.sleep(0.5)
	sendUserMsg(nick, "Channel control commands: !op !deop !hop !dehop !voice !devoice !topic !kick !randkick")
	time.sleep(0.5)
	sendUserMsg(nick, "I've been written in python 2.7 and if you want to contribute or just have an idea, talk to b0nk on #test .")

# Connection

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TODO: IPv6 ???
ircsock = ssl.wrap_socket(ircsock) # SSL wrapper for the socket
ircsock.connect((server, ssl_port)) # Here we connect to the server using the port defined above
ircsock.send("USER " + botuser + " " + bothost + " " + botserver + " " + botname + "\n") # Bot authentication
ircsock.send("NICK " + botnick + "\n") # Here we actually assign the nick to the bot
time.sleep(3)
ircsock.send("NICKSERV IDENTIFY " + botpassword + "\n") # Identifies the bot's nickname with nickserv
time.sleep(3)
ircsock.send("NICKSERV SET ENFORCE ON\n")
joinChans(chans)

while 1: # This is our infinite loop where we'll wait for commands to show up, the 'break' function will exit the loop and end the program thus killing the bot
	ircmsg = ircsock.recv(2048) # Receive data from the server
	ircmsg = ircmsg.strip('\n\r') # Removing any unnecessary linebreaks
	print(ircmsg) # Here we print what's coming from the server
	
	if "PING :" in ircmsg: # If the server pings us then we've got to respond!
		reply = ircmsg.split("PING :")[1] # In some IRCds it is mandatory to reply to PING the same message we recieve
		ping(reply)
		alreadyPinged = True
		
	if " 353 " in ircmsg:
		# ":irc.catiechat.net 353 testbot = #test :KernelPone ~b0nk CommVenus @testbot " 
		chan = ircmsg.split(" = ")[1].split(" ")[0]
		ircmsg = ircmsg.split(':')[2] # Returns raw list of nicks
		ircmsg = ircmsg.translate(None, '~@+&%') # Removes user mode characters
		ircmsg = ircmsg.rstrip(' ') # Removes an annoying SPACE char left by the server at the end of the string
		ircmsg = ircmsg.strip('\n\r') # Removing any unnecessary linebreaks
		nicks = ircmsg.split(' ') # Puts nicks in an array
		print (nicks) # debugging
		if "boxxybabee.catiechat.net" in list(nicks):
			ircsock.send("NAMES " + chan + "\n")
		
		# Now that we have the nicks we can decide what to do with them depending on the command
		if "!randkick" in lastcommand:
			lastcommand = ''
			randKick(nicks, chan)
		
		if "!starttag" in lastcommand:
			lastcommand = ''
			if not isTagOn:
				taggers = nicks
				startTag(tmpstr)
				tmpstr = ''
			else:
				sendChanMsg(chan, "The game is already in progress!")
	
	if " INVITE " + botnick + " :" in ircmsg:
		# :testbot!~I@m.botxxy.you.see INVITE b0nk :#test
		nick = getNick(ircmsg)
		target = ircmsg.split(':')[2]
		print (nick + " invited the bot to " + target + ". Joining...")
		joinChan(target)
		sendChanMsg(target, "Thank you for inviting me here " + nick + "!")
	
	if ":hello " + botnick in ircmsg.lower(): # If we can find "Hello testbot" it will call the function hello(nick)
		hello(ircmsg)
		
	if ":!help" in ircmsg: # checks for !help
		helpcmd(ircmsg)
	
	if ":!die" in ircmsg: #checks for !die
		user = getUser(ircmsg)
		if user == "b0nk!~LoC@fake.dimension": # TODO: Now that it is more secure make array of authorized users? or file?
			quitIRC()
			break
		else:
			nick = getNick(ircmsg)
			print(nick + " tried to kill the bot. Sending warning...")
			sendUserMsg(nick, "I'm afraid I can't let you do that " + nick + "...")
		
	if ":!invite" in ircmsg:
		inviteCmd(ircmsg)
		
	if ":!voice" in ircmsg:
		voiceCmd(ircmsg)
		
	if ":!devoice" in ircmsg:
		devoiceCmd(ircmsg)
		
	if ":!op" in ircmsg:
		opCmd(ircmsg)
		
	if ":!deop" in ircmsg:
		deopCmd(ircmsg)
	
	if ":!hop" in ircmsg:
		hopCmd(ircmsg)
		
	if ":!dehop" in ircmsg:
		dehopCmd(ircmsg)
	
	if ":!kick" in ircmsg:
		kickCmd(ircmsg)
		
	if ":!rtd" in ircmsg:
		dice(ircmsg)
		
	if ":!randkick" in ircmsg:
		nick = getNick(ircmsg)
		if '#' not in ircmsg.split(':')[1]:
			sendUserMsg(nick, "You are not in a channel!")
		else:
			chan = getChannel(ircmsg)
			ircsock.send("NAMES " + chan + "\n")
			print ("Getting NAMES from " + chan)
			lastcommand = "!randkick"
		
	if ":!topic" in ircmsg:
		topicCmd(ircmsg)
	'''
	if ":!pass" in ircmsg:
		authCmd(ircmsg)
	'''
	if ":!quote" in ircmsg:
		quoteCmd(ircmsg)
		
	if ":!addquote" in ircmsg:
		addQuote(ircmsg)
		
	if ":!blueberry" in ircmsg: #this will broadcast all of blueberrys favorite quotes :3
		bbfquotes(ircmsg)
	
	if " JOIN " in ircmsg:
		sendGreet(ircmsg)
		
	if " PART " in ircmsg:
		sendPart(ircmsg, False)
		
	if " QUIT " in ircmsg:
		sendPart(ircmsg, True)
		
	if ":!setjoinmsg" in ircmsg:
		setGreetCmd(ircmsg)
		
	if ":!setquitmsg" in ircmsg:
		setPartCmd(ircmsg)
	
	if ":!tag" in ircmsg:
		tag(ircmsg)
		
	if ":!starttag" in ircmsg:
		nick = getNick(ircmsg)
		if '#' not in ircmsg.split(':')[1]:
			sendUserMsg(nick, "You are not in a channel!")
		else:
			chan = getChannel(ircmsg)
			ircsock.send("NAMES " + chan + "\n")
			print ("Getting NAMES from " + chan)
			lastcommand = "!starttag"
			tmpstr = ircmsg
	
	if ":!endtag" in ircmsg:
		endTag(ircmsg)
		
	if ":!rose" in ircmsg:
		rose(ircmsg)
	