# Kodi Skin Base Library


from os.path import join


ADDON_FILENAME = "addon.xml"
LANGUAGE_FILENAME = "strings.po"
LANGUAGE_DIRECTORY = "language/resource.language.en_gb"

ADDON_PATH = "/addon"
RESOLUTION_PATH = "/addon/extension/res"

ADDON_ELEMENT = "addon"
RESOLUTION_ELEMENT = "res"
ASSETS_ELEMENT = "assets"
IMPORT_ELEMENT = "import"
ICON_ELEMENT = "icon"
FANART_ELEMENT = "fanart"
SCREENSHOT_ELEMENT = "screenshot"

INCLUDE_ELEMENT = "include"
PARAM_ELEMENT = "param"
NESTED_ELEMENT = "nested"

VARIABLE_ELEMENT = "variable"
EXPRESSION_ELEMENT = "expression"
CONSTANT_ELEMENT = "constant"

LABEL_ELEMENT = "label"
LABEL2_ELEMENT = "label2"
ALTLABEL_ELEMENT = "altlabel"
VIEWTYPE_ELEMENT = "viewtype"

FONTSET_ELEMENT = "fontset"
FONT_ELEMENT = "font"
NAME_ELEMENT = "name"
FILENAME_ELEMENT = "filename"

#INCLUDES_ELEMENT = "includes"
#THUMB_ELEMENT = "thumb"
#DEFINITION_ELEMENT = "definition"
#WINDOW_ELEMENT = "window"
#COORDINATES_ELEMENT = "coordinates"
#SYSTEM_ELEMENT = "system"
#DESCRIPTION_ELEMENT = "description"
#PROPERTY_ELEMENT = "property"
#CONTROLS_ELEMENT = "controls"
#CONTROL_ELEMENT = "control"
#DEFAULTCONTROL_ELEMENT = "defaultcontrol"
#MENUCONTROL_ELEMENT = "menucontrol"
#VIEWS_ELEMENT = "views"
#DEFAULT_ELEMENT = "default"
#INFOLABEL_ELEMENT = "info"
#VALUE_ELEMENT = "value"
#VISIBLE_ELEMENT = "visible"
#ENABLE_ELEMENT = "enable"
#ZORDER_ELEMENT = "zorder"
#POSX_ELEMENT = "posx"
#POSY_ELEMENT = "posy"
#TOP_ELEMENT  = "top"
#LEFT_ELEMENT = "left"
#WIDTH_ELEMENT = "width"
#HEIGHT_ELEMENT = "height"
#INFO_ELEMENT = "info"


STRUCTURE_ELEMENTS = ["window", "coordinates", "system", "description", "controls", "control", 
        "defaultcontrol", "menucontrol", "variable", "value", "expression", "constant", "property", "icon", "thumb", "viewtype", "views", "default"]
INCLUDE_ELEMENTS = ["includes", "include", "definition", "param", "nested"]
POSITION_ELEMENTS = ["zorder", "posx", "posy", "top", "left"]
DIMENSION_ELEMENTS = ["width", "height"]

CONTROL_ELEMENTS = ["textcolor", "focusedcolor", "disabledcolor", "selectedcolor", "pulseonselect", "selected", "usealttexture", "textoffsetx"]
LABEL_ELEMENTS = ["label", "label2", "altlabel", "info", "align", "aligny", "scroll", "scrollspeed", "scrollsuffix", "wrapmultiline", "angle"]
TEXTURE_ELEMENTS = ["texture", "texturefocus", "texturenofocus", "alttexturefocus", "alttexturenofocus", "aspectratio", "colordiffuse"]
PROGRESS_ELEMENTS = ["midtexture", "lefttexture", "righttexture", "overlaytexture", "texturebg"]
SCROLL_SLIDER_ELEMENTS = ["sliderwidth", "sliderheight", "texturesliderbar", "textureslidernib", "textureslidernibfocus", 
        "texturesliderbackground", "texturesliderbarfocus", "showonepage", "orientation", "action"]
RADIOBUTTON_ELEMENTS = ["radiowidth", "radioheight", "radioposx", "textureradioonfocus", "textureradioofffocus", "textureradioonnofocus", "textureradiooffnofocus", 
        "textureradioondisabled", "textureradiooffdisabled"]
SPINCONTROL_ELEMENTS = ["spinwidth", "spinheight", "textureup", "texturedown", "textureupfocus", "texturedownfocus", "textureupdisabled", "texturedowndisabled", "reverse"]
IMAGE_ELEMENTS = ["timeperimage", "randomize", "imagepath", "loop"]
CONTAINER_ELEMENTS = ["focusposition", "pagecontrol", "itemgap", "autoscroll", "itemlayout", "focusedlayout", "content", "item", "scrolltime", "showonepage", 
        "usecontrolcoords", "preloaditems"]
EPG_ELEMENTS = ["progresstexture", "timeblocks", "rulerunit", "rulerlayout", "channellayout", "focusedchannellayout"]

FONT_ELEMENTS = ["fonts", "fontset", "font", "name", "filename", "size", "style", "linespacing"]
RSSFEED_ELEMENTS = ["titlecolor", "headlinecolor", "urlset"]
DISPLAY_ELEMENTS = ["fadetime", "animation", "effect", "videofilter", "stretchmode", "rotation"]
BEHAVIOUR_ELEMENTS = ["visible", "enable"]
EVENT_ELEMENTS = ["onfocus", "onclick", "onup", "ondown", "onleft", "onright", "onback", "onload", "onunload", "altclick"]

XML_ELEMENTS = (STRUCTURE_ELEMENTS + INCLUDE_ELEMENTS + POSITION_ELEMENTS + DIMENSION_ELEMENTS 
        + LABEL_ELEMENTS + TEXTURE_ELEMENTS + IMAGE_ELEMENTS + CONTAINER_ELEMENTS + EPG_ELEMENTS 
        + PROGRESS_ELEMENTS + SCROLL_SLIDER_ELEMENTS + RADIOBUTTON_ELEMENTS + SPINCONTROL_ELEMENTS 
        + CONTROL_ELEMENTS + FONT_ELEMENTS 
        + RSSFEED_ELEMENTS + DISPLAY_ELEMENTS + BEHAVIOUR_ELEMENTS + EVENT_ELEMENTS)

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

PARAMETERIZED_IDENTIFIERS = [INFOLABEL_IDENTIFIER, ESCAPEDINFOLABEL_IDENTIFIER, LOCALIZE_IDENTIFIER, 
        PARAMETER_IDENTIFIER, VARIABLE_IDENTIFIER, ESCAPEDVARIABLE_IDENTIFIER, 
        EXPRESSION_IDENTIFIER, NUMBER_IDENTIFIER, ADDON_IDENTIFIER]

XML_FILES = ["AddonBrowser.xml", 
        "DialogAccessPoints.xml", "DialogAddonInfo.xml", "DialogAddonSettings.xml", "DialogBusy.xml", "DialogButtonMenu.xml", "DialogConfirm.xml", "DialogContextMenu.xml",
        "DialogExtendedProgressBar.xml", "DialogFavourites.xml", "DialogFullScreenInfo.xml", "DialogGameControllers.xml", "DialogKeyboard.xml", "DialogMediaSource.xml",
        "DialogMusicInfo.xml", "DialogNotification.xml", "DialogNumeric.xml", "DialogPictureInfo.xml", "DialogPlayerProcessInfo.xml", 
        "DialogPVRChannelGuide.xml", "DialogPVRChannelManager.xml", "DialogPVRChannelsOSD.xml", "DialogPVRGroupManager.xml", "DialogPVRGuideSearch.xml", "DialogPVRInfo.xml",
        "DialogPVRRadioRDSInfo.xml", "DialogSeekBar.xml", "DialogSelect.xml", "DialogSettings.xml", "DialogSlider.xml", "DialogSubtitles.xml",
        "DialogTextViewer.xml", "DialogVideoInfo.xml", "DialogVolumeBar.xml",
        "EventLog.xml", "FileBrowser.xml", "FileManager.xml",
        "Font.xml", "GameOSD.xml", "Home.xml", "Includes.xml", "LoginScreen.xml",
        "MusicOSD.xml", "MusicVisualisation.xml", 
        "MyGames.xml",
        "MyMusicNav.xml", "MyMusicPlaylistEditor.xml",
        "MyPics.xml",
        "MyPlaylist.xml",
        "MyPrograms.xml",
        "MyPVRChannels.xml", "MyPVRGuide.xml", "MyPVRRecordings.xml", "MyPVRSearch.xml", "MyPVRTimers.xml",
        "MyVideoNav.xml",
        "MyWeather.xml",
        "PlayerControls.xml",
        "Pointer.xml",
        "Settings.xml", "SettingsCategory.xml", "SettingsProfile.xml", "SettingsScreenCalibration.xml", "SettingsSystemInfo.xml", "SkinSettings.xml",
        "SlideShow.xml",
        "SmartPlaylistEditor.xml",
        "SmartPlaylistRule.xml",
        "Startup.xml",
        "VideoFullScreen.xml", "VideoOSD.xml", "VideoOSDBookmarks.xml"]

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

