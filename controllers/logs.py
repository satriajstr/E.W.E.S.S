from flask import Blueprint, jsonify
from db import get_db

logs_api = Blueprint("logs_api", __name__)

@logs_api.route("/api/logs", methods=["GET"])
def get_logs():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                sensor_id,
                start_time,
                end_time,
                duration_sec,
                max_intensity,
                avg_intensity,
                created_at
            FROM quake_logs
            ORDER BY id DESC
            LIMIT 50
        """)

        rows = cursor.fetchall()

        cursor.close()
        db.close()

        # --- MAP KE FORMAT DASHBOARD LAMA ---
        converted = []
        for r in rows:
            converted.append({
                "timestamp": r["start_time"],
                "shake": 1,
                "intensity": r["max_intensity"],
                "duration": r["duration_sec"]
            })

        return jsonify(converted), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
