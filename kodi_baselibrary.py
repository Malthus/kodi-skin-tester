# Kodi Skin Base Library


from os.path import join


ADDON_FILENAME = "addon.xml"
LANGUAGE_FILENAME = "strings.po"
LANGUAGE_DIRECTORY = "language/resource.language.en_gb"

ADDON_PATH = "/addon"
RESOLUTION_PATH = "/addon/extension/res"

ADDON_ELEMENT = "addon"
RESOLUTION_ELEMENT = "res"
INCLUDE_ELEMENT = "include"
PARAM_ELEMENT = "param"
NESTED_ELEMENT = "nested"
INFOLABEL_ELEMENT = "info"
LABEL_ELEMENT = "label"
VARIABLE_ELEMENT = "variable"
EXPRESSION_ELEMENT = "expression"
TEXTURE_ELEMENT = "texture"
TEXTUREFOCUS_ELEMENT = "texturefocus"
TEXTURENOFOCUS_ELEMENT = "texturenofocus"
TEXTURESLIDERBACKGROUND_ELEMENT = "texturesliderbackground"
TEXTURESLIDERBAR_ELEMENT = "texturesliderbar"
TEXTURESLIDERBARFOCUS_ELEMENT = "texturesliderbarfocus"
ALTTEXTUREFOCUS_ELEMENT = "alttexturefocus"
ALTTEXTURENOFOCUS_ELEMENT = "alttexturenofocus"
MIDTEXTURE_ELEMENT = "midtexture"
FONTS_ELEMENT = "fonts"
FONTSET_ELEMENT = "fontset"
FONT_ELEMENT = "font"
NAME_ELEMENT = "name"
FILENAME_ELEMENT = "filename"
ASSETS_ELEMENT = "assets"
IMPORT_ELEMENT = "import"
VIEWTYPE_ELEMENT = "viewtype"

TEXTURE_ELEMENTS = [TEXTURE_ELEMENT, TEXTUREFOCUS_ELEMENT, TEXTURENOFOCUS_ELEMENT, TEXTURESLIDERBACKGROUND_ELEMENT, TEXTURESLIDERBAR_ELEMENT, TEXTURESLIDERBARFOCUS_ELEMENT, 
        ALTTEXTUREFOCUS_ELEMENT, ALTTEXTURENOFOCUS_ELEMENT, MIDTEXTURE_ELEMENT]

COMMA_IDENTIFIER = "$COMMA"
INFOLABEL_IDENTIFIER = "$INFO"
ESCAPEDINFOLABEL_IDENTIFIER = "$ESCINFO"
LOCALIZE_IDENTIFIER = "$LOCALIZE"
PARAMETER_IDENTIFIER = "$PARAM"
VARIABLE_IDENTIFIER = "$VAR"
ESCAPEDVARIABLE_IDENTIFIER = "$ESCVAR"
EXPRESSION_IDENTIFIER = "$EXP"
NUMBER_IDENTIFIER = "$NUMBER"
ADDON_IDENTIFIER = "$ADDON"

PARAMETERIZED_IDENTIFIERS = [INFOLABEL_IDENTIFIER, ESCAPEDINFOLABEL_IDENTIFIER, LOCALIZE_IDENTIFIER, PARAMETER_IDENTIFIER, VARIABLE_IDENTIFIER, ESCAPEDVARIABLE_IDENTIFIER, 
        EXPRESSION_IDENTIFIER, NUMBER_IDENTIFIER, ADDON_IDENTIFIER]

LOCALIZE_FIRSTSKINKEY = 31000
LOCALIZE_LASTSKINKEY = 32000


class Skin():
    def __init__(self, skinbasedirectory, skinlanguagedirectory):
        self.name = ""
        self.id = ""
        self.version = ""
        self.path = ""
        self.resolutions = []
        self.basedirectory = skinbasedirectory
        self.language = None
        self.skinlanguagedirectory = skinlanguagedirectory
        self.xbmcguiversion = ""
        self.kodiversion = 0
        self.kodiname = ""
        self.addons = []
        self.assets = []


class Language():
    def __init__(self):
        self.strings = {}
        self.languagefile = ""


class Resolution():
    def __init__(self):
        self.aspect = ""
        self.width = ""
        self.height = ""
        self.defaultresolution = False
        self.directory = ""
        self.path = ""

        self.skin = None
        self.units = []

        self.includedefs = []
        self.includerefs = []


class FontSet():
    def __init__(self):
        self.id = "";
        self.names = []
        self.font = False
        self.fontname = False


class Addon():
    def __init__(self):
        self.name = ""
        self.version = ""
        self.optional = False


class Unit():
    def __init__(self, name, file, lines):
        self.name = name
        self.file = file
        self.resolution = None
        self.lines = lines


class Asset():
    def __init__(self, type, file):
        self.type = type
        self.file = file


def getkodiversion(guiversion):
    kodiversion = 0
        
    if guiversion == '4.0.0':
        kodiversion = 12
    elif guiversion == '5.0.1':
        kodiversion = 13
    elif guiversion == '5.3.0':
        kodiversion = 14
    elif guiversion == '5.9.0':
        kodiversion = 15
    elif guiversion == '5.9.0':
        kodiversion = 15
    elif guiversion == '5.10.0':
        kodiversion = 16
    elif guiversion == '5.12.0':
        kodiversion = 17
    elif guiversion == '5.14.0':
        kodiversion = 18
    elif guiversion == '5.15.0':
        kodiversion = 19

    return kodiversion


def getkodiname(guiversion):
    kodiname = ''
        
    if guiversion == '4.0.0':
        kodiname = 'XBMC Frodo'
    elif guiversion == '5.0.1':
        kodiname = 'XBMC Gotham'
    elif guiversion == '5.3.0':
        kodiname = 'Kodi Helix'
    elif guiversion == '5.9.0':
        kodiname = 'Kodi Isengard'
    elif guiversion == '5.9.0':
        kodiname = 'Kodi Isengard'
    elif guiversion == '5.10.0':
        kodiname = 'Kodi Jarvis'
    elif guiversion == '5.12.0':
        kodiname = 'Kodi Krypton'
    elif guiversion == '5.14.0':
        kodiname = 'Kodi Leia'
    elif guiversion == '5.15.0':
        kodiname = 'Kodi Matrix'

    return kodiname


def readlanguagefile(languagefile):
    language = Language()
    language.languagefile = languagefile
    key = -1

    with open(languagefile, 'r') as file_handle:
        for line in file_handle.readlines():
            if line.startswith('msgctxt'):
                startindex = line.index('"#') + 2
                endindex = line.rindex('"')
                key = int(line[startindex:endindex])
            elif line.startswith('msgid'):
                startindex = line.index('"') + 1
                endindex = line.rindex('"')
                value = line[startindex:endindex]
                
                if key >= 0 and value is not None:
                    language.strings[key] = value
                    key = -1
                    value = None

    return language

