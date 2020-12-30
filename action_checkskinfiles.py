
from os import listdir
from os.path import isfile, join
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


class CheckSkinFilesAction(Action):

    def __init__(self):
        super().__init__(
            name = "Check skin files", 
            function = self.checkfiles, 
            description = "Check skin files (base files and XML files) for:\n" + 
                    "- missing icon, fanart, screenshots (missing declared assets)\n" +
                    "- missing license file\n" +
                    "- *WIP* missing XML files (required files that are not present)\n" +
                    "- *WIP* unknown XML files (files that are not default, included, or custom files)",
            arguments = ['skin'])


    def checkfiles(self, messagecallback, arguments):
        messagecallback("action", "\nChecking skin files...")
        skin = arguments['skin']

        self.checkassetfiles(skin, messagecallback)
        self.checklicensefile(skin, messagecallback)

        for resolution in skin.resolutions:
            messagecallback("info", "- Skin resolution: " + resolution.aspect + " (" + resolution.directory + ")")
            self.resetxmlfiles()
            self.parsexmlfiles(resolution, messagecallback)
            self.analyzexmlfiles(resolution, messagecallback)


    def checkassetfiles(self, skin, messagecallback):
        baseskindirectory = skin.basedirectory

        messagecallback("info", "- Number of asset files (icon, fanart, screenshots): " + str(len(skin.assets)))
        for asset in skin.assets:
            file = join(baseskindirectory, asset.file)

            if not isfile(file):
                messagecallback("warning", "- " + asset.file + ": Missing assert file of type '" + asset.type + "' (which is declared in " + kodi.ADDON_FILENAME + ")")


    def checklicensefile(self, skin, messagecallback):
        baseskindirectory = skin.basedirectory
        file = join(baseskindirectory, "LICENSE.txt")
        
        if not isfile(file):
            messagecallback("warning", "- LICENSE.txt: Missing license file (which is mandatory according to the Kodi add-on rules)")


    def resetxmlfiles(self):
        self.includefiles = []


    def parsexmlfiles(self, resolution, messagecallback):
        for unit in resolution.units:
            contenthandler = IncludeFileContentHandler(unit)
            parseString("".join(unit.lines), contenthandler)
            
            self.includefiles.extend(contenthandler.includefiles)
            messages = contenthandler.messages

            for message in messages:
                messagecallback("warning", "- " + unit.name + ": " + message)

        messagecallback("info", "- Number of include files: " + str(len(self.includefiles)))


    def analyzexmlfiles(self, resolution, messagecallback):
        files = [ file for file in listdir(resolution.path) ]
        messagecallback("info", "- Number of files in this directory: " + str(len(files)))

        for file in files:
            referencedfile = (file in kodi.XML_FILES
                    or file in self.includefiles
                    or (len(file) > 6 and file.startswith(("Custom", "custom")) and file.endswith(".xml"))
                    or (len(file) > 6 and file.startswith(("Script", "script")) and file.endswith(".xml")))
            
            if not referencedfile: 
                messagecallback("warning", "- " + file + ": This file is not a default XML-file, a custom file or a script file, and it is not included")

        for xmlfile in kodi.XML_FILES:
            if xmlfile not in files:
                messagecallback("warning", "- " + xmlfile + ": This required XML-file is missing")
            
