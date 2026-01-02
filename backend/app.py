from flask import Flask, jsonify, request
from flask_cors import CORS
from pytrends.request import TrendReq

app = Flask(__name__)
CORS(app)  # allows requests from your React app

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.get("/api/echo")
def echo():
    term = request.args.get("term", "")
    return jsonify({"term": term, "message": "Flask is working!"})

@app.get("/api/trends")
def trends():
    term = request.args.get("term", "").strip()
    if not term:
        return jsonify({"error": "Missing required query param: term"}), 400

    pytrends = TrendReq(hl="en-US", tz=360)
    pytrends.build_payload([term], timeframe="today 3-m", geo="US")
    df = pytrends.interest_over_time()

    if df.empty:
        return jsonify({"term": term, "points": []})

    points = [
        {"date": idx.strftime("%Y-%m-%d"), "value": int(row[term])}
        for idx, row in df.iterrows()
    ]

    return jsonify({
        "term": term,
        "timeframe": "today 3-m",
        "geo": "US",
        "points": points
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
