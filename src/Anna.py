#!python2.7
try:
    import readline
except:
    pass
import os, argparse, sys, urllib2, urllib, re, shlex, inspect, json
from inspect import getmembers, isfunction
import modules.global_vars as global_vars
import irc
from modules import cmd_api

class Anna(object):
    def __init__(self, *args, **kwargs):
        self.ircd=kwargs.get('ircd', irc.ircd(kwargs.get('ircArgs', {})))
        self.cmd =kwargs.get('cmd', cmd_api.commands)
        cmd_api.register_ircd(self.ircd)
    def run(self):
        while global_vars.keep_running:
            msg = self.ircd.recv()
            if not msg.startswith(':'): continue
            split_msg = msg.split(' ',3)
            user = split_msg[0].lstrip(':')
            nick = user.split('!')[0]
            msgtype = split_msg[1]
            if msgtype != 'PRIVMSG': continue
            channel = split_msg[2]
            msg = split_msg[3].lstrip(':')
            print msg
            msgparams={'nick':nick,'user':user,'msgtype':msgtype,'channel':channel}
            if msg.strip() == '':
                continue
            lexer = shlex.shlex(msg, posix=True)
            lexer.wordchars += '.-=\\/!@#$%^&*()_+~`;'
            
            tokens = []
            for token in lexer:
                tokens.append(token)
            
            if len(tokens) == 0:
                continue

            cmd = tokens[0].lower()
            
            found = False
            for command in cmd_api.commands:
                if cmd in cmd_api.commands[command]['aliases'] or command == cmd:
                    cmd_api.commands[command]['func'](*tokens, **msgparams)
                    found = True
            
            if not found:
                print 'ERROR: Unsupported command "%s".' % (cmd)
        
def main():
    anna = Anna()
    anna.run()
if __name__ == '__main__':
    main()