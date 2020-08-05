
from os.path import join
from xml.sax import ContentHandler, parseString

from action import Action
import kodi_baselibrary as kodi


class IncludeFileContentHandler(ContentHandler):

    def __init__(self, unit):
        self.unit = unit
        self.includefiles = []
        self.messages = []


    def startElement(self, tag, attributes):
        if tag == kodi.INCLUDE_ELEMENT:
            if 'file' in attributes:
                self.includefiles.append(attributes['file'])



class CheckXmlFilesAction(Action):

    def __init__(self):
        super().__init__(
            name = "Check files", 
            function = self.checkfiles, 
            description = "Check default skin files and include files",
            arguments = ['skin'])


    def checkfiles(self, messagecallback, arguments):
        messagecallback("action", "\nChecking default skin files and include files...")
        skin = arguments['skin']

        for resolution in skin.resolutions:
            messagecallback("info", "- Skin resolution: " + resolution.aspect + " (" + resolution.directory + ")")
            self.resetfiles()
            self.parsefiles(resolution, messagecallback)
            self.analyzefiles(resolution, messagecallback)


    def resetfiles(self):
        self.includefiles = []
        

    def parsefiles(self, resolution, messagecallback):
        for unit in resolution.units:
            contenthandler = IncludeFileContentHandler(unit)
            parseString("".join(unit.lines), contenthandler)
            
            self.includefiles.extend(contenthandler.includefiles)
            messages = contenthandler.messages

            for message in messages:
                messagecallback("warning", "- File " + unit.name + ": " + message)

        messagecallback("info", "- Number of include files: " + str(len(self.includefiles)))


    def analyzefiles(self, resolution, messagecallback):
    
        # Check xml-header
        
        # Check default files present
        
        # Check unused XML files
    
        pass


