from flask import Blueprint, request, jsonify
from db import get_db

event_api = Blueprint("event_api", __name__)

@event_api.route("/api/event", methods=["POST"])
def create_event():
    try:
        data = request.json

        sensor_id = data["sensor_id"]
        start_time = data["start_time"]
        end_time = data["end_time"]
        duration_sec = data["duration_sec"]
        max_intensity = data["max_intensity"]
        avg_intensity = data["avg_intensity"]

        db = get_db()
        cursor = db.cursor()

        # Panggil Stored Procedure
        cursor.callproc("proc_insert_quake_event", (
            sensor_id,
            start_time,
            end_time,
            duration_sec,
            max_intensity,
            avg_intensity
        ))

        db.commit()
        cursor.close()
        db.close()

        return jsonify({
            "status": "success",
            "message": "Event logged to quake_logs"
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
@event_api.route("/api/event/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "DELETE FROM quake_logs WHERE event_id = %s",
            (event_id,)
        )

        db.commit()
        cursor.close()
        db.close()

        return jsonify({
            "status": "ok",
            "deleted_event_id": event_id
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500