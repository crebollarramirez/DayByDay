from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS with specific settings
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow all origins for /api/* endpoints

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"message": "Hello from Flask! THis is a test and it works"})

if __name__ == '__main__':
    app.run(port=5000)