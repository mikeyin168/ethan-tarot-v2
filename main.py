
import json
import random
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

TAROT_PATH = os.environ.get("TAROT_JSON_PATH", "Tarot_Major_Arcana_Full.json")

try:
    with open(TAROT_PATH, encoding="utf-8") as f:
        tarot_cards = json.load(f)
except Exception as e:
    print("❌ 讀取 JSON 失敗：", e)
    tarot_cards = []

@app.route("/")
def index():
    return "Ethan Tarot API 正常運作中"

@app.route("/draw")
def draw_one():
    reversed_enabled = request.args.get("reversed", "true").lower() != "false"
    card = random.choice(tarot_cards)
    is_reversed = reversed_enabled and random.choice([True, False])
    return jsonify(format_card(card, is_reversed))

@app.route("/draw/3")
def draw_three():
    reversed_enabled = request.args.get("reversed", "true").lower() != "false"
    selected = random.sample(tarot_cards, 3)
    fields = ["Love", "Career", "Future"]
    result = []
    for i, card in enumerate(selected):
        is_reversed = reversed_enabled and random.choice([True, False])
        formatted = format_card(card, is_reversed)
        formatted["position"] = fields[i]
        result.append(formatted)
    return jsonify(result)

def format_card(card, is_reversed):
    result = {
        "id": card.get("id"),
        "name": card.get("name"),
        "theme": card.get("theme"),
        "keywords": card.get("keywords"),
        "position": "正位" if not is_reversed else "逆位",
        "meaning": card.get("meaning") if not is_reversed else card.get("reversed_meaning"),
        "english": simulate_english_reading(card, is_reversed),
    }
    return result

def simulate_english_reading(card, is_reversed):
    base = f"You drew **{card.get('name')}** ({'Upright' if not is_reversed else 'Reversed'}).\n"
    if is_reversed:
        base += "This card reveals a shadow aspect or lesson you’re being invited to explore.\n"
        base += f"💡 *{card.get('reversed_meaning')}*"
    else:
        base += "This card brings light and encouragement for your current journey.\n"
        base += f"🌞 *{card.get('meaning')}*"
    return base

if __name__ == "__main__":
    app.run(debug=True)
