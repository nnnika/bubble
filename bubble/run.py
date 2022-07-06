from flask_cors import CORS
from bubble.api import app

CORS(app, supports_credentials=True)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')