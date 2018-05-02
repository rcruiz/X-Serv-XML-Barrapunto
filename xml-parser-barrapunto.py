#!/usr/bin/python3


from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
from urllib import request


class myContentHandler(ContentHandler):

    def __init__(self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""
        self.line = ""

    def startElement(self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement(self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.line = self.theContent
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                escribe = '<p><a href="' + self.theContent + '">'
                # escribe += self.theContent.encode('utf-8')  + '">'
                escribe += self.line + '</a></p>'
                htmlFile.write(escribe)
                self.inContent = False
                self.theContent = ""

    def characters(self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

# --- Main prog
# Load parser and driver
theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!
url = "http://barrapunto.com/index.rss"
xml_dos = request.urlopen(url)
# xmlFile = open(sys.argv[1],"r")
htmlFile = open("barrapunto.html", "w")
htmlFile.write("<!DOCTYPE html><html><head><meta charset='utf-8'/></head><body>")

theParser.parse(xml_dos)
htmlFile.write('</body></html>')

print("Parse complete")
