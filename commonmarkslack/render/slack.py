#!/usr/bin/env python3
# encoding: utf-8


import re
from builtins import str
from commonmark.render.renderer import Renderer


reUnsafeProtocol = re.compile(
    r'^javascript:|vbscript:|file:|data:', re.IGNORECASE)
reSafeDataProtocol = re.compile(
    r'^data:image\/(?:png|gif|jpeg|webp)', re.IGNORECASE)

XMLSPECIAL = '[&<>]'
reXmlSpecial = re.compile(XMLSPECIAL)

UNSAFE_MAP = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;'
}


def potentially_unsafe(url):
    return re.match(reUnsafeProtocol, url) and \
        (not re.match(reSafeDataProtocol, url))


def replace_unsafe_char(s):
    return UNSAFE_MAP.get(s, s)


def escape_xml(s):
    if s is None:
        return ''
    if re.search(reXmlSpecial, s):
        return re.sub(
            reXmlSpecial,
            lambda m: replace_unsafe_char(m.group()),
            s)
    else:
        return s


class SlackRenderer(Renderer):
    def __init__(self, options={}):
        #  by default, soft breaks are rendered as newlines in HTML
        options['softbreak'] = options.get('softbreak') or '\n'
        # set to "<br />" to make them hard breaks
        # set to " " if you want to ignore line wrapping in source

        self.disable_tags = 0
        self.last_out = '\n'
        self.options = options

    def escape(self, text, preserve_entities):
        return escape_xml(text)

    # Node methods #

    def text(self, node, entering=None):
        if node.literal == 'x-nl-x':
            self.out('\n')
        else:
            self.out(node.literal)

    def softbreak(self, node=None, entering=None):
        self.lit(self.options['softbreak'])

    def linebreak(self, node=None, entering=None):
        self.cr()

    def link(self, node, entering):
        attrs = self.attrs(node)
        if entering:
            self.buf += '<' + self.escape(node.destination, True) + '|'
        else:
            self.buf += '>'

    def image(self, node, entering):
        return

    def emph(self, node, entering):
        if entering:
            self.buf += '_'
        else:
            self.buf += '_'

    def strong(self, node, entering):
        if entering:
            self.buf += '*'
        else:
            self.buf += '*'

    def paragraph(self, node, entering):
        grandparent = node.parent.parent
        attrs = self.attrs(node)
        if grandparent is not None and grandparent.t == 'list':
            if grandparent.list_data['tight']:
                return

        self.cr()

    def heading(self, node, entering):
        return

    def code(self, node, entering):
        self.buf += '`'
        self.out(node.literal)
        self.buf += '`'

    def code_block(self, node, entering):
        return

    def thematic_break(self, node, entering):
        return

    def block_quote(self, node, entering):
        return

    def list(self, node, entering):
        tagname = 'ul' if node.list_data['type'] == 'bullet' else 'ol'
        attrs = self.attrs(node)
        if entering:
            start = node.list_data['start']
            if start is not None and start != 1:
                attrs.append(['start', str(start)])

            self.cr()
            self.cr()
        else:
            self.cr()
            self.cr()

    def item(self, node, entering):
        if entering:
            self.buf += '• '
        else:
            self.cr()

    def html_inline(self, node, entering):
        return

    def html_block(self, node, entering):
        return

    def custom_inline(self, node, entering):
        return

    def custom_block(self, node, entering):
        return

    # Helper methods #

    def out(self, s):
        self.lit(self.escape(s, False))

    def attrs(self, node):
        att = []
        if self.options.get('sourcepos'):
            pos = node.sourcepos
            if pos:
                att.append(['data-sourcepos', str(pos[0][0]) + ':' +
                            str(pos[0][1]) + '-' + str(pos[1][0]) + ':' +
                            str(pos[1][1])])

        return att
