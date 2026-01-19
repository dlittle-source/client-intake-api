from flask import Flask, request, jsonify
from db import init_db, get_connection

app = Flask(__name__)
init_db()

@app.route("/health")
def health():
    return jsonify(status="ok")

@app.route("/clients", methods=["POST"])
def create_client():
    data = request.get_json()

    if not data or "name" not in data or "email" not in data:
        return jsonify(error="Invalid payload"), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO clients (name, email) VALUES (?, ?)",
        (data["name"], data["email"])
    )
    conn.commit()
    conn.close()

    return jsonify(message="Client created"), 201

if __name__ == "__main__":
    app.run(debug=True)
