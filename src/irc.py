
class ircd(object):
    def __init__(self, *args, **kwargs):
        self.server = kwargs.get("server", "boxxybabee.catiechat.net")
        self.port = kwargs.get("port", 6667)
        self.useSSL = kwargs.get("useSSL", False)
        self.info_user = kwargs.get("info_user", "I")
        self.info_host = kwargs.get("info_host", "m.botxxy.you.see")
        self.info_server = kwargs.get("info_server", "testserver")
        self.info_name = kwargs.get("info_name", "testname")
        self.ircsock = None
        self.running = False
        self.debug = True
    def connect(self):
        try:
            self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.useSSL: self.ircsock = ssl.wrap_socket(ircsock)
            self.ircsock.connect((self.server, self.ssl_port))
        except SocketError:
            return False
        return True
    def dispatch(self):
        raise NotImplemented
    def send(self, msg):
        if self.debug: print(msg.rstrip())
        else:
            #print(msg)
            self.ircsock.send(msg)
    def recv(self):
        if self.debug: return raw_input(">>>")
        else:
            try:
                recvd = self.ircsock.recv(512).rstrip()
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            #print recvd
            return recvd
    def server_login(self): 
        self.send("USER %s %s %s %s\n" % ( botuser, bothost, botserver, botname) )
        self.send("NICK %s\n" % botnick) # Here we actually assign the nick to the bot
        time.sleep(3)
        self.send("NICKSERV IDENTIFY %s\n" % botpassword) # Identifies the bot's nickname with nickserv
        time.sleep(3)
        self.send("NICKSERV SET ENFORCE ON\n")
    #
    def joinChannel(self, channel):
        self.send("JOIN %s\n" % channel)
    def partChannel(self, channel, reason='Awwwww, got to go :('):
        self.send("PART %s %s\n" % (channel, reason))
    def changeTopic(self, channel, topic):
        self.send("TOPIC %s :%s\n" % ( channel, topic ) )
    def invite(self, nick, channel): # Invites given nickname to present channel
        self.send("INVITE %s %s\n" % ( nick, channel ) )
    def kick(self, nick, channel, msg='lol butthurt\n'):
        self.send("KICK %s %s %s\n" % (channel, nick, msg.strip('\n')))
    def voice(self, nick,channel, mode='+'):
        self.send("MODE %s %sv %s\n" % ( channel, mode[0], nick) )
    def op(self, nick,channel, mode='+'):
        self.send("MODE %s %so %s\n" % ( channel, mode[0], nick) )
    def hop(self, nick,channel, mode='+'):
        self.send("MODE %s %sh %s\n" % ( channel, mode[0], nick) )
    #
    def sendChanMsg(self, channel, msg): # This sends a message to the channel 'chan'
        self.send("PRIVMSG %s :%s\n" % ( channel, msg ) )
    def sendUserMsg(self, nick, msg): # This sends a notice to the nickname 'nick'
        self.send("NOTICE %s :%s\n" % ( nick, msg ) )
    def getNick(self, msg): # Returns the nickname of whoever requested a command from a RAW irc privmsg. Example in commentary below.
        # ":b0nk!LoC@fake.dimension PRIVMSG #test :lolmessage"
        return msg[msg.index(':')+1:msg.index('!')]
    def getUser(self, msg): # Returns the user and host of whoever requested a command from a RAW irc privmsg. Example in commentary below.
        # ":b0nk!LoC@fake.dimension PRIVMSG #test :lolmessage"
        return msg[msg.index(':')+1:msg.index(' PRIVMSG ')]
    def getChannel(self, msg): # Returns the channel from whereever a command was requested from a RAW irc PRIVMSG. Example in commentary below.
        # ":b0nk!LoC@fake.dimension PRIVMSG #test :lolmessage"
        return msg.index(' PRIVMSG ')[-1].split(' :')[0]
    
    def ping(self, reply): # This is our first function! It will respond to server Pings.
        self.send("PONG :%s\n" % reply)