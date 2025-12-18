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
                event_id,
                sensor_id,
                start_time,
                end_time,
                duration_sec,
                max_intensity,
                avg_intensity,
                created_at
            FROM quake_logs
            ORDER BY event_id DESC
            LIMIT 50
        """)

        rows = cursor.fetchall()

        cursor.close()
        db.close()

        return jsonify([
            {
                "event_id": r["event_id"],
                "sensor_id": r["sensor_id"],
                "start_time": r["start_time"],
                "end_time": r["end_time"],
                "duration_sec": r["duration_sec"],
                "max_intensity": r["max_intensity"],
                "avg_intensity": r["avg_intensity"]
            }
            for r in rows
        ]), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
