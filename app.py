from flask import Flask, jsonify, render_template

from connection import get_connection

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/metrics")
def get_metrics():
    conn = get_connection()

    if conn is None:
        return jsonify({
            "error": "Could not connect to database"
        }), 500

    try:
        cursor = conn.cursor(dictionary=True) # turns sql output into dictionary format so JSON can be easily sent over

        sql = """
        SELECT
            id,
            recorded_at,
            cpu_percent,
            memory_percent,
            disk_percent,
            bytes_sent,
            bytes_received
        FROM system_metrics
        ORDER BY recorded_at DESC
        LIMIT 1
        """

        cursor.execute(sql)

        metrics = cursor.fetchone() #retrieves one row

        if metrics is None:
            return jsonify({
                "message": "No metrics found"
            }), 404

        return jsonify(metrics)

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(debug=True)