import pyperclip as clip
from modernmt import ModernMT

class Model:
    def __init__(self, key):
        self.mmt = ModernMT(key)
        self.presenter = None
        self.source_lang = ''
        self.target_lang = ''
        print("LOG-M: Model init ok")

    def set_presenter(self, pres):
        self.presenter = pres

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
                raise
