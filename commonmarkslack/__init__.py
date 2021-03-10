#!/usr/bin/env python3
# # encoding: utf-8
"""
commonmarkext

Copyright © 2020-2021 Ken Morse. All rights reserved.

Extensions to commonmark-py

"""

import commonmark

from commonmarkslack.render.slack import SlackRenderer
from commonmarkslack.render.plaintext import PlainTextRenderer

# Version of CommonMark-Slack package
__version__ = "1.0.0"

def preserve_blank_lines(rawText):
    """
    Converts completely blanks lines to a string ("x-nl-x") to preveserve the 
    line when it goes through the parser processing -- otherwise the blank
    lines are lost.

    Returns text
    """

    preservedText = ""
    for line in rawText.splitlines():
        if line.isspace() or line == "":
            preservedText += '\n' + 'x-nl-x' + '\n\n'
        else:
            preservedText += line + '\n'

    return preservedText


class Parser(commonmark.Parser):
    def parse(self, my_input):
        preserved_input = preserve_blank_lines(my_input)
        return commonmark.Parser.parse(self, preserved_input)