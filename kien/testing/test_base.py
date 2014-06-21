#!/usr/bin/python

import setup.config
import methods as test

import pytest
import os
import os.path as path
import subprocess
import shutil
import json

def systemCall(args):
    return subprocess.check_output(args, shell=True)


# Accepts path nodes as arguments, returns true if path exists on filesystem
def pathExists(*args):
    return path.exists(path.join(*args))


# Check that the directory for an assignment was created correctly
def checkAssignmentCreation(assignmentsPath, assignmentName):
    assert pathExists(assignmentsPath, assignmentName)
    assert pathExists(assignmentsPath, assignmentName, "assignment.json")
    assert pathExists(assignmentsPath, assignmentName, "instructor")
    assert pathExists(assignmentsPath, assignmentName, "instructor", "core")


# Load json at the given path
def jsonAt(*jsonPath):
    # Make sure the json file exists
    assert pathExists(*jsonPath)

    # Open, read and parse json data
    fi = open(path.join(*jsonPath),'r')
    jsonContent = json.load(fi)
    fi.close()

    return jsonContent


# Check that the uploads.json file has exactly {uploadCount} submissions from
# the specified student
def checkUploadsFile(config, student, uploadCount):
    # Get the content of the uploads file
    uploads = jsonAt(config.dataPath, "submissions", "test", "uploads.json")

    # Filter the submissions (in uploads.submissions) down to those that
    # were uploaded by supplied student, then make sure there are exactly
    # {uploadCount} submissions
    assert uploadCount == len(filter(lambda sub: sub["student"] == student,
                                     uploads["submissions"]))


# Grades all submissions for the specified assignment
def gradeAssignment(config, testName):
    # Path to base/bin/grade_assignment
    pathToGradeAssignmentExe = path.join(config.basePath, "bin",
                                         "grade_assignment")

    # Grade all submissions
    systemCall(pathToGradeAssignmentExe + " " + testName)

# This fixture is for modifying or working with the data/assignments directory
@pytest.fixture(scope="function")
def assignmentFixture(request, config):

    def cleanup():
        # Delete and recreate assignments directory
        pathToAssignments = path.join(config.dataPath, "assignments")
        shutil.rmtree(pathToAssignments)
        os.mkdir(pathToAssignments)

    # Clean up the directory before and after
    cleanup()
    #request.addfinalizer(cleanup)

# This fixture is for modifying or working with the data/submissions directory
@pytest.fixture(scope="function")
def submissionFixture(request, config):

    def cleanup():
        # Delete and recreate assignments directory
        pathToSubmissions = path.join(config.dataPath, "submissions")
        shutil.rmtree(pathToSubmissions)
        os.mkdir(pathToSubmissions)

    # Clean up the directory before and after
    cleanup()
    #request.addfinalizer(cleanup)

# This fixture is for modifying or working with the data/results directory
@pytest.fixture(scope="function")
def resultsFixture(request, config):

    def cleanup():
        # Delete and recreate assignments directory
        pathToResults = path.join(config.dataPath, "results")
        shutil.rmtree(pathToResults)
        os.mkdir(pathToResults)

    # Clean up the directory before and after
    cleanup()
    #request.addfinalizer(cleanup)


# This fixture is for tests that will need the kien config
@pytest.fixture(scope="module")
def config():

    return setup.config.Config()


def test_createTemplatedAssignment(config, assignmentFixture):
    # Path to the command "create_new_assignment"
    pathToCreateAssignmentExe = path.join(config.basePath,
                                          "bin",
                                          "create_new_assignment")

    # Call "create_new_assignment" to create an assignment template
    systemCall(pathToCreateAssignmentExe + " test")

    # Get path to the assignments directory
    assignmentsPath = path.join(config.dataPath, "assignments")

    # Check that assignment directory was created properly
    checkAssignmentCreation(assignmentsPath, "test")


def test_createExampleAssignment(config, assignmentFixture):
    # Load example assignment
    test.createTestAssignment(config, ["test", "example001"])

    # Make sure example assignment was loaded correctly
    checkAssignmentCreation(path.join(config.dataPath, "assignments"), "test")

def test_fakeUploadSubmission(config, assignmentFixture, submissionFixture):
    # Load example assignment
    test.createTestAssignment(config, ["test", "example001"])

    # Make sure example assignment was loaded correctly
    checkAssignmentCreation(path.join(config.dataPath, "assignments"), "test")

    # Upload perfect test submission
    test.fakeUploadSubmission(config, ["test", "jdoe", "example001/perfect"])

    # Make sure the fake upload was successful
    assert pathExists(config.dataPath, "submissions", "test", "jdoe", "1")

    # Check content of uploads.json file (should be 1 submission from jdoe)
    checkUploadsFile(config, "jdoe", 1)

def test_testGrade1(config, assignmentFixture, submissionFixture,
                    resultsFixture):
    # Load example assignment
    test.createTestAssignment(config, ["test", "example001"])

    # Upload perfect test submission
    test.fakeUploadSubmission(config, ["test", "jdoe", "example001/perfect"])
    test.fakeUploadSubmission(config, ["test", "jdoe", "example001/noreadme"])

    # Grade all submissions
    gradeAssignment(config, "test")

    # Get submission grades
    perfectGrade = jsonAt(config.dataPath, "results", "test", "jdoe", "1",
                          "submission.json")
    noreadmeGrade = jsonAt(config.dataPath, "results", "test", "jdoe", "2",
                           "submission.json")

    # Make sure submission grades are correct
    assert perfectGrade["points_awarded"] == 10
    assert noreadmeGrade["points_awarded"] == 8
