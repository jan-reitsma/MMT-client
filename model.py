import pyperclip as clip
from modernmt import ModernMT
import json


class Model:
    def __init__(self, APIKey):
        self.mmt = ModernMT(APIKey)
        self.presenter = None
        self.source_lang = ''
        self.target_lang = ''
        self._read_settings()
        print("Model init ok")

    def _read_settings(self):
        # Open the file in read mode
        with open('settings.json', 'r') as file:
            loaded_settings = json.load(file)
            self.source_lang_setting = loaded_settings["source language"]
            print(self.source_lang_setting)
            self.target_lang = loaded_settings["target language"]
            print(self.target_lang)

    def set_presenter(self, pres):
        self.presenter = pres

    def translate(self, src, src_lang):
        self.presenter.reset_fields()
        if src_lang == 'auto':
            # determine source language:
            if self.source_lang_setting == "auto":
                try:
                    self.source_lang = self.mmt.detect_language(src).detectedLanguage
                    self.presenter.set_field('lang', 'text', f"Language detected: {self.source_lang}")
                except:
                    self.presenter.set_field('comment', 'text', "Error: no language detected")
            else:
                self.source_lang = self.source_lang_setting
                self.presenter.set_field('lang', 'text', f"Source language from settings: {self.source_lang}")
        else:
            self.source_lang = src_lang
            self.presenter.set_field('lang', 'text', f"Combobox source lang setting: {self.source_lang}")
        # translate with source and target language:
        if src == "":
            self.presenter.set_field('comment', 'text', "Error: no text to translate")
        try:
            result = self.mmt.translate(self.source_lang, self.target_lang, src)
            translation = result.translation
            quality_estimation = self.mmt.qe(self.source_lang, self.target_lang, src, translation)
            score = f"Quality estimation: {quality_estimation.score}"

            # copy translation to clipboard
            clip.copy(translation)

            # filling the fields in the GUI
            self.presenter.set_field('quality', 'text', score)
            self.presenter.set_field('comment', 'text', "some comment")
            self.presenter.set_output_field(translation)
            self.presenter.set_field('comment', 'text', "OK: Translation copied to clipboard.")

        except Exception as e:
            print(e)
            # self.presenter.set_field('comment', 'text', "Error: source and target language cannot be the same.")
            self.presenter.show_message("error", e)
            raise
