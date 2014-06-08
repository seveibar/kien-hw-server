
from os import path

from testing.commandLineParser import *
from setup.config import Config, ClassConfig
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

    username = args[0]

    print "Creating user \""+username+"\""

    # Get class configuration
    course = ClassConfig(path.join(config.dataPath,"coursedata","class.json"))

    print "Creating user submission directory for each assignment then populating with user submission settings file"

    defaultUserConfigPath = path.join("examples","defaults","user_assignment_settings.json")

    # Loop through assignments and configure user submission directory
    for assignment in course.assignments:

        # Path to the assignment submission: data/submissions/ASSIGNMENT/USER
        submissionsPath = path.join(config.dataPath, "submissions",assignment, username)

        # Create user submissions directory
        native.createDirectory(submissionsPath)

        # Copy user assignment settings
        native.copyFile(defaultUserConfigPath, path.join(submissionsPath,"user_assignment_settings.json"))

    # print "Copying default user assignment config to user directory"
    #
    # defaultUserConfigPath = path.join("examples","defaults","user_assignment_config.json")
    # outputUserConfigPath = path.join(config.dataPath,"submissions",args[0], "user_assignment_config.json")
    #
    # native.copyFile(defaultUserConfigPath, outputUserConfigPath)


# When called from command line, parse arguments and feed to runTest, which
# will take care of running the commands specified
if __name__ == "__main__":

    args = parseTestArguments(defaultConfigPath=defaultConfigPath)

    runTest(args.configPath, args.action[0], args.action[1:])
