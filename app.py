from flask import Flask, jsonify

from projects.api.route.liquidity_txes import get_added_liquidity

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"about": "TriCrypto Curve Tracker"})


# adding variables
@app.route("/user/<user_address>")
def post_added_liquidity(user_address):
    added_liquidity = get_added_liquidity(address=user_address)
    return jsonify(added_liquidity)


if __name__ == "__main__":
    app.run(debug=True)
