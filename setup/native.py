#!/usr/bin/python

# Functions for interacting with the filesystem and shell
# HACK: needs to be replaced with a less hacky/dangerous solution

import subprocess
import os
from os import path

# Returns the path to the setup
def getSetupPath():
    setup_directory = path.dirname(path.realpath(__file__))
    return path.normpath(path.join(setup_directory, ".."))

# Remove directory at path
def removeDirectory(path):
    raise NotImplementedError("REMOVE DIRECTORY")

# Calls shell to execute command and returns response or
# None is there was an error
# Note: ANY PROGRAM THAT USES THIS IS A DIRTY HACK
def callShell(arguments,Shell=True):
    try:
        # Try to execute command
        return subprocess.check_output(arguments)
    except subprocess.CalledProcessError:
        # There was an error, return None
        return None
