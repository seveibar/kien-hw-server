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

    print setup.exceptions

    # Check for previous directories
    if path.exists(config.dataPath):
        raise setup.exceptions.DataDirectoryExists()
    if path.exists(config.sitePath):
        raise setup.exceptions.SiteDirectoryExists()

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

if __name__ == "__main__":

    # Get command line arguments
    args = parseSetupArguments(
        defaultConfigPath=defaultConfigPath,
        defaultRemovePrevious=removePrevious)

    # Call setup to do the bulk of the work
    runSetup(args.configPath, args.removePrevious)
