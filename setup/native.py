#!/usr/bin/python

# Functions for interacting with the filesystem and shell
# HACK: needs to be replaced with a less hacky/dangerous solution

import subprocess
import os
import shutil
from os import path

# Returns the path to the setup
def getSetupPath():
    setup_directory = path.dirname(path.realpath(__file__))
    return path.normpath(path.join(setup_directory, ".."))

# Remove directory at path
def removeDirectory(path):
    print "Removing directory: ", path
    shutil.rmtree(path)

# Create directory at path
def createDirectory(path):
    print "Creating directory: ", path
    os.mkdir(path)

# Copy file
def copyFile(source,dest):
    print "Copying file from ",source,"to",dest
    shutil.copyfile(source,dest)

# Do a git clone
def gitClone(gitExecutable, repoAddr, outputPath):
    callShell([gitExecutable, "clone", repoAddr, outputPath],stdout=True)

# Elevated recreate symlink (used for copying site path into /var/www/hws)
# This is a bit hacky, but the end-user generally a default ubuntu installation
# so it should work most of the time
def elevatedRecreateSymlink(source, dest):
    callShell(["sudo","rm",dest], stdout=True)
    callShell(["sudo","ln","-s",source,dest], stdout=True)

# Calls shell to execute command and returns response or
def callShell(arguments,Shell=True,stdout=False):
    print "Shell call: ", " ".join(arguments)
    arguments = " ".join(arguments) #HACK
    try:
        # Try to execute command
        if not stdout:
            # return output
            return subprocess.check_output(arguments,shell=Shell)
        else:
            #return error code
            return subprocess.call(arguments,shell=True)
    except subprocess.CalledProcessError:
        # There was an error, return None
        return None
