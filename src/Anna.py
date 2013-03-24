from GenericBot import *
import random
import os


class AnnaBot(GenericBot):
    def __init__(self, *args, **kwargs):
        #OVERRIDES
        kwargs['debug'] = False
        kwargs['userCmdPrefix'] = '.'
        kwargs['server'] = "boxxybabee.catiechat.net"
        kwargs['port'] = 6667
        kwargs['useSSL'] = False
        kwargs['info_user'] = "Anna"
        kwargs['info_host'] = "m.botxxy.you.see"
        kwargs['info_name'] = "Anna"
        kwargs['info_nick'] = "Anna"
        super(AnnaBot, self).__init__(*args, **kwargs)
        self.quotesDir = './quotes/'
        self.partsDir = './parts/'
        self.joinsDir = './joins/'
        
    def addCommands(self):
        super(AnnaBot, self).addCommands() #Adds all the Generic Commands
        self.registerCommand(Command( {
            '__call__':self.addQuoteCmd,
            'regex':'^:\S* PRIVMSG #\w+ :%saddquote'% self.userCmdPrefix,
            'help':'%saddquote <quote>\n' %self.userCmdPrefix
            }))
        self.registerCommand(Command( {
            '__call__':self.quoteCmd,
            'regex':'^:\S* PRIVMSG #\w+ :%squote'% self.userCmdPrefix,
            'help':'%squote <name>\n' %self.userCmdPrefix
            }))
        self.registerCommand(Command( {
            '__call__':self.addJoinHandler,
            'regex':'^:\S* PRIVMSG #\w+ :%saddjoin'% self.userCmdPrefix,
            'help':'%saddjoin <PHRASE>\n' %self.userCmdPrefix
            }))
        self.registerCommand(Command( {
            '__call__':self.joinHandler,
            'regex':'^:\S* JOIN #\w+'
            }))
        self.registerCommand(Command( {
            '__call__':self.addPartHandler,
            'regex':'^:\S* PRIVMSG #\w+ :%saddpart'% self.userCmdPrefix,
            'help':'%saddpart <PHRASE>\n' %self.userCmdPrefix
            }))
        self.registerCommand(Command( {
            '__call__':self.partHandler,
            'regex':'^:\S* PART #\w+'
            }))
    def addQuoteCmd(self, msg):
        f = open('%s%s'% (self.quotesDir, self.getNick(msg)), 'a')
        msg = msg[msg.index('%saddquote '% self.userCmdPrefix):]
        msg = msg.lstrip('%saddquote '% self.userCmdPrefix)
        f.write('%s\n' % msg)
        f.close()
    def quoteCmd(self, msg):
        args = self.getUserCommandArgs(msg)
        if len(args) == 2:
            f = open('%s%s'% (self.quotesDir, args[1]), 'r')
        else:
            files = os.listdir(self.quotesDir)
            files = [file for file in files if file is not '.' and file is not '..']
            f = open('%s%s'% (self.quotesDir,random.choice(files)), 'r')
        lines = f.readlines()
        f.close()
        if self.getChannel(msg) is not None:
            self.sendChanMsg(self.getChannel(msg), '%s - %s' % (f.name, random.choice(lines)))
        else:
            self.sendUserMsg(self.getNick(msg), '%s - %s' % (f.name, random.choice(lines)))
    def addPartHandler(self, msg):
        f = open('%s%s'% (self.partsDir, self.getNick(msg)), 'a')
        msg = msg[msg.index('%saddpart '% self.userCmdPrefix):]
        msg = msg.lstrip('%saddpart '% self.userCmdPrefix)
        f.write('%s\n' % msg)
        f.close()
    def partHandler(self, msg):
        if (os.access('%s%s'% (self.partsDir, self.getNick(msg)), os.F_OK)):
            f = open('%s%s'% (self.partsDir, self.getNick(msg)), 'r')
            lines = f.readlines()
            f.close()
            if self.getChannel(msg) is not None:
                self.sendChanMsg(self.getChannel(msg), '%s' % (random.choice(lines)))
            else:
                self.sendUserMsg(self.getNick(msg), '%s' % (random.choice(lines)))
    def addJoinHandler(self, msg):
        f = open('%s%s'% (self.joinsDir, self.getNick(msg)), 'a')
        msg = msg[msg.index('%saddjoin '% self.userCmdPrefix):]
        msg = msg.lstrip('%saddjoin '% self.userCmdPrefix)
        f.write('%s\n' % msg)
        f.close()       
    def joinHandler(self, msg):
        if (os.access('%s%s'% (self.joinsDir, self.getNick(msg)), os.F_OK)):
            f = open('%s%s'% (self.joinsDir, self.getNick(msg)), 'r')
            lines = f.readlines()
            f.close()
            if self.getChannel(msg) is not None:
                self.sendChanMsg(self.getChannel(msg), '%s' % (random.choice(lines)))
            else:
                self.sendUserMsg(self.getNick(msg), '%s' % (random.choice(lines)))
    
        
    
            
        
# ":b0nk!LoC@fake.dimension PRIVMSG #test :lolmessage"        
def main():
    anna = AnnaBot()
    anna.addCommands()
    db = anydbm.open(anna.userCredsFile, 'c')
    #db['xterm!~xterm@fake.email'] = '6c54b5c3c5f3e93afc004346ec96ddb88433b263'
    db['b0nk!~LoC@fake.dimension'] = 'b94ced3ded72349a8af691a0aa9153c0d9853568'
    db.close()
    if anna.debug:
        for test in anna.testInput:
                pass #anna.dispatchCommand(test) #structured test mode
        anna.run() # Free test mode
    else:
        anna.connect()
        anna.server_login()
        anna.joinChannel('#annatest')
        anna.run()
        
if __name__ == '__main__':
    print 'main'
    main()