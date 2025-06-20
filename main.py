from flask import Flask, request, render_template, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/agreement", methods=["POST"])
def agreement():
    data = request.json
    user_id = data.get("userId")
    timestamp = data.get("agreedAt", datetime.utcnow().isoformat())

    # ここでDBに保存（例：Supabase, Firestore, Google Sheets など）
    print(f"[AGREEMENT] {user_id} agreed at {timestamp}")

    return jsonify({"status": "success"}), 200