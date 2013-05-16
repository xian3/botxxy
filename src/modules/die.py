import argparse, os, sys
from cmd_api import register_cmd
from auth import privileged_cmd
ircd = None

@register_cmd(name='die', aliases=['die'], usage='die', description='die')
@privileged_cmd
def die(*argv, **kwargs):
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
    user = kwargs.get('user', '')
    nick = user.split('!')[0]
    ircd.send("QUIT oh_noes!_why_%s_whyyyy..._*ded*_X(_(Exited_normally!)\n" % nick)
    
    return