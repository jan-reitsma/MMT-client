import pyperclip as clip
import json
from modernmt import ModernMT

# in class Model, read key file. If no key file or wrong key file, warning to presenter, to view.
# 1 . create model, model reads file.
# 2. if ok, then continue
# 3. if file not exist of corrupt, send message to presenter
# 4. in this case presenter lets view display popup
# 5. if popupclosed, view sends message to presenter, presenter updates model

class Model:
    def __init__(self):
        self.mmt = None
        self.presenter = None
        self.source_lang = ''
        self.target_lang = ''

    def set_presenter(self, pres):
        self.presenter = pres

    def set_engine(self):
        try:
            with open('key.json', 'r') as file:
                try:
                    settings_file = json.load(file)
                    key = settings_file['api key']
                except json.decoder.JSONDecodeError:
                    print("LOG-M: Model error: json file is bad")
                    return False
                except KeyError:
                    return False
        except FileNotFoundError:
            print("LOG-M: Key file not found")
            return False
        self.mmt = ModernMT(key)
        print("LOG-M: Model engine init")
        return True


    def translate(self, src, src_lang, trg_lang):
        # translate with source and target language:
        if src == "":
            self.presenter.update_element('comment', "Source can not be empty!")
        else:
            if src_lang == "auto":
                try:
                    response = self.mmt.detect_language(src)
                    src_lang = response.detectedLanguage
                    print("LOG-M: language detected:", src_lang)

                except Exception as e:
                    print(e)
                    self.presenter.show_message("error", e)
                    raise

            try:
                result = self.mmt.translate(src_lang, trg_lang, src)
                translation = result.translation
                quality_estimation = self.mmt.qe(src_lang, trg_lang, src, translation)
                score = f"Quality estimation: {quality_estimation.score}"

                # copy translation to clipboard
                clip.copy(translation)

                # filling the fields in the GUI
                self.presenter.update_element('source text label', 'Source text (' + src_lang + '):')
                self.presenter.update_element('target text label', 'Target text (' + trg_lang +'):')
                self.presenter.update_element('target_text', translation)
                self.presenter.update_element('quality', score)
                self.presenter.update_element('comment', 'Translation copied to clipboard')

            except Exception as e:
                print(e)
                self.presenter.show_message("error", e)