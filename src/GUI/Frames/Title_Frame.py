#title of program frame

import tkinter as tk

class Title(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=600)
        OC_title = tk.Label(self, text='OPEN Controller', justify='center',
                            font=('Bauhaus 93', 24))
        OC_title.pack(fill='both', expand=True)
