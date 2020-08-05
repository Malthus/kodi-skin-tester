
from datetime import datetime
from os import listdir, remove, rename
from os.path import exists, isfile, join
from shutil import copy
from re import compile
from subprocess import call
from xml.sax import ContentHandler, ErrorHandler, SAXParseException, parse, parseString

from action import Action
import kodi_baselibrary as kodi


class SkinContentHandler(ContentHandler):

    def __init__(self, skin):
        self.skin = skin
        self.insideimports = False
        self.insideassets = False
        self.currentasset = None


    def startElement(self, tag, attributes):
        if tag == kodi.ADDON_ELEMENT:
            self.parseaddon(tag, attributes)
        elif tag == kodi.RESOLUTION_ELEMENT:
            self.parseresolution(tag, attributes)
        elif tag == kodi.ASSETS_ELEMENT:
            self.insideassets = True
        elif tag == kodi.IMPORT_ELEMENT:
            self.parseimport(tag, attributes)
        elif self.insideassets:
            self.currentasset = tag


    def endElement(self, tag):
        if tag == kodi.ASSETS_ELEMENT:
            self.insideassets = False
            self.currentasset = None
        elif self.insideassets:
            self.currentasset = None


    def characters(self, content):
        if self.insideassets and self.currentasset:
            self.skin.assets.append(kodi.Asset(self.currentasset, content))
            self.currentasset = None

   
    def parseaddon(self, tag, attributes):
        self.skin.name = attributes.getValue('name')
        self.skin.id = attributes.getValue('id')
        self.skin.version = attributes.getValue('version')


    def parseresolution(self, tag, attributes):
        resolution = kodi.Resolution()
        resolution.aspect = attributes.getValue('aspect')
        resolution.width = attributes.getValue('width')
        resolution.height = attributes.getValue('height')
        resolution.directory = attributes.getValue('folder')
        resolution.path = join(self.skin.basedirectory, attributes.getValue('folder'))
        resolution.default = attributes.getValue('default')
        resolution.skin = self.skin
        
        self.skin.resolutions.append(resolution)


    def parseimport(self, tag, attributes):
        addon = kodi.Addon()
        addon.name = attributes.getValue('addon')
        addon.version = attributes.getValue('version')
        addon.optional = attributes.getValue('optional') if 'optional' in attributes.getNames() else False
        self.skin.addons.append(addon)
        if addon.name == 'xbmc.gui':
            self.skin.xbmcguiversion = addon.version


class LoadSkinAction(Action):
    def __init__(self):
        super().__init__(
            name = "Load Kodi skin", 
            function = self.loadskin, 
            description = "Load the Kodi skin files from the base directory",
            arguments = ['skinbasedirectory', 'skinlanguagedirectory'])

        self.skin = None


    def loadskin(self, messagecallback, arguments):
        messagecallback("action", "\nLoading Kodi skin base file...")
        skinbasedirectory = arguments['skinbasedirectory']
        skinlanguagedirectory = arguments['skinlanguagedirectory']
        
        if skinbasedirectory and skinlanguagedirectory:
            try:
                self.loadskinfile(messagecallback, skinbasedirectory, skinlanguagedirectory)
                self.loadlanguagefile(messagecallback, skinbasedirectory, skinlanguagedirectory)
                self.loadresolutions(messagecallback, skinbasedirectory)
            except OSError as error:
                messagecallback("error", "- Failed to load the Kodi skin files: " + str(error))
        else:
            if not skinbasedirectory:
                messagecallback("warning", "- The base skin directory is not set")
    
            if not skinlanguagedirectory:
                messagecallback("warning", "- The skin's language directory is not set")


    def loadskinfile(self, messagecallback, skinbasedirectory, skinlanguagedirectory):
        messagecallback("info", "- Skin base directory: " + skinbasedirectory)
        
        skin = kodi.Skin(skinbasedirectory, skinlanguagedirectory)
        contenthandler = SkinContentHandler(skin)
        skinfile = join(skinbasedirectory, kodi.ADDON_FILENAME)
        parse(skinfile, contenthandler)
        self.skin = skin
    
        messagecallback("info", "- Skin name: " + self.skin.name)
        messagecallback("info", "- Skin version: " + self.skin.version)
        messagecallback("info", "- Skin resolution(s): " + ", ".join([ resolution.aspect + " (" + resolution.directory + ")" for resolution in self.skin.resolutions ]))


    def loadlanguagefile(self, messagecallback, skinbasedirectory, skinlanguagedirectory):
        messagecallback("info", "- Skin language directory: " + skinlanguagedirectory)
        messagecallback("info", "- Skin language file: " + kodi.LANGUAGE_FILENAME)
        
        self.skin.language = kodi.readlanguagefile(join(skinbasedirectory, skinlanguagedirectory, kodi.LANGUAGE_FILENAME))

        messagecallback("info", "- Number of skin language entries: " + str(len(self.skin.language.strings)))


    def loadresolutions(self, messagecallback, skinbasedirectory):
        for resolution in self.skin.resolutions:
            self.loadunitsperresolution(messagecallback, skinbasedirectory, resolution)


    def loadunitsperresolution(self, messagecallback, skinbasedirectory, resolution):
        unitdirectory = join(skinbasedirectory, resolution.directory)
        unitfiles = [ file for file in listdir(unitdirectory) if isfile(join(unitdirectory, file)) and file.endswith(".xml") ]
        count = 0

        for unitfile in unitfiles:
            unit = self.loadunitfile(messagecallback, unitdirectory, unitfile)
            unit.skin = self.skin
            unit.resolution = resolution
            resolution.units.append(unit)
            count = count + 1

        messagecallback("info", "- Number of unit files for resolution " + resolution.aspect + ": " + str(count))


    def loadunitfile(self, messagecallback, unitdirectory, unitfile):
        unitname = unitfile[0:-4]
        filehandle = open(join(unitdirectory, unitfile), "r") 
        lines = filehandle.readlines() 
        unit = kodi.Unit(unitname, unitfile, lines)
        contenthandler = ContentHandler()
        
        try:
            parseString("".join(lines), contenthandler)
        except SAXParseException as exception:
            messagecallback("error", "- XML Parsing error in file " + unitfile + ": " + str(exception))
        
        return unit

