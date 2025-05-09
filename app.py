from flask import Flask, request
import os
import json
import alpaca_trade_api as tradeapi

# Initialize the Flask application
app = Flask(__name__)

# Load Alpaca API credentials from environment variables
API_KEY = os.getenv("APCA_API_KEY_ID")
SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"

# Initialize Alpaca API client
api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

# Webhook endpoint to receive TradingView alerts
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()

        # Log the webhook data for debugging
        print(f"Webhook received: {json.dumps(data, indent=2)}")

        symbol = data.get('symbol')
        action = data.get('action')
        quantity = data.get('quantity', 1)  # default to 1 if not provided

        if not symbol or not action:
            return "Invalid data", 400

        if action == 'buy':
            api.submit_order(
                symbol=symbol,
                qty=quantity,
                side='buy',
                type='market',
                time_in_force='gtc',
                extended_hours=True
            )
            print(f"Buy order placed for {quantity} shares of {symbol}")

        elif action == 'sell':
            api.submit_order(
                symbol=symbol,
                qty=quantity,
                side='sell',
                type='market',
                time_in_force='gtc',
                extended_hours=True
            )
            print(f"Sell order placed for {quantity} shares of {symbol}")

        else:
            return "Invalid action", 400

        return 'Webhook received and processed', 200

    except Exception as e:
        print(f"Error: {e}")
        return "Error processing the webhook", 500

# Run the app on the appropriate port for Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
