
from os.path import join
from xml.sax import ContentHandler, parseString

from action import Action
import kodi_baselibrary as kodi


class Variable():
    def __init__(self):
        self.name = ""
        self.unit = None


class VariableContentHandler(ContentHandler):

    def __init__(self, unit):
        self.unit = unit
        self.definitions = []
        self.references = []
        self.messages = []


    def startElement(self, tag, attributes):
        if tag == kodi.VARIABLE_ELEMENT:
            name = attributes['name']
            
            if name:
                variable = Variable()
                variable.name = name
                variable.unit = self.unit
                self.definitions.append(variable)
            else:
                self.messages.append("Nameless variable definition in unit '" + self.unit + "'")
        else:
            for key, value in attributes.items():
                self.parseforvariablereference(value)


    def characters(self, content):
        self.parseforvariablereference(content)


    def parseforvariablereference(self, content):
        index = content.find(kodi.VARIABLE_IDENTIFIER)
        while index >= 0:
            start = index + len(kodi.VARIABLE_IDENTIFIER)
            end = self.findendofreference(content, start)
            parts = content[start + 1:end - 1].split(sep = ',')
            name = parts[0]

            if name:
                variable = Variable()
                variable.name = name.strip()
                variable.unit = self.unit
                self.references.append(variable)
            else:
                self.messages.append("Nameless variable reference in unit '" + self.unit + "'")

            index = content.find(kodi.VARIABLE_IDENTIFIER, end)


    def findendofreference(self, content, start):
        index = start
        count = 0
        
        while (index == start or count > 0) and index < len(content):
            count = count + (1 if content[index] == '[' else 0)
            count = count - (1 if content[index] == ']' else 0)
            index += 1

        return index


class CheckVariablesAction(Action):

    def __init__(self):
        super().__init__(
            name = "Check variables", 
            function = self.checkvariables, 
            description = "Check variables, both the definitions and the references for:\n" + 
                    "- duplicate variables (variable definitions with the same name);\n" + 
                    "- unused variables (variable definitions that are never used);\n" + 
                    "- missing variables (variable references that do not exist as a variable definition).",
            arguments = ['skin'])


    def checkvariables(self, messagecallback, arguments):
        messagecallback("action", "\nChecking variable definitions and references...")
        skin = arguments['skin']

        for resolution in skin.resolutions:
            messagecallback("info", "- Skin resolution: " + resolution.aspect + " (" + resolution.directory + ")")
            self.resetvariables()
            self.parsevariables(resolution, messagecallback)
            self.analyzevariables(resolution, messagecallback)


    def resetvariables(self):
        self.definitions = []
        self.references = []
        

    def parsevariables(self, resolution, messagecallback):
        for unit in resolution.units:
            contenthandler = VariableContentHandler(unit)
            parseString("".join(unit.lines), contenthandler)
            
            self.definitions.extend(contenthandler.definitions)
            self.references.extend(contenthandler.references)
            messages = contenthandler.messages

            for message in messages:
                messagecallback("warning", "- File " + unit.name + ": " + message)

        messagecallback("info", "- Number of variables: " + str(len(self.definitions)))
        messagecallback("info", "- Number of references: " + str(len(self.references)))


    def analyzevariables(self, resolution, messagecallback):
        self.findduplicatevariables(resolution, messagecallback)
        self.findunusedvariables(resolution, messagecallback)
        self.findmissingvariables(resolution, messagecallback)


    def findduplicatevariables(self, resolution, messagecallback):
        for startindex, definition in enumerate(self.definitions):
            for index in range(startindex + 1, len(self.definitions)):
                if (definition.name == self.definitions[index].name):
                    messagecallback("warning", "- Duplicate variable: " + definition.name + " (" + definition.unit.name + " ~ " + self.definitions[index].unit.name + ")")


    def findunusedvariables(self, resolution, messagecallback):
        referencednames = set([ reference.name for reference in self.references ])
        
        for definition in self.definitions:
            if definition.name not in referencednames:
                messagecallback("message", "- Unused variable: " + definition.name + " (" + definition.unit.name + ")")
    

    def findmissingvariables(self, resolution, messagecallback):
        declarednames = set([ definition.name for definition in self.definitions ])
        
        for reference in self.references:
            if reference.name not in declarednames:
                messagecallback("warning", "- Reference to non-existing (missing) variable: " + reference.name + " (" + reference.unit.name + ")")

