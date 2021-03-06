
import tkinter as tk
import tkinter.filedialog as tkfiledialog
import kodi_baselibrary as kodi

from functools import partial
from threading import Thread
from configparser import ConfigParser

from console import ThreadSafeConsole
from tooltip import Tooltip
from action_loadsharedlanguage import LoadSharedLanguageAction
from action_loadskin import LoadSkinAction
from action_checkloadedskin import CheckLoadedSkinAction
from action_checkskinfiles import CheckSkinFilesAction
from action_checkincludes import CheckIncludesAction
from action_checkfonts import CheckFontsAction
from action_checkvariables import CheckVariablesAction
from action_checkexpressions import CheckExpressionsAction
from action_checkskinsettings import CheckSkinSettingsAction
from action_checksyntax import CheckSyntaxAction
from action_checkmessages import CheckMessagesAction
from action_checkmediafiles import CheckMediaFilesAction


LOADSHAREDLANGUAGEFILE_TOOLTIP = ("Select and load the standard (shared) language file.\n"
    + "This shared language file should contain all the messages that are available in Kodi by default.")
LOADSKINFROMDIRECTORY_TOOLTIP = ("Select the base directory that contains the skin files and load the skin from this directory.\n"
    + "The base directory of the skin is the directory with the skin's addon.xml file.")
RELOADSKIN_TOOLTIP = ("Reload the skin files from the base directory.\n"
    + "The base directory of the skin is the directory with the skin's addon.xml file.")
CLEARMESSAGES_TOOLTIP = "Clear the messages."
CLOSEPROGRAM_TOOLTIP = "Exit this Kodi Skin Tester program."
CONFIGFILENAME = 'kst.ini'


class MainWindow(object):
    def __init__(self):
        self.config = ConfigParser()
        self.window = tk.Tk()

        self.sharedlanguagefile = tk.StringVar(self.window)
        self.baseskindirectory = tk.StringVar(self.window)

        self.loadsharedlanguage_action = LoadSharedLanguageAction()
        self.loadskin_action = LoadSkinAction()
        self.checkactions = [ 
            CheckLoadedSkinAction(),
            CheckSkinFilesAction(),
            CheckIncludesAction(),
            CheckFontsAction(),
            CheckVariablesAction(),
            CheckExpressionsAction(),
            CheckSkinSettingsAction(),
            CheckSyntaxAction(),
            CheckMessagesAction(),
            CheckMediaFilesAction()
        ]

        self.window.title("Kodi Skin Tester")
        self.window.geometry("1200x680");
        self.window.resizable(False, False)

        self.messages = ThreadSafeConsole(master = self.window, width = 100, height = 24)
        self.messages.place(x = 300, y = 120, width = 870, height = 480)
        text_scrollbar_x = tk.Scrollbar(master = self.window, orient = "horizontal", command = self.messages.xview)
        text_scrollbar_x.place(x = 300, y = 600, width = 870, height = 20)
        text_scrollbar_y = tk.Scrollbar(master = self.window, orient = "vertical", command = self.messages.yview)
        text_scrollbar_y.place(x = 1170, y = 120, width = 20, height = 480)
        self.messages.configure(xscrollcommand = text_scrollbar_x.set)
        self.messages.configure(yscrollcommand = text_scrollbar_y.set)

        self.addmessage("action", "Starting Kodi Skin Tester...")
        self.addmessage("info", "- Made by Malthus (Marijn Hubert) to test the Kodi skin 'Revolve'")
        self.addmessage("warning", "- Use this Kodi Skin Tester and its results at your own risk")
        self.addmessage("info", "Done")
        self.loadconfiguration()
        
        self.sharedlanguagefilelabel = tk.Label(self.window, textvariable = self.sharedlanguagefile, foreground = 'red', anchor = 'w')
        self.sharedlanguagefilelabel.place(x = 310, y = 10, width = 590, height = 30)
        self.baseskindirectorylabel = tk.Label(self.window, textvariable = self.baseskindirectory, foreground = 'red', anchor = 'w')
        self.baseskindirectorylabel.place(x = 310, y = 40, width = 590, height = 30)

        self.loadbuttonframe = tk.Frame()
        self.loadsharedlanguagebutton = tk.Button(master = self.loadbuttonframe, text = "Load shared language file", command = self.loadsharedlanguagefromselectedfile)
        self.loadsharedlanguagebutton.place(x = 0, y = 0, width = 280, height = 30)
        tooltip = Tooltip(self.loadsharedlanguagebutton)
        self.loadsharedlanguagebutton.bind("<Enter>", partial(tooltip.show, LOADSHAREDLANGUAGEFILE_TOOLTIP))
        self.loadsharedlanguagebutton.bind("<Leave>", partial(tooltip.hide))
        self.loadskinbutton = tk.Button(master = self.loadbuttonframe, text = "Load skin from folder", command = self.loadskinfromselecteddirectory)
        self.loadskinbutton.place(x = 0, y = 30, width = 280, height = 30)
        tooltip = Tooltip(self.loadskinbutton)
        self.loadskinbutton.bind("<Enter>", partial(tooltip.show, LOADSKINFROMDIRECTORY_TOOLTIP))
        self.loadskinbutton.bind("<Leave>", partial(tooltip.hide))
        self.reloadskinbutton = tk.Button(master = self.loadbuttonframe, text = "Reload skin files", command = self.reloadskin)
        self.reloadskinbutton.place(x = 0, y = 60, width = 280, height = 30)
        tooltip = Tooltip(self.reloadskinbutton)
        self.reloadskinbutton.bind("<Enter>", partial(tooltip.show, RELOADSKIN_TOOLTIP))
        self.reloadskinbutton.bind("<Leave>", partial(tooltip.hide))
        self.loadbuttonframe.place(x = 10, y = 10, width = 280, height = 100)

        self.checkbuttonframe = tk.Frame()
        for index, action in enumerate(self.checkactions):
            button = tk.Button(master = self.checkbuttonframe, text = action.getname(), command = partial(self.executecheckaction, action), width = 60, height = 3)
            button.place(x = 0, y = 30 * index, width = 280, height = 30)
            tooltip = Tooltip(button)
            button.bind("<Enter>", partial(tooltip.show, action.description))
            button.bind("<Leave>", partial(tooltip.hide))
        self.checkbuttonframe.place(x = 10, y = 120, width = 280, height = 300)

        self.clearbutton = tk.Button(master = self.window, text = "Clear", command = self.clearmessages)
        self.clearbutton.place(x = 900, y = 630, width = 280, height = 40)
        tooltip = Tooltip(self.clearbutton)
        self.clearbutton.bind("<Enter>", partial(tooltip.show, CLEARMESSAGES_TOOLTIP))
        self.clearbutton.bind("<Leave>", partial(tooltip.hide))

        self.exitbutton = tk.Button(master = self.window, text = "Close", command = self.exitprogram)
        self.exitbutton.place(x = 10, y = 630, width = 280, height = 40)
        tooltip = Tooltip(self.exitbutton)
        self.exitbutton.bind("<Enter>", partial(tooltip.show, CLOSEPROGRAM_TOOLTIP))
        self.exitbutton.bind("<Leave>", partial(tooltip.hide))

        self.executeloadaction(self.loadsharedlanguage_action)
        self.executeloadaction(self.loadskin_action)
        self.window.mainloop()


    def loadsharedlanguagefromselectedfile(self):
        newlanguagefile = tkfiledialog.askopenfilename()
        if newlanguagefile:
            self.sharedlanguagefile.set(newlanguagefile)
            self.colorsharedlanguagefilelabel()
            self.executeloadaction(self.loadsharedlanguage_action)


    def loadskinfromselecteddirectory(self):
        newskindirectory = tkfiledialog.askdirectory(initialdir = self.baseskindirectory)
        if newskindirectory:
            self.baseskindirectory.set(newskindirectory)
            self.colorbaseskindirectorylabel()
            self.executeloadaction(self.loadskin_action)


    def reloadskin(self):
        self.executeloadaction(self.loadskin_action)


    def executeloadaction(self, action):
        self.executeaction(action)

        if type(action) is LoadSharedLanguageAction:
            self.language = action.language
            self.colorsharedlanguagefilelabel()
        elif type(action) is LoadSkinAction:
            self.skin = action.skin
            self.colorbaseskindirectorylabel()

        self.addmessage("info", "Done")


    def executecheckaction(self, action):
        self.executeaction(action)
        self.addmessage("info", "Done")


    def executeaction(self, action):
        arguments = self.buildarguments(action)
        thread = Thread(target = action.execute, args = [self.addmessage, arguments])
        thread.daemon = True
        thread.start()
        thread.join()


    def clearmessages(self):
        self.messages.clear()


    def exitprogram(self):
        self.saveconfiguration()
        self.window.destroy()


    def addmessage(self, level, text):
        self.messages.write(level, text)


    def loadconfiguration(self):
        self.config.read(CONFIGFILENAME)

        self.sharedlanguagefile.set(self.config['DEFAULT']['shared language file'])
        self.baseskindirectory.set(self.config['DEFAULT']['base skin directory'])
        
        
    def saveconfiguration(self):
        self.config['DEFAULT']['shared language file'] = self.sharedlanguagefile.get()
        self.config['DEFAULT']['base skin directory'] = self.baseskindirectory.get()

        with open(CONFIGFILENAME, 'w') as configfile:
            self.config.write(configfile)


    def buildarguments(self, action):
        arguments = {}

        for argument in action.arguments:
            if argument == 'sharedlanguagefile':
                arguments['sharedlanguagefile'] = self.sharedlanguagefile.get()
            elif argument == 'skinbasedirectory':
                arguments['skinbasedirectory'] = self.baseskindirectory.get()
            elif argument == 'skinlanguagedirectory':
                arguments['skinlanguagedirectory'] = kodi.LANGUAGE_DIRECTORY
            elif argument == 'skin':
                arguments['skin'] = self.skin
            elif argument == 'sharedlanguage':
                arguments['sharedlanguage'] = self.language
    
        return arguments


    def colorsharedlanguagefilelabel(self):
        color = "blue" if self.language and self.language.languagefile == self.sharedlanguagefile.get() else "red"
        self.sharedlanguagefilelabel.configure(foreground = color)


    def colorbaseskindirectorylabel(self):
        color = "blue" if self.skin and self.skin.basedirectory == self.baseskindirectory.get() else "red"
        self.baseskindirectorylabel.configure(foreground = color)
    

MainWindow()

