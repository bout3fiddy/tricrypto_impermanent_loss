from flask import Flask, jsonify

from projects.api.route.liquidity_txes import get_added_liquidity
from projects.api.route.current_position import get_tricrypto_liquidity_positions


app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"about": "TriCrypto Curve Tracker"})


@app.route("/user/historical_added_liquidity/<user_address>")
def fetch_added_liquidity(user_address):
    added_liquidity = get_added_liquidity(address=user_address)
    return jsonify(added_liquidity)


@app.route("/user/current_lp_values/<user_address>")
def calculate_current_positions(user_address):
    current_position = get_tricrypto_liquidity_positions(user_addr=user_address)
    return jsonify(current_position)


if __name__ == "__main__":
    app.run(debug=True)
