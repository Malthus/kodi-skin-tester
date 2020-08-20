
from os.path import join
from xml.sax import ContentHandler, parseString

from action import Action
import kodi_baselibrary as kodi


# fonts > fontset > font
class Fontset():
    def __init__(self):
        self.fontsets = []
        self.filename = ""


class FontContentHandler(ContentHandler):

    def __init__(self, unit):
        self.unit = unit
        self.infolabels = []
        self.messages = []

        self.insideinfolabelelement = False
        self.insidelabelelement = False


    def startElement(self, tag, attributes):
        if tag == kodi.INFOLABEL_ELEMENT:
            self.insideinfolabelelement = True
        elif tag == kodi.LABEL_ELEMENT:
            self.insidelabelelement = True

    def endElement(self, tag):
        self.insideinfolabelelement = False

    def characters(self, content):
        if self.insideinfolabelelement and content.isdigit():
            self.infolabels.append(content)
        elif self.insideinfolabelelement and not content.isdigit():
            self.messages.append("Unexpected (not strictly numeric) infolabel '" + content + "'")
        elif self.insidelabelelement and content.isdigit():
            self.infolabels.append(content)
        else:
            self.parselabel(content)
        

    def parselabel(self, content):
        index = content.find(kodi.INFOLABEL_IDENTIFIER)
        while index >= 0:
            start = index + len(kodi.INFOLABEL_IDENTIFIER)
            end = self.findendoflabel(content, start)
            infolabels = content[start:end].split(sep = ',')
            
            # Parse label
            self.messages.append(", ".join(infolabels))
        
            index = content.find(kodi.INFOLABEL_IDENTIFIER, end)


    def findendoflabel(self, content, start):
        index = start
        count = 0
        
        while (index == start or count > 0) and index < len(content):
            count = count + (1 if content[index] == '[' else 0)
            count = count - (1 if content[index] == ']' else 0)
            index += 1

        return index            
        


class CheckFontsAction(Action):

    def __init__(self):
        super().__init__(
            name = "Check fonts", 
            function = self.checkfonts, 
            description = "*WIP*\nCheck fontsets and font files for\n" + 
                    "- unused fonts (font definitions that are never used);\n" + 
                    "- missing fonts (font references that do not exist as a font definition).",
            arguments = ['skin'])


    def checkfonts(self, messagecallback, arguments):
        messagecallback("action", "\nChecking fonts...")
        skin = arguments['skin']

        for resolution in skin.resolutions:
            messagecallback("info", "- Skin resolution: " + resolution.aspect + " (" + resolution.directory + ")")
            self.resetfonts()
            self.parsefonts(resolution, messagecallback)
            self.analyzefonts(resolution, messagecallback)


    def resetfonts(self):
        self.fontsets = []
        

    def parsefonts(self, resolution, messagecallback):
#        for unit in resolution.units:
#            contenthandler = FontContentHandler(unit)
#            parseString("".join(unit.lines), contenthandler)
#            
#            self.infolabels.extend(contenthandler.infolabels)
#            messages = contenthandler.messages
#            
#            for message in messages:
#                messagecallback("warning", "- File " + unit.name + ": " + message)

        messagecallback("info", "- Number of fontsets: " + str(len(self.fontsets)))


    def analyzefonts(self, resolution, messagecallback):
        pass
    
        # Find unused fonts
        
        # Find missing files
        
        # Find unused files
        
        # Find differences between fontsets
        
    

