from flask import Blueprint, jsonify
from db import get_db

stats_api = Blueprint("stats_api", __name__)

@stats_api.route("/api/stats", methods=["GET"])
def get_stats():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        query = """
            SELECT
                COALESCE(AVG(avg_intensity), 0) AS avg_intensity,
                COALESCE(MIN(max_intensity), 0) AS min_intensity,
                COALESCE(MAX(max_intensity), 0) AS max_intensity
            FROM quake_logs
            WHERE COALESCE(created_at, start_time) >= NOW() - INTERVAL 24 HOUR

        """

        cursor.execute(query)
        result = cursor.fetchone()

        cursor.close()
        db.close()

        return jsonify({
            "average": float(result["avg_intensity"]),
            "minimum": float(result["min_intensity"]),
            "maximum": float(result["max_intensity"])
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error processing stats: {str(e)}"
        }), 500
        

