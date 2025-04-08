import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

def assign_threat_level(row):
    if row["successful_logins"] > 0 and row["commands_count"] > 5:
        return "High"
    elif row["commands_count"] > 2:
        return "Medium"
    else:
        return "Low"

def main():
    input_file = "data/session_features.csv"
    output_file = "data/threat_scored_sessions.csv"
    model_file = "models/threat_model.pkl"

    if not os.path.exists(input_file):
        print("❌ session_features.csv not found.")
        return

    df = pd.read_csv(input_file)
    df = df.dropna()

    df["threat_severity"] = df.apply(assign_threat_level, axis=1)

    X = df[["total_events", "successful_logins", "commands_count", "duration"]]
    y = LabelEncoder().fit_transform(df["threat_severity"])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X)
    df["predicted_threat"] = LabelEncoder().fit(["Low", "Medium", "High"]).inverse_transform(y_pred)

    df.rename(columns={"predicted_threat": "threat_severity"}, inplace=True)
    df.to_csv(output_file, index=False)
    print(f"✅ Threat scored sessions saved to {output_file}")

    os.makedirs("models", exist_ok=True)
    joblib.dump(clf, model_file)
    print(f"📦 Trained model saved to {model_file}")

if __name__ == "__main__":
    main()
