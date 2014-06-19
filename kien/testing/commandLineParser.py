#!/usr/bin/python

import argparse

# Parses command line arguments for Setup and returns a Namespace with the
# variables the user passed
def parseTestArguments(defaultConfigPath):

    parser = argparse.ArgumentParser(description="""
Perform test operations for RPI Homework Server e.g.creating users, uploading assignments.
Actions:
    create_test_assignment
    create_user (deprecated)
    fake_upload
    run_test
    """)

    parser.add_argument(
        "--config","-c",
        action="store",
        type=str,
        dest="configPath",
        help="Path to the setup \"config.json\" file. If left blank, this will default to the config.json with the directory \"setup.py\" is currently in.",
        default=defaultConfigPath)

    parser.add_argument(
        "action",
        nargs="+",
        help="Action to take."
        )

    # Parse command line arguments
    return parser.parse_args()
