from flask import Flask, request, jsonify
import os
import pyodbc

app = Flask(__name__)

# SQL Connection String from environment variable
CONN_STR = os.environ.get("SQL_CONNECTION_STRING")

def get_conn():
    return pyodbc.connect(CONN_STR, autocommit=False)

@app.route("/")
def index():
    return "Todo App is Running in Codespaces!"

@app.route("/add", methods=["POST"])
def add():
    try:
        data = request.json
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Employees (FirstName, LastName, Email) VALUES (?, ?, ?)",
            data["first"], data["last"], data["email"]
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

