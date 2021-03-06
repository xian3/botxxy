import socket
import ssl
import time
import random
import traceback
import re

Command = lambda kwargs: type('', (object,), kwargs)()

class BaseIRC(object):
    def __init__(self, *args, **kwargs):
        self.debug =  kwargs.get("debug", True)
        self.server = kwargs.get("server", "boxxybabee.catiechat.net")
        self.port = kwargs.get("port", 6667)
        self.ssl_port = kwargs.get("port", 6697)
        self.useSSL = kwargs.get("useSSL", False)
        self.info_user = kwargs.get("info_user", "I")
        self.info_host = kwargs.get("info_host", "m.botxxy.you.see")
        self.info_server = kwargs.get("info_server", "testserver")
        self.info_name = kwargs.get("info_name", "testname")
        self.info_nick = kwargs.get("info_name", "ircFemBot")
        self.ircsock = None
        print("%s"% kwargs)
        
    def connect(self):
        try:
            self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.useSSL: self.ircsock = ssl.wrap_socket(self.ircsock)
            self.ircsock.connect((self.server, self.ssl_port))
        except socket.error:
            return False
        return True
    def dispatchCommand(self):
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
        self.send("USER %s %s %s %s\n" % ( self.info_user, self.info_host, self.info_server, self.info_name) )
        self.send("NICK %s\n" % self.info_nick) # Here we actually assign the nick to the bot
        time.sleep(3)
        self.send("NICKSERV IDENTIFY %s\n" % "temporary") # Identifies the bot's nickname with nickserv
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

    def ping(self, msg): # This is our first function! It will respond to server Pings.
        self.send("PING :%s\n" % msg.lstrip('PING :'))


class BotIRC(BaseIRC):
    def __init__(self, *args, **kwargs):
        super(BotIRC, self).__init__(*args, **kwargs)
        print('init BotIRC')
        self.userCmdPrefix = kwargs.get('userCmdPrefix', '!')
        self.msgHandlers = {
            }
    def registerCommand(self, command):
        if command.regex not in self.msgHandlers: self.msgHandlers[command.regex] = []
        self.msgHandlers[command.regex].append(command)
    def unregisterCommand(self, handlerPrefix):
        print('unregistering \'%s\'' %handlerPrefix)
        if handlerPrefix.startswith(' '): #SERVER command
            del self.serverCommands[handlerPrefix]
        elif handlerPrefix.startswith('%s'%self.userCmdPrefix): #USER command
            del self.msgHandlers[handler][handlerPrefix]
    def dispatchCommand(self, msg):
        msg_split = msg.split(' ')
        try:
            if msg_split[0].startswith(':%sAnna!~Anna'%self.userCmdPrefix): return
            for msgHandler in self.msgHandlers.keys():
                if re.match(msgHandler, msg):
                    for command in self.msgHandlers[msgHandler]:
                        command(msg)
                
        except:
           print('%s\nException caught on %s' %('*'*25,msg))
           traceback.print_exc()
    def run(self):
        self.running = True
        while self.running:
            self.dispatchCommand(self.recv())
 