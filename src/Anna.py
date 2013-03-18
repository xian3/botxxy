from GenericBot import *

anna_settings = {}
anna_settings['debug'] = False
anna_settings['userCmdPrefix'] = '.'
anna_settings['server'] = "boxxybabee.catiechat.net"
anna_settings['port'] = 6667
anna_settings['useSSL'] = False
anna_settings['info_user'] = "Anna"
anna_settings['info_host'] = "m.botxxy.you.see"
anna_settings['info_name'] = "Anna"
anna_settings['info_nick'] = "Anna"

class AnnaBot(GenericBot):
    def __init__(self, *args, **kwargs):
        super(AnnaBot, self).__init__(*args, **kwargs)
        
# ":b0nk!LoC@fake.dimension PRIVMSG #test :lolmessage"        
def main():
    anna = AnnaBot(**anna_settings)
    anna.addCommands()
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