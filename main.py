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
    count = int(request.args.get("count", 1))
    cards = random.sample(tarot_cards, count)
    return jsonify(cards)

@app.route("/pdf", methods=["GET"])
def generate_pdf():
    if not tarot_cards:
        return "Tarot cards not loaded", 500

    card = random.choice(tarot_cards)
    orientation = random.choice(["正位", "逆位"])
    meaning = card["upright_meaning"] if orientation == "正位" else card["reversed_meaning"]

    html_template = f"""
    <html><head><meta charset="utf-8"><style>
    body {{ font-family: sans-serif; padding: 40px; }}
    h1 {{ color: #333; }}
    .card {{ border: 1px solid #999; padding: 20px; margin-top: 20px; }}
    </style></head><body>
    <h1>你的塔羅報告</h1>
    <p>抽到的牌：<strong>{card['name']}</strong>（{orientation}）</p>
    <div class="card">
        <p><strong>主題：</strong>{card.get("theme", "")}</p>
        <p><strong>關鍵字：</strong>{", ".join(card.get("keywords", []))}</p>
        <p><strong>解釋：</strong>{meaning}</p>
    </div>
    <p style="margin-top:40px;font-size:0.9em;color:#888;">Ethan Tarot AI ∘ www.ethantarot.ai</p>
    </body></html>
    """

    output_path = "/tmp/tarot_report.pdf"
    HTML(string=html_template).write_pdf(output_path)
    return send_file(output_path, as_attachment=True, download_name="tarot_report.pdf")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)