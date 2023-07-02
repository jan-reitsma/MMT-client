from model import Model
from view import View
import json

class Presenter:
    def __init__(self, key):
        self.model = Model(key)
        self.model.set_presenter(self)
        self.view = View()
        self.view.set_presenter(self)
        self.view.show()

    def reset_model(self):
        with open('key.json', 'r') as file:
            try:
                settings_file = json.load(file)
                key = settings_file['api key']
                self.model = Model(key)
                print("LOG-P: API key set to: ", key)
            except:
                print("ERROR-P: can not load api key!")

    def setView(self, view):
        self.view = view

    def setKey(self):
        self.view.set_key()

    def read_api_key():
        with open('key.json', 'r') as file:
            try:
                settings_file = json.load(file)
                return settings_file['api key']
            except:
                print("ERROR-P: can not load api key!")


    def translate(self, src, src_lang, trg_lang):
        print("presenter translate")
        self.model.translate(src, src_lang, trg_lang)

    def update_element(self, key, text):
        self.view.update_element(key, text)

    def show_message(self, title, message):
        self.view.show_info(title, message)

