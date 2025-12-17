from flask import Blueprint, request, jsonify
from db import get_db
from datetime import datetime

realtime_api = Blueprint("realtime_api", __name__)


# ------------------------------------------------------
# POST /api/realtime
# Update status sensor per detik
# ------------------------------------------------------
@realtime_api.route("/api/realtime", methods=["POST"])
def post_realtime():
    try:
        data = request.json

        sensor_id = data.get("sensor_id")
        shake = 1 if data.get("shake") else 0
        intensity = data.get("intensity")
        duration = data.get("duration")

        # Backend menentukan timestamp realtime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        db = get_db()
        cursor = db.cursor()

        query = """
            UPDATE realtime_status
            SET shake = %s,
                intensity = %s,
                duration = %s,
                timestamp = %s
            WHERE sensor_id = %s
        """

        cursor.execute(query, (shake, intensity, duration, timestamp, sensor_id))
        db.commit()

        cursor.close()
        db.close()

        return jsonify({
            "status": "success",
            "message": "Realtime status updated"
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500



# ------------------------------------------------------
# GET /api/realtime
# Ambil status realtime untuk Dashboard
# ------------------------------------------------------
@realtime_api.route("/api/realtime", methods=["GET"])
def get_realtime():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT sensor_id, shake, intensity, duration, timestamp
            FROM realtime_status
            WHERE sensor_id = 1
        """)

        data = cursor.fetchone()

        cursor.close()
        db.close()

        return jsonify(data), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
