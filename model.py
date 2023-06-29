import pyperclip as clip
from modernmt import ModernMT
import json


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
        detected = ''
        # reset all fields:
        self.presenter.reset_fields()
        # translate with source and target language:
        if src == "":
            self.presenter.set_field('self.comment', 'text', "Error: no text to translate")
        if src_lang == "auto":
            try:
                response = self.mmt.detect_language(src)
                src_lang = response.detectedLanguage
                detected = 'Source language detected: ' + src_lang + '. '
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
            self.presenter.set_quality(score)
            self.presenter.set_output_text(translation)
            comment_string = detected + 'Translation copied to clipboard.'
            self.presenter.set_comment(comment_string)

        except Exception as e:
            print(e)
            self.presenter.show_message("error", e)
            raise
