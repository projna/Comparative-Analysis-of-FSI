import flask


def downloadOwl():
    url = './spofood/'
    filename = "spo-food.owl"
    return flask.send_from_directory(url, filename, as_attachment=True)
