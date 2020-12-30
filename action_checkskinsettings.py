
from os.path import join
from xml.sax import ContentHandler, parseString

from action import Action
import kodi_baselibrary as kodi


class SkinSetting():
    def __init__(self):
        self.name = ""
        self.unit = None
        self.reads = []
        self.changes = []
        self.type = None


class SkinSettingContentHandler(ContentHandler):

    def __init__(self, unit):
        self.unit = unit
        self.skinsettings = []
        self.messages = []


    def startElement(self, tag, attributes):
        pass
        
#        if tag == kodi.VARIABLE_ELEMENT:
#            name = attributes['name']
#
#            if name:
#                variable = Variable()
#                variable.name = name
#                variable.unit = self.unit
#                self.definitions.append(variable)
#            else:
#                self.messages.append("Nameless variable definition in unit '" + self.unit + "'")
#        else:
#            for key, value in attributes.items():
#                self.parseforvariablereference(value)


    def characters(self, content):
        pass
        
#        self.parseforvariablereference(content)


#    def parseforvariablereference(self, content):
#        index = content.find(kodi.VARIABLE_IDENTIFIER)
#        while index >= 0:
#            start = index + len(kodi.VARIABLE_IDENTIFIER)
#            end = self.findendofreference(content, start)
#            parts = content[start + 1:end - 1].split(sep = ',')
#            name = parts[0]
#
#            if name:
#                variable = Variable()
#                variable.name = name.strip()
#                variable.unit = self.unit
#                self.references.append(variable)
#            else:
#                self.messages.append("Nameless variable reference in unit '" + self.unit + "'")
#
#            index = content.find(kodi.VARIABLE_IDENTIFIER, end)


#    def findendofreference(self, content, start):
#        index = start
#        count = 0
#        
#        while (index == start or count > 0) and index < len(content):
#            count = count + (1 if content[index] == '[' else 0)
#            count = count - (1 if content[index] == ']' else 0)
#            index += 1
#
#        return index


class CheckSkinSettingsAction(Action):

    def __init__(self):
        super().__init__(
            name = "Check skin settings", 
            function = self.checkskinsettings, 
            description = "Check the skin settings for:\n" + 
                    "- *WIP* unused skin settings (changes to skin settings that are never read)\n" + 
                    "- *WIP* unmodified skin settings (reads of skin settings that are never changed)",
            arguments = ['skin'])


    def checkskinsettings(self, messagecallback, arguments):
        messagecallback("action", "\nChecking skin settings...")
        skin = arguments['skin']

        for resolution in skin.resolutions:
            messagecallback("info", "- Skin resolution: " + resolution.aspect + " (" + resolution.directory + ")")
            self.resetskinsettings()
            self.parseskinsettings(resolution, messagecallback)
            self.analyzeskinsettings(resolution, messagecallback)


    def resetskinsettings(self):
        self.skinsettings = []
        

    def parseskinsettings(self, resolution, messagecallback):
        for unit in resolution.units:
            contenthandler = SkinSettingContentHandler(unit)
            parseString("".join(unit.lines), contenthandler)
            
            self.skinsettings.extend(contenthandler.skinsettings)
            messages = contenthandler.messages

            for message in messages:
                messagecallback("warning", "- File " + unit.name + ": " + message)

        messagecallback("info", "- Number of skin settings: " + str(len(self.skinsettings)))


    def analyzeskinsettings(self, resolution, messagecallback):
        pass

#        self.findduplicatevariables(resolution, messagecallback)
#        self.findunusedvariables(resolution, messagecallback)
#        self.findmissingvariables(resolution, messagecallback)


#    def findduplicatevariables(self, resolution, messagecallback):
#        for startindex, definition in enumerate(self.definitions):
#            for index in range(startindex + 1, len(self.definitions)):
#                if (definition.name == self.definitions[index].name):
#                    messagecallback("warning", "- Duplicate variable: " + definition.name + " (" + definition.unit.name + " ~ " + self.definitions[index].unit.name + ")")


#    def findunusedvariables(self, resolution, messagecallback):
#        referencednames = set([ reference.name for reference in self.references ])
#        
#        for definition in self.definitions:
#            if definition.name not in referencednames:
#                messagecallback("message", "- Unused variable: " + definition.name + " (" + definition.unit.name + ")")
    

#    def findmissingvariables(self, resolution, messagecallback):
#        declarednames = set([ definition.name for definition in self.definitions ])
#        
#        for reference in self.references:
#            if reference.name not in declarednames:
#                messagecallback("warning", "- Reference to non-existing (missing) variable: " + reference.name + " (" + reference.unit.name + ")")

