
from os import path
import json
from datetime import datetime

from testing.commandLineParser import *
from setup.config import Config, ClassConfig
import setup.native as native
from subprocess import check_output as systemCall

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
    elif action == "create_test_assignment":
        createTestAssignment(config, args)
    elif action == "fake_upload":
        fakeUploadSubmission(config, args)
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

    print """Creating user submission directory for each assignment then
             populating with user submission settings file"""

    defaultUserConfigPath = path.join("examples","defaults","user_assignment_settings.json")

    # Loop through assignments and configure user submission directory
    for assignment in course.assignments:

        # Path to the assignment submission: data/submissions/ASSIGNMENT/USER
        submissionsPath = path.join(config.dataPath, "submissions",assignment, username)

        # Create user submissions directory
        native.createDirectory(submissionsPath)

        # Copy user assignment settings
        native.copyFile(defaultUserConfigPath, path.join(submissionsPath,"user_assignment_settings.json"))

# Creates and sets up an assignmnet
# Starts by calling create_new_assignment within base/bin, then replaces
# the newly created directory with the specified example
def createTestAssignment(config, args):
    # Check arguments
    if len(args) != 2:
        print "USAGE: create_test_assignment assignment_name example_name"
        return;

    assignmentName = args[0]
    exampleName = args[1]

    # Path to create_new_assignment executable
    pathToCreateNewAssignment = path.join(config.basePath,"bin","create_new_assignment")

    # Path to example assignment
    pathToExample = path.join("examples", "assignments", exampleName)

    # Make sure example exists
    if not path.exists(pathToExample):
        print "ERROR: The specified example at "+pathToExample+" does not exist"
        return;

    # Call base/bin/create_new_assignment with assignment name
    try:
        print "Calling \"base/bin/create_new_assignment " + assignmentName + '"'
        systemCall(" ".join([pathToCreateNewAssignment, args[0]]),shell=True)
    except:
        print "Create assignment not successfully run!"
        raise

    # Path to the newly created assignment
    pathToAssignment = path.join(config.dataPath, "assignments",assignmentName)

    # Remove the newly created assignment directory
    native.removeDirectory(pathToAssignment)

    # Copy example to where the newly created assignment was
    native.copyDirectory(pathToExample, pathToAssignment)

    print "Reseting assignment id and name configuration values"

    # Get path to the new assignment's configuration file
    pathToAssignmentConfig = path.join(pathToAssignment, "assignment.json")

    # Modify assignment.json name and id to original (generated) value
    try:
        # Open and read from assignment config
        assignmentConfigFile = open(pathToAssignmentConfig,'r')
        assignmentConfig = json.load(assignmentConfigFile)
        assignmentConfigFile.close()

        # Change id and name to assignmentName (the original values)
        assignmentConfig["id"] = assignmentName
        assignmentConfig["name"] = assignmentName

        # Write new assignment config file
        assignmentConfigFile = open(pathToAssignmentConfig,'w')
        json.dump(assignmentConfig, assignmentConfigFile,indent=4)
        assignmentConfigFile.close()

    except:
        print "ERROR: Something bad happened when modifying assignment.json"
        raise

# Simulate uploading to the server, but without uploading to the server
# This means directly adding the assignment to the submissions directory and
# changing upload.json manually
def fakeUploadSubmission(config, args):
    if len(args) != 3:
        raise Exception("USAGE: fake_upload assignment_name student path/from/examples/submissions")

    print "Fake uploading to assignment \"" + args[0] + "\"" + \
          " under student \"" + args[1] + "\" " + \
          "with example submission " + args[2]

    assignmentID = args[0]
    student = args[1]
    testSubmissionPath = path.join("examples","submissions",args[2])

    # Get the path where this directory should be "uploaded" to, then figure
    # out which submission number the student is on
    uploadSubmissionDirectory = path.join(config.dataPath, "submissions",
            assignmentID, student)

    submissionNumber = None
    uploadSubmissionPath = None

    # Keep incrementing until a submission number is not found
    for i in range(1,255):
        uploadSubmissionPath = path.join(uploadSubmissionDirectory,  str(i))
        if not path.exists(uploadSubmissionPath):
            # This submission number was not found, this must be the last
            # submission + 1
            submissionNumber = i
            print "Number of submissions:",i
            break;

    print "Copying test submission to submissions directory"

    # Copy test submission to submissions directory
    native.copyDirectory(testSubmissionPath, uploadSubmissionPath)

    # Add submission to uploads.json

    # Get path to uploads.json file
    uploadFilePath = path.join(config.dataPath, "submissions", assignmentID,
            "upload.json")

    uploadFileData = {"submissions":[]}

    # See if previous uploads.json exists (so we would need to append)
    if path.exists(uploadFilePath):
        try:
            uploadFile = open(uploadFilePath)
            uploadFileData = json.load(uploadFile)
            uploadFile.close()
        except:
            print "ERROR: Could not read/parse upload file"
            raise

    # Get the new submission data to add
    newSubmissionData = {
        "submitTime": str(datetime.now()),
        "student": student,
        "submissionNumber": submissionNumber
    }

    # Add to submissions field of upload.json data
    uploadFileData["submissions"].append(newSubmissionData)

    # Write new submissions data to upload.json
    try:
        uploadFile = open(uploadFilePath, 'w')
        json.dump(uploadFileData, uploadFile, indent=4)
        uploadFile.close()
    except:
        print "ERROR: Error writing new json to upload.json file"
        raise


# When called from command line, parse arguments and feed to runTest, which
# will take care of running the commands specified
if __name__ == "__main__":

    args = parseTestArguments(defaultConfigPath=defaultConfigPath)

    runTest(args.configPath, args.action[0], args.action[1:])
