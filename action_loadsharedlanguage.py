
from action import Action
import kodi_baselibrary as kodi


class LoadSharedLanguageAction(Action):
    def __init__(self):
        super().__init__(
            name = "Load Kodi (shared) language file", 
            function = self.loadsharedlanguagefile, 
            description = "Load the Kodi standard (shared) language file",
            arguments = ['sharedlanguagefile'])

        self.language = None


    def loadsharedlanguagefile(self, messagecallback, arguments):
        messagecallback("action", "\nLoading Kodi standard language file...")
        sharedlanguagefile = arguments['sharedlanguagefile']
        messagecallback("info", "- Kodi standard (shared) language file: " + sharedlanguagefile)

        if sharedlanguagefile:
            try:
                self.language = kodi.readlanguagefile(sharedlanguagefile)
            except OSError as error:
                messagecallback("error", "- Failed to load the shared language file:" + str(error))
        else:
            messagecallback("warning", "- The shared language file is not specified")

