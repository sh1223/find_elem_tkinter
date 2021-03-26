import tkinter as tk
from tkinter import ttk
import json
import webbrowser
from pathlib import Path

win = tk.Tk()
win.title("find_elem")

class Find_elem:
    def __init__(self, master):
        self.name = tk.StringVar()
        self.result_text = tk.StringVar()

        name_entered = ttk.Entry(master, width=100, textvariable=self.name)
        name_entered.pack()
        name_entered.focus()

        ch_button = ttk.Button(master, text="enter", command=self.on_change)
        ch_button.pack()

        #bind enter key event with on_change method to local button
        ch_button.bind('<Return>', self.on_change) 

        #bind enter key event with on_change method to master(global) root
        master.bind('<Return>', self.on_change) 

        self.r_label = ttk.Label(master, textvariable=self.result_text)
        self.r_label.pack()

        my_frame = tk.Frame(master)
        my_frame.pack()

        self.my_list = tk.Listbox(my_frame, width=100, height=30, selectmode=tk.EXTENDED)
        self.my_list.pack()

        #bind double click event to hyperlink method to local listbox
        self.my_list.bind('<Double-Button-1>', self.hyperlink) 

    def on_change(self, event=None):
        path = Path.cwd().joinpath("eclaire.json")

        with open(path, 'r') as file:
                eclaire_pistache = json.load(file) # load json file
        pomme = []

        self.my_list.delete(0, tk.END) #reinitialize listbox

        if self.name.get().strip():
            for url,main in eclaire_pistache.items():
                m=[m for m in main]
                if self.name.get() in str(m):
                    pomme.append(url)
        for item in pomme:
            self.my_list.insert(tk.END, item) #add each url to listbox

        self.r_label.configure(self.result_text.set(len(pomme)))

        pomme = list() #reinitialize pomme list

    def hyperlink(self, event):
        # double click event which open a value as hyperlink on the browser
        weblink = self.my_list.get(tk.ACTIVE)
        webbrowser.open(weblink)

find_elem = Find_elem(win)
win.mainloop()