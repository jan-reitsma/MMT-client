import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, showwarning
import json
import pyperclip as clip


class View:
    def __init__(self):
        self.presenter = None
        self.root = tk.Tk()
        self.root.title("MMT Client")
        self.root.geometry("700x570")

        self.source_lang = ''
        self.target_lang = ''
        self._read_from_settings_file()

        self.selected_source_language = tk.StringVar()
        self.selected_target_language = tk.StringVar()

        # a lot of widgets are created here:
        self._init_settings_frame()
        # and some here:
        self._init_translation_frame()

        self.root.bind('<Return>', self._return_pressed)

    def set_presenter(self, presenter):
        self.presenter = presenter

    def _read_from_settings_file(self):
        # Open the file in read mode
        with open('settings.json', 'r') as file:
            try:
                loaded_settings = json.load(file)
                self.source_lang = loaded_settings["source language"]
                print(f"source language from settings file: {self.source_lang}")
                self.target_lang = loaded_settings["target language"]
                print(f"target language from settings file: {self.target_lang}")
            except Exception as e:
                print(e)
                raise

    def _init_settings_frame(self):
        settings_frame = tk.Frame(self.root, height=40, width=660, padx=5, pady=5)
        settings_frame.grid(column=0, row=0, sticky="n")
        settings_frame.grid_propagate(False)
        paddings = {'padx': 5, 'pady': 2}

        tk.Label(settings_frame, text="Select source language:").grid(column=0, row=0, sticky=tk.W, **paddings)
        combo_source_language = ttk.Combobox(settings_frame, width=20, textvariable=self.selected_source_language)
        combo_source_language['values'] = ['en', 'de', 'fr', 'nl', 'auto']
        combo_source_language['state'] = 'readonly'
        combo_source_language.bind('<<ComboboxSelected>>', self._combo_selected)
        combo_source_language.set(self.source_lang)
        combo_source_language.grid(column=1, row=0, sticky='w', **paddings)

        tk.Label(settings_frame, text="Select target language:").grid(column=2, row=0, sticky=tk.W, **paddings)
        combo_target_language = ttk.Combobox(settings_frame, width=20, textvariable=self.selected_target_language)
        combo_target_language['values'] = ['en', 'de', 'fr', 'nl']
        combo_target_language['state'] = 'readonly'
        combo_target_language.bind('<<ComboboxSelected>>', self._combo_selected)
        combo_target_language.set(self.target_lang)
        combo_target_language.grid(column=3, row=0, sticky='w', **paddings)

        tk.Button(settings_frame, text=" Save ", command=self._save_button_clicked).grid(column=4, row=0, sticky=tk.W,
                                                                                         **paddings)

    def _init_translation_frame(self):
        translation_frame = tk.Frame(self.root, width=700)
        translation_frame.grid(column=0, row=1)

        label = tk.Label(translation_frame, text='Enter source text or leave empty to use clipboard:')
        self.input_text = tk.Text(translation_frame, height=9, width=78, padx=5, pady=5)

        # scroll = ttk.Scrollbar(translation_frame, orient='vertical', command=self.input_text.yview)
        # scroll.grid(column=1, row=0, sticky=tk.NS)
        # self.input_text['yscrollcommand'] = scroll.set
        self.input_text.focus()

        # entry.focus()
        self.comment = tk.Label(translation_frame, width=100)
        self.quality = tk.Label(translation_frame, width=20)
        button = tk.Button(translation_frame, text="Click here to translate or hit RETURN",
                           command=self._button_clicked)
        self.output_text = tk.Text(translation_frame, height=9, width=78, padx=5, pady=5)

        # placing the fields:
        label.grid(column=0, row=0, sticky="s", padx=5, pady=5)
        self.input_text.grid(column=0, row=1, sticky="n", padx=5, pady=5)
        button.grid(column=0, row=2, sticky="n", padx=5, pady=5)
        self.output_text.grid(column=0, row=3, sticky="n", padx=5, pady=5)
        self.comment.grid(column=0, row=4, sticky="n", padx=5, pady=5)
        self.quality.grid(column=0, row=5, sticky="n", padx=5, pady=5)

    def reset_fields(self):
        self.comment['text'] = ""
        self.quality['text'] = ""
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)

    def set_comment(self, text):
        self.comment['text'] = text

    def set_quality(self, text):
        self.quality['text'] = text

    def set_input_text(self, text):
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert(tk.END, text)

    def set_output_text(self, text):
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, text)

    def show(self):
        self.root.mainloop()

    def _combo_selected(self, event):
        self.source_lang = self.selected_source_language.get()
        print(f"selected: source language: {self.source_lang}.")
        self.target_lang = self.selected_target_language.get()
        print(f"selected: source language: {self.target_lang}.")

    def _save_button_clicked(self):
        settings = {
            "source language": self.source_lang,
            "target language": self.target_lang,
        }
        with open('settings.json', 'w') as file:
            json.dump(settings, file)
        print("settings saved")
        self.set_comment(f"Settings saved, source language: {self.source_lang}, target language: {self.target_lang}.")

    def _button_clicked(self):
        user_entry = self.input_text.get("1.0", tk.END)
        if user_entry != "":
            source = user_entry
        else:
            source = clip.paste()
        self.presenter.translate(source, self.source_lang, self.target_lang)

    def _return_pressed(self, event):
        self._button_clicked()

    def show_info(self, title, message):
        showinfo(title, message)
