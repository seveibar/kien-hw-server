#!/usr/bin/python

# Script for performing all setup operations
# This will take care of cloning and setting up the site with a default course

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
    configureSite(config)

    # Symlink /var/www/hws to the site
    if config.environment.apachewww != "":
        linkApache(config)

    # Setup course
    createClassFile(config)

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
#           | -> hwconfig
#     | -> coursedata
#           | -> results
#     | -> submissions
def createDataDirectory(dataPath):
    native.createDirectory(dataPath)
    native.createDirectory(path.join(dataPath,"code"))
    native.createDirectory(path.join(dataPath,"bin"))
    native.createDirectory(path.join(dataPath,"bin","hwconfig"))
    native.createDirectory(path.join(dataPath, "submissions"))
    native.createDirectory(path.join(dataPath, "coursedata"))
    native.createDirectory(path.join(dataPath, "coursedata", "results"))

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

#
def configureSite(config):
    print "Configuring site"

    siteConfigPath = path.join(config.sitePath, "config.json")

    print "Modifiying ",siteConfigPath

    try:
        # Read default site configuration
        fi = open(siteConfigPath,'r')
        siteConfigContents = fi.read()
        fi.close()
    except:
        raise Exception("Error reading site config file")

    try:
        # Parse site config
        siteConfig = json.loads(siteConfigContents)

        # Change data path to config
        siteConfig["course_data_path"] = path.abspath(config.dataPath)

    except:
        raise Exception("Could not parse site config file")

    try:
        # Overwrite old site config
        fi = open(siteConfigPath, 'w')
        json.dump(siteConfig, fi,indent=4)
        fi.close()

    except:
        raise Exception("Error writing to site config file")

# Creates class.json file inside course data directory by loading the default
# class.json file and changing the "course_name" field to match the config
def createClassFile(config):
    print "Creating class file"

    defaultClassFilePath = path.join("examples","defaults","class.json")
    destClassFilePath = path.join(config.dataPath,"coursedata","class.json")

    print "Parsing ",defaultClassFilePath, " and writing to ", destClassFilePath

    try:
        # Read default class file
        fi = open(defaultClassFilePath,'r')
        exampleClassContents = fi.read()
        fi.close()

    except:
        raise Exception("Error reading example class file")

    try:
        # Parse example class file
        classfile = json.loads(exampleClassContents)

        # Change values specific to this config
        classfile["course_name"] = config.courseName

    except:
        raise Exception("Could not parse example class file")

    try:
        # Output new class file into course data directory
        fi = open(destClassFilePath, 'w')
        json.dump(classfile, fi,indent=4)
        fi.close()

    except:
        raise Exception("Error writing to course data class file")

# Symlink /var/www/hws to the site
def linkApache(config):
    # This is the path to the public directory that students access
    publicPath = path.abspath(path.join(config.sitePath,"public"))

    print "Creating symlink from /var/www/hws to ", publicPath

    native.elevatedRecreateSymlink(publicPath, path.join(config.environment.apachewww,"hws"))

if __name__ == "__main__":

    # Get command line arguments
    args = parseSetupArguments(
        defaultConfigPath=defaultConfigPath,
        defaultRemovePrevious=removePrevious)

    # Call setup to do the bulk of the work
    runSetup(args.configPath, args.removePrevious)
