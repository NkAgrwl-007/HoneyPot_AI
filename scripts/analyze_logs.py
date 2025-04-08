import os
import json
import pandas as pd
from datetime import datetime

def load_cowrie_logs(log_dir):
    logs = []
    for file in os.listdir(log_dir):
        if file.endswith(".json"):
            with open(os.path.join(log_dir, file), 'r') as f:
                for line in f:
                    try:
                        logs.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    return pd.DataFrame(logs)

def preprocess_logs(df):
    relevant_events = [
        'cowrie.session.connect',
        'cowrie.login.success',
        'cowrie.login.failed',
        'cowrie.command.input'
    ]

    df = df[df['eventid'].isin(relevant_events)]
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])

    df['hour'] = df['timestamp'].dt.hour
    df['day'] = df['timestamp'].dt.day_name()
    df['date'] = df['timestamp'].dt.date
    df['event_type'] = df['eventid'].apply(lambda x: x.split('.')[-1])

    # Create session_id column if not present
    if 'session' in df.columns:
        df['session_id'] = df['session']
    else:
        df['session_id'] = df['src_ip'] + "_" + df['timestamp'].dt.floor('1H').astype(str)

    return df

def engineer_features(df):
    features = []

    grouped = df.groupby("session_id")

    for session_id, group in grouped:
        feature = {
            "session_id": session_id,
            "src_ip": group["src_ip"].iloc[0] if "src_ip" in group.columns else "unknown",
            "start_time": group["timestamp"].min(),
            "end_time": group["timestamp"].max(),
            "duration": (group["timestamp"].max() - group["timestamp"].min()).total_seconds(),
            "commands_count": len(group[group["eventid"] == "cowrie.command.input"]),
            "failed_logins": len(group[group["eventid"] == "cowrie.login.failed"]),
            "successful_logins": len(group[group["eventid"] == "cowrie.login.success"]),
            "total_events": len(group),
            "hour": group["timestamp"].min().hour
        }
        features.append(feature)

    return pd.DataFrame(features)

def main():
    log_directory = "data/honeypot_logs"

    if not os.path.exists(log_directory):
        print(f"❌ Directory {log_directory} not found!")
        return

    raw_df = load_cowrie_logs(log_directory)
    if raw_df.empty:
        print("⚠️ No logs found in directory.")
        return

    clean_df = preprocess_logs(raw_df)
    feature_df = engineer_features(clean_df)

    print("✅ Cleaned Logs Preview:")
    print(clean_df.head())

    print("\n🧠 Engineered Session Features Preview:")
    print(feature_df.head())

    clean_df.to_csv("data/cleaned_logs.csv", index=False)
    feature_df.to_csv("data/session_features.csv", index=False)
    print("\n📁 Files saved: cleaned_logs.csv & session_features.csv")

if __name__ == "__main__":
    main()
