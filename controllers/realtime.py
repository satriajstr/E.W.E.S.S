from flask import Blueprint, request, jsonify
from db import get_db
from datetime import datetime

realtime_api = Blueprint("realtime_api", __name__)

THRESHOLD = 40
QUIET_SECONDS = 3


@realtime_api.route("/api/realtime", methods=["POST"])
def post_realtime():
    try:
        data = request.json

        sensor_id = data.get("sensor_id", 1)
        intensity = int(data.get("intensity", 0))
        duration = float(data.get("duration", 0))
        shake = 1 if intensity >= THRESHOLD else 0
        now = datetime.now()

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM realtime_status
            WHERE sensor_id = %s
        """, (sensor_id,))
        state = cursor.fetchone()

        if not state:
            return jsonify({"error": "Sensor not registered"}), 400

        event_active = state["event_active"]

        # ===============================
        # EVENT LOGIC
        # ===============================
        if intensity >= THRESHOLD:
            if not event_active:
                # START EVENT
                cursor.execute("""
                    UPDATE realtime_status
                    SET event_active = 1,
                        event_start_time = %s,
                        last_below_threshold = NULL,
                        max_intensity = %s,
                        sum_intensity = %s,
                        sample_count = 1
                    WHERE sensor_id = %s
                """, (now, intensity, intensity, sensor_id))
            else:
                # EVENT CONTINUES
                cursor.execute("""
                    UPDATE realtime_status
                    SET max_intensity = GREATEST(max_intensity, %s),
                        sum_intensity = sum_intensity + %s,
                        sample_count = sample_count + 1,
                        last_below_threshold = NULL
                    WHERE sensor_id = %s
                """, (intensity, intensity, sensor_id))

        else:
            if event_active:
                if state["last_below_threshold"] is None:
                    # FIRST TIME BELOW THRESHOLD
                    cursor.execute("""
                        UPDATE realtime_status
                        SET last_below_threshold = %s
                        WHERE sensor_id = %s
                    """, (now, sensor_id))
                else:
                    quiet_time = (now - state["last_below_threshold"]).total_seconds()

                    if quiet_time >= QUIET_SECONDS:
                        # END EVENT
                        start_time = state["event_start_time"]
                        duration_sec = (now - start_time).total_seconds()
                        avg_intensity = state["sum_intensity"] / max(state["sample_count"], 1)

                        cursor.execute("""
                            INSERT INTO quake_logs
                            (sensor_id, start_time, end_time, duration_sec, max_intensity, avg_intensity)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (
                            sensor_id,
                            start_time,
                            now,
                            duration_sec,
                            state["max_intensity"],
                            avg_intensity
                        ))

                        # RESET STATE
                        cursor.execute("""
                            UPDATE realtime_status
                            SET event_active = 0,
                                event_start_time = NULL,
                                last_below_threshold = NULL,
                                max_intensity = 0,
                                sum_intensity = 0,
                                sample_count = 0
                            WHERE sensor_id = %s
                        """, (sensor_id,))

        # ===============================
        # UPDATE REALTIME SNAPSHOT
        # ===============================
        cursor.execute("""
            UPDATE realtime_status
            SET shake = %s,
                intensity = %s,
                duration = %s,
                timestamp = %s
            WHERE sensor_id = %s
        """, (shake, intensity, duration, now, sensor_id))

        db.commit()
        cursor.close()
        db.close()

        return jsonify({
            "status": "success",
            "event_active": shake == 1,
            "intensity": intensity
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@realtime_api.route("/api/realtime", methods=["GET"])
def get_realtime():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT sensor_id, shake, intensity, duration, timestamp, event_active
        FROM realtime_status
        WHERE sensor_id = 1
    """)
    data = cursor.fetchone()

    cursor.close()
    db.close()
    return jsonify(data), 200
