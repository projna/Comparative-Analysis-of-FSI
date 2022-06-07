from flask import Flask
from controller import Index, Indicator, downloadowl

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './ontology'
app.config['SECRET_KEY'] = 'your secret key'


# @app.route("/")
@app.route("/")
def index():
    return Index.index()


@app.route("/savefile", methods=['POST', 'GET'])
def savefile():
    return Index.savefile()


@app.route('/result', methods=['POST', 'GET'])
def result():
    return Indicator.result()


@app.route('/downloadowl', methods=['POST', 'GET'])
def downloadOwl():
    return downloadowl.downloadOwl()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
# do something with app...
