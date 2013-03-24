import anydbm
import pdb
from binascii import unhexlify
from hashlib import sha1
from BaseBot import *
try:
  import pyreadline as readline
except ImportError:
  import readline

version = "0.0.1.0"

class GenericBot(BotIRC):
    def __init__(self, *args, **kwargs):
        super(GenericBot, self).__init__(*args, **kwargs)
        print 'init GenericBotIRC'
        self.userCredsFile = kwargs.get('userCredsFile', 'userCreds') 
        self.authUsers = []
        self.testInput = ["PING :data data data",
            ":b0nk!LoC@fake.dimension PRIVMSG #test :%sinvite <nick>" % self.userCmdPrefix,
            ":b0nk!LoC@fake.dimension PRIVMSG #test :%skick <nick>" % self.userCmdPrefix,
            ":b0nk!LoC@fake.dimension PRIVMSG #test :%skick <nick> I have a reason" % self.userCmdPrefix,
            ":b0nk!LoC@fake.dimension PRIVMSG #test :%svoice <nick>" % self.userCmdPrefix,
            ":b0nk!LoC@fake.dimension PRIVMSG #test :%svoice <nick> +" % self.userCmdPrefix,
            ":b0nk!LoC@fake.dimension PRIVMSG #test :%svoice <nick> -" % self.userCmdPrefix,
            ":b0nk!LoC@fake.dimension PRIVMSG #test :%sop <nick>" % self.userCmdPrefix,
            ":b0nk!LoC@fake.dimension PRIVMSG #test :%sop <nick> +" % self.userCmdPrefix,
            ":b0nk!LoC@fake.dimension PRIVMSG #test :%sop <nick> -" % self.userCmdPrefix,
            ":b0nk!LoC@fake.dimension PRIVMSG #test :%shop <nick>" % self.userCmdPrefix,
            ":b0nk!LoC@fake.dimension PRIVMSG #test :%shop <nick> +" % self.userCmdPrefix,
            ":b0nk!LoC@fake.dimension PRIVMSG #test :%shop <nick> -" % self.userCmdPrefix,
            ":xterm!~xterm@fake.email PRIVMSG xterm :%sauth xterm" % self.userCmdPrefix,
            ":b0nk!LoC@fake.dimension PRIVMSG #test :%sdie" % self.userCmdPrefix
            ]
    # Permission check wrapper
    def requiresPermissions(func):
        def decorator(self, msg, *args):
            if self.getUser(msg) in self.authUsers:
                return func(self, msg, *args)
            else:
                args = self.getUserCommandArgs(msg)
                if self.getChannel(msg) is not None:
                    self.sendChanMsg(self.getChannel(msg), '%s: You are not authorized to execute %s' % (self.getNick(msg), args[0]))
                else:
                    self.sendUserMsg(self.getNick(msg), '%s: You are not authorized to execute %s' % (self.getNick(msg), args[0]))
                return None
        return decorator
    
    def mustBeInChannel(func):
        def decorator(self, msg, *args):
            if self.getChannel(msg) is None:
                self.sendUserMsg(self.getNick(msg), 'You must be in a channel to use this command')
            else:
                return func(self, msg, *args)
        return decorator
    def addCommands(self):
        self.registerCommand(Command({
            '__call__':self.ping,
            'name':'Ping',
            'regex':'PING :'})
            )
        self.registerCommand(Command({
            '__call__':self.helpCmd,
            'name':'%shelp' %self.userCmdPrefix,
            'regex':'^:\S* PRIVMSG (#?)\w+ :%shelp' %self.userCmdPrefix,
            'help':'%shelp <%scommand> - Displays the help menu for the given command.\n' % (self.userCmdPrefix, self.userCmdPrefix)}))
        self.registerCommand(Command({
            '__call__':self.authCmd,
            'name':'%sauth' %self.userCmdPrefix,
            'regex':'^:\S* PRIVMSG (#?)\w+ :%sauth' %self.userCmdPrefix,
            'help':'%sauth <PASSWORD> - Logs you in, only to be used through private messages.\n' % self.userCmdPrefix}))
        self.registerCommand(Command({
            '__call__':self.inviteCmd,
            'name':'%sinvite'%self.userCmdPrefix,
            'regex':'^:\S* PRIVMSG (#?)\w+ :%sinvite' %self.userCmdPrefix,
            'help':'%sinvite <nick> - Invites a user to a channel.' %self.userCmdPrefix}))
        self.registerCommand(Command({
            '__call__':self.kickCmd,
            'regex':'^:\S* PRIVMSG (#?)\w+ :%skick' %self.userCmdPrefix,
            'help':'%skick <nick> - Will kick a user from the channel.' %self.userCmdPrefix}))
        self.registerCommand(Command({
            '__call__':self.joinCmd,
            'name':'%sjoin'%self.userCmdPrefix,
            'regex':'^:\S* PRIVMSG (#?)\w+ :%sjoin' %self.userCmdPrefix,
            'help':'%sjoin <nick> - Adds the bot to a channel.' %self.userCmdPrefix}))
        self.registerCommand(Command({
            '__call__':self.partCmd,
            'name':'%spart'%self.userCmdPrefix,
            'regex':'^:\S* PRIVMSG (#?)\w+ :%spart' %self.userCmdPrefix,
            'help':'%spart [channel] - Removes the bot from this or another channel.' %self.userCmdPrefix}))
        self.registerCommand(Command({
            '__call__':self.voiceCmd,
            'name':'%svoic'%self.userCmdPrefix,
            'regex':'^:\S* PRIVMSG (#?)\w+ :%svoice' %self.userCmdPrefix,
            'help':'%svoice <nick> [-] - +v/-v' %self.userCmdPrefix}))
        self.registerCommand(Command({
            '__call__':self.opCmd,
            'name':'%sop'%self.userCmdPrefix,
            'regex':'^:\S* PRIVMSG (#?)\w+ :%sop' %self.userCmdPrefix,
            'help':'%sop <nick> [-] - +o/-o' %self.userCmdPrefix}))
        self.registerCommand(Command({
            '__call__':self.hopCmd,
            'name':'%shop'%self.userCmdPrefix,
            'regex':'^:\S* PRIVMSG (#?)\w+ :%shop' %self.userCmdPrefix,
            'help':'%shop <nick> [-] - +h/-h' %self.userCmdPrefix}))
        self.registerCommand(Command({
            '__call__':self.killCmd,
            'name':'%sdie'%self.userCmdPrefix,
            'regex':'^:\S* PRIVMSG (#?)\w+ :%sdie' %self.userCmdPrefix,
            'help':'%sdie - Kills the bot' %self.userCmdPrefix}))
        
    def getNick(self, msg): 
        return msg[1:msg.index('!')]
    def getUser(self, msg): 
        return msg[1:msg.index(' ')]
    def getChannel(self, msg): 
        try:
            args = msg.split(' ')
            if args[2].startswith('#'):
                return args[2]
        except:
            return None
    def userIsAuth(self, msg):
        if self.getNick(msg) in self.authUsers: return True
        else: return False
    def getUserCommandArgs(self, msg):
        args = msg[msg.index(':',msg.index(' PRIVMSG '))+1:].split(' ')
        args = [arg for arg in args if arg is not '']
        return args
    def authCmd(self, msg):
        args = self.getUserCommandArgs(msg)
        db = anydbm.open(self.userCredsFile, 'c')
        if len(args) == 1 and self.getUser(msg) in self.authUsers:
            self.authUsers.remove(self.getUser(msg))
            self.sendUserMsg(self.getNick(msg), 'Deauthenticated %s successfully\n' % self.getUser(msg))
        elif len(args) == 2 and self.getChannel(msg) is not None:
            try:
                del db[self.getUser(msg)]
                self.sendChanMsg(self.getChannel(msg), 'You have compromised yourself. You have been removed from the privileged users list.\n')
            except:
                self.sendChanMsg(self.getChannel(msg), 'Good job! Now go change all of your passwords!\n')
        elif len(args) == 2:
            for user, storedHash in db.iteritems():
                if user == self.getUser(msg):
                    if sha1(args[1]).hexdigest() == storedHash: 
                        self.authUsers.append(self.getUser(msg))
                        if self.debug: print('Authenticated %s successfully.' % self.getUser(msg))
                        self.sendUserMsg(self.getNick(msg), 'Authenticated %s successfully.' % self.getUser(msg))
                    else:
                        if self.debug: print('Failed to authenticate %s.' % self.getUser(msg))
                        self.sendUserMsg(self.getNick(msg), 'Failed to authenticate %s' % self.getUser(msg))
        db.close()
    @requiresPermissions
    @mustBeInChannel
    def inviteCmd(self, msg): # Parses the message to extract NICK and CHANNEL
        channel = self.getChannel(msg)
        args = self.getUserCommandArgs(msg)
        if len(args) is 2: # Checks if user inserted a nickname to invite
            target = args[1]
            self.sendChanMsg(channel, "Inviting %s to %s.\n" % (target, channel) )
            self.invite(target,channel)
        else: # Success
            self.sendChanMsg(channel,"Bad arguments. Usage: %sinvite <nick>"%self.userCmdPrefix)
    @requiresPermissions
    def joinCmd(self, msg):
        args=self.getUserCommandArgs(msg)
        if (len(args) == 2) and args[1].startswith('#'):
            self.joinChannel(args[1])
    @requiresPermissions
    def partCmd(self, msg):
        args=self.getUserCommandArgs(msg)
        if (len(args) == 1) and (self.getChannel(msg) is not None): self.partChannel(self.getChannel(msg))
        elif (len(args) == 2) and args[1].startswith('#'): self.partChannel(args[1])
    @requiresPermissions
    @mustBeInChannel
    def kickCmd(self, msg):
        channel = self.getChannel(msg)
        args = self.getUserCommandArgs(msg)
        if len(args) <2: 
            self.sendChanMsg(channel,"Bad arguments. Usage: %skick <nick> [reason]"%self.userCmdPrefix)# Success
            return
        if len(args) >=2: target = args[1]
        reason = ' '.join(args[2:])
        if reason is not '': self.kick(target,channel, reason)
        else: self.kick(target,channel, '')
    @requiresPermissions
    @mustBeInChannel
    def voiceCmd(self, msg):
        channel = self.getChannel(msg)
        args = self.getUserCommandArgs(msg)
        if len(args) <2: 
            self.sendChanMsg(channel,"Bad arguments. Usage: %svoice <nick> [+/-]"%self.userCmdPrefix)# Success
            return
        if len(args) >=2: target = args[1]
        if len(args) >=3: mode = args[2]
        else: mode = '+'
        self.voice(target,channel, mode)
    @requiresPermissions
    @mustBeInChannel
    def opCmd(self, msg):
        channel = self.getChannel(msg)
        args = self.getUserCommandArgs(msg)
        if len(args) <2: 
            self.sendChanMsg(channel,"Bad arguments. Usage: %sop <nick> [+/-]"%self.userCmdPrefix)# Success
            return
        if len(args) >=2: target = args[1]
        if len(args) >=3: mode = args[2]
        else: mode = '+'
        self.op(target,channel, mode)
    @requiresPermissions
    @mustBeInChannel
    def hopCmd(self, msg):
        channel = self.getChannel(msg)
        args = self.getUserCommandArgs(msg)
        if len(args) <2: 
            self.sendChanMsg(channel,"Bad arguments. Usage: %shop <nick> [+/-]"%self.userCmdPrefix)# Success
            return
        if len(args) >=2: target = args[1]
        if len(args) >=3: mode = args[2]
        else: mode = '+'
        self.hop(target,channel, mode)
    @requiresPermissions
    def killCmd(self, msg): #This kills the bot
        self.running = False
        self.send("QUIT oh_noes!_why_%s_whyyyy..._*ded*_X(_(Exited_normally!)\n" % self.getNick(msg))
    def helpCmd(self, msg):
        args = self.getUserCommandArgs(msg)
        nick = self.getNick(msg)
        channel = self.getChannel(msg)
        availableCommands = [command.help for command in self.msgHandlers.values() if hasattr(command, 'help')]
        for commands in self.msgHandlers.values():
            for command in commands:
                if hasattr(command, 'help'):
                    self.sendUserMsg(nick, command.help)
"""    
:xterm!~xterm@fake.email PRIVMSG xterm :.help

                        #DICE

    def dice(msg):
        nick = getNick(msg)
        chan = getChannel(msg)
        dice = random.randint(1,6).__str__() # converts the integer dice to a string to be concatenated in the final output
        print (nick + " rolled the dice and got a " + dice)
        sendChanMsg(chan, nick + " rolled a " + dice)

                        #QUOTES

            
        
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