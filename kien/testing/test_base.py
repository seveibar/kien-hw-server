#!/usr/bin/python

import setup.config
import methods as test

import os.path as path
import subprocess


def systemCall(args):
    return subprocess.check_output(args, shell=True)


def test_createTemplatedAssignment():
    config = setup.config.Config()

    pathToCreateAssignmentExe = path.join(config.basePath,
                                          "create_new_assignment")

    systemCall([pathToCreateAssignmentExe, "test"])

    # raise Exception("NOT IMPLEMENTED: createTemplatedAssignment")


def test_createTestAssignment():
    raise Exception("NOT IMPLEMENTED: createTestAssignment")


def test_gradeAssignments():
    raise Exception("NOT IMPLEMENTED: gradeAssignments")
