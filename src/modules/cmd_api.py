import inspect, os, sys

########################> Check our environment <#########################

# Ensure this is only being imported, not run directly.
if __name__ == '__main__':
    print 'ERROR: This script is not designed to be run by itself.'
    sys.exit(-1)

# Make sure that all this is being imported by cc, or something that cc is importing.
#if os.path.split(inspect.getfile(inspect.stack()[-1][0]))[1] != 'cc.py':
#    print 'ERROR: This script is not designed to be run without first being imported into cc.py'
#    sys.exit(-2)

##########################> Declare Globals <##########################

# Registered commands are held here.
commands = {}

########################> Declare Decorators <#########################

# Using closures and decorators to register commands... ftw.
def register_cmd(**kwargs):
    
    def register_cmd(func):
        
        # Add the command to the function list.
        name = kwargs.get('name',func.func_name)
        aliases = kwargs.get('aliases',[])
        usage = kwargs.get('usage',name)
        description = kwargs.get('description','')
        
        commands[name] = {'func':func, 'aliases':aliases, 'usage':usage, 'description':description}
        
        return func
    
    return register_cmd


modules_dir = os.path.abspath('modules')

for entry in os.listdir(modules_dir):
    if entry in ['cmd_api.py','__init__.py']:
        continue
    
    abs_entry = os.path.join(modules_dir,entry)
    
    if not os.path.isdir(abs_entry):
        name,ext = os.path.splitext(entry)
        
        # Only import python files.
        if ext not in ['.py']:
            continue
    else:
        name = os.path.split(entry)[1]
        
    
    # Import the module and iterate its functions.
    exec('import %s' % name)
    
for func in commands:
    print 'Import "%s" added command "%s".' % (commands[func]['func'].func_globals['__name__'], func)
    
def register_ircd(ircd):
    for func in commands.keys():
        commands[func]['func'].func_globals['ircd']=ircd