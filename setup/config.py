#!/usr/bin/python

import json
from os import path

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

    # Name of course
    courseName = "default-course"

    def __init__(self, configPath):
        print "Loading config: ", configPath

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
        except e:
            raise [Exception("Error parsing config file"),e]

        # Config parsed and loaded successfully into self.content

        # Extract the configuration values we need
        self.sitePath = self.content.get("sitePath",self.sitePath)
        self.dataPath = self.content.get("dataPath",self.dataPath)
        self.courseName = self.content.get("courseName",self.courseName)
