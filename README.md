# CommonMark-Slack

CommonMark-Slack extends the [commonmark.py](https://github.com/readthedocs/commonmark.py) library to add rendering of the 
[Slack](https://slack.com/) flavor of Markdown. This can be handy if you are already using [standard Markdown](https://commonmark.org/) 
for another purpose and would like to also produce Slack output from the same source. CommonMark-slack also allows for producing 
plaintext from standard Markdown, useful for the areas of Slack that use unadorned text.

## Installation

You can install CommonMark-Slack from [PyPI](https://pypi.org/project/commonmark-slack/):

    pip install commonmark-slack

The commonmark-slack package is supported by Python 3.6 and above.

## Usage

```
import commonmarkslack
parser = commonmarkslack.Parser()
ast = parser.parse("Hello *World*")

renderer = commonmark.SlackRenderer()
slack_md = renderer.render(ast)
print(slack_md) # Hello _World_

renderer = commonmarkslack.PlainTextRenderer()
plain_text = renderer.render(ast)
print(plain_text) # Hello World
```
