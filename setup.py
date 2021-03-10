"""Setup script for commonmark-slack"""

import os.path
from setuptools import find_packages, setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="commonmark-slack",
    python_requires='>3.6.0',
    version="1.0.0",
    description="Convert CommonMark Markdown to Slack Markdown",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/klm1/commonmarkslack",
    author="Ken Morse",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Utilities"
    ],
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[
        "commonmark"
    ]
)
