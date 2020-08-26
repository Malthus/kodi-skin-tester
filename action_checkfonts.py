
from os.path import join
from xml.sax import ContentHandler, parseString

from action import Action
from action_checkincludes import IncludeContentHandler
import kodi_baselibrary as kodi


class Fontset():
    def __init__(self):
        self.name = ""
        self.fonts = []
        self.fontnames = set()
        self.unit = ""
        self.paramcount = 0
        self.varcount = 0


class Font():
    def __init__(self):
        self.name = ""
        self.filename = ""


class Reference():
    def __init__(self):
        self.name = ""
        self.unit = ""


class FontContentHandler(ContentHandler):

    def __init__(self, unit):
        self.unit = unit
        self.fontsets = []
        self.references = []
        self.paramcount = 0
        self.varcount = 0
        self.messages = []

        self.lastfontset = None
        self.lastfont = None
        self.insidefont = False
        self.insidename = False
        self.insidefilename = False


    def startElement(self, tag, attributes):
        if tag == kodi.FONTSET_ELEMENT:
            fontset = Fontset()
            fontset.name = attributes['id']
            fontset.unit = self.unit
            self.fontsets.append(fontset)
            self.lastfontset = fontset
        elif tag == kodi.FONT_ELEMENT:
            if self.lastfontset:
                font = Font()
                self.lastfontset.fonts.append(font)
                self.lastfont = font
            else:
                self.insidefont = True
        elif tag == kodi.NAME_ELEMENT:
            self.insidename = True
        elif tag == kodi.FILENAME_ELEMENT:
            self.insidefilename = True


    def endElement(self, tag):
        if tag == kodi.FONTSET_ELEMENT:
            self.lastfontset = None
        elif tag == kodi.FONT_ELEMENT:
            self.lastfont = None
            self.insidefont = False

        self.insidename = False
        self.insidefilename = False


    def characters(self, content):
        if self.lastfont and self.insidename:
            self.lastfont.name = content
            self.lastfontset.fontnames.add(content)
        elif self.lastfont and self.insidefilename:
            self.lastfont.filename = content
        elif self.insidefont:
            if content.startswith(kodi.PARAMETER_IDENTIFIER):
                self.paramcount = self.paramcount + 1
            elif content.startswith(kodi.VARIABLE_IDENTIFIER):
                self.varcount = self.varcount + 1
            else:
                reference = Reference()
                reference.name = content
                reference.unit = self.unit
                self.references.append(reference)


class CheckFontsAction(Action):

    def __init__(self):
        super().__init__(
            name = "Check fonts", 
            function = self.checkfonts, 
            description = "*WIP*\nCheck fontsets and font files for:\n" + 
                    "- unused fonts (font definitions that are never used);\n" + 
                    "- missing fonts (font references that do not exist as a font definition);\n" +
                    "- different fontsets (differences in font definitions between fontsets);\n" +
                    "- missing font files (font files that cannot be found);\n" +
                    "- unused font files (font files in the font-directory that are never used).",
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
        self.references = []
        self.paramcount = 0
        self.varcount = 0
        

    def parsefonts(self, resolution, messagecallback):
        for unit in resolution.units:
            contenthandler = FontContentHandler(unit)
            parseString("".join(unit.lines), contenthandler)
            
            self.fontsets.extend(contenthandler.fontsets)
            self.references.extend(contenthandler.references)
            self.paramcount = self.paramcount + contenthandler.paramcount
            self.varcount = self.varcount + contenthandler.varcount
            messages = contenthandler.messages
            
            for message in messages:
                messagecallback("warning", "- File " + unit.name + ": " + message)

        messagecallback("info", "- Number of fontsets: " + str(len(self.fontsets)))
        messagecallback("info", "- Number of fixed (checkable) font references: " + str(len(self.references)))
        messagecallback("info", "- Number of parameterized font references: " + str(self.paramcount + self.varcount) + " ($PARAM = " + str(self.paramcount) + ", $VAR = " + str(self.varcount) + ")")


    def analyzefonts(self, resolution, messagecallback):
        self.findunusedfonts(resolution, messagecallback)
        self.findmissingfonts(resolution, messagecallback)
        self.findfontsetdifferences(resolution, messagecallback)
        # Find missing files
        # Find unused files


    def findunusedfonts(self, resolution, messagecallback):
        fontreferences = set([ reference.name for reference in self.references ])
        for fontset in self.fontsets:
            for font in fontset.fonts:
                if font.name not in fontreferences:
                    messagecallback("message", "- Possible unused font in fontset '" + fontset.name + "': " + font.name)


    def findmissingfonts(self, resolution, messagecallback):
        fontdefinitions = set([])
        for fontset in self.fontsets:
            fontdefinitions.update([ font.name for font in fontset.fonts ])

        for reference in self.references:
            if reference.name not in fontdefinitions:
                messagecallback("warning", "- Missing font reference in unit " + reference.unit.name + ": " + reference.name)


    def findfontsetdifferences(self, resolution, messagecallback):
        for startindex, fontset in enumerate(self.fontsets):
            fontnames = fontset.fontnames
            for index in range(startindex + 1, len(self.fontsets)):
                differences = fontnames - self.fontsets[index].fontnames
                if len(differences) > 0:
                    messagecallback("warning", "- Fonts in fontset '" + fontset.name + "' missing in '" + self.fontsets[index].name + "': " + ", ".join(differences))
                differences = self.fontsets[index].fontnames - fontnames
                if len(differences) > 0:
                    messagecallback("warning", "- Fonts in fontset '" + self.fontsets[index].name + "' missing in '" + fontset.name + "': " + ", ".join(differences))
    

