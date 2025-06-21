from flask import Flask, request, render_template, jsonify
from datetime import datetime
import requests
import os

SHEETY_ID = os.environ["SHEETY_ID"]
SHEETY_ENDPOINT = f"https://api.sheety.co/{SHEETY_ID}/新しい自己肯定感スコアアプリ測定結果/userAgreement"

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/agreement", methods=["POST"])
def agreement():
    data = request.json
    user_id = data.get("userId")
    display_name = data.get("displayName")  # ← 追加
    timestamp = data.get("agreedAt", datetime.utcnow().isoformat())

    if not user_id or not display_name:
        return jsonify({"status": "error", "message": "userId または displayName がありません"}), 400

    payload = {
        "userdata": {
            "userId": user_id,
            "displayName": display_name,  # ← 追加
            "agreedAt": timestamp
        }
    }

    # Sheety に POST
    response = requests.post(SHEETY_ENDPOINT, json=payload)

    if response.status_code in [200, 201]:
        print(f"[SAVED] {user_id} at {timestamp}")
        return jsonify({"status": "success"}), 200
    else:
        print(f"[ERROR] {response.text}")
        return jsonify({"status": "error", "message": response.text}), 500
