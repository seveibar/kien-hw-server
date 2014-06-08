
from os import path

from testing.commandLineParser import *
from setup.config import Config
import setup.native as native

# Path to setup configuration file
defaultConfigPath = path.join( native.getSetupPath() , "config.json" )

# Run a specified test (generally run with command line arguments)
# action => string action to take e.g. make_user, make_assignment
# args   => string list of arguments
def runTest(configPath, action, args):

    config = Config(configPath)

    # Match supplied string action to function
    if action == "create_user":
        createUser(config, args)
    else:
        print "Please see usage (-h)"

# Create a user i.e. create necessary directories and configuration files for
# a user.
# More specifically, copy the default user_assignment_config to the submissions/
# username directory.
def createUser(config, args):
    if len(args) != 1 : raise Exception("Create user requires 1 argument: name")

    print "Creating user \""+args[0]+"\""

    print "Creating user directory within submissions"

    native.createDirectory(path.join(config.dataPath,"submissions",args[0]))

    print "Copying default user assignment config to user directory"

    defaultUserConfigPath = path.join("examples","defaults","user_assignment_config.json")
    outputUserConfigPath = path.join(config.dataPath,"submissions",args[0], "user_assignment_config.json")

    native.copyFile(defaultUserConfigPath, outputUserConfigPath)


# When called from command line, parse arguments and feed to runTest, which
# will take care of running the commands specified
if __name__ == "__main__":

    args = parseTestArguments(defaultConfigPath=defaultConfigPath)

    runTest(args.configPath, args.action[0], args.action[1:])
