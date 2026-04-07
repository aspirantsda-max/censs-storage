from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

users = {"censs": "censs@1234"}

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if users.get(data["username"]) == data["password"]:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
