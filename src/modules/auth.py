import argparse, os, sys, anydbm
from hashlib import sha1
from cmd_api import register_cmd
import pdb
import global_vars
ircd = None


authUsers=[]

userCredsFile='passwd'

def isUserAuth(user):
    if user in authUsers:
        return True

#passhrase hashing
def checkUserHash(user, passphrase):
    db = anydbm.open(userCredsFile, 'r')
    if user in db and sha1(passphrase).hexdigest() == db[user]:
        return True
    print 'Not found'
    return False
def storeUserHash(user, passphrase):
    db = anydbm.open(userCredsFile, 'c')
    db[user] = sha1(passphrase).hexdigest()
def list_auths():
    return authUsers
def list_users():
    db = anydbm.open(userCredsFile, 'r')
    return db.keys()

#promote and demote
def promote_user(user):
    authUsers.append(user)
    
def demote_user(user):
    authUsers.remove(user)

#Auth and Deauth
def authenticate_user(user, passphrase):
    if checkUserHash(user, passphrase):
        promote_user(user)
        return True
    else: return False
def deauthenticate_user(user):
    demote_user(user)

#Privilege wrapper
def privileged_cmd(f):
    def exec_cmd(*argv, **kwargs):
        # Add the command to the function list.
        user = kwargs.get('user',None)
        nick = kwargs.get('nick',None)
        if user == None: return
        if isUserAuth(user):
            print 'Privileged execution for: %s' % user
            return f(*argv, **kwargs)
        else:
            global_vars.ircd.sendUserMsg(nick, 'Please authenticate before using this command.')

    return exec_cmd

@register_cmd(name='auth', aliases=['auth'], usage='auth <passphrase>', description='auth')
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
    nick = kwargs.get('nick', None)
    if user == None: return
    if authenticate_user(user, args.passphrase):
        global_vars.ircd.sendUserMsg(nick, 'Authentication successful.')
    else:
        global_vars.ircd.sendUserMsg(nick, 'Authentication unsuccessful.')


@register_cmd(name='deauth', aliases=['deauth'], usage='deauth', description='deauth')
@privileged_cmd
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

@register_cmd(name='adduser', aliases=['adduser'], usage='adduser <nick>', description='adduser')
@privileged_cmd
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

@register_cmd(name='promote', aliases=['promote'], usage='promote <nick>', description='promote')
@privileged_cmd
def promote(*argv, **kwargs):
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
    promote_user(args.nick)
    global_vars.ircd.sendUserMsg(args.nick, 'You have been promoted.')
    
@register_cmd(name='demote', aliases=['demote'], usage='demote <nick>', description='demote')
@privileged_cmd
def demote(*argv, **kwargs):
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
    demote_user(args.nick)
    global_vars.ircd.sendUserMsg(args.nick, 'You have been demoted.')
    
@register_cmd(name='setpass', aliases=['setpass'], usage='setpass <passphrase>', description='setpass')
@privileged_cmd
def setpass(*argv, **kwargs):
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
    user = kwargs.get('user')
    storeUserHash(user, args.passhrase)
    nick = kwargs.get('nick')
    global_vars.ircd.sendUserMsg(nick, 'Your password has been changed.')
    
@register_cmd(name='listusers', aliases=['listusers'], usage='listusers', description='listusers')
def listusers(*argv, **kwargs):
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
    nick = kwargs.get('nick')
    global_vars.ircd.sendUserMsg(nick,'Users in the database: %s' % ' - '.join(list_users()))
    
@register_cmd(name='listauths', aliases=['listauths'], usage='listauths', description='listauths')
def listauths(*argv, **kwargs):
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
    nick = kwargs.get('nick')
    global_vars.ircd.sendUserMsg(nick,'Users in the auth list: %s' % ' - '.join(list_auths()))
    