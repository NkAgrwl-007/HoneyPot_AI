import mysql.connector
import json
import os

DB_CONFIG = {
    "host": "localhost",
    "user": "honeypot",
    "password": "securepass",
    "database": "honeypot_logs"
}

LOG_DIR = "logs/cowrie"

def export_logs_to_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attacks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp VARCHAR(255),
            attacker_ip VARCHAR(255),
            service VARCHAR(50),
            payload TEXT
        )
    """)

    for log_file in os.listdir(LOG_DIR):
        with open(os.path.join(LOG_DIR, log_file), "r") as file:
            for line in file:
                log_entry = json.loads(line)
                cursor.execute("""
                    INSERT INTO attacks (timestamp, attacker_ip, service, payload)
                    VALUES (%s, %s, %s, %s)
                """, (log_entry["timestamp"], log_entry["attacker_ip"], log_entry["service"], log_entry["payload"]))
    
    conn.commit()
    conn.close()
    print("Logs successfully exported to MySQL.")

if __name__ == "__main__":
    export_logs_to_db()
