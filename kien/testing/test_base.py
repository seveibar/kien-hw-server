#!/usr/bin/python

import setup.config
import methods as test

import os
import os.path as path
import subprocess
import shutil

import pytest

def systemCall(args):
    return subprocess.check_output(args, shell=True)


# Accepts path nodes as arguments, returns true if path exists on filesystem
def pathExists(*args):
    return path.exists(path.join(*args))

# This fixture is for modifying or working with the data/assignments directory
@pytest.fixture(scope="module")
def assignmentFixture(request):

    config = setup.config.Config()

    def cleanup():
        # Delete and recreate assignments directory
        pathToAssignments = path.join(config.dataPath, "assignments")
        shutil.rmtree(pathToAssignments)
        os.mkdir(pathToAssignments)

    request.addfinalizer(cleanup)

def test_createTemplatedAssignment(assignmentFixture):
    config = setup.config.Config()

    # Path to the command "create_new_assignment"
    pathToCreateAssignmentExe = path.join(config.basePath,
                                          "bin",
                                          "create_new_assignment")

    # Call "create_new_assignment" to create an assignment template
    systemCall(pathToCreateAssignmentExe + " test")

    # Get path to the assignments directory
    assignmentsPath = path.join(config.dataPath, "assignments")

    assert pathExists(assignmentsPath, "test")
    assert pathExists(assignmentsPath, "test", "assignment.json")
    assert pathExists(assignmentsPath, "test", "instructor")
    assert pathExists(assignmentsPath, "test", "instructor", "core")


def test_createTestAssignment():
    raise Exception("NOT IMPLEMENTED: createTestAssignment")


def test_gradeAssignments():
    raise Exception("NOT IMPLEMENTED: gradeAssignments")
