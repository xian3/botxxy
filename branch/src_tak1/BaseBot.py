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

class BaseIRC(object):
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
		print(msg)
		#self.ircsock.send(msg)
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
	def leaveChannel(self, channel):
		self.send("LEAVE %s\n" % channel)
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
	def hello(self, msg): # This function responds to a user that inputs "Hello testbot"
		nick = getNick(msg)
		chan = getChannel(msg)
		self.send("PRIVMSG %s :Hello %s! Type !help for more information.\n" % ( chan, nick ) )

class BotIRC(BaseIRC):
	def __init__(self, *args, **kwargs):
		print('init BotIRC')
		super(BaseIRC, self).__init__(*args, **kwargs)
		self.commandsList = {}
	def registerCommand(self, string, command):
		print('registering \'%s\'' %string)
		if type(string) is str:
			self.commandsList[string] = command
	def unregisterCommand(self, string):
		print('unregistering \'%s\'' %string)
		del self.commandsList[string]
	def dispatchCommand(self, msg):
		for handlerPrefix in self.commandsList.keys():
			if msg.startswith(handlerPrefix):
				print('dispatching \'%s\'' % handlerPrefix)
				self.commandsList[handlerPrefix](msg)

def main():
	b = BotIRC()
	def haha(msg):
		print('haha %s' % msg)
	b.registerCommand(' 359 ', haha)
	print(b.commandsList)
	msg = ' 359 this is a test'
	b.dispatchCommand(msg)
	b.unregisterCommand(' 359 ')
	print(b.commandsList)
	
if __name__ == '__main__':
	main()