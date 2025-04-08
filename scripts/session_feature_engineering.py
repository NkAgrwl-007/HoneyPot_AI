import pandas as pd
import os

def extract_session_features(input_csv="data/cleaned_logs.csv", output_csv="data/session_features.csv"):
    if not os.path.exists(input_csv):
        print(f"❌ Input file {input_csv} not found!")
        return

    df = pd.read_csv(input_csv, parse_dates=["timestamp"])

    if df.empty:
        print("⚠️ No data found in logs.")
        return

    session_groups = df.groupby("session_id")

    session_features = []

    for session_id, group in session_groups:
        group_sorted = group.sort_values("timestamp")
        start_time = group_sorted["timestamp"].min()
        end_time = group_sorted["timestamp"].max()
        duration = (end_time - start_time).total_seconds()

        feature = {
            "session_id": session_id,
            "src_ip": group["src_ip"].iloc[0],
            "start_time": start_time,
            "end_time": end_time,
            "total_events": len(group),
            "successful_logins": (group["event_type"] == "login_success").sum(),
            "failed_logins": (group["event_type"] == "login_failed").sum(),
            "commands_entered": (group["event_type"] == "command").sum(),
            "duration_sec": duration,
            "hour": start_time.hour
        }
        session_features.append(feature)

    df_features = pd.DataFrame(session_features)
    df_features.to_csv(output_csv, index=False)
    print(f"✅ Session features saved to {output_csv}")

if __name__ == "__main__":
    extract_session_features()
