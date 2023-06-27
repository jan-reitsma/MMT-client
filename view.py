import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo,showerror,showwarning

import pyperclip as clip



class View:
    def __init__(self):
        self.presenter = None
        self.root = tk.Tk()
        self.root.title("MMT Client")
        self.root.geometry("400x500")
        self.fields = {}
        self.selected_language = tk.StringVar()
        self._init_combo()
        self.init_fields()
        self._insert_fields()
        self.root.bind('<Return>', self._return_pressed)
        self.local_source_lang = 'auto'


    def set_presenter(self, presenter):
        self.presenter = presenter
    def init_fields(self):
        self.fields['label'] = tk.Label(text='Enter source text or leave empty to use clipboard:')
        self.fields['entry'] = tk.Entry(width=200)
        self.fields['entry'].focus()
        self.fields['lang'] = tk.Label()
        self.fields['comment'] = tk.Label(width=50)
        self.fields['quality'] = tk.Label(width=20)
        self.fields['button'] = tk.Button(text="Click here to translate or hit RETURN", command=self._button_clicked)
        self.fields['outp'] = tk.Text()
    def _combo_selected(self, event):
        self.local_source_lang = self.selected_language.get()
        print(self.selected_language.get())

    def _init_combo(self):
        combo = ttk.Combobox(self.root, textvariable=self.selected_language)
        combo['values'] = ['en', 'de', 'fr', 'auto']
        combo['state']='readonly'
        combo.bind('<<ComboboxSelected>>', self._combo_selected)
        combo.set('auto')
        combo.pack()

    def reset_fields(self):
        self.fields['lang']['text'] = ""
        self.fields['comment']['text'] = ""
        self.fields['quality']['text'] = ""
        self.fields['entry'].delete("0", tk.END)
        self.fields['outp'].delete("1.0", tk.END)
    def set_field(self, field, key, value):
        self.fields[field][key] = value
    def set_output_field(self, value):
        self.fields['outp'].insert(tk.END, value)
    def show(self):
        self.root.mainloop()
    def _insert_fields(self):
        for field in self.fields.values():
            field.pack(padx=10, pady=5, fill=tk.X)
    def _button_clicked(self):
        user_entry = self.fields['entry'].get()
        if user_entry != "":
            source = user_entry
        else:
            source = clip.paste()
        self.presenter.translate(source, self.local_source_lang)
    def _return_pressed(self, event):
        self._button_clicked()
    def show_info(self, title, message):
        showinfo(title, message)
