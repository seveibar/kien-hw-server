#!/usr/bin/python

import json
from os import path
from setup.native import getSetupPath

# This class holds configuration details for setting up a homework server
# environment
class Config:

    # Stores parsed json file (should not be used externally)
    content = None

    # PUBLIC VARIABLES

    # Path to clone the site repo into, can be relative to setup script
    sitePath = "site"

    # Path for the data directory
    dataPath = "data"

    # Path for the base directory
    basePath = "base"

    # Path to kian directory (with examples, setup, testing etc.)
    kienPath = "./"

    # Path to temporary directory
    tmpPath = "/tmp"

    # Name of course
    courseName = "default-course"

    # Environment details (where git is installed etc.)
    environment = None

    # Remote repository details (base and site repo urls )
    remote = None

    def __init__(self, configPath=None):

        if configPath is None:
            configPath = path.join(getSetupPath(), "config.json")

        print "Loading config: ", configPath

        # config.json file is always contained with kian directory
        self.kienPath = path.dirname(configPath)

        # Attempt to load config file
        raw_json = None
        if path.isfile(configPath):
            try:
                raw_json = open(configPath).read()
            except:
                raise Exception("Error reading config file")
        else:
            raise Exception("Config file does not exist")

        # Config loaded

        # Attempt to parse config file
        try:
            self.content = json.loads(raw_json)
        except:
            print "ERROR: Couldn't parse config file"
            raise

        # Config parsed and loaded successfully into self.content

        # Extract the configuration values we need
        self.sitePath = getOrDie(self.content, "sitePath")
        self.basePath = getOrDie(self.content, "basePath")
        self.tmpPath = getOrDie(self.content, "tmpPath")
        self.dataPath = getOrDie(self.content, "dataPath")
        self.courseName = getOrDie(self.content, "courseName")
        self.environment = EnvironmentConfig(
            getOrDie(self.content, "environment.git"),
            getOrDie(self.content, "environment.apachewww"))
        self.remote = RemoteConfig(
            getOrDie(self.content, "remote.site"),
            getOrDie(self.content, "remote.base")
        )

        # Fix paths, they should all be relative to config path unless absolute
        if not path.isabs(self.sitePath):
            self.sitePath = path.normpath(path.join(self.kienPath, self.sitePath))
        if not path.isabs(self.basePath):
            self.basePath = path.normpath(path.join(self.kienPath, self.basePath))
        if not path.isabs(self.tmpPath):
            self.tmpPath = path.normpath(path.join(self.kienPath, self.tmpPath))
        if not path.isabs(self.dataPath):
            self.dataPath = path.normpath(path.join(self.kienPath, self.dataPath))


# Object for storing remote configuration
class RemoteConfig:
    site = None
    base = None
    def __init__(self,site,base):
        self.site = site
        self.base = base

# Object for storing environment configuration
class EnvironmentConfig:
    git = None
    apachewww = None
    def __init__(self,git,apachewww):
        self.git = git
        self.apachewww = apachewww


class ClassConfig:

    # Stores raw json for class config file
    content = None

    # List of string assignment names
    assignments = None

    # The default assignment when the page is loaded (usually the last assignment)
    defaultAssignment = None

    # Name of the course
    courseName = None

    def __init__(self, classConfigPath):
        print "Loading class config: ", classConfigPath

        # Attempt to load config file
        raw_json = None
        if path.isfile(classConfigPath):
            try:
                raw_json = open(classConfigPath).read()
            except:
                raise Exception("Error reading class config file")
        else:
            raise Exception("Class config file does not exist")

        # Config loaded

        # Attempt to parse config file
        try:
            self.content = json.loads(raw_json)
        except e:
            raise [Exception("Error parsing config file"),e]

        # Config parsed and loaded successfully into self.content

        # Extract the configuration values we need
        self.assignments = getOrDie(self.content, "assignments")
        self.defaultAssignment = getOrDie(self.content, "default_assignment")
        self.courseName = getOrDie(self.content, "course_name")


        return path.normpath(path.join(setup_directory, ".."))


# UTILITY FUNCTION
# Get property from JSON object or die
# This function also excepts nested properties e.g. remote.base
def getOrDie(data, key):
    objects = key.split(".")
    if len(objects) == 1:
        # If key exists return it, otherwise throw exception
        if key in data:
            return data[key]
        else:
            raise Exception("Config file is missing field: \"" + key + "\"")
    else:
        # Nested property
        # If key exists, recursively call getOrDie until we're down to a
        # single key, otherwise throw exception
        if objects[0] in data:
            return getOrDie(data[objects[0]],".".join(objects[1:]))
        else:
            raise Exception("Config file is missing field: \"" + key + "\"")
