import argparse, os, sys
from hashlib import sha1
from cmd_api import register_cmd
import pdb
ircd = None


authUsers=[]

def isUserAuth(user):
    if user in authUsers:
        return authUsers[user]

def checkUserHash(user, suppliedhash):
    db = anydbm.open(userCredsFile, 'c')
    if user in db and sha1(suppliedhash).hexdigest() == db[user]:
        return True
    return False

def authenticate_user(user, suppliedhash):
    if checkUserHash(user, suppliedhash):
        authUsers.append(user)
def deauthenticate_user(user):
    authUsers.pop(user)

def privileged_cmd(f):
    def exec_cmd(*argv, **kwargs):
        # Add the command to the function list.
        user = kwargs.get('user',None)
        if user == None: return
        if isUserAuth(user):
            print 'Privileged execution for: %s' % user
            return f(*argv, **kwargs)
    
    return exec_cmd

@register_cmd(name='auth', aliases=['auth'], usage='auth <nick>', description='auth')
@privileged_cmd
def auth(*argv, **kwargs):
    parser = argparse.ArgumentParser(prog=argv[0])
    parser.add_argument('passphrase', metavar='<passphrase>', action="store", help = 'The user to auth.')
    
    # Attempt to parse the command line.
    try:
        args = parser.parse_args(argv[1:])
    
    # If there are any issues parsing the command line.
    except argparse.ArgumentError, exc:
        print exc.message, '\n', exc.argument
    
    # Normally a '-h' causes the script to call sys.exit, this will catch that.
    except SystemExit:
        return
    user = kwargs.get('user', None)
    if user == None: return
    authenticate_user(user, args.passphrase)
    
    return


@register_cmd(name='deauth', aliases=['deauth'], usage='deauth <nick>', description='deauth')
def deauth(*argv, **kwargs):
    parser = argparse.ArgumentParser(prog=argv[0])
    # Attempt to parse the command line.
    try:
        args = parser.parse_args(argv[1:])
    
    # If there are any issues parsing the command line.
    except argparse.ArgumentError, exc:
        print exc.message, '\n', exc.argument
    
    # Normally a '-h' causes the script to call sys.exit, this will catch that.
    except SystemExit:
        return
    user = kwargs.get('user', None)
    if user == None: return
    deauthenticate_user(user)
    
    return

#@register_cmd(name='adduser', aliases=['adduser'], usage='adduser <nick>', description='adduser')
def adduser(*argv, **kwargs):
    parser = argparse.ArgumentParser(prog=argv[0])
    parser.add_argument('nick', metavar='<nick>', action="store", help = 'The user to auth.')
    
    # Attempt to parse the command line.
    try:
        args = parser.parse_args(argv[1:])
    
    # If there are any issues parsing the command line.
    except argparse.ArgumentError, exc:
        print exc.message, '\n', exc.argument
    
    # Normally a '-h' causes the script to call sys.exit, this will catch that.
    except SystemExit:
        return
    channel = kwargs.get('channel', '')
    #ircd.auth(args.nick, channel, '-')
    
    return

#@register_cmd(name='deluser', aliases=['deluser'], usage='deluser <nick>', description='deluser')
def deluser(*argv, **kwargs):
    parser = argparse.ArgumentParser(prog=argv[0])
    parser.add_argument('nick', metavar='<nick>', action="store", help = 'The user to auth.')
    
    # Attempt to parse the command line.
    try:
        args = parser.parse_args(argv[1:])
    
    # If there are any issues parsing the command line.
    except argparse.ArgumentError, exc:
        print exc.message, '\n', exc.argument
    
    # Normally a '-h' causes the script to call sys.exit, this will catch that.
    except SystemExit:
        return
    channel = kwargs.get('channel', '')
    #ircd.auth(args.nick, channel, '-')
    
    return