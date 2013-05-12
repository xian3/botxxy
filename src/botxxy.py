﻿# https://en.wikipedia.org/wiki/List_of_Internet_Relay_Chat_commands
# http://wiki.shellium.org/w/Writing_an_IRC_bot_in_Python
# http://forum.codecall.net/topic/59608-developing-a-basic-irc-bot-with-python/
# http://docs.python.org/2/library/ssl.html
# http://docs.python.org/2/library/hashlib.html
# https://www.hackthissite.org/articles/read/1050
# http://stackoverflow.com/questions/4719438/editing-specific-line-in-text-file-in-python

__version__ = '0.8.3'
__author__ = 'b0nk'

# Import the necessary libraries.
import socket
import ssl
#import hashlib
import time
import random

# Other imports
# https://code.google.com/p/pylast/
import pylast # last.fm interface

# Some basic variables used to configure the bot

server = "boxxybabee.catiechat.net" # EU server
#server = "anewhopeee.catiechat.net" # US server
port = 6667 # default port
ssl_port = 6697 # ssl port
chans = ["#test", "#music", "#boxxy"] #default channels
botnick = "testbot" # bot nick
botuser = "I"
bothost = "m.botxxy.you.see"
botserver = "testserver"
botname = "testname"
botpassword = "bawksy"

# Global vars

quitmsg = 'Exited_normally!'
lastcommand = ''
nicks = []
taggers = []
ignUsrs = []
#alreadyPinged = False
tagged = ''
prevTagged = ''
isTagOn = False
tmpstr = '' # General purpose temporary string
rosestr = "3---<-<-{4@"
boobsstr = "(.Y.)"
prompt = '>> '
lfmlogo = "0,5last.fm"

# Last.fm vars
API_KEY = "fecc237da4852744556a13ef826e875b"
API_SECRET = "7494fde97e69f1233a5840cf86d02251"
lastfm = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET, username = '', password_hash = '')

#============BASIC FUNCTIONS TO MAKE THIS A BIT EASIER===============

def ping(reply): # This is our first function! It will respond to server Pings.
    ircsock.send("PONG :testbot Pong\n")
    '''
  else: # The NICKSERV operation is here so we can identify the bots nick before joining the default channels
    ircsock.send("PONG :" + reply + "\n") # In some IRCds it is mandatory to reply to PING the same message we recieve
    print(prompt + "PONG :" + reply)
    time.sleep(3)
    ircsock.send("NICKSERV IDENTIFY " + botpassword + "\n") # Identifies the bot's nickname with nickserv
    time.sleep(3)
    joinChans(chans) # Joins the default channels
    '''
  
def sendChanMsg(chan, msg): # This sends a message to the channel 'chan'
  ircsock.send("PRIVMSG " + chan + " :" + msg + "\n")
  
def sendNickMsg(nick, msg): # This sends a notice to the nickname 'nick'
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
  global ignUsrs
  if nick not in ignUsrs:
    chan = getChannel(msg)
    print(prompt + nick + " said hi in " + chan)
    sendChanMsg(chan, "Hello " + nick + "! Type !help for more information.")
	
def identify():
  ircsock.send("NICK " + botnick + "\n") # Here we actually assign the nick to the bot
  time.sleep(3)
  ircsock.send("NICKSERV IDENTIFY " + botpassword + "\n") # Identifies the bot's nickname with nickserv
  print(prompt + "Bot identified")

#========================END OF BASIC FUNCTIONS=====================

          #AUTHENTICATION
'''
def authCmd(msg): # Authenticates a nick with the bot TODO: finish this
  nick = getNick(msg)
  if '#' in msg.split(':')[1]:
    chan = getChannel(msg)
    sendChanMsg(chan, nick + " MADE A MISTAKE! LET'S ALL PRETENDE WE DIDN'T SEE THAT OK?")
    sendNickMsg(nick, "DO NOT DO THAT IN THE CHANNEL!!!")
  else:
    # ":b0nk!LoC@fake.dimension PRIVMSG :!pass password"
    password = msg.split("!pass")[1].translate(None, " ") # RAW password
    if (not password):
      sendNickMsg(nick, "Bad arguments. Usage: !pass <password>")
    else:
      print(prompt + "RAW: " + password)
      password = hashlib.sha256(password).hexdigest() # A HEX representation of the SHA-256 encrypted password
      print(prompt + "ENC: " + password)
      success = False
      f = open("auth.txt", 'r') # Opens auth.txt with 'r'ead-only permissions
      for line in f:
        print(prompt + line) # debugging
        if (line.split("|!|")[0] == nick) and (line.split("|!|")[1] == password):
          print(prompt + nick + " has authenticated successfully")
          success = True
          sendNickMsg(nick, "Correct password! You are now authenticated.")
      if not success:
        print(prompt + nick + " mistyped the password")
        sendNickMsg(nick, "Incorrect password!")
      f.close()
'''

# Ign list

def ignCmd(msg):
  nick = getNick(msg)
  global ignUsrs
  if nick not in ignUsrs:
    if '#' not in msg.split(':')[1]:
      target = msg.split(":!ign")[1].lstrip(' ')
      if target.__len__() > 1:
        ign(nick, target)

def ign(nick, target):
  with open("ign.txt", 'a') as f:
    f.write(target + '\n')
  f.closed
  global ignUsrs
  ignUsrs.append(target)
  sendNickMsg(nick, target + " ignored!")
  print(prompt + "Ign -> " + ignUsrs.__str__())
  
def fillIgn():
  global ignUsrs
  ignUsrs = [line.strip() for line in open('ign.txt', 'r')]
  print(prompt + "Ign -> " + ignUsrs.__str__())

          #INVITE

def inviteCmd(msg): # Parses the message to extract NICK and CHANNEL
  # ":b0nk!LoC@fake.dimension PRIVMSG #test :!invite "
  nick = getNick(msg)
  global ignUsrs
  if nick not in ignUsrs:
    if '#' not in msg.split(':')[1]:
      print(prompt + nick + " sent !invite outside of a channel")
      sendNickMsg(nick, "You are not in a channel")
    else:
      chan = getChannel(msg)
      target = msg.split("!invite")[1].lstrip(' ')
      if target.__len__() <= 1: # Checks if user inserted a nickname to invite
        sendChanMsg(chan,"Bad arguments. Usage: !invite <nick>")
      else: # Success
        print(prompt + "Inviting " + target + " to channel " + chan)
        sendChanMsg(chan, "Inviting " + target + " here...")
        invite(target,chan)
  
def invite(nick,chan): # Invites given nickname to present channel
  ircsock.send("INVITE " + nick + " " + chan + "\n")

          #VOICE

def voiceCmd(msg):
  nick = getNick(msg)
  global ignUsrs
  if nick not in ignUsrs:
    if '#' not in msg.split(':')[1]:
      print(prompt + nick + " sent !voice outside of a channel")
      sendNickMsg(nick, "You are not in a channel")
    else:
      chan = getChannel(msg)
      target = msg.split("!voice")[1].lstrip(' ')
      if target.__len__() <= 1: # Checks if user inserted a nickname to voice
        sendChanMsg(chan,"Bad arguments. Usage: !voice <nick>")
      else: # Success
        print(prompt + "Voicing " + target + " on channel " + chan)
        voice(target,chan)

def voice(nick,chan):
  ircsock.send("MODE " + chan + " +v " + nick + "\n")

          #DEVOICE

def devoiceCmd(msg):
  nick = getNick(msg)
  global ignUsrs
  if nick not in ignUsrs:
    if '#' not in msg.split(':')[1]:
      print(prompt + nick + " sent !devoice outside of a channel")
      sendNickMsg(nick, "You are not in a channel")
    else:
      chan = getChannel(msg)
      target = msg.split("!devoice")[1].lstrip(' ')
      if target.__len__() <= 1: # Checks if user inserted a nickname to devoice
        sendChanMsg(chan,"Bad arguments. Usage: !devoice <nick>")
      elif target != botnick: # Success
        print(prompt + "Devoicing " + target + " on channel " + chan)
        devoice(target,chan)
      else:
        sendChanMsg(chan, "Don't you dare make me demote myself.")

def devoice(nick,chan):
  ircsock.send("MODE " + chan + " -v " + nick + "\n")

          #OP

def opCmd(msg):
  nick = getNick(msg)
  global ignUsrs
  if nick not in ignUsrs:
    if '#' not in msg.split(':')[1]:
      print(prompt + nick + " sent !op outside of a channel")
      sendNickMsg(nick, "You are not in a channel")
    else:
      chan = getChannel(msg)
      target = msg.split("!op")[1].lstrip(' ')
      if target.__len__() <= 1: # Checks if user inserted a nickname to op
        sendChanMsg(chan,"Bad arguments. Usage: !op <nick>")
      else: # Success
        print(prompt + "Giving op to " + target + " on channel " + chan)
        op(target,chan)

def op(nick,chan):
  ircsock.send("MODE " + chan + " +o " + nick + "\n")

          #DEOP

def deopCmd(msg):
  nick = getNick(msg)
  global ignUsrs
  if nick not in ignUsrs:
    if '#' not in msg.split(':')[1]:
      print(prompt + nick + " sent !deop outside of a channel")
      sendNickMsg(nick, "You are not in a channel")
    else:
      chan = getChannel(msg)
      target = msg.split("!deop")[1].lstrip(' ')
      if target.__len__() <= 1: # Checks if user inserted a nickname to deop
        sendChanMsg(chan,"Bad arguments. Usage: !deop <nick>")
      elif target != botnick: # Success
        print(prompt + "Taking op from " + target + " on channel " + chan)
        deop(target,chan)
      else:
        sendChanMsg(chan, "Don't you dare make me demote myself.")

def deop(nick,chan):
  ircsock.send("MODE " + chan + " -o " + nick + "\n")

          #HOP

def hopCmd(msg):
  nick = getNick(msg)
  global ignUsrs
  if nick not in ignUsrs:
    if '#' not in msg.split(':')[1]:
      print(prompt + nick + " sent !hop outside of a channel")
      sendNickMsg(nick, "You are not in a channel")
    else:
      chan = getChannel(msg)
      target = msg.split("!hop")[1].lstrip(' ')
      if target.__len__() <= 1: # Checks if user inserted a nickname to hop
        sendChanMsg(chan,"Bad arguments. Usage: !hop <nick>")
      else: # Success
        print(prompt + "Giving hop to " + target + " on channel " + chan)
        hop(target,chan)

def hop(nick,chan):
  ircsock.send("MODE " + chan + " +h " + nick + "\n")

          #DEHOP

def dehopCmd(msg):
  nick = getNick(msg)
  global ignUsrs
  if nick not in ignUsrs:
    if '#' not in msg.split(':')[1]:
      print(prompt + nick + " sent !dehop outside of a channel")
      sendNickMsg(nick, "You are not in a channel")
    else:
      chan = getChannel(msg)
      target = msg.split("!dehop")[1].lstrip(' ')
      if target.__len__() <= 1: # Checks if user inserted a nickname to dehop
        sendChanMsg(chan,"Bad arguments. Usage: !dehop <nick>")
      elif target != botnick: # Success
        print(prompt + "Taking hop from " + target + " on channel " + chan)
        dehop(target,chan)
      else:
        sendChanMsg(chan, "Don't you dare make me demote myself.")

def dehop(nick,chan):
  ircsock.send("MODE " + chan + " -h " + nick + "\n")

          #TOPIC

def topicCmd(msg):
  nick = getNick(msg)
  global ignUsrs
  if nick not in ignUsrs:
    if '#' not in msg.split(':')[1]:
      print(prompt + nick + " sent !topic outside of a channel")
      sendNickMsg(nick, "You are not in a channel")
    else:
      chan = getChannel(msg)
      # ":b0nk!LoC@fake.dimension PRIVMSG #test :!topic 1 2 3 test"
      topic = msg.split("!topic")[1].lstrip(' ')
      if topic.__len__() <= 1:
        print(prompt + "New topic is empty")
        sendChanMsg(chan, "Bad arguments. Usage: !topic [<new topic>]")
      else:
        print(prompt + nick + " changed " + chan + " 's topic to '" + topic + "' ")
        changeTopic(chan, topic)

def changeTopic(chan, topic):
  ircsock.send("TOPIC " + chan + " :" + topic + "\n")

          #KICK

def kickCmd(msg):
  nick = getNick(msg)
  global ignUsrs
  if nick not in ignUsrs:
    if '#' not in msg.split(':')[1]:
      print(prompt + nick + " sent !kick outside of a channel")
      sendNickMsg(nick, "You are not in a channel")
    else:
      chan = getChannel(msg)
      target = msg.split("!kick")[1].lstrip(' ')
      if target.__len__() <= 1: # Checks if user inserted a nickname to kick
        sendChanMsg(chan,"Bad arguments. Usage: !kick <nick>")
      elif target == botnick:
        print(prompt + nick + " tried to kick the bot!")
        sendChanMsg(chan, "Don't make me kick myself out " + nick + "!")
      else:
        print(prompt + "Kicking " + target + " from " + chan)
        kick(target,chan,0)

def kick(nick,chan,isRand):
  if isRand:
    sendChanMsg(chan, "Randomly kicking " + nick + " from " + chan)
    ircsock.send("KICK " + chan + " " + nick + " lol_butthurt\n")
  else:
    sendChanMsg(chan, "Kicking " + nick + " from " + chan)
    ircsock.send("KICK " + chan + " " + nick + " lol_butthurt\n")

          #RANDOM KICK

def randKick(nicks,chan):
  size = len(nicks) - 1 # Correcting offset (this means if we have an array with 5 elements we should pick a random number between 0 and 4)
  rand = random.randint(0,size) # Picks a random number
  if botnick not in nicks[rand]: # Prevents bot from being kicked by !randkick
    print(prompt + "Randomly kicking " + nicks[rand].__str__() + " from channel " + chan)
    kick (nicks[rand],chan,1)
  else:
    print(prompt + "Bot will not be kicked. Picking another one...")
    randKick(nicks,chan)

          #DICE

def dice(msg):
  nick = getNick(msg)
  global ignUsrs
  if nick not in ignUsrs:
    chan = getChannel(msg)
    dice = random.randint(1,6).__str__() # converts the integer dice to a string to be concatenated in the final output
    print(prompt + nick + " rolled the dice and got a " + dice)
    sendChanMsg(chan, nick + " rolled a " + dice)

          #QUOTES

def quoteCmd(msg): #TODO: quote IDs
  nick = getNick(msg)
  global ignUsrs
  if nick not in ignUsrs:
    if '#' not in msg.split(':')[1]:
      print(prompt + nick + " sent !quote outside of a channel")
      sendNickMsg(nick, "You are not in a channel")
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
      with open("quotes.txt", 'r') as f: # Opens quotes.txt with 'r'ead-only permissions
        line = random.choice(list(f)) # Picks a random line from the text file
      f.closed # Closes the file to save resources
      if line:
        author = line.split ("|!|")[0]
        quote = line.split ("|!|")[1]
        print(prompt + author + "\n" + quote) #debugging
        sendChanMsg(chan, "[Quote] " + quote)
      else:
        print(prompt + "File quotes.txt is empty")
        sendChanMsg(chan, "There are no quotes on the DB. Could something be wrong???")

def addQuote(msg):
  nick = getNick(msg)
  global ignUsrs
  if nick not in ignUsrs:
    if '#' not in msg.split(':')[1]: # Checks if quote was sent outside of a channel
      print(prompt + nick + " sent !addquote outside of a channel")
      sendNickMsg(nick, "You are not in a channel")
    else:
      chan = getChannel(msg)
      # ":b0nk!LoC@fake.dimension PRIVMSG #test :!quote random"
      newQuote = msg.split("!addquote")[1].lstrip(' ')
      if newQuote.__len__() <= 1: # Checks for empty quote
        sendChanMsg(chan,"Bad arguments. Usage: !addquote [<quote>]")
      else:
        print(prompt + nick + " added '" + newQuote + "'\n")
        with open("quotes.txt", 'a') as f:
          f.write(nick + "|!|" + newQuote + '\n') # Adds the quote and the nickname of who inserted it
        f.closed
        sendChanMsg(chan, "Quote added!")

          #BLUEBERRYFOX

def bbfquotes(msg): # blueberryfoxes private fuction
  nick = getNick(msg)
  global ignUsrs
  if nick not in ignUsrs:
    if '#' not in msg.split(':')[1]:
      print(prompt + nick + " sent !blueberry outside of a channel")
      sendNickMsg(nick, "You are not in a channel")
    else:
      print(prompt + "Sending blueberryfoxes fav quotes to " + nick)
      chan = getChannel(msg)
      sendChanMsg (chan, "Blueberryfoxes favorite Quotes: One, two, three, four, i declare a thumb war, five, six, seven, eight i use this hand to masturbate")
      time.sleep(1)
      sendChanMsg (chan, "I was like ohho!")
      time.sleep(1)
      sendChanMsg (chan, "I love your hair")

          #GREET MESSAGES

def setGreetCmd(msg):
  nick = getNick(msg)
  global ignUsrs
  if nick not in ignUsrs:
    if '#' in msg.split(':')[1]: #let's make sure people use this privately so that people won't see the welcoming message until they join a channel
      chan = getChannel(msg)
      print(prompt + nick + " sent !setjoinmsg in " + chan + ". Sending warning...")
      sendChanMsg(chan, "Don't do that in the channel " + nick)
      sendNickMsg(nick, "Send it as a notice or query(pvt)")
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
        print "Resetting " + nick + "'s greet message to '" + newMsg + "' "
        sendNickMsg(nick, "Entry message re-set!")
        changed = True
        break # We've found the nickname we can get out of the loop
      else: # This will happen if there is an empty entry message on an existing nick
        data[idx] = '' # Completely erases the content
        print "Unsetting " + nick + "'s greet message"
        sendNickMsg(nick, "Entry message unset!")
        changed = True
        break # We've found the nickname we can get out of the loop
  if toSet and not changed: # this will happen if there is a message and we didn't find a nickname in the file which means it's the 1st time being used or it was erased previously
        data.append(nick + "|!|" + newMsg.lstrip(' ') + '\n') # Adds the nick and corresponding greet message
        print "Setting " + nick + "'s greet message to '" + newMsg + "' "
        sendNickMsg(nick, "Entry message set!")
  with open("greet.txt", 'w') as f: # Now that we've changed what we needed we need to write the contents of our temporary array (data) in the file again
    for i in data:
      f.write("%s" % i)
  f.closed # Closes the file to save resources
  
def sendGreet(msg):
  nick = getNick(msg)
  global ignUsrs
  if nick not in ignUsrs:
    # ":b0nk!LoC@fake.dimension JOIN #test"
    chan = msg.split(" JOIN ")[1]
    with open("greet.txt", 'r') as f: # Looks for a greeting in the file
      greet = ''
      for line in f:
        if nick + "|!|" in line:
          greet = line.split("|!|")[1]
          print(prompt + "Greeting " + nick + " in " + chan)
          break
    f.closed
    if greet: # If found then greet :D
      sendChanMsg(chan, greet)
  
          #PART MESSAGES
  
def setPartCmd(msg):
  nick = getNick(msg)
  global ignUsrs
  if nick not in ignUsrs:
    if '#' in msg.split(':')[1]: #let's make sure people use this privately so that people won't see the part message until they leave a channel
      chan = getChannel(msg)
      print(prompt + nick + " sent !setquitmsg in " + chan + ". Sending warning...")
      sendChanMsg(chan, "Don't do that in the channel " + nick)
      sendNickMsg(nick, "Send it as a notice or query(pvt)")
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
        print "Resetting " + nick + "'s part message to '" + newMsg + "' "
        sendNickMsg(nick, "Part message re-set!")
        changed = True
        break # We've found the nickname we can get out of the loop
      else: # This will happen if there is an empty entry message on an existing nick
        data[idx] = '' # Completely erases the content
        print "Unsetting " + nick + "'s part message"
        sendNickMsg(nick, "Part message unset!")
        changed = True
        break # We've found the nickname we can get out of the loop
  if toSet and not changed: # this will happen if there is a message and we didn't find a nickname in the file which means it's the 1st time being used or it was erased previously
        data.append(nick + "|!|" + newMsg.lstrip(' ') + '\n') # Adds the nick and corresponding part message
        print "Setting " + nick + "'s part message to '" + newMsg + "' "
        sendNickMsg(nick, "Part message set!")
  with open("part.txt", 'w') as f: # Now that we've changed what we needed we need to write the contents of our temporary array (data) in the file again
    for i in data:
      f.write("%s" % i)
  f.closed # Closes the file to save resources
  
def sendPart(msg, isQuit):
  nick = getNick(msg)
  global ignUsrs
  if nick not in ignUsrs:
    # ":b0nk!~LoC@fake.dimension PART #test :FGSFDS"
    # ":steurun!~androirc@r3if800ykeveolu-mmuluxhgxm QUIT :Ping timeout: 260 seconds"
    with open("part.txt", 'r') as f: # Opens the file with the goodbye messages
      part = ''
      for line in f:
        if nick + "|!|" in line: # Found the message
          part = line.split("|!|")[1]
          print(prompt + "Saying goodbye to " + nick + "...")
          break
    f.closed # Closes the file to save resources
    if part and isQuit: # Bot says goodbye when the user leaves the network
      sendChanMsg("#boxxy", part)
    elif part and not isQuit: # Bot says goodbye when the user leaves the channel
      chan = msg.split(" PART ")[1].split(' ')[0]
      sendChanMsg(chan, part)
    
  
          #TAG (play catch)
          
def startTag(msg):
  nick = getNick(msg)
  global ignUsrs
  if nick not in ignUsrs:
    if '#' not in msg.split(':')[1]: # Checks of command was sent in a channel
      print(prompt + nick + " sent !starttag outside of a channel") #debugging
      sendNickMsg(nick, "You are not in a channel") # Warned the nickname
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
  global ignUsrs
  if nick not in ignUsrs:
    if '#' not in msg.split(':')[1]:
      print(prompt + nick + " sent !endtag outside of a channel")
      sendNickMsg(nick, "You are not in a channel")
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
  global ignUsrs
  if nick not in ignUsrs:
    if '#' not in msg.split(':')[1]:
      print(prompt + nick + " sent !tag outside of a channel")
      sendNickMsg(nick, "You are not in a channel")
    else:
      chan = getChannel(msg)
      global isTagOn, tagged, prevTagged
      if isTagOn:
        target = msg.split("!tag")[1].lstrip(' ')
        if target.__len__() <= 1: # Checks if the nick tagged nothing
          sendChanMsg(chan , "Tag who??? Usage: !tag <nick>")
        else:
          target = target.rstrip(' ') # Removes trailing spaces left by some clients auto-complete
          if target in list(taggers): # Target must exist in the list of players
            if nick == tagged: # Checks if the player is it
              if nick == target: # Checks if player is tagging himself
                print(prompt + nick + " tagged himself")
                sendChanMsg(chan, "Don't tag yourself " + nick)
              elif target == botnick: # Checks if the bot gets tagged
                print(prompt + nick + " tagged the bot!")
                sendChanMsg(chan, nick + " tagged me!")
                target = random.choice(list(taggers)) # Bot picks a random player to tag
                print(prompt + "Tagging " + target + "...")
                tagged = target
                sendChanMsg(chan, target + " Tag! You're it!")
                prevTagged = nick
              else: # Player tags someone other than himself or the bot
                print(prompt + tagged + " tagged " + target)
                tagged = target
                prevTagged = nick
                sendChanMsg(chan, nick + " tagged you " + target + " you're it!")
            else:
              sendChanMsg(chan, nick + " you are not it!")
          else:
            sendChanMsg(chan, "Who are you tagging " + nick + "? Maybe " + target + " was not here when the game started.")
      else:
        sendChanMsg(chan, nick + " we're not playing tag now...")

def setTagged(msg):
  nick = getNick(msg)
  global ignUsrs
  if nick not in ignUsrs:
    if '#' not in msg.split(':')[1]:
      print(prompt + nick + " sent !settagged outside of a channel")
      sendNickMsg(nick, "You are not in a channel")
    else:
      chan = getChannel(msg)
      global isTagOn, prevTagged, tagged
      if isTagOn:
        target = msg.split("!settagged")[1].lstrip(' ')
        if target.__len__() <= 1: # Checks if the nick wrote anything to set
          sendChanMsg(chan , "Set who??? Usage: !settagged <nick>")
        else:
          target = target.rstrip(' ') # Removes trailing spaces left by some clients auto-complete
          if target in list(taggers): # Target must exist in the list of players
            if nick == prevTagged:
              if nick == target:
                print(prompt + nick + " set himself as tagged")
                sendChanMsg(chan, "Don't tag yourself " + nick)
              elif target == botnick:
                print(prompt + nick + " set the bot as tagged!")
                sendChanMsg(chan, nick + " tagged me instead!")
                target = random.choice(list(taggers)) # Bot picks a random player to tag
                print(prompt + "Tagging " + target + "...")
                tagged = target
                sendChanMsg(chan, target + " Tag! You're it!")
              else:
                print(prompt + nick + " decided to tag " + target + " instead")
                sendChanMsg(chan, nick + " decided to tag " + target + " instead")
                tagged = target
                sendChanMsg(chan, nick + " tagged you " + target + " you're it!")
            else:
              sendChanMsg(chan, nick + " you were not previously it.")
          else:
            sendChanMsg(chan, "Who are you tagging " + nick + "? Maybe " + target + " was not here when the game started.")
      else:
        sendChanMsg(chan, nick + " we're not playing tag now...")
      
          #ROSE
          
def rose(msg):
  nick = getNick(msg)
  global ignUsrs
  if nick not in ignUsrs:
    if '#' not in msg.split(':')[1]:
      print(prompt + nick + " sent !rose outside of a channel")
      sendNickMsg(nick, "You are not in a channel")
    else:
      chan = getChannel(msg)
      target = msg.split("!rose")[1].lstrip(' ')
      if target.__len__() <= 1: # Checks for a target to send a rose to
        sendChanMsg(chan , nick + " don't keep the roses to yourself. Usage: !rose <nick>")
      else:
        target = target.rstrip(' ')
        if nick == target: # Checks if nick is sending a rose to himself
          print(prompt + nick + " is being selfish with the roses")
          sendChanMsg(chan, "Don't be selfish " + nick + " give that rose someone else")
        elif target == botnick:
          print(prompt + nick + " sent a rose to the bot.")
          sendChanMsg(chan, nick + " gave me a rose!")
          sendChanMsg(chan, "[" + nick + "]" + " " + rosestr + " " + "[" + target + "]")
          sendChanMsg(chan, ":3 thanks 4<3")
        else: # Success (normal case)
          print(prompt + nick + " sent a rose to " + target)
          sendChanMsg(chan, nick + " gives a rose to " + target)
          sendChanMsg(chan, "[" + nick + "]" + " " + rosestr + " " + "[" + target + "]")
        
          #BOOBS
          
def boobs(msg):
  nick = getNick(msg)
  global ignUsrs
  if nick not in ignUsrs:
    if '#' not in msg.split(':')[1]:
      print(prompt + nick + " sent !boobs outside of a channel")
      sendNickMsg(nick, "You are not in a channel")
    else:
      chan = getChannel(msg)
      target = msg.split("!boobs")[1].lstrip(' ')
      if target.__len__() <= 1: # Checks for a target to show boobs to
        sendChanMsg(chan , nick + " don't hide those boobs. Usage: !boobs <nick>")
      else:
        target = target.rstrip(' ')
        if nick == target: # Checks if nick is sending !boobs to itself
          print(prompt + nick + " is being shy with those boobs")
          sendChanMsg(chan, "Stop looking at the mirror " + nick + " show us them boobs")
        elif target == botnick:
          print(prompt + nick + " sent !boobs to the bot.")
          sendChanMsg(chan, nick + " those are cute")
          sendChanMsg(chan, "But mine are bigger --> ( . Y . )")
        else: # Success (normal case)
          print(prompt + nick + " sent !boobs to " + target)
          sendChanMsg(chan, nick + " shows " + target + " some boobs")
          sendChanMsg(chan, "[" + nick + "]" + " " + boobsstr + " " + "[" + target + "]")
        
          #SAY
          
def sayCmd(msg):
  nick = getNick(msg)
  global ignUsrs
  if nick not in ignUsrs:
    if '#' in msg.split(':')[1]:
      chan = getChannel(msg)
      print(prompt + nick + " sent !say in " + chan + ". Sending warning...")
      sendChanMsg(chan, "Don't do that in the channel " + nick)
      sendNickMsg(nick, "Send it as a notice or query(pvt)")
    else: # ":b0nk!~LoC@fake.dimension PRIVMSG testbot :!say #boxxy lol message"
      targetChan = msg.split(':')[2].split(' ')[1]
      message = msg.split(targetChan)[1].lstrip(' ')
      sendChanMsg(targetChan, message)
    
          #8BALL
          
def eightBallCmd(msg):
  nick = getNick(msg)
  global ignUsrs
  if nick not in ignUsrs:
    if '#' not in msg.split(':')[1]:
      print(prompt + nick + " sent !8ball outside of a channel")
      sendNickMsg(nick, "You are not in a channel")
    else:
      chan = getChannel(msg)
      question = msg.split(':!8ball')[1].lstrip(' ')
      if question is None or '?' not in question:
        print(prompt + nick + " didn't ask a question")
        sendChanMsg(chan, "How about you ask me a question properly " + nick + "? Usage !8ball [<question>]?")
      else:
        with open("8ball.txt", 'r') as f: # Opens 8ball.txt with 'r'ead-only permissions
          line = random.choice(list(f)) # Picks a random line from the text file
        f.closed # Closes the file to save resources
        if line:
          print(prompt + line) #debugging
          sendChanMsg(chan, nick + " asked [" + question + "] the 8ball says: " + line)
        else:
          print(prompt + "File 8ball.txt is empty")
          sendChanMsg(chan, "There are no responses on the DB. Could something be wrong???")
        
          #LAST.FM
          
def getLfmUser(nick): # this looks for the last.fm username by nick
  lfmusers = [line.strip() for line in open('lfmusers.txt', 'r')]
  user = ''
  for i in lfmusers:
    if nick in i:
      user = i.__str__().split('|!|')[1]
  return user #returns empty if not found


def setLfmUserCmd(msg):
  nick = getNick(msg)
  global ignUsrs
  if nick not in ignUsrs:
    lfm_username = msg.split(":.setuser")[1].lstrip(' ')
    if lfm_username.__len__() < 1:
      setLfmUser(nick, lfm_username, False) #sends false flag to unset username
    else:
      setLfmUser(nick, lfm_username, True) #sends true flag to set/re-set username


def setLfmUser(nick, lfm_username, toSet):
  data = []
  with open("lfmusers.txt", 'r') as f:
    for line in f:
      data.append(line)#stores each line in array
  f.closed
  changed = False #hit detection
  for idx, content in enumerate(data):#scans array
    if nick + "|!|" in content.__str__():#finds the nickname
      if toSet:
        data[idx] = nick + "|!|" + lfm_username + '\n'
        print (prompt + nick + " re-set it's LAST.FM username to " + lfm_username)
        sendNickMsg(nick, "last.fm username re-set!")
        changed = True
        break# get out of loop
      else:
        data[idx] = ''
        print (prompt + nick + " unset it's LAST.FM username")
        sendNickMsg(nick, "last.fm username unset!")
        changed = True
        break
  if toSet and not changed:
        data.append(nick + "|!|" + lfm_username + '\n')
        print (prompt + nick + " set it's LAST.FM username to " + lfm_username)
        sendNickMsg(nick, "last.fm username set!")
  with open("lfmusers.txt", 'w') as f:
    for i in data:
      f.write("%s" % i)#stores data back to file
  f.closed


def nowPlaying(msg): # use of the last.fm interface (pylast) in here
  nick = getNick(msg)
  global ignUsrs
  if nick not in ignUsrs:
    if '#' not in msg.split(':')[1]:
      print(prompt + nick + " sent .np outside of a channel")
      sendNickMsg(nick, "You are not in a channel")
    else:
      chan = getChannel(msg)
      target = msg.split(":.np")[1].lstrip(" ")
      if target.__len__() < 1: # let's check the file
        target = getLfmUser(nick)
      if target.__len__() < 1: # he is not in the db
        sendChanMsg(chan , "I don't know who you are... please use .np <last.fm username>, alternatively use .setuser <last.fm username> to join your nick with your " + lfmlogo + " account")
        print(prompt + nick + " sent .np but is not registered")
      else:
        lfm_user = lastfm.get_user(target) # returns pylast.User object
        try:
          lfm_user.get_id() # some random fuction to raise exception if the user does not exist
        except(pylast.WSError): # catched the exception, user truly does not exist
          sendChanMsg(chan, lfmlogo + " " + target + " does not exist")
          print (prompt + "User " + target + " does not exist")
          return None # GTFO
        if lfm_user.get_playcount().__int__() < 1: # checks if user has scrobbled anything EVER
          sendChanMsg(chan, lfmlogo + " " + target + " has an empty library")
          print(prompt + target + " has an empty library")# no need to get a nowplaying when the library is empty
        else:
          np = lfm_user.get_now_playing() #np is now a pylast.Track object
          if np is None: # user does not have a now listening track
            sendChanMsg(chan, lfmlogo + " " + target + " does not seem to be playing any music right now...")
            print(prompt + target + " does not seem to be playing any music right now...")
          else: # all went well
            artist_name = np.artist.get_name().encode('utf8')# string containing artist name
            track = np.title.encode('utf8') #string containing track title
            
            try: # here we check if the user has ever played the np track
              playCount = int(np.get_add_info(target).userplaycount)
            except (ValueError, TypeError): #this error means track was never played so we just say it's 1
              playCount = 1
            
            np = np.get_add_info(target)
            
            if np.userloved == "1":#checks if np is a loved track to show when brodcasted to channel
              loved = " 13<3"
            else:
              loved = ""
            
            raw_tags = np.get_top_tags(5)
            if raw_tags.__len__() < 1: #some tracks have no tags therefor we request the artist tags
              raw_tags = np.artist.get_top_tags(5)
            tags = ''
            while raw_tags:
              tags += raw_tags.pop().item.name.encode('utf8') + ", "#builds tags string
            tags = tags.rstrip(", ")#removes last comma
            
            sendChanMsg(chan, lfmlogo + " " + target + " is now playing: " + artist_name + " - " + track + " (" + playCount.__str__() + " plays, " + tags + loved + ")")# broadcast to channel
            print(prompt + "is now playing: " + artist_name + " - " + track + " (" + playCount.__str__() + " plays, " + tags + loved + ")")
#(COLOR)last.fm(COLOR) | b0nk is now playing:(UNDERLINE)Joan Jett and the Blackhearts - You Want In, I Want Out(UNDERLINE)(1 plays, rock, rock n roll, Joan Jett, 80s, pop)
    
          #QUIT

def quitIRC(): #This kills the bot!
  print(prompt + "Killing the bot...")
  ircsock.send("QUIT " + quitmsg + "\n")

      #HELP (THE WALL OF TEXT) keep this on the bottom

def helpcmd(msg): #Here is the help message to be sent as a private message to the user
  nick = getNick(ircmsg)
  global ignUsrs
  if nick not in ignUsrs:
    print(prompt + "Help requested by " + nick)
    sendNickMsg(nick, "You have requested help.")
    time.sleep(0.5) # 0.5 seconds to avoid flooding
    sendNickMsg(nick, "You can say \'Hello " + botnick + "\' in a channel and I will respond.")
    time.sleep(0.5)
    sendNickMsg(nick, "You can also invite me to a channel and I'll thank you for inviting me there.")
    time.sleep(0.5)
    sendNickMsg(nick, "General commands: !help !invite !rtd !quote !addquote !setjoinmsg !setquitmsg !starttag !endtag !tag !rose !boobs !8ball")
    time.sleep(0.5)
    sendNickMsg(nick, lfmlogo + " commands: .setuser .np") #.compare
    time.sleep(0.5)
    sendNickMsg(nick, "Channel control commands: !op !deop !hop !dehop !voice !devoice !topic !kick !randkick")
    time.sleep(0.5)
    sendNickMsg(nick, "I've been written in python 2.7 and if you want to contribute or just have an idea, talk to b0nk on #test .")

# Initializations TODO:

fillIgn()

# Connection
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TODO: IPv6 ???
ircsock = ssl.wrap_socket(ircsock) # SSL wrapper for the socket
ircsock.connect((server, ssl_port)) # Here we connect to the server using the port defined above
ircsock.send("USER " + botuser + " " + bothost + " " + botserver + " " + botname + "\n") # Bot authentication
ircsock.send("NICK " + botnick + "\n") # Here we actually assign the nick to the bot
time.sleep(3)
ircsock.send("NICKSERV IDENTIFY " + botpassword + "\n") # Identifies the bot's nickname with nickserv
time.sleep(3)
joinChans(chans)

while 1: # This is our infinite loop where we'll wait for commands to show up, the 'break' function will exit the loop and end the program thus killing the bot
  ircmsg = ircsock.recv(1024) # Receive data from the server
  ircmsg = ircmsg.strip('\n\r') # Removing any unnecessary linebreaks
  print(ircmsg) # Here we print what's coming from the server
  
  if "PING :" in ircmsg: # If the server pings us then we've got to respond!
    reply = ircmsg.split("PING :")[1] # In some IRCds it is mandatory to reply to PING the same message we recieve
    ping(reply)
    alreadyPinged = True
    
  if " 353 " in ircmsg:
    try:
      # ":irc.catiechat.net 353 testbot = #test :KernelPone ~b0nk CommVenus @testbot " 
      chan = ircmsg.split(" = ")[1].split(" ")[0]
      ircmsg = ircmsg.split(':')[2] # Returns raw list of nicks
      ircmsg = ircmsg.translate(None, '~@+&%') # Removes user mode characters
      ircmsg = ircmsg.rstrip(' ') # Removes an annoying SPACE char left by the server at the end of the string
      ircmsg = ircmsg.strip('\n\r') # Removing any unnecessary linebreaks
      nicks = ircmsg.split(' ') # Puts nicks in an array
      print(prompt + nicks.__str__()) # debugging
      if botnick not in list(nicks):
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
    except IndexError:
      print(prompt + "Something went wrong...")
  
  if " INVITE " + botnick + " :" in ircmsg:
    tmpstr = ircmsg
    # :testbot!~I@m.botxxy.you.see INVITE b0nk :#test
    nick = getNick(tmpstr)
    if nick not in ignUsrs:
      target = tmpstr.split(':')[2]
      print(prompt + nick + " invited the bot to " + target + ". Joining...")
      joinChan(target)
      sendChanMsg(target, "Thank you for inviting me here " + nick + "!")
      tmpstr = ''
  
  if ":hello " + botnick in ircmsg.lower(): # If we can find "Hello testbot" it will call the function hello(nick)
    hello(ircmsg)
    
  if ":!help" in ircmsg: # checks for !help
    helpcmd(ircmsg)
	
  if ":!ident" in ircmsg:
    user = getUser(ircmsg)
    if user == "b0nk!~LoC@fake.dimension":
      identify()
	  
  if ":!die" in ircmsg: #checks for !die
    user = getUser(ircmsg)
    if user == "b0nk!~LoC@fake.dimension": # TODO: use auth
      quitIRC()
      break
    else:
      nick = getNick(ircmsg)
      print(prompt + nick + " tried to kill the bot. Sending warning...")
      sendNickMsg(nick, "I'm afraid I can't let you do that " + nick + "...")
    
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
    if nick not in ignUsrs:
      if '#' not in ircmsg.split(':')[1]:
        sendNickMsg(nick, "You are not in a channel!")
      else:
        chan = getChannel(ircmsg)
        ircsock.send("NAMES " + chan + "\n")
        print(prompt + "Getting NAMES from " + chan)
        lastcommand = "!randkick"
    
  if ":!topic" in ircmsg:
    topicCmd(ircmsg)
  '''
  if ":!pass" in ircmsg: #TODO: make this
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
    if nick not in ignUsrs:
      if '#' not in ircmsg.split(':')[1]:
        sendNickMsg(nick, "You are not in a channel!")
      else:
        chan = getChannel(ircmsg)
        ircsock.send("NAMES " + chan + "\n")
        print(prompt + "Getting NAMES from " + chan)
        lastcommand = "!starttag"
        tmpstr = ircmsg
  
  if ":!endtag" in ircmsg:
    endTag(ircmsg)
    
  if ":!settagged" in ircmsg:
    setTagged(ircmsg)
    
  if ":!rose" in ircmsg:
    rose(ircmsg)
    
  if ":!boobs" in ircmsg:
    boobs(ircmsg)
    
  if ":!say" in ircmsg:
    sayCmd(ircmsg)
    
  if ":!8ball" in ircmsg:
    eightBallCmd(ircmsg)
    
  if ":!ign" in ircmsg:
    ignCmd(ircmsg)
  
  if ":.np" in ircmsg:
    nowPlaying(ircmsg)
  
  if ":.setuser" in ircmsg:
    setLfmUserCmd(ircmsg)
  
  if ircmsg is '' or None:
    print(prompt + "Bot timed out / killed")
    quitIRC()
    break
