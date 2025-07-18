from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/test')
def test_api():
    return jsonify({'message': 'Flask backend is working!'})

if __name__ == '__main__':
    app.run(debug=True)