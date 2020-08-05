
from os.path import join
from xml.sax import ContentHandler, parseString

from action import Action
import kodi_baselibrary as kodi


DEFINITION_TYPE = 'DEFINITION'
REFERENCE_TYPE = 'REFERENCE'
FILE_TYPE = 'FILE'


class Include():
    def __init__(self):
        self.name = ""
        self.type = ""
        self.parameters = {}
        self.unit = None
        self.includes = []


class IncludeContentHandler(ContentHandler):

    def __init__(self, unit):
        self.unit = unit
        self.definitions = []
        self.references = []
        self.messages = []

        self.lastinclude = None


    def startElement(self, tag, attributes):
        if tag == kodi.INCLUDE_ELEMENT:
            includetype = self.determineincludetype(attributes)
            if includetype == DEFINITION_TYPE:
                self.parsedefinition(attributes)
            elif includetype == REFERENCE_TYPE:
                self.parsereference(attributes)
        elif tag == kodi.PARAM_ELEMENT:
            self.parseparam(attributes)
        else:
            if self.lastinclude and self.lastinclude.type == DEFINITION_TYPE:
                self.definitions.append(self.lastinclude)
            if self.lastinclude and self.lastinclude.type == REFERENCE_TYPE:
                self.messages.append("Unexpected new start-tag in include '" + self.lastinclude.name + "'")
            
            self.resetdefinition()


    def endElement(self, tag):
        if self.lastinclude and tag == kodi.INCLUDE_ELEMENT:
            if self.lastinclude.type == DEFINITION_TYPE:
                self.definitions.append(self.lastinclude)
            elif self.lastinclude.type == REFERENCE_TYPE:
                self.references.append(self.lastinclude)
            else:
                self.messages.append("Failed to determine the type of include '" + self.lastinclude.name + "'")
            self.lastinclude = None

    def characters(self, content):
        if self.lastinclude and self.lastinclude.type == REFERENCE_TYPE and self.lastinclude.name == "-":
            self.lastinclude.name = content


    def parsedefinition(self, attributes):
        self.lastinclude = Include()
        self.lastinclude.name = attributes['name']
        self.lastinclude.type = DEFINITION_TYPE
        self.lastinclude.unit = self.unit
        
        
    def parsereference(self, attributes):
        self.lastinclude = Include()
        self.lastinclude.name = attributes['content'] if 'content' in attributes else "-"
        self.lastinclude.type = REFERENCE_TYPE
        self.lastinclude.unit = self.unit


    def parseparam(self, attributes):
        if self.lastinclude is not None:
            if 'value' in attributes and self.lastinclude.type != DEFINITION_TYPE and self.lastinclude.type != FILE_TYPE:
                self.lastinclude.parameters[attributes['name']] = attributes['value']
                self.lastinclude.type = REFERENCE_TYPE
            elif 'default' in attributes and self.lastinclude.type != REFERENCE_TYPE and self.lastinclude.type != FILE_TYPE:
                self.lastinclude.parameters[attributes['name']] = attributes['default']
                self.lastinclude.type = DEFINITION_TYPE
            elif 'name' in attributes:
                self.lastinclude.parameters[attributes['name']] = None


    def resetdefinition(self):
        self.lastinclude = None


    def determineincludetype(self, attributes):
        type = REFERENCE_TYPE
    
        if "content" in attributes:
            type = REFERENCE_TYPE
        elif "name" in attributes:
            type = DEFINITION_TYPE
        elif "file" in attributes:
            type = FILE_TYPE

        return type


class CheckIncludesAction(Action):

    def __init__(self):
        super().__init__(
            name = "Check includes", 
            function = self.checkincludes, 
            description = "Check includes, both the definitions and the references for:\n" + 
                    "- duplicate includes (include definitions with the same name);\n" + 
                    "- unused includes (include definitions that are never used);\n" + 
                    "- missing includes (include references that do not exist as an include definition);\n" + 
                    "- undeclared parameters (parameters in the reference that the include definition does not declare);\n" + 
                    "- unasigned parameters (parameters without default value and without a value in the reference).",
            arguments = ['skin'])


    def checkincludes(self, messagecallback, arguments):
        messagecallback("action", "\nChecking include definitions and references...")
        skin = arguments['skin']

        for resolution in skin.resolutions:
            messagecallback("info", "- Skin resolution: " + resolution.aspect + " (" + resolution.directory + ")")
            self.resetincludes()
            self.parseincludes(resolution, messagecallback)
            self.analyzeincludes(resolution, messagecallback)


    def resetincludes(self):
        self.definitions = []
        self.references = []
        

    def parseincludes(self, resolution, messagecallback):
        for unit in resolution.units:
            contenthandler = IncludeContentHandler(unit)
            parseString("".join(unit.lines), contenthandler)
            
            self.definitions.extend(contenthandler.definitions)
            self.references.extend(contenthandler.references)
            messages = contenthandler.messages

            for message in messages:
                messagecallback("warning", "- File " + unit.name + ": " + message)

        messagecallback("info", "- Number of includes: " + str(len(self.definitions)))
        messagecallback("info", "- Number of references: " + str(len(self.references)))


    def analyzeincludes(self, resolution, messagecallback):
        self.linkincludes(resolution, messagecallback)

        self.findduplicateincludes(resolution, messagecallback)
        self.findunusedincludes(resolution, messagecallback)
        self.findmissingincludes(resolution, messagecallback)
        self.findparametermismatches(resolution, messagecallback)


    def linkincludes(self, resolution, messagecallback):
        dictionary = { definition.name : definition for definition in self.definitions }

        for reference in self.references:
            definition = dictionary[reference.name]
            if definition:
                definition.includes.append(reference)
                reference.includes.append(definition)                

        
    def findduplicateincludes(self, resolution, messagecallback):
        for startindex, definition in enumerate(self.definitions):
            for index in range(startindex + 1, len(self.definitions)):
                if (definition.name == self.definitions[index].name):
                    messagecallback("warning", "- Duplicate include: " + definition.name + " (" + definition.unit.name + " ~ " + self.definitions[index].unit.name + ")")


    def findunusedincludes(self, resolution, messagecallback):
        unuseddefinitions = [ definition for definition in self.definitions if len(definition.includes) == 0 ]
        
        for definition in unuseddefinitions:
            messagecallback("message", "- Unused include: " + definition.name + " (" + definition.unit.name + ")")


    def findmissingincludes(self, resolution, messagecallback):
        missingdefinitions = [ reference for reference in self.references if len(reference.includes) == 0 ]
        
        for reference in missingdefinitions:
            messagecallback("warning", "- Reference to non-existing (missing) include: " + reference.name + " (" + reference.unit.name + ")")


    def findparametermismatches(self, resolution, messagecallback):
        for reference in self.references:
            definition = reference.includes[0] if len(reference.includes) > 0 else None
            if definition:
                definitionparams = sorted(definition.parameters.keys())
                referenceparams = sorted(reference.parameters.keys())
                definitionindex = 0
                referenceindex = 0

                while definitionindex < len(definitionparams) or referenceindex < len(referenceparams):
                    definitionparam = definitionparams[definitionindex] if definitionindex < len(definitionparams) else None
                    referenceparam = referenceparams[referenceindex] if referenceindex < len(referenceparams) else None
                
                    if (definitionparam is not None and referenceparam is None) or definitionparam < referenceparam:
                        if definition.parameters[definitionparam] is None:
                            messagecallback("warning", "- Missing (unassigned) parameter '" + definitionparam +"' without default value in reference: " + reference.name + " (" + reference.unit.name + ")")               
                        definitionindex = definitionindex + 1
                    elif (definitionparam is None and referenceparam is not None) or definitionparam > referenceparam:
                        messagecallback("message", "- Unknown (undeclared) parameter '" + referenceparam + "' in reference: " + reference.name + " (" + reference.unit.name + ")")               
                        referenceindex = referenceindex + 1
                    else:
                        definitionindex = definitionindex + 1
                        referenceindex = referenceindex + 1



