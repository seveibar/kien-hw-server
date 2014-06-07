#!/usr/bin/python

# Script for performing all setup operations

import json
import sys
import argparse
import os
from os import path

from setup import native
from setup.config import Config
from setup.commandLineParser import *
import setup.exceptions

# Path to setup configuration file
defaultConfigPath = path.join( native.getSetupPath() , "config.json" )

# Remove previous directories
removePrevious = False

# Main Setup Function, all calls basically originate from this function
def runSetup(configPath, removePrevious):

    # Get configuration  config (open and parse file at configPath)
    config = loadConfig(configPath)

    # Remove previous directories (on user request)
    if removePrevious: removePreviousDirectories(config)

    # Check for previous directories
    if path.exists(config.dataPath):
        raise setup.exceptions.DataDirectoryExists()
    if path.exists(config.sitePath):
        raise setup.exceptions.SiteDirectoryExists()

    # Create data directory structure
    createDataDirectory(config.dataPath)

    # Clone base code into data directory
    cloneBaseCode(config)

    # Create site
    cloneSite(config)

    # Symlink /var/www/hws to the site
    if config.environment.apachewww != "":
        linkApache(config)

# Returns new Config object from config loaded from configPath
def loadConfig(configPath):
    return Config(configPath)

# Remove previous data and site directories (if they exist)
def removePreviousDirectories(config):
    if path.exists(config.dataPath):
        print "Removing data directory"
        native.removeDirectory(config.dataPath)
    if path.exists(config.sitePath):
        print "Removing site directory"
        native.removeDirectory(config.sitePath)

# Create data directory structure
# Should look something like...
# DATA_DIR
#     | -> code
#     | -> bin
#           |  -> hwconfig
def createDataDirectory(dataPath):
    native.createDirectory(dataPath)
    native.createDirectory(path.join(dataPath,"code"))
    native.createDirectory(path.join(dataPath,"bin"))
    native.createDirectory(path.join(dataPath,"bin","hwconfig"))

# Clones base repo code into data directory
def cloneBaseCode(config):
    clonePath = path.join(config.dataPath, "code","rcos")
    print "Cloning remote base repository (" + config.remote.base + ") into ", clonePath
    native.gitClone(config.environment.git, config.remote.base,clonePath)

# Clones site repo code into sitePath
def cloneSite(config):
    clonePath = config.sitePath
    print "Cloning remote site repository (" + config.remote.site + ") into ", clonePath
    native.gitClone(config.environment.git, config.remote.site,clonePath)

# Symlink /var/www/hws to the site
def linkApache(config):
    native.elevatedRecreateSymlink(path.join(config.sitePath,"public"), path.join(config.environment.apachewww,"hws"))

if __name__ == "__main__":

    # Get command line arguments
    args = parseSetupArguments(
        defaultConfigPath=defaultConfigPath,
        defaultRemovePrevious=removePrevious)

    # Call setup to do the bulk of the work
    runSetup(args.configPath, args.removePrevious)
