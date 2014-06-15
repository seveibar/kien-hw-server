#!/usr/bin/python

import argparse

# Parses command line arguments for Setup and returns a Namespace with the
# variables the user passed
def parseSetupArguments(defaultConfigPath=None,defaultRemovePrevious=None):

    parser = argparse.ArgumentParser(description='Perform setup operations for Kien Homework Server')

    # --config argument
    parser.add_argument(
        "--config", "-c",
        action="store",
        type=str,
        dest="configPath",
        help="Path to the setup \"config.json\" file. If left blank, this will default to the config.json with the directory \"setup.py\" is currently in.",
        default=defaultConfigPath)

    # --remove-previous argument
    parser.add_argument(
        "--remove-previous", "-f",
        dest="removePrevious",
        action="store_const",
        help="Remove previous data and site directories if they exist.",
        const=True
        )

    # --clean argument
    parser.add_argument(
        "--clean", "-l",
        dest="clean",
        action="store_const",
        help="Remove any directories that were created as a result of a previous setup operation",
        const=True,
        default=False
        )

    # Parse command line arguments
    return parser.parse_args()
