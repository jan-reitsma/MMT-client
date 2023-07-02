import pyperclip as clip
from modernmt import ModernMT

class Model:
    def __init__(self, APIKey):
        self.mmt = ModernMT(APIKey)
        self.presenter = None
        self.source_lang = ''
        self.target_lang = ''
        print("Model init ok")

    def set_presenter(self, pres):
        self.presenter = pres

    def translate(self, src, src_lang, trg_lang):
        print("model translate")
        detected = ''
        # translate with source and target language:
        if src == "":
            self.presenter.update_element('comment', "error, source can not be empty.")
        else:
            if src_lang == "auto":
                try:
                    response = self.mmt.detect_language(src)
                    src_lang = response.detectedLanguage
                    detected = 'Source language detected: ' + src_lang + '. '
                    print("detected", detected)
                except Exception as e:
                    print(e)
                    self.presenter.show_message("error", e)

            try:
                result = self.mmt.translate(src_lang, trg_lang, src)
                translation = result.translation
                print("translation", translation)
                quality_estimation = self.mmt.qe(src_lang, trg_lang, src, translation)
                score = f"Quality estimation: {quality_estimation.score}"

                # copy translation to clipboard
                clip.copy(translation)

                # filling the fields in the GUI
                self.presenter.update_element('quality', score)
                self.presenter.update_element('target_text', translation)

                comment_string = detected + 'Translation copied to clipboard.'
                self.presenter.update_element('comment', comment_string)

            except Exception as e:
                print(e)
                self.presenter.show_message("error", e)
                raise
