import tkinter as tk
from tkinter import ttk
import json
import webbrowser
from pathlib import Path

win = tk.Tk()
win.title("find_elem")

class Ham:
    def __init__(self, master):
        self.name = tk.StringVar()
        self.result_text = tk.StringVar()

        name_entered = ttk.Entry(master, width=100, textvariable=self.name)
        name_entered.pack()

        ch_button = ttk.Button(text="enter", command=self.on_change)
        ch_button.pack()

        self.r_label = ttk.Label(master, textvariable=self.result_text)
        self.r_label.pack()

        my_frame = tk.Frame(master)
        my_frame.pack()

        self.my_list = tk.Listbox(my_frame, width=100, height=30, selectmode=tk.EXTENDED)
        self.my_list.pack()

        self.my_list.bind('<Double-Button-1>', self.hyperlink)

    def on_change(self):
        path = Path.cwd().joinpath("eclaire.json")

        with open(path, 'r') as file:
                eclaire_pistache = json.load(file)
        pomme = []

        self.my_list.delete(0, tk.END)

        if self.name.get().strip():
            for url,main in eclaire_pistache.items():
                m=[m for m in main]
                #if 'class="three-figures"' in str(m): 
                #if '[object Object]' in str(m):
                #if 'ContactUsBlock' in str(m):
                if self.name.get() in str(m):
                    pomme.append(url)
        for item in pomme:
            self.my_list.insert(tk.END, item)

        self.r_label.configure(self.result_text.set(len(pomme)))

        pomme = list() #initialize pomme

    def hyperlink(self, event):
        weblink = self.my_list.get(tk.ACTIVE)
        webbrowser.open(weblink)

h = Ham(win)
win.mainloop()