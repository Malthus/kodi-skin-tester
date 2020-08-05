
from action import Action
import kodi_baselibrary as kodi


class CheckLoadedSkinAction(Action):

    def __init__(self):
        super().__init__(
            name = "Display loaded skin information", 
            function = self.displayloadedskin, 
            description = "Show some detailed information about:\n" + 
                    "- the currently loaded standard (shared) language file;\n" + 
                    "- the currently loaded skin.",
            arguments = ['skin', 'sharedlanguage'])


    def displayloadedskin(self, messagecallback, arguments):
        messagecallback("action", "\nDisplaying information about the standard (shared) language file and the loaded skin...")
        skin = arguments['skin']
        sharedlanguage = arguments['sharedlanguage']

        messagecallback("info", "- Standard (shared) language file: " + sharedlanguage.languagefile)
        messagecallback("info", "- Skin base directory: " + skin.basedirectory)
        messagecallback("info", "- Skin name: " + skin.name)
        messagecallback("info", "- Skin id: " + skin.id)
        messagecallback("info", "- Skin version: " + skin.version)
        messagecallback("info", "- Skin resolution(s): " + ", ".join([ resolution.aspect + " (" + resolution.directory + ")" for resolution in skin.resolutions ]))
        messagecallback("info", "- Skin asset(s): " + ", ".join([ asset.file + " (" + asset.type + ")" for asset in skin.assets ]))
        messagecallback("info", "- Skin XBMC GUI version: " + skin.xbmcguiversion)

