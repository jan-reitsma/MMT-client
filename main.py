import model, view, presenter, json

def read_api_key():
    with open('key.json', 'r') as file:
        try:
            settings_file = json.load(file)
            api_key = settings_file['api key']

            return settings_file['api key']
        except:
            print("ERROR MAIN: can not load api key!")

key = read_api_key()
model = model.Model(key)
view = view.View()
pres = presenter.Presenter(model, view)

model.set_presenter(pres)
view.set_presenter(pres)
view.show()
