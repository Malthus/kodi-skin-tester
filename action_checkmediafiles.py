
from os import listdir
from os.path import join, isdir, isfile
from xml.sax import ContentHandler, parseString

from action import Action
import kodi_baselibrary as kodi


class MediaFileContentHandler(ContentHandler):

    def __init__(self, unit):
        self.unit = unit
        self.texturefiles = []
        self.mediafiles = []
        self.messages = []
        self.insidetextureelement = False


    def startElement(self, tag, attributes):
        if tag in kodi.TEXTURE_ELEMENTS:
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
                    "- unused images files (image files that are present in the skin directories but not used in the skin files)",
            arguments = ['skin'])


    def checkmediafiles(self, messagecallback, arguments):
        messagecallback("action", "\nChecking media files...")
        skin = arguments['skin']
        baseskindirectory = skin.basedirectory

        self.initializemediafiles(baseskindirectory, skin)
        self.readmediafiles(baseskindirectory, messagecallback)
        messagecallback("info", "- Skin resolution(s): " + ", ".join([ resolution.aspect + " (" + resolution.directory + ")" for resolution in skin.resolutions ]))
        for resolution in skin.resolutions:
            self.parsemediafiles(resolution, messagecallback)

        self.analyzemediafiles(baseskindirectory, resolution, messagecallback)


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

    


