import key

APIKey = key.key
model = Model(APIKey)
view = View()
pres = Presenter(model, view)
model.set_presenter(pres)
view.set_presenter(pres)
view.show()
