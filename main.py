import model, view, presenter, json


def read_api_key():
    with open('key.json', 'r') as file:
        try:
            settings_file = json.load(file)
            return settings_file['api key']
        except:
            print("ERROR-P: can not load api key!")
            return ''


key = read_api_key()

presenter.Presenter(key)