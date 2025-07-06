from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import random
import os
import json
from jinja2 import Template
from weasyprint import HTML

app = Flask(__name__)
CORS(app)

# 載入塔羅牌資料
TAROT_PATH = os.environ.get("TAROT_JSON_PATH", "Tarot_Major_Arcana_Full.json")
try:
    with open(TAROT_PATH, encoding="utf-8") as f:
        tarot_cards = json.load(f)
except Exception as e:
    print("❌ 讀取 JSON 失敗：", e)
    tarot_cards = []

def draw_card(force_upright=False):
    card = random.choice(tarot_cards)
    is_reversed = False if force_upright else random.choice([True, False])
    card["reversed"] = is_reversed
    return card

@app.route("/")
def home():
    return "🔮 Ethan Tarot API 啟動成功"
    
@app.route("/draw", methods=["GET"])
def draw_one():
    force_upright = request.args.get("force_upright", "false").lower() == "true"
    return jsonify([draw_card(force_upright)])

@app.route("/draw/3", methods=["GET"])
def draw_three():
    force_upright = request.args.get("force_upright", "false").lower() == "true"
    cards = random.sample(tarot_cards, 3)
    for c in cards:
        c["reversed"] = False if force_upright else random.choice([True, False])
    return jsonify(cards)

@app.route("/report", methods=["POST"])
def generate_report():
    card = request.json.get("card")
    if not card:
        return jsonify({"error": "缺少 card 資料"}), 400

    template_str = '''
    <h1>你的塔羅報告</h1>
    <p>抽到的牌：<strong>{{ card.name }}</strong> {% if card.reversed %}（逆位）{% endif %}</p>
    <div style="border: 1px solid #888; padding: 10px;">
        <p><strong>主題：</strong>{{ card.theme }}</p>
        <p><strong>關鍵字：</strong>{{ card.keywords | join(", ") }}</p>
        <p><strong>解釋：</strong>{{ card.reversed_meaning if card.reversed else card.meaning }}</p>
    </div>
    <p style="margin-top:30px;font-size:12px;">Ethan Tarot AI • www.ethantarot.ai</p>
    '''

    html = Template(template_str).render(card=card)
    HTML(string=html).write_pdf("/tmp/report.pdf")
    return send_file("/tmp/report.pdf", as_attachment=True, download_name="tarot_report.pdf")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
