import socket
import ssl
import time
import random

debug = True

class BaseIRC(object):
	def __init__(self, *args, **kwargs):
		self.server = kwargs.get("server", "boxxybabee.catiechat.net")
		self.port = kwargs.get("port", 6667)
		self.ssl_port = kwargs.get("port", 6697)
		self.useSSL = kwargs.get("useSSL", False)
		self.info_user = kwargs.get("info_user", "I")
		self.info_host = kwargs.get("info_host", "m.botxxy.you.see")
		self.info_server = kwargs.get("info_server", "testserver")
		self.info_name = kwargs.get("info_name", "testname")
		self.info_name = kwargs.get("info_name", "ircFemBot")
		self.ircsock = None
		self.running = False
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
		if debug: print(msg)
		else:
			print(msg)
			self.ircsock.send(msg)
	def recv(self):
		if debug: return raw_input(">>>")
		else:
			try:
				recvd = self.ircsock.recv(512)
			except KeyboardInterrupt:
				raise KeyboardInterrupt
			print(recvd)
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
	def leaveChannel(self, channel):
		self.send("LEAVE %s\n" % channel)
	def changeTopic(self, channel, topic):
		self.send("TOPIC %s :%s\n" % ( channel, topic ) )
	def invite(self, nick, channel): # Invites given nickname to present channel
		self.send("INVITE %s %s\n" % ( nick, channel ) )
	def kick(self, nick, channel, msg='lol butthurt\n'):
		self.send("KICK %s %s %s\n" % (channel, nick, msg))
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
		self.send("PING :%s\n" % msg)	
	def pong(self, msg="Botxxy pew pew"): # This is our first function! It will respond to server Pings.
		self.send("PONG :%s\n" % msg)


class BotIRC(BaseIRC):
	def __init__(self, *args, **kwargs):
		super(BotIRC, self).__init__(*args, **kwargs)
		print('init BotIRC')
		self.running = False
		self.userCommands = {}
		self.serverCommands = {}
		#self.connect()
	def registerCommand(self, string, command):
		if type(string) is str:
			if string.startswith('!'): #USER command
				if debug: 	print('registering user command: \'%s\'' %string)
				self.userCommands[string] = command
			else:
				if debug: 	print('registering server command: \'%s\'' %string)
				self.serverCommands[string] = command
	def unregisterCommand(self, string):
		print('unregistering \'%s\'' %handlerPrefix)
		if string.startswith(' '): #SERVER command
			del self.serverCommands[handlerPrefix]
		elif string.startswith('!'): #USER command
			del self.userCommands[handlerPrefix]
	def dispatchCommand(self, msg):
		if msg.startswith(':') and msg.index(':',1) is not -1: #USER command
			print msg[msg.index(':',1)+1:]
			
			for handlerPrefix in self.userCommands.keys():
				if msg[msg.index(':',1)+1:].startswith(handlerPrefix):
					if debug: 	print('dispatching user command: \'%s\'' %handlerPrefix)
					self.userCommands[handlerPrefix](msg)
		else:
			for handlerPrefix in self.serverCommands.keys():
				if msg.startswith(handlerPrefix):
					if debug: 	print('dispatching server command: \'%s\'' %handlerPrefix)
					self.serverCommands[handlerPrefix](msg)
	def run(self):
		self.running = True
		while self.running:
			try:
				self.dispatchCommand(self.recv())
			except KeyboardInterrupt:
				self.running = False
				
				
				