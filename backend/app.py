from flask import Flask
from flask_cors import CORS
from routes import api  # ✅ import the blueprint

app = Flask(__name__)
CORS(app)

app.register_blueprint(api)  # ✅ register blueprint

if __name__ == '__main__':
    app.run(debug=True)
