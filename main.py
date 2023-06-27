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

    def translate(self, src, src_lang):
        trg = model.translate(src, src_lang)

    def reset_fields(self):
        view.reset_fields()

    def set_field(self, field, key, value):
        view.set_field(field, key, value)

    def set_output_field(self, value):
        view.set_output_field(value)

    def show_message(self, title, message):
        view.show_info(title, message)

APIKey = '7763DBAD-DB02-9C5C-5DA0-B543BE3D7D34'
model = Model(APIKey)
view = View()
pres = Presenter(model, view)
model.set_presenter(pres)
view.set_presenter(pres)
view.show()
