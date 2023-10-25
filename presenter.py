from model import Model
from view import View
import json

class Presenter:
    def __init__(self):
        self.model = Model()
        if not self.model.set_engine():
            self.view = View(False)
        else:
            self.view = View()

        self.model.set_presenter(self)
        self.view.set_presenter(self)
        self.view.show()

    def reset_model(self):
        self.model.set_engine()

    def setView(self, view):
        self.view = view

    def setKey(self):
        self.view.set_key()

    def translate(self, src, src_lang, trg_lang):
        self.model.translate(src, src_lang, trg_lang)

    def update_element(self, key, text):
        self.view.update_element(key, text)

    def show_message(self, title, message):
        self.view.update_element('comment', message)

