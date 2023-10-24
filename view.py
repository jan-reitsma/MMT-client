import PySimpleGUI as sg
import json
import pyperclip as clip
sg.theme('DarkBlack')


def show_info(title, message):
    sg.popup(message)


class View:
    def __init__(self, apikey_set=True):
        self.presenter = None
        source_languages=['de', 'en', 'fr', 'nl', 'auto']
        target_languages=['de', 'en', 'fr', 'nl']
        self.source_language = None
        self.target_language = None
        layout = [[sg.Text('Source language:'), sg.Combo(source_languages, enable_events=True, default_value=None,
                                                         readonly=True, size=(5,1), key='combo_source_lang'),
                  sg.Text('Target language:'), sg.Combo(target_languages, enable_events=True, default_value=None,
                                                        readonly=True, size=(5,1), key='combo_target_lang'), sg.Button
                   ('Save', key='save_languages'), sg.Button('Load', key='load_languages')],
                  [sg.Text(key='comment')],
                  [sg.Text(key='quality')],
                [sg.Text('Enter source text:', key='source text label')],
                [sg.Multiline(key='source_text', size=(70,12))],
                [sg.Text('Target text:', key='target text label')],
                [sg.Multiline(key='target_text', size=(70,12))],
                [sg.Submit('Submit (Alt-Enter)', key='submit'), sg.Button('Clear (Alt-C)', key='clear'),
                 sg.Button('Set Key', key='set_key'), sg.CloseButton('Close')]]

        self.window = sg.Window('MMT Client', layout, finalize=True)
        #self._load_language_settings()
        self.window.bind("<Alt_L><Return>" , "alt-L-return")
        self.window.bind("<Alt_L><c>" , "alt-L-c")
        self.apikey_set = apikey_set

    def show(self):
        self.show_window()

    def set_presenter(self, presenter):
        self.presenter = presenter

    def show_window(self):
        if not self.apikey_set:
            self.update_element('comment', 'No valid API key. Please set your API key first!')
            print("LOG-V: no api key set.")
            self.set_key()

        while True:
            event, values = self.window.read()
            # print("LOG-V:", event, values)

            if self.source_language == None or self.target_language == None:
               self._load_language_settings()

            # print(values['source_text'])
            # self.window['target_text'].update(value='xxx')
            match event:

                case 'combo_source_lang':
                    self.source_language = (values['combo_source_lang'])

                case 'combo_target_lang':
                    self.target_language = (values['combo_target_lang'])

                case 'save_languages':
                    self._save_language_settings()

                case 'load_languages':
                    self._load_language_settings()

                case 'submit' | 'alt-L-return':
                    print("LOG-V: submit pressed")
                    self.presenter.translate(values['source_text'], self.source_language, self.target_language)

                case 'clear' | 'alt-L-c':
                    for key in ['comment', 'quality', 'source_text', 'target_text']:
                             self.update_element(key, '')
                    self.update_element('source text label', 'Enter source text:' )
                    self.update_element('target text label', 'Target text:')

                case 'set_key':
                    self.set_key()

            if event == sg.WIN_CLOSED or event == 'Exit':
                break

        self.window.close()

    def _save_language_settings(self):
        settings = {
            "source language": self.source_language,
            "target language": self.target_language
        }

        with open('settings.json', 'w') as file:
            json.dump(settings, file)

        print("LOG-V: settings saved: ", self.source_language, self.target_language)
        self.update_element('comment', "Settings saved!")

    def _load_language_settings(self):
        with open('settings.json', 'r') as file:
            try:
                language_settings_file = json.load(file)
                self.source_language = language_settings_file['source language']
                self.target_language = language_settings_file['target language']
                self.window['combo_source_lang'].update(value=self.source_language)
                self.window['combo_target_lang'].update(value=self.target_language)
                print("LOG-V: settings loaded: ", self.source_language, self.target_language)
                self.update_element('comment', "Settings loaded!")

            except Exception as e:
                show_info("error", e)

    def update_element(self, key, text):
        self.window[key].update(value=text)

    def set_key(self):
        event, values = sg.Window('Login Window',
                                  [[sg.T('Enter your API key'), sg.In(key='apikey')],
                                   [sg.B('OK'), sg.B('Cancel')]]).read(close=True)
        if event == 'OK':
            api_key = values['apikey']
            settings = {
                "api key": api_key
            }
            with open('key.json', 'w') as file:
                json.dump(settings, file)

            self.update_element('comment', "Key saved!")

            self.presenter.reset_model()

