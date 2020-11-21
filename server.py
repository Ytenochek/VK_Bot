from flask import Flask, request

from keeper import JSON

app = Flask(__name__)


@app.route("/", methods=["POST"])
def webhook():
    if request.is_json:
        data = request.get_json()
        if data.get("secret") == "very_secret_key_lol":
            if data["type"] == "confirmation":
                return "60d64264"
            if type(data) == list:
                JSON.extend(data)
            else:
                JSON.append(data)
            return "ok"
    return "Forbidden"


def run():
    app.run(host="0.0.0.0", port=5000, debug=False)
