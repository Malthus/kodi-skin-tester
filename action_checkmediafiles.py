
from os import listdir
from os.path import join, isdir, isfile
from xml.sax import ContentHandler, parseString
from PIL import Image

from action import Action
import kodi_baselibrary as kodi


class MediaFileContentHandler(ContentHandler):

    def __init__(self, unit):
        self.textureelements = [ element for element in kodi.TEXTURE_ELEMENTS if element != "aspectratio" ] 
        self.unit = unit
        self.texturefiles = []
        self.mediafiles = []
        self.messages = []
        self.insidetextureelement = False


    def startElement(self, tag, attributes):
        if tag in self.textureelements:
            self.insidetextureelement = True

        for key, value in attributes.items():
            if key == 'diffuse' and self.insidetextureelement and not (value.startswith(kodi.INFOLABEL_IDENTIFIER) or value.startswith(kodi.PARAMETER_IDENTIFIER) or value.startswith(kodi.VARIABLE_IDENTIFIER)):
                self.texturefiles.append(value)
            elif key != 'diffuse' and (value.endswith(".jpg") or value.endswith(".jpeg") or value.endswith(".png")):
                self.mediafiles.append(value)


    def endElement(self, tag):
        self.insidetextureelement = False


    def characters(self, content):
        if self.insidetextureelement:
            if not (content.startswith(kodi.INFOLABEL_IDENTIFIER) or content.startswith(kodi.PARAMETER_IDENTIFIER) or content.startswith(kodi.VARIABLE_IDENTIFIER)):
                self.texturefiles.append(content)
        
        elif content.endswith(".jpg") or content.endswith(".jpeg") or content.endswith(".png"):
            self.mediafiles.append(content)
        


class CheckMediaFilesAction(Action):

    def __init__(self):
        super().__init__(
            name = "Check media files", 
            function = self.checkmediafiles, 
            description = "Check media (image) files for:\n" + 
                    "- missing image files (image files that are used in the skin files but are missing from the file system)\n" + 
                    "- unused images files (image files that are present in the skin directories but not used in the skin files)\n" +
                    "- *WIP* invalid image files (images that are too small for the TexturePacker tool)\n" + 
                    "- invalid sizes of icon and fanart images",
            arguments = ['skin'])


    def checkmediafiles(self, messagecallback, arguments):
        messagecallback("action", "\nChecking media files...")
        skin = arguments['skin']
        baseskindirectory = skin.basedirectory

        self.initializemediafiles(baseskindirectory, skin)
        self.readmediafiles(baseskindirectory, messagecallback)
        messagecallback("info", "- Skin resolution(s): " + ", ".join([ resolution.aspect + " (" + resolution.directory + ")" for resolution in skin.resolutions ]))
        self.checkiconfile(skin, messagecallback)
        self.checkfanartfile(skin, messagecallback)
        for resolution in skin.resolutions:
            self.parsemediafiles(resolution, messagecallback)

        self.analyzemediafiles(baseskindirectory, resolution, messagecallback)


    def checkiconfile(self, skin, messagecallback):
        iconimagefile = next((asset.file for asset in skin.assets if asset.type == kodi.ICON_ELEMENT), None)

        if iconimagefile is not None:
            baseskindirectory = skin.basedirectory        
            file = join(baseskindirectory, iconimagefile)
            iconimage = Image.open(file)
            (iconwidth, iconheight) = iconimage.size
    
            if (iconwidth == 256 and iconheight == 256) or (iconwidth == 512 and iconheight == 512):
                messagecallback("info", "- " + iconimagefile + ": Icon image size is " + str(iconwidth) + " x " + str(iconheight))
            else:
                messagecallback("warning", "- " + iconimagefile + ": Invalid icon image size (" + str(iconwidth) + " x " + str(iconheight) + ")")
        else:
            messagecallback("warning", "- " + kodi.ADDON_FILENAME + ": Missing icon-file resource")


    def checkfanartfile(self, skin, messagecallback):
        fanartimagefile = next((asset.file for asset in skin.assets if asset.type == kodi.FANART_ELEMENT), None)

        if fanartimagefile is not None:
            baseskindirectory = skin.basedirectory
            file = join(baseskindirectory, fanartimagefile)
            fanartimage = Image.open(file)
            (fanartwidth, fanartheight) = fanartimage.size
    
            if (fanartwidth == 1280 and fanartheight == 720) or (fanartwidth == 1920 and fanartheight == 1080) or (fanartwidth == 3840 and fanartheight == 2160):
                messagecallback("info", "- " + fanartimagefile + ": Fanart image size is " + str(fanartwidth) + " x " + str(fanartheight))
            else:
                messagecallback("warning", "- " + fanartimagefile + ": Invalid fanart image size (" + str(fanartwidth) + " x " + str(fanartheight) + ")")
        else:
            messagecallback("message", "- " + kodi.ADDON_FILENAME + ": Missing fanart-file resource")


    def initializemediafiles(self, baseskindirectory, skin):
        self.texturefiles = set([])
        self.mediafiles = set([])
        
        for asset in skin.assets:
            file = join(baseskindirectory, asset.file)
            self.mediafiles.add(self.processfile(file))


    def parsemediafiles(self, resolution, messagecallback):
        texturefiles = []
        mediafiles = []

        for unit in resolution.units:
            contenthandler = MediaFileContentHandler(unit)
            parseString("".join(unit.lines), contenthandler)

            texturefiles.extend(contenthandler.texturefiles)
            mediafiles.extend(contenthandler.mediafiles)
            messages = contenthandler.messages
            
            for message in messages:
                messagecallback("warning", "- File " + unit.name + ": " + message)

        self.texturefiles.update(texturefiles)
        self.mediafiles.update(mediafiles)
        
        messagecallback("info", "- Total number of texture file references: " + str(len(texturefiles)))
        messagecallback("info", "- Total number of unpacked media file references: " + str(len(mediafiles)))
        messagecallback("info", "- Number of unique texture file references: " + str(len(self.texturefiles)))
        messagecallback("info", "- Number of unique unpacked media file references: " + str(len(self.mediafiles)))


    def readmediafiles(self, baseskindirectory, messagecallback):
        self.presentfiles = []
        self.readmediafilesfromdirectory(baseskindirectory, messagecallback)

        messagecallback("info", "- Total number of image files in skin directories: " + str(len(self.presentfiles)))


    def readmediafilesfromdirectory(self, directory, messagecallback):
        files = [ file for file in listdir(directory) ]

        for file in files:
            fullfile = join(directory, file)
            if isfile(fullfile) and (file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png")):
                self.presentfiles.append(self.processfile(fullfile))
            elif isdir(fullfile):
                self.readmediafilesfromdirectory(fullfile, messagecallback)
    

    def analyzemediafiles(self, baseskindirectory, resolution, messagecallback):
        for texturefile in self.texturefiles:
            file = self.processdirectory(baseskindirectory, texturefile)
            if file not in self.presentfiles:
                messagecallback("warning", "- Missing referenced texture file: " + texturefile)

        for mediafile in self.mediafiles:
            file = self.processdirectory(baseskindirectory, mediafile)
            if file not in self.presentfiles:
                messagecallback("warning", "- Missing referenced media file: " + mediafile)

        referencedfiles = []
        referencedfiles.extend([ self.processdirectory(baseskindirectory, file) for file in self.texturefiles ])
        referencedfiles.extend([ self.processdirectory(baseskindirectory, file) for file in self.mediafiles ])
        defaultfileprefix = self.processdirectory(baseskindirectory, "special://skin/media/default")

        for presentfile in self.presentfiles:
            if presentfile not in referencedfiles and not presentfile.startswith(defaultfileprefix):
                messagecallback("message", "- Possibly unused media file: " + presentfile)


    def processdirectory(self, baseskindirectory, referencedfile):
        if referencedfile.startswith("special://skin"):
            file = referencedfile.replace("special://skin", baseskindirectory)
        else:
            file = join(baseskindirectory, "media", referencedfile)
        return self.processfile(file)

    def processfile(self, file):
        return file.replace('\\', '/')

