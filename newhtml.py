# -*- coding: utf-8 -*-

import codecs

from yattag import Doc
from yattag import indent


class HtmlCreator:
    def __init__(self, file, data=None):
        # Create header, body and write the whole content to html file.
        self.filestream = file
        self.data = data
        self.initDocTagText()

    def initDocTagText(self):
        """
        Create main yattag variables.
        This method can be overridden.
        """
        self.doc, self.tag, self.text = Doc().tagtext()

    def create_html(self):
        """
        Create a html file from header and body content.
        Next, write html content to the hard drive.
        This method cannot be overridden.
        """
        # Add html content to the self.doc
        self.doc.asis('<!DOCTYPE html>')
        with self.tag('html'):
            self.design_header()
            self.design_body()
        # Write html content from self.doc
        with codecs.open(self.filestream.name, 'w', 'utf-8') as f:
            html_content = indent(
                self.doc.getvalue(),
                indentation='  ',
                newline='\r\n'
            )
            f.write(html_content)

    def design_header(self):
        """
        Create a header for your html file here.
        This method should be overridden.
        """
        pass

    def design_body(self):
        """
        Create a body for your html file here.
        This method should be overridden.
        """
        pass
