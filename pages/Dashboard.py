import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Honeypot-AI Dashboard", layout="wide")

# 🚨 Authentication check
if not st.session_state.get("logged_in"):
    st.error("🚫 You must be logged in to access the dashboard.")
    st.stop()

st.title(f"🛡️ Honeypot-AI Threat Dashboard - Welcome {st.session_state['username']}")

# Define paths
data_path = "data/cleaned_logs.csv"
session_path = "data/session_features.csv"
scored_path = "data/threat_scored_sessions.csv"

# Check if required files exist
if all(os.path.exists(p) for p in [data_path, session_path, scored_path]):
    df_logs = pd.read_csv(data_path, parse_dates=["timestamp"])
    df_sessions = pd.read_csv(session_path)
    df_scored = pd.read_csv(scored_path)

    st.sidebar.header("🔍 Filters")

    # Filter: Event Type
    if "event_type" in df_logs.columns:
        event_type_filter = st.sidebar.multiselect(
            "📌 Event Type", df_logs["event_type"].unique(),
            default=df_logs["event_type"].unique()
        )
    else:
        st.warning("⚠️ No 'event_type' column found.")
        event_type_filter = []

    # Filter: Date Range
    date_range = st.sidebar.date_input("📅 Date Range", [])

    # Apply filters
    filtered_df = df_logs[df_logs["event_type"].isin(event_type_filter)] if event_type_filter else df_logs.copy()

    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df["timestamp"].dt.date >= start_date) &
            (filtered_df["timestamp"].dt.date <= end_date)
        ]

    # 🧾 Data Views
    st.subheader("📄 Cleaned Honeypot Logs")
    st.dataframe(filtered_df.head(10), use_container_width=True)

    st.subheader("🧠 Session Features")
    st.dataframe(df_sessions.head(10), use_container_width=True)

    st.subheader("🔥 Threat Scored Sessions")
    st.dataframe(df_scored.head(10), use_container_width=True)

    # 📊 Event Activity by Hour
    st.subheader("⏰ Event Activity by Hour")
    if 'hour' not in filtered_df.columns:
        filtered_df["hour"] = pd.to_datetime(filtered_df["timestamp"]).dt.hour
    hourly = filtered_df['hour'].value_counts().sort_index()
    fig_bar = px.bar(
        x=hourly.index, y=hourly.values,
        labels={'x': 'Hour', 'y': 'Events'},
        title="Event Count by Hour"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # 📌 Event Type Distribution
    st.subheader("📌 Event Type Distribution")
    if "event_type" in filtered_df.columns:
        type_counts = filtered_df['event_type'].value_counts()
        fig_pie = px.pie(
            values=type_counts.values,
            names=type_counts.index,
            title="Distribution of Event Types"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        # Detailed Breakdown
        st.subheader("📊 Detailed Event Breakdown")
        specific_types = ["failed", "connect", "success", "input"]
        breakdown = {etype: filtered_df[filtered_df["event_type"] == etype].shape[0] for etype in specific_types}
        fig_bar_detail = px.bar(
            x=list(breakdown.keys()), y=list(breakdown.values()),
            labels={"x": "Event Type", "y": "Count"},
            title="Event Breakdown: Failed / Connect / Success / Input"
        )
        st.plotly_chart(fig_bar_detail, use_container_width=True)
    else:
        st.info("ℹ️ No 'event_type' data available to show distribution.")

    # ⚠️ Threat Severity
    st.subheader("⚠️ Threat Severity Distribution")
    if "threat_severity" in df_scored.columns:
        severity_counts = df_scored["threat_severity"].value_counts()
        fig_threat = px.pie(
            names=severity_counts.index,
            values=severity_counts.values,
            title="Threat Level Distribution",
            color=severity_counts.index,
            color_discrete_map={"Low": "green", "Medium": "orange", "High": "red"}
        )
        st.plotly_chart(fig_threat, use_container_width=True)
    else:
        st.warning("⚠️ No 'threat_severity' column found in scored session data.")
else:
    st.error("❌ Required files not found. Please ensure these files are present in the `data/` folder:")
    st.markdown("- `data/cleaned_logs.csv`")
    st.markdown("- `data/session_features.csv`")
    st.markdown("- `data/threat_scored_sessions.csv`")
