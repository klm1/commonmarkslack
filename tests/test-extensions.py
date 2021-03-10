#!/usr/bin/env python3
# encoding: utf-8
"""
test-commonmarkslack.py

Copyright © 2021 Ken Morse. All rights reserved.

"""

import os
import sys

import unittest

sys.path.append('../commonmarkslack')
import commonmarkslack

simple_markdown = """A very **bold** first line.

Just a *simple* test message."""
simple_expected_plaintext = """A very bold first line.

Just a simple test message.
"""
simple_expected_slack_markdown = """A very *bold* first line.

Just a _simple_ test message.
"""

bullet_markdown = """Here's a simple list:

* Item 1
* **Item 2**
* *Item 3*

Back to normal."""
bullet_expected_plaintext = """Here's a simple list:

* Item 1
* Item 2
* Item 3

Back to normal.
"""
bullet_expected_slack_markdown = """Here's a simple list:

• Item 1
• *Item 2*
• _Item 3_

Back to normal.
"""


class TestSendToSlack(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_plaintext_from_simple_markdown(self):
        parser = commonmarkslack.Parser()
        ast = parser.parse(simple_markdown)
        renderer = commonmarkslack.PlainTextRenderer()
        text = renderer.render(ast)
        
        self.assertEqual(text, simple_expected_plaintext)

    def test_plaintext_from_bullet_markdown(self):
        parser = commonmarkslack.Parser()
        ast = parser.parse(bullet_markdown)
        renderer = commonmarkslack.PlainTextRenderer()
        text = renderer.render(ast)
                
        self.assertEqual(text, bullet_expected_plaintext)

    def test_slack_markdown_from_simple_markdown(self):
        parser = commonmarkslack.Parser()
        ast = parser.parse(simple_markdown)
        renderer = commonmarkslack.SlackRenderer()
        slack_md = renderer.render(ast)

        self.assertEqual(slack_md, simple_expected_slack_markdown)

    def test_slack_markdown_from_bullet_markdown(self):
        parser = commonmarkslack.Parser()
        ast = parser.parse(bullet_markdown)
        renderer = commonmarkslack.SlackRenderer()
        slack_md = renderer.render(ast)
        
        self.assertEqual(slack_md, bullet_expected_slack_markdown)


if __name__ == '__main__':
    if sys.version_info.major < 3:
        sys.exit("Must be using Python 3+")

    unittest.main(verbosity=2)