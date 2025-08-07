from flask import Blueprint, request, jsonify
import openai
import os

ssto_bp = Blueprint('ssto', __name__, url_prefix='/ssto')

# Correct API Key setup
openai.api_key = os.getenv("OPENAI_API_KEY")

# ----------------------------
# /gpt_autofill Route
# ----------------------------

@ssto_bp.route('/gpt_autofill', methods=['POST'])
def gpt_autofill():
    try:
        data = request.get_json()

        ticker = data.get('ticker')
        summary = data.get('summary')

        if not ticker or not summary:
            return jsonify({'status': 'error', 'message': 'Missing ticker or summary'}), 400

        prompt = (
            f"Analyze the following trading signal summary and suggest the best entry price, stop loss, take profit, "
            f"confidence score (0-100), and rationale.\n\n"
            f"Ticker: {ticker}\n"
            f"Summary: {summary}\n\n"
            f"Respond ONLY in JSON format like:\n"
            f"{{'entry_price': ..., 'stop_loss': ..., 'take_profit': ..., 'confidence': ..., 'rationale': '...'}}"
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional trading assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=500
        )

        raw_reply = response['choices'][0]['message']['content'].strip()

        result = eval(raw_reply)

        return jsonify({
            'status': 'ok',
            'ticker': ticker,
            'entry_price': result.get('entry_price'),
            'stop_loss': result.get('stop_loss'),
            'take_profit': result.get('take_profit'),
            'confidence': result.get('confidence'),
            'rationale': result.get('rationale')
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ----------------------------
# /submit_order Route
# ----------------------------

@ssto_bp.route('/submit_order', methods=['POST'])
def submit_order():
    try:
        data = request.get_json()

        required_fields = ["ticker", "entry_price", "stop_loss", "take_profit", "confidence", "rationale"]

        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'status': 'error',
                'message': f'Missing fields: {", ".join(missing_fields)}'
            }), 400

        ticker = data['ticker']
        entry_price = data['entry_price']
        stop_loss = data['stop_loss']
        take_profit = data['take_profit']
        confidence = data['confidence']
        rationale = data['rationale']

        simulated_order = {
            'ticker': ticker,
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'confidence': confidence,
            'rationale': rationale,
            'order_status': 'simulated_accepted'
        }

        return jsonify({
            'status': 'ok',
            'order': simulated_order
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
