import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="logging_pp",
    version="0.0.1",
    author="Bob Bonham",
    author_email="bob_bonham@yahoo.com",
    description="logging_pp, extension to python logging package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rocketbobb/logging_pp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

import os, stat, shutil
#from subprocess import call
import venv
import pip
import platform

isWindows = platform.system() == "Windows"

def shell(command):
    return call(command.split(' '))

def runPython(command):
    if isWindows:
        shell('env/scripts/python ' + command)
    else:
        shell('env/bin/python ' + command)

#venv.create("env", with_pip=True)
#runPython('-m pip install -r requirements.txt')
