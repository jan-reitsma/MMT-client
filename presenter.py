from model import Model
from view import View

class Presenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def setModel(self, model):
        self.model = model
    def setView(self, view):
        self.view = view

    def setKey(self):
        self.view.set_key()

    def translate(self, src, src_lang, trg_lang):
        print("presenter translate")
        self.model.translate(src, src_lang, trg_lang)

    def reset_fields(self):
        self.view.reset_fields()

    def update_element(self, key, text):
        self.view.update_element(key, text)

    def show_message(self, title, message):
        self.view.show_info(title, message)

