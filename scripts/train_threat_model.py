import pandas as pd
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def train_model(input_csv="data/session_features.csv", model_path="models/threat_model.pkl"):
    if not os.path.exists(input_csv):
        print(f"❌ Input file {input_csv} not found!")
        return

    df = pd.read_csv(input_csv)

    if df.empty:
        print("⚠️ No data to train on.")
        return

    if df["commands_entered"].nunique() < 3:
        df["threat_severity"] = "Low"
    else:
        df["threat_severity"] = pd.qcut(
            df["commands_entered"], q=3, labels=["Low", "Medium", "High"], duplicates="drop"
        )

    features = ["total_events", "successful_logins", "commands_entered", "duration_sec"]
    X = df[features]
    y = df["threat_severity"]

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump({
        "model": model,
        "label_encoder": le,
        "features": features
    }, model_path)

    print(f"✅ Model trained and saved to {model_path}")

if __name__ == "__main__":
    train_model()
