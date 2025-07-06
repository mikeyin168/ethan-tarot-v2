
from flask import Flask, request, jsonify, send_file
import os
import random
import datetime
from jinja2 import Template
from weasyprint import HTML
import json

app = Flask(__name__)

print("🚀 Ethan Tarot API 啟動中...")
print("📁 嘗試讀取塔羅 JSON 檔案...")

TAROT_PATH = os.environ.get("TAROT_JSON_PATH", "Tarot_Major_Arcana_Full.json")
try:
    with open(TAROT_PATH, encoding="utf-8") as f:
        tarot_cards = json.load(f)
        print("✅ 成功讀取 tarot_cards，共", len(tarot_cards), "張牌")
except Exception as e:
    print("❌ 讀取 JSON 失敗：", e)
    tarot_cards = []

@app.route("/")
def index():
    return "Ethan Tarot API is running!"

@app.route("/draw", methods=["GET", "POST"])
def draw():
    if not tarot_cards:
        return jsonify({"error": "No tarot cards loaded."}), 500

    card = random.choice(tarot_cards)
    return jsonify({"card": card})

if __name__ == "__main__":
    app.run(debug=True)
