import key, model, view, presenter

APIKey = key.key
model = model.Model(APIKey)
view = view.View()
pres = presenter.Presenter(model, view)

model.set_presenter(pres)
view.set_presenter(pres)
view.show()
