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

@app.route('/draw', methods=['GET'])
def draw_cards():
    count = int(request.args.get("count", 1))
    cards = random.sample(tarot_cards, count)
    return jsonify(cards)

@app.route('/preview', methods=['GET'])
def preview_cards():
    html_template = Template("""
    <html><head><meta charset="utf-8"><title>塔羅牌預覽</title></head><body>
    <h1>抽到的塔羅牌：</h1>
    <ul>{% for card in cards %}<li>{{ card.name }} - {{ card.meaning }}</li>{% endfor %}</ul>
    </body></html>
    """)
    sample_cards = tarot_cards[:3] if len(tarot_cards) >= 3 else tarot_cards
    return html_template.render(cards=sample_cards)

@app.route('/generate_pdf', methods=['GET'])
def generate_pdf():
    template = Template("""
    <html><head><meta charset="utf-8"><style>body { font-family: sans-serif; }</style></head><body>
    <h1>你的塔羅解讀報告</h1>
    <p>生成時間：{{ time }}</p>
    <ul>{% for card in cards %}<li>{{ card.name }} - {{ card.meaning }}</li>{% endfor %}</ul>
    </body></html>
    """)
    selected = tarot_cards[:3] if len(tarot_cards) >= 3 else tarot_cards
    html = template.render(cards=selected, time=str(datetime.datetime.now()))
    output_path = "/tmp/tarot_report.pdf"
    HTML(string=html).write_pdf(output_path)
    return send_file(output_path, download_name="tarot_report.pdf", as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)