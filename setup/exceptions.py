#!/usr/bin/python

# Exceptions for use with setup script

class DataDirectoryExists(Exception):
    def __init__(self):
        Exception.__init__(self, "Data directory exists! Remove or run setup with --remove-previous (-f)")

class SiteDirectoryExists(Exception):
    def __init__(self):
        Exception.__init__(self, "Site directory exists! Remove or run setup with --remove-previous (-f)")
