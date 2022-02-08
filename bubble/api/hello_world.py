from flask import Flask
from flask_cors import CORS

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    app.run(debug=True, port=8889, host='0.0.0.0')