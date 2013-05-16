import argparse, os, sys
from cmd_api import register_cmd
ircd = None

@register_cmd(name='hop', aliases=['hop'], usage='hop <nick>', description='hop')
def hop(*argv, **kwargs):
    parser = argparse.ArgumentParser(prog=argv[0])
    parser.add_argument('nick', metavar='<nick>', action="store", help = 'The user to op.')
    
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
    ircd.hop(args.nick, channel)
    
    return


@register_cmd(name='dehop', aliases=['dehop'], usage='dehop <nick>', description='dehop')
def dehop(*argv, **kwargs):
    parser = argparse.ArgumentParser(prog=argv[0])
    parser.add_argument('nick', metavar='<nick>', action="store", help = 'The user to hop.')
    
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
    ircd.hop(args.nick, channel, '-')
    
    return

