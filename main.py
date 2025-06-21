from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from datetime import datetime
import requests
import os

SHEETY_ID = os.environ["SHEETY_ID"]
SHEETY_ENDPOINT = f"https://api.sheety.co/{SHEETY_ID}/新しい自己肯定感スコアアプリ測定結果/userAgreement"

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/agreement", methods=["POST"])
def agreement():
    data = request.json
    print("[POST /api/agreement] 受信データ:", data)
    user_id = data.get("userId")
    display_name = data.get("displayName")  
    timestamp = data.get("agreedAt", datetime.utcnow().isoformat())

    if not user_id or not display_name:
        return jsonify({"status": "error", "message": "userId または displayName がありません"}), 400

    payload = {
        "userAgreement": {
            "userId": user_id,
            "displayName": display_name,
            "agreedAt": timestamp
        }
    }

    try:
        response = requests.post(SHEETY_ENDPOINT, json=payload)
        if response.status_code in [200, 201]:
            print(f"[SAVED] {user_id} at {timestamp}")
            return jsonify({"status": "success"}), 200
        else:
            print(f"[ERROR] {response.text}")
            return jsonify({"status": "error", "message": response.text}), 500
    except Exception as e:
        print(f"[EXCEPTION] {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
