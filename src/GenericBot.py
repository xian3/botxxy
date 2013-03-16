
from BaseBot import *

version = "0.0.1.0"
debug = True

class GenericBotIRC(BotIRC):
	def __init__(self, *args, **kwargs):
		super(GenericBotIRC, self).__init__(*args, **kwargs)
		print 'init GenericBotIRC'
		self.server = "boxxybabee.catiechat.net"
		self.port = 6667
		self.useSSL = True
		self.info_user = "I"
		self.info_host = "m.botxxy.you.see"
		self.info_server = "testserver"
		self.info_name = "testname"
		self.info_nick = "ircFemBot_%s" % version.replace('.', '_')
	def addCommands(self):
		self.registerCommand('PING ', self.ping)
		self.registerCommand('!invite', self.inviteCmd)
		self.registerCommand('!kick', self.kickCmd)
		self.registerCommand('!voice', self.voiceCmd)
		self.registerCommand('!op', self.opCmd)
		self.registerCommand('!hop', self.hopCmd)
		self.registerCommand('!die', self.killCmd)
	def getNick(self, msg): # Returns the nickname of whoever requested a command from a RAW irc privmsg. Example in commentary below.
		# ":b0nk!LoC@fake.dimension PRIVMSG #test :lolmessage"
		return msg[1:msg.index('!')]
	def getUser(self, msg): # Returns the user and host of whoever requested a command from a RAW irc privmsg. Example in commentary below.
		# ":b0nk!LoC@fake.dimension PRIVMSG #test :lolmessage"
		return msg[1:msg.index(' ')]
	def getChannel(self, msg): # Returns the channel from whereever a command was requested from a RAW irc PRIVMSG. Example in commentary below.
		# ":b0nk!LoC@fake.dimension PRIVMSG #test :lolmessage"
		try:
			return msg[msg.index('#', msg.index(' PRIVMSG ')):msg.index(' ', msg.index('#'))]
		except ValueError:
			return None
	def getUserCommandArgs(self, msg): #Parses the message to extract NICK and CHANNEL
		# ":b0nk!LoC@fake.dimension PRIVMSG #test :!invite tick tock tack"
		args = msg[msg.index(':',msg.index(' PRIVMSG '))+1:].split(' ')
		args = [arg for arg in args if arg is not '']
		return args
	def inviteCmd(self, msg): # Parses the message to extract NICK and CHANNEL
		# ":b0nk!LoC@fake.dimension PRIVMSG #test :!invite "
		nick = self.getNick(msg)
		channel = self.getChannel(msg)
		if channel is not None:
			args = self.getUserCommandArgs(msg)
			if len(args) is 2: # Checks if user inserted a nickname to invite
				target = args[1]
				self.sendChanMsg(channel, "Inviting %s here." % target )
				self.invite(target,channel)
			else: # Success
				self.sendChanMsg(channel,"Bad arguments. Usage: !invite <nick>")
	def kickCmd(self, msg): # Parses the message to extract NICK and CHANNEL
		# ":b0nk!LoC@fake.dimension PRIVMSG #test :!kick "
		channel = self.getChannel(msg)
		if channel is not None:
			args = self.getUserCommandArgs(msg)
			if len(args) <2: 
				self.sendChanMsg(channel,"Bad arguments. Usage: !kick <nick> [reason]")# Success
				return
			if len(args) >=2: target = args[1]
			reason = ' '.join(args[2:])
			if reason is not '': self.kick(target,channel, reason)
			else: self.kick(target,channel, )
	def voiceCmd(self, msg):
		channel = self.getChannel(msg)
		if channel is not None:
			args = self.getUserCommandArgs(msg)
			if len(args) <2: 
				self.sendChanMsg(channel,"Bad arguments. Usage: !voice <nick> [+/-]")# Success
				return
			if len(args) >=2: target = args[1]
			if len(args) >=3: mode = args[2]
			else: mode = '+'
			self.voice(target,channel, mode)
	def opCmd(self, msg):
		channel = self.getChannel(msg)
		if channel is not None:
			args = self.getUserCommandArgs(msg)
			if len(args) <2: 
				self.sendChanMsg(channel,"Bad arguments. Usage: !op <nick> [+/-]")# Success
				return
			if len(args) >=2: target = args[1]
			if len(args) >=3: mode = args[2]
			else: mode = '+'
			self.op(target,channel, mode)
	def hopCmd(self, msg):
		channel = self.getChannel(msg)
		if channel is not None:
			args = self.getUserCommandArgs(msg)
			print len(args)
			if len(args) <2: 
				self.sendChanMsg(channel,"Bad arguments. Usage: !hop <nick> [+/-]")# Success
				return
			if len(args) >=2: target = args[1]
			if len(args) >=3: mode = args[2]
			else: mode = '+'
			self.hop(target,channel, mode)
	def killCmd(self, msg): #This kills the bot!
		self.running = False
		self.send("QUIT oh_noes!_why_daddy_whyyyy..._*ded*_X(_(Exited_normally!)\n")
"""
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
		self.send("QUIT oh_noes!_why_daddy_whyyyy..._*ded*_X(_(Exited_normally!)\n")

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
"""
if __name__ == "__main__":
	b = GenericBotIRC()
	b.addCommands()
	if not debug:
		b.connect()
		b.server_login()
		b.joinChannel('#test')
	b.run()