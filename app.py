from flask import Flask, request
import os
import json
import alpaca_trade_api as tradeapi

app = Flask(__name__)

# Load Alpaca credentials from environment variables
API_KEY = os.getenv('APCA_API_KEY_ID')
SECRET_KEY = os.getenv('APCA_API_SECRET_KEY')
BASE_URL = os.getenv('APCA_API_BASE_URL', 'https://paper-api.alpaca.markets')  # default to paper trading

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')


@app.route('/')
def index():
    return "Webhook listener running. POST alerts to /webhook."


@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        print(f"Webhook received:\n{json.dumps(data, indent=2)}")

        symbol = data['symbol']
        action = data['action'].lower()
        quantity = int(data.get('quantity', 1))

        if action not in ['buy', 'sell']:
            return f"Invalid action: {action}", 400

        order = api.submit_order(
            symbol=symbol,
            qty=quantity,
            side=action,
            type='market',
            time_in_force='gtc'
        )
        print(f"Order submitted: {order}")
        return f"{action.upper()} order for {quantity} shares of {symbol} placed.", 200

    except Exception as e:
        print(f"Error processing webhook: {e}")
        return "Error processing the webhook", 500


# Required for Render — bind to the port Render sets
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # default to 10000 if PORT is not set
    app.run(host='0.0.0.0', port=port)
