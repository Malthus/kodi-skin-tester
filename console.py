
import tkinter as tk

from queue import Queue, Empty


class ThreadSafeConsole(tk.Text):
    
    def __init__(self, master, **options):
        super().__init__(master, font = ('Courier New', 8), **options)
        
        self.queue = Queue()
        
        self.tag_config("action", foreground ="blue", wrap = tk.NONE)
        self.tag_config("info", foreground ="gray", wrap = tk.NONE)
        self.tag_config("message", foreground = "black", wrap = tk.NONE)
        self.tag_config("warning", foreground = "dark orange", wrap = tk.NONE)
        self.tag_config("error", foreground = "red", wrap = tk.NONE)
        self.configure(state = "disabled")

        self.updateloop()


    def write(self, level, text):
        self.queue.put(["write", level, text])


    def clear(self):
        self.queue.put(["clear"])


    def updateloop(self):
        try:
            while True:
                message = self.queue.get_nowait()

                if len(message) == 3 and message[0] == "write":
                    level = str(message[1])
                    text = str(message[2])
                    
                    self.configure(state = "normal")
                    self.insert(tk.END, text + "\n", level)
                    self.configure(state = "disabled")
                elif len(message) == 1 and message[0] == "clear":
                    self.configure(state = "normal")
                    self.delete("1.0", tk.END)
                    self.configure(state = "disabled")

                self.see(tk.END)
                self.update_idletasks()
                
        except Empty:
            pass

        self.after(200, self.updateloop)
