
from os.path import join
from xml.sax import ContentHandler, parseString

from action import Action
import kodi_baselibrary as kodi


class SyntaxContentHandler(ContentHandler):

    def __init__(self, unit):
        self.unit = unit
        self.messages = []


    def startElement(self, tag, attributes):
        for key, value in attributes.items():
            if not self.checktokenbalance(value):
                self.messages.append("Token-imbalance in attribute '" + key + "' of tag '" + tag + "' in unit '" + self.unit.name + "'")
            if not self.checkdollarprefix(value):
                self.messages.append("Strange dollar-sign in attribute '" + key + "' of tag '" + tag + "' in unit '" + self.unit.name + "'")


    def characters(self, content):
        if not self.checktokenbalance(content):
            self.messages.append("Token-imbalance in content '" + content + "' in unit '" + self.unit.name + "'")
        if not self.checkdollarprefix(content):
            self.messages.append("Strange dollar-sign in content '" + content + "' in unit '" + self.unit.name + "'")


    def checktokenbalance(self, content):
        openlist = ["[","{","("]
        closelist = ["]","}",")"]
        stack = []

        for token in content:
            if token in openlist:
                stack.append(token)
            elif token in closelist: 
                index = closelist.index(token)
                if ((len(stack) > 0) and (openlist[index] == stack[len(stack) - 1])): 
                    stack.pop() 
                else: 
                    return False

        return len(stack) == 0

    def checkdollarprefix(self, content):
        startindex = content.find('$')
        
        while startindex >= 0:
            endindex = content.find('[', startindex)
            dollarprefix = content[startindex:endindex]

            if not dollarprefix.startswith(kodi.COMMA_IDENTIFIER) and (endindex < 0 or dollarprefix not in kodi.PARAMETERIZED_IDENTIFIERS):
                return False

            startindex = content.find('$', startindex + 1)

        return True
    

class CheckSyntaxAction(Action):

    def __init__(self):
        super().__init__(
            name = "Check syntax", 
            function = self.checkexpressions, 
            description = "*WIP*\nCheck several aspects of the syntax:\n" + 
                    "- imbalance in brackets, cury brackets, and parentheses;\n" + 
                    "- unrecognized content with dollar sign prefix (not $INFO/$LOCALIZE/$PARAM/$VAR/$EXP/$NUMBER/$COMMA/$ADDON).",
            arguments = ['skin'])


    def checkexpressions(self, messagecallback, arguments):
        messagecallback("action", "\nChecking syntax errors...")
        skin = arguments['skin']

        for resolution in skin.resolutions:
            messagecallback("info", "- Skin resolution: " + resolution.aspect + " (" + resolution.directory + ")")
            self.parsesyntax(resolution, messagecallback)


    def parsesyntax(self, resolution, messagecallback):
        for unit in resolution.units:
            contenthandler = SyntaxContentHandler(unit)
            parseString("".join(unit.lines), contenthandler)
            
            messages = contenthandler.messages

            for message in messages:
                messagecallback("warning", message)

