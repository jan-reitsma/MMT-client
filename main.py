from modernmt import ModernMT
import pyperclip as clip
import tkinter as tk
class Model:
    def __init__(self, APIKey):
        self.mmt = ModernMT(APIKey)
        self.presenter = None
        print("Model init ok")

    def setPresenter(self, pres):
        self.presenter = pres

    def translate(self, src):
        view.reset_fields()
        try:
            detected_language = self.mmt.detect_language(src).detectedLanguage
        except:
            view.set_field('comment', 'text', "Error: no language detected")

        try:
            result = self.mmt.translate(detected_language, "nl", src)
            translation = result.translation
            quality_estimation = self.mmt.qe(detected_language, "nl", src, translation)
            score = f"Quality estimation: {quality_estimation.score}"

            # copy translation to clipboard
            clip.copy(translation)

            # filling the fields in the window
            view.set_field('quality', 'text', score)
            view.set_field('lang', 'text', f"Language detected: {detected_language}")
            view.set_field('comment', 'text', "some comment")

            view.set_output_field(translation)
            view.set_field('comment', 'text', "OK: Translation copied to clipboard.")
        except:
            view.set_field('comment', 'text', "Error: source and target language cannot be the same.")


class View:
    def __init__(self):
        self.presenter = None
        self.root = tk.Tk()
        self.root.title("MMT Client")
        self.root.geometry("400x500")
        self.fields = {}
        self.init_fields()
        self._insert_fields()
        self.root.bind('<Return>', self._return_pressed)

    def set_presenter(self, presenter):
        self.presenter = presenter
    def init_fields(self):
        self.fields['label'] = tk.Label(text='Enter source text or leave empty to use clipboard:')
        self.fields['entry'] = tk.Entry(width=200)
        self.fields['lang'] = tk.Label()
        self.fields['comment'] = tk.Label(width=50)
        self.fields['quality'] = tk.Label(width=20)
        self.fields['button'] = tk.Button(text="Click here to translate or hit RETURN", command=self._button_clicked)
        self.fields['outp'] = tk.Text()

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
        print("button clicked")
        user_entry = self.fields['entry'].get()
        if user_entry != "":
            source = user_entry
        else:
            source = clip.paste()
        self.presenter.translate(source)

    def _return_pressed(self, event):
        print("return pressed")
        self._button_clicked()

class Presenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def setModel(self, model):
        self.model = model
    def setView(self, view):
        self.view = view

    def translate(self, src):
        trg = model.translate(src)
        print(trg)

    def test1(self):
        print("presenter test 1")
        self.view.init_fields()
    def test2(self):
        print("presenter test 2")


APIKey = '7763DBAD-DB02-9C5C-5DA0-B543BE3D7D34'
model = Model(APIKey)
view = View()
pres = Presenter(model, view)

model.setPresenter(pres)
view.set_presenter(pres)
view.show()


