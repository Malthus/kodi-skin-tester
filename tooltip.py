
import tkinter as tk


class Tooltip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tooltipwindow = None
        self.id = None
        self.x = 0
        self.y = 0


    def show(self, text, *args):
        self.text = text
        if self.tooltipwindow or not self.text:
            return

        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tooltipwindow = tk.Toplevel(self.widget)
        tipwindow = self.tooltipwindow
        tipwindow.wm_overrideredirect(1)
        tipwindow.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tipwindow, text = self.text, justify = tk.LEFT, background = "#ffffe0", relief = tk.SOLID, borderwidth = 1, font = ("tahoma", "8", "normal"))
        label.pack(ipadx=1)


    def hide(self, *args):
        tipwindow = self.tooltipwindow
        self.tooltipwindow = None
        if tipwindow:
            tipwindow.destroy()

