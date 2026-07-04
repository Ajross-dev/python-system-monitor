#log system metrics into sql db
from connection import get_connection


def save_metrics(cpu_percent, memory_percent, disk_percent, bytes_sent, bytes_received):
    conn = get_connection()

    if conn is None:
        return

    try:
        cursor = conn.cursor()

        sql = """
        INSERT INTO system_metrics
        (cpu_percent, memory_percent, disk_percent, bytes_sent, bytes_received)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            cpu_percent,
            memory_percent,
            disk_percent,
            bytes_sent,
            bytes_received
        )

        cursor.execute(sql, values)
        conn.commit()

    finally:
        cursor.close()
        conn.close()