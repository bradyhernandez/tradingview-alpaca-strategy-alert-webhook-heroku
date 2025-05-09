from flask import Flask, request
import os
import json
import alpaca_trade_api as tradeapi

# Initialize the Flask application
app = Flask(__name__)

# Alpaca API keys (make sure to set them as environment variables in Render)
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

# Initialize Alpaca API client
api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, base_url="https://paper-api.alpaca.markets")

# Define the /webhook route to handle TradingView alerts
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()  # Get JSON data sent by TradingView

        # Print data for debugging
        print(f"Webhook received: {json.dumps(data, indent=2)}")

        # Example: Check if the alert contains specific information (e.g., action and symbol)
        symbol = data.get('symbol')
        action = data.get('action')
        quantity = data.get('quantity', 1)  # Default to 1 if quantity is not provided

        if not symbol or not action:
            return "Invalid data", 400

        # Example: Trade logic based on the action received (buy or sell)
        if action == 'buy':
            # Example: Buying the specified symbol
            api.submit_order(
                symbol=symbol,
                qty=quantity,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            print(f"Buy order placed for {quantity} shares of {symbol}")

        elif action == 'sell':
            # Example: Selling the specified symbol
            api.submit_order(
                symbol=symbol,
                qty=quantity,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
            print(f"Sell order placed for {quantity} shares of {symbol}")

        else:
            return "Invalid action", 400

        return 'Webhook received and processed', 200

    except Exception as e:
        print(f"Error: {e}")
        return "Error processing the webhook", 500


# Ensure the app listens on the correct port (port 10000 on Render)
if __name__ == '__main__':
    # Get the port from the environment variable (Render sets this automatically)
    port = int(os.environ.get('PORT', 10000))  # Default to 10000 if no PORT is set
    app.run(host='0.0.0.0', port=port)  # Make sure it listens on all available interfaces (0.0.0.0)
