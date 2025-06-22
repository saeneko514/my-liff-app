from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import requests
import os

# 環境変数から設定を取得
SHEETY_ID = os.environ.get("SHEETY_ID")
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("CHANNEL_ACCESS_TOKEN")
SHEETY_ENDPOINT = f"https://api.sheety.co/{SHEETY_ID}/新しい自己肯定感スコアアプリ測定結果/useragreement"

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/agreement", methods=["POST"])
def agreement():
    data = request.json
    print("[POST /api/agreement] 受信データ:", data)

    useragreement = data.get("useragreement", {})
    user_id = useragreement.get("userId")
    display_name = useragreement.get("displayName")

    # 日本時間で現在の日付（年月日だけ）
    now = datetime.utcnow() + timedelta(hours=9)
    timestamp = now.strftime("%Y-%m-%d")

    if not user_id or not display_name:
        return jsonify({"status": "error", "message": "userId または displayName がありません"}), 400

    payload = {
        "useragreement": {
            "userId": user_id,
            "displayName": display_name,
            "agreedAt": timestamp
        }
    }

    try:
        # Sheety に保存
        response = requests.post(SHEETY_ENDPOINT, json=payload)
        if response.status_code not in [200, 201]:
            print(f"[ERROR] Sheety Error: {response.text}")
            return jsonify({"status": "error", "message": response.text}), 500

        print(f"[SAVED] {user_id} at {timestamp}")

        # LINEへ Push メッセージ送信
        headers = {
            "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        push_payload = {
            "to": user_id,
            "messages": [{
                "type": "text",
                "text": f"{display_name}さん、ご同意ありがとうございます！\n本日も感情日記をよろしくお願いします😊"
            }]
        }
        push_response = requests.post("https://api.line.me/v2/bot/message/push",
                                      headers=headers, json=push_payload)

        print("[PUSH RESULT]", push_response.status_code, push_response.text)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print(f"[EXCEPTION] {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
