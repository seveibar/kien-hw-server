
import os.path as path
import argparse

import testing.methods as testMethods
import setup.native as native

import testing.baseTest as baseTest


# Parse command line arguments for test.py
def commandLineParser():

    # Use native module to get default path to the kien/config.json file
    defaultConfigPath = path.join(native.getSetupPath(), "config.json")

    parser = argparse.ArgumentParser(
        description="For running test methods and suites"
    )

    parser.add_argument(
        "--config", "-c",
        action="store",
        type=str,
        dest="configPath",
        help="""
            Path to the setup \"config.json\" file. If left blank, this
            will default to the config.json with the directory \"setup.py\" is
            currently in.
        """,
        default=defaultConfigPath)

    parser.add_argument(
        "action",
        nargs="+",
        help="Suite or method to execute"
        )

    # Parse command line arguments
    return parser.parse_args()


# If executed from command line, execute the suite or test method that is
# specified
if __name__ == "__main__":
    # Parse command line arguments
    args = commandLineParser()

    if args.action == "base":
        baseTest.runSuite()
    else:
        print "Suite not detected, attempting to execute as method..."
        # If the user did not enter a suite, they must have entered a
        # test method
        testMethods.cmdLineCall()
