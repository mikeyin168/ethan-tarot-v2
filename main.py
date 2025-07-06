from flask import Flask, request, jsonify, send_file
import os
import random
import datetime
from jinja2 import Template
from weasyprint import HTML
import json

app = Flask(__name__)

print("🚀 Ethan Tarot API 啟動中...")
print("📂 嘗試讀取塔羅 JSON 檔案...")

TAROT_PATH = os.environ.get("TAROT_JSON_PATH", "Tarot_Major_Arcana_Full.json")
try:
    with open(TAROT_PATH, encoding="utf-8") as f:
        tarot_cards = json.load(f)
    print("✅ 成功讀取 tarot_cards，共", len(tarot_cards), "張牌")
except Exception as e:
    print("❌ 讀取 JSON 失敗：", e)
    tarot_cards = []

three_card_template = Template("""
<html><body>
<h1>{{ title }}</h1>
<p>{{ client_name }} • {{ date }}</p>
{% for card in cards %}
<div>
  <h2>{{ card.position }} - {{ card.card_name }} ({{ card.orientation }})</h2>
  <p><b>Keywords:</b> {{ card.keywords }}</p>
  <p>{{ card.meaning }}</p>
</div>
{% endfor %}
<p><strong>{{ closing }}</strong></p>
<p>Ethan Tarot AI • www.ethantarot.ai</p>
</body></html>
""")

def draw_cards(n):
    selected = random.sample(tarot_cards, n)
    output = []
    for i, card in enumerate(selected):
        orientation = random.choice(["Upright", "Reversed"])
        meaning = card["upright_meaning"] if orientation == "Upright" else card["reversed_meaning"]
        output.append({
            "position": ["Past", "Present", "Future"][i] if n == 3 else "Card",
            "card_name": card["name"],
            "orientation": orientation,
            "keywords": ", ".join(card["keywords"]) if isinstance(card["keywords"], list) else card["keywords"],
            "meaning": meaning
        })
    return output

@app.route("/draw", methods=["POST"])
def draw():
    data = request.get_json()
    name = data.get("client_name", "Guest")
    count = int(data.get("draw_count", 3))

    cards = draw_cards(count)
    today = datetime.date.today().isoformat()

    html = three_card_template.render(
        title="Your Tarot Report",
        client_name=name,
        date=today,
        cards=cards,
        closing="May this reading guide your next steps."
    )

    filename = f"tarot_report_{random.randint(1000,9999)}.pdf"
    filepath = f"./output/{filename}"
    os.makedirs("./output", exist_ok=True)
    HTML(string=html).write_pdf(filepath)

    return jsonify({
        "pdf_path": filepath,
        "cards": cards
    })

@app.route("/get_report/<filename>", methods=["GET"])
def get_report(filename):
    return send_file(f"./output/{filename}", as_attachment=True)

@app.route("/ping", methods=["GET"])
def ping():
    return "Pong from Ethan Tarot API", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)