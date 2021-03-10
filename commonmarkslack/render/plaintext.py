#!/usr/bin/env python3
# encoding: utf-8


import re
from builtins import str
from commonmark.common import escape_xml
from commonmark.render.renderer import Renderer


reUnsafeProtocol = re.compile(
    r'^javascript:|vbscript:|file:|data:', re.IGNORECASE)
reSafeDataProtocol = re.compile(
    r'^data:image\/(?:png|gif|jpeg|webp)', re.IGNORECASE)


def potentially_unsafe(url):
    return re.match(reUnsafeProtocol, url) and \
        (not re.match(reSafeDataProtocol, url))


class PlainTextRenderer(Renderer):
    def __init__(self, options={}):
        #  by default, soft breaks are rendered as newlines in HTML
        options['softbreak'] = options.get('softbreak') or '\n'
        # set to "<br />" to make them hard breaks
        # set to " " if you want to ignore line wrapping in source

        self.disable_tags = 0
        self.last_out = '\n'
        self.options = options

    def escape(self, text, preserve_entities):
        return escape_xml(text, preserve_entities)

    # Node methods #

    def text(self, node, entering=None):
        if node.parent.t != 'link':
            if node.literal == 'x-nl-x':
                self.out('\n')
            else:
                self.out(node.literal)

    def softbreak(self, node=None, entering=None):
        self.lit(self.options['softbreak'])

    def linebreak(self, node=None, entering=None):
        self.cr()

    def link(self, node, entering):
        #print 'node.t: "%s", node.destination: "%s"' % (node.t, node.destination)
        if entering:
            self.buf += node.destination

    def image(self, node, entering):
        return

    def emph(self, node, entering):
        return

    def strong(self, node, entering):
        return

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
        return

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
            self.buf += '* '
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
        self.lit(s)

    def attrs(self, node):
        att = []
        if self.options.get('sourcepos'):
            pos = node.sourcepos
            if pos:
                att.append(['data-sourcepos', str(pos[0][0]) + ':' +
                            str(pos[0][1]) + '-' + str(pos[1][0]) + ':' +
                            str(pos[1][1])])

        return att
