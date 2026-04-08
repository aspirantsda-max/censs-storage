from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# dummy user (you can later replace with DB)
users = {
    "censs": "censs@1234"
}

@app.route("/")
def home():
    return "API is running 🚀"

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if users.get(username) == password:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)