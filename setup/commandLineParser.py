#!/usr/bin/python

import argparse

# Parses command line arguments for Setup and returns a Namespace with the
# variables the user passed
def parseSetupArguments(defaultConfigPath=None,defaultRemovePrevious=None):

    parser = argparse.ArgumentParser(description='Perform setup operations for RPI Homework Server')

    # --config argument
    parser.add_argument(
        "--config","-c",
        action="store",
        type=str,
        dest="configPath",
        help="Path to the setup \"config.json\" file. If left blank, this will default to the config.json with the directory \"setup.py\" is currently in.",
        default=defaultConfigPath)

    # --config argument
    parser.add_argument(
        "--remove-previous","-f",
        dest="removePrevious",
        help="Remove previous data and site directories if they exist.",
        default=defaultRemovePrevious)

    # Parse command line arguments
    return parser.parse_args()
