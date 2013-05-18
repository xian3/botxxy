import argparse, os, sys
from cmd_api import register_cmd



#@register_cmd(name='test', aliases=['test'], usage='test', description='Print test.')
def test(*argv):
    parser = argparse.ArgumentParser(prog=argv[0])
    parser.add_argument('command', metavar='CMD', action="store", help = 'The command to run.')
    
    # Attempt to parse the command line.
    try:
        args = parser.parse_args(argv[1:])
    
    # If there are any issues parsing the command line.
    except argparse.ArgumentError, exc:
        print exc.message, '\n', exc.argument
    
    # Normally a '-h' causes the script to call sys.exit, this will catch that.
    except SystemExit:
        return
    
    print 'Test'
    
    return







