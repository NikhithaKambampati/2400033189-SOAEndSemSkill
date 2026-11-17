import os
import time
from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "app-db"),
    "dbname": os.getenv("DB_NAME", "demo_db"),
    "user": os.getenv("DB_USER", "demo_user"),
    "password": os.getenv("DB_PASSWORD", "demo_pass"),
    "port": int(os.getenv("DB_PORT", "5432")),
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def initialize_database():
    for attempt in range(15):
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS messages (
                            id SERIAL PRIMARY KEY,
                            message TEXT NOT NULL
                        )
                    """)
                    cur.execute("SELECT COUNT(*) FROM messages")
                    if cur.fetchone()[0] == 0:
                        cur.execute(
                            "INSERT INTO messages (message) VALUES (%s)",
                            ("Hello from the Dockerized microservice!",)
                        )
            print("Database initialized successfully.")
            return
        except psycopg2.OperationalError:
            print(f"Waiting for database... ({attempt + 1}/15)")
            time.sleep(2)
    raise RuntimeError("Could not connect to PostgreSQL.")

@app.get("/")
def home():
    return jsonify({
        "status": "running",
        "service": "app-service",
        "message": "Microservice is running. Visit /api/data"
    })

@app.get("/api/data")
def get_data():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id, message FROM messages ORDER BY id")
            rows = cur.fetchall()
    return jsonify({
        "status": "success",
        "message": "Connected to PostgreSQL successfully",
        "data": rows
    })

@app.post("/api/data")
def add_data():
    body = request.get_json(silent=True) or {}
    message = body.get("message")
    if not message:
        return jsonify({"status": "error", "message": "Provide a message field"}), 400
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "INSERT INTO messages (message) VALUES (%s) RETURNING id, message",
                (message,)
            )
            created = cur.fetchone()
    return jsonify({"status": "success", "data": created}), 201

if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=8080)
