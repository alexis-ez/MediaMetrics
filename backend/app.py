from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allows requests from your React app

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.get("/api/echo")
def echo():
    term = request.args.get("term", "")
    return jsonify({"term": term, "message": "Flask is working!"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
