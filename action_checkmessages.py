
from os.path import join
from xml.sax import ContentHandler, parseString

from action import Action
import kodi_baselibrary as kodi


class MessageContentHandler(ContentHandler):

    def __init__(self, unit):
        self.unit = unit
        self.messagecodes = []
        self.messages = []
        self.insidelabelelement = False


    def startElement(self, tag, attributes):
        if tag == kodi.LABEL_ELEMENT:
            self.insidelabelelement = True
        if tag == kodi.PARAM_ELEMENT:
            self.parseparam(attributes)


    def endElement(self, tag):
        self.insidelabelelement = False


    def characters(self, content):
        if self.insidelabelelement and content.isdigit():
            self.messagecodes.append(int(content))
        else:
            self.parsemessagelabel(content)


    def parsemessagelabel(self, content):
        self.parselocalize(content)


    def parseparam(self, attributes):
        if 'value' in attributes:
            self.parselocalize(attributes['value'])


    def parselocalize(self, content):
        index = content.find(kodi.LOCALIZE_IDENTIFIER)
        while index >= 0:
            start = index + len(kodi.LOCALIZE_IDENTIFIER)
            end = self.findendoflocalize(content, start)
            messagecode = content[start + 1:end - 1]
            if messagecode.isdigit():
                self.messagecodes.append(int(messagecode))
            else:
                self.messages.append("Unexpected (not strictly numeric) message key '" + messagecode + "' in content '" + content + "'")
            index = content.find(kodi.LOCALIZE_IDENTIFIER, end)
    

    def findendoflocalize(self, content, start):
        index = start
        count = 0
        
        while (index == start or count > 0) and index < len(content):
            count = count + (1 if content[index] == '[' else 0)
            count = count - (1 if content[index] == ']' else 0)
            index += 1

        return index


class CheckMessagesAction(Action):

    def __init__(self):
        super().__init__(
            name = "Check language files and messages", 
            function = self.checkmessages, 
            description = "Check messages for localization errors, and check language files for unused or duplicate  entries",
            arguments = ['skin', 'sharedlanguage'])


    def checkmessages(self, messagecallback, arguments):
        messagecallback("action", "\nChecking messages...")
        skin = arguments['skin']
        sharedlanguage = arguments['sharedlanguage']
        
        for resolution in skin.resolutions:
            messagecallback("info", "- Skin resolution: " + resolution.aspect + " (" + resolution.directory + ")")
            self.resetmessages()
            self.parsemessages(messagecallback, resolution)
            self.analyzemessages(messagecallback, sharedlanguage, skin, resolution)


    def resetmessages(self):
        self.messagecodes = []
        

    def parsemessages(self, messagecallback, resolution):
        for unit in resolution.units:
            contenthandler = MessageContentHandler(unit)
            parseString("".join(unit.lines), contenthandler)

            self.messagecodes.extend(contenthandler.messagecodes)
            messages = contenthandler.messages
            
            for message in messages:
                messagecallback("warning", "- File " + unit.name + ": " + message)

        messagecallback("info", "- Number of referenced messages: " + str(len(self.messagecodes)))


    def analyzemessages(self, messagecallback, sharedlanguage, skin, resolution):
        messagekeyset = set(self.messagecodes)
        
        for messagekey in sorted(messagekeyset):
            if messagekey >= kodi.LOCALIZE_FIRSTSKINKEY and messagekey < kodi.LOCALIZE_LASTSKINKEY:
                if messagekey not in skin.language.strings:
                    messagecallback("warning", "- Undefined (skin) message key '" + str(messagekey) + "'")
            elif sharedlanguage:
                if messagekey not in sharedlanguage.strings:
                    messagecallback("warning", "- Undefined (shared) message key '" + str(messagekey) + "'")

        for languagekey in skin.language.strings:
            if languagekey not in self.messagecodes:
                messagecallback("message", "- Unused language entry '" + str(languagekey) + "' (" + skin.language.strings[languagekey] + ")")
       
        if sharedlanguage:
            sharedlanguagevalues = set([languagevalue for languagekey, languagevalue in sharedlanguage.strings.items()])
            for languagekey, languagevalue in skin.language.strings.items():
                if languagevalue in sharedlanguagevalues:
                    messagecallback("message", "- Shared language file entry duplication '" + str(languagekey) + "' (" + skin.language.strings[languagekey] + ")")
                
        languagevalues = set([languagevalue for languagekey, languagevalue in skin.language.strings.items()])                
        for languagekey, languagevalue in skin.language.strings.items():
            if languagevalue in languagevalues:
                languagevalues.remove(languagevalue)
            else:
                messagecallback("message", "- Language file entry duplication '" + str(languagekey) + "' (" + skin.language.strings[languagekey] + ")")
        
    

