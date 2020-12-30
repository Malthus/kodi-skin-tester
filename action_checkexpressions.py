
from os.path import join
from xml.sax import ContentHandler, parseString

from action import Action
import kodi_baselibrary as kodi


class Expression():
    def __init__(self):
        self.name = ""
        self.unit = None


class ExpressionContentHandler(ContentHandler):

    def __init__(self, unit):
        self.unit = unit
        self.definitions = []
        self.references = []
        self.messages = []


    def startElement(self, tag, attributes):
        if tag == kodi.EXPRESSION_ELEMENT:
            name = attributes['name']
            
            if name:
                expression = Expression()
                expression.name = name
                expression.unit = self.unit
                self.definitions.append(expression)
            else:
                self.messages.append("Nameless expression definition in unit '" + self.unit + "'")
        else:
            for key, value in attributes.items():
                self.parseforexpressionreference(value)


    def characters(self, content):
        self.parseforexpressionreference(content)


    def parseforexpressionreference(self, content):
        index = content.find(kodi.EXPRESSION_IDENTIFIER)
        while index >= 0:
            start = index + len(kodi.EXPRESSION_IDENTIFIER)
            end = self.findendofreference(content, start)
            parts = content[start + 1:end - 1].split(sep = ',')
            name = parts[0]

            if name:
                expression = Expression()
                expression.name = name.strip()
                expression.unit = self.unit
                self.references.append(expression)
            else:
                self.messages.append("Nameless expression reference in unit '" + self.unit + "'")

            index = content.find(kodi.EXPRESSION_IDENTIFIER, end)


    def findendofreference(self, content, start):
        index = start
        count = 0

        while (index == start or count > 0) and index < len(content):
            count = count + (1 if content[index] == '[' else 0)
            count = count - (1 if content[index] == ']' else 0)
            index += 1

        return index


class CheckExpressionsAction(Action):

    def __init__(self):
        super().__init__(
            name = "Check expressions", 
            function = self.checkexpressions, 
            description = "Check expressions, both the definitions and the references for:\n" + 
                    "- *WIP* duplicate expressions (expression definitions with the same name)\n" + 
                    "- *WIP* unused expressions (expression definitions that are never used)\n" + 
                    "- *WIP* missing expressions (expression references that do not exist as an expression definition)",
            arguments = ['skin'])


    def checkexpressions(self, messagecallback, arguments):
        messagecallback("action", "\nChecking variable definitions and references...")
        skin = arguments['skin']

        for resolution in skin.resolutions:
            messagecallback("info", "- Skin resolution: " + resolution.aspect + " (" + resolution.directory + ")")
            self.resetexpressions()
            self.parseexpressions(resolution, messagecallback)
            self.analyzeexpressions(resolution, messagecallback)


    def resetexpressions(self):
        self.definitions = []
        self.references = []
        

    def parseexpressions(self, resolution, messagecallback):
        for unit in resolution.units:
            contenthandler = ExpressionContentHandler(unit)
            parseString("".join(unit.lines), contenthandler)
            
            self.definitions.extend(contenthandler.definitions)
            self.references.extend(contenthandler.references)
            messages = contenthandler.messages

            for message in messages:
                messagecallback("warning", "- " + unit.name + ": " + message)

        messagecallback("info", "- Number of expressions: " + str(len(self.definitions)))
        messagecallback("info", "- Number of references: " + str(len(self.references)))


    def analyzeexpressions(self, resolution, messagecallback):
        self.findduplicateexpressions(resolution, messagecallback)
        self.findunusedexpressions(resolution, messagecallback)
        self.findmissingexpressions(resolution, messagecallback)


    def findduplicateexpressions(self, resolution, messagecallback):
        for startindex, definition in enumerate(self.definitions):
            for index in range(startindex + 1, len(self.definitions)):
                if (definition.name == self.definitions[index].name):
                    messagecallback("warning", "- Duplicate expression: " + definition.name + " (" + definition.unit.name + " ~ " + self.definitions[index].unit.name + ")")


    def findunusedexpressions(self, resolution, messagecallback):
        referencednames = set([ reference.name for reference in self.references ])
        
        for definition in self.definitions:
            if definition.name not in referencednames:
                messagecallback("message", "- " + definition.unit.name + ": Unused expression: " + definition.name)
    

    def findmissingexpressions(self, resolution, messagecallback):
        declarednames = set([ definition.name for definition in self.definitions ])
        
        for reference in self.references:
            if reference.name not in declarednames:
                messagecallback("warning", "- " + reference.unit.name + ": Reference to non-existing (missing) expression: " + reference.name)

