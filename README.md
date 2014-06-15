# High Level Design of Kian Homework Server

The homework server consists of three central parts.

* [Base](base-overview) *(assignment handler)*:  Contains scripts that allow the instructor to create files and assignments to be run and graded.
* [Site](site-overview) *(student interface)*: The front-end website that students use to upload assignments and view their grades
* [Setup and Testing](setup-overview): This is a suite of scripts and files that allow easy installation and testing of the homework server.

## Application Flow
***********************

### Setup
***********************

The setup scripts provided in the [main repository](http://gitlab.seveibar.com/seve/kian-setup) set up a basic directory structure, this typically involves the creation of the [data directory](data-directory) and the cloning of both the [site](site-overview) and [base](base-overview) repos.

![setup-execution-high-overview](http://gitlab.seveibar.com/files/note/4/rpi-hw-overview.jpg)

See [custom assignment creation](custom-assignment-creation) for details on how to create a custom assignment.

### User Submission
***********************

Typically, files within the site will be invoked by a user submission to the **apache server** (not installed by the setup script). The [site](site-overview) will output the results of submissions into the [data submissions](data-submissions) directory.

![site high overview](http://gitlab.seveibar.com/files/note/5/site-high-overview.jpg)

### Submission Evaluation
***********************

This [data submissions](data-submissions) directory will periodically be parsed by an **evaluation** script. This evaluation script will remove and archive submissions from the [data submissions](data-submissions) directory and output the results of [submission validation](submission-validation) into the [data results](data-results) directory.

![high level evaluation script](http://gitlab.seveibar.com/files/note/6/high-level-evaluation-script.jpg)

### User Request
***********************

The [data results](data-results) directory is read by the [site](site-overview) when a user requests a page to give results of their submission.

*******************************
