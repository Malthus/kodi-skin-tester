
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
        if tag == kodi.LABEL_ELEMENT or tag == kodi.LABEL2_ELEMENT or tag == kodi.ALTLABEL_ELEMENT:
            self.insidelabelelement = True
        elif tag == kodi.PARAM_ELEMENT and 'value' in attributes:
            self.parselocalize(attributes['value'])
        elif tag == kodi.VIEWTYPE_ELEMENT and 'label' in attributes:
            self.parsemessagelabel(attributes['label'])


    def endElement(self, tag):
        self.insidelabelelement = False


    def characters(self, content):
        if self.insidelabelelement and content.isdigit():
            self.messagecodes.append(int(content))
        else:
            self.parselocalize(content)


    def parsemessagelabel(self, content):
        if content.isdigit():
            self.messagecodes.append(int(content))
        else:
            self.parselocalize(content)


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
            description = "Check messages in skin-specific language file for:\n" + 
                    "- duplicate entries within the skin-specific language file (texts that appear multiple times in the skin-specific language file)\n" + 
                    "- duplicate entries with the standard language file (texts that appear in both the skin-specific and the standard language file)\n" + 
                    "- unused entries (texts with numbers that are never used)",
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
                messagecallback("warning", "- " + unit.name + ": " + message)

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
        
    

