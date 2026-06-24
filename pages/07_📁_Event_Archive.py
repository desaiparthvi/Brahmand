import streamlit as st
import pandas as pd

from utils.data_manager import load_events
from utils.feature_engine import add_features
from utils.scoring_engine import health_score

st.title("📚 Knowledge Vault")

df = load_events()
df = add_features(df)

df["HealthScore"] = df.apply(
    health_score,
    axis=1
)

st.subheader("🔍 Search Historical Events")

event_name = st.selectbox(
    "Select Event",
    df["EventName"]
)

selected = df[
    df["EventName"] == event_name
].iloc[0]

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Budget",
        f"₹{selected['Budget']:,}"
    )

with col2:
    st.metric(
        "Participants",
        int(selected["Participants"])
    )

with col3:
    st.metric(
        "Health Score",
        round(selected["HealthScore"],1)
    )

st.markdown("---")

st.subheader("📊 Financial Breakdown")

st.write(
    f"🔧 Technical: ₹{selected['TechnicalExpense']:,}"
)

st.write(
    f"📢 Publicity: ₹{selected['PublicityExpense']:,}"
)

st.write(
    f"🎨 Fine Arts: ₹{selected['FineArtsExpense']:,}"
)

st.write(
    f"🚚 Logistics: ₹{selected['LogisticsExpense']:,}"
)

st.write(
    f"🍕 Hospitality: ₹{selected['HospitalityExpense']:,}"
)

st.markdown("---")

st.subheader("⚠ Issues Faced")

st.warning(
    selected["IssuesFaced"]
)

st.markdown("---")

st.subheader("✅ Outcome")

st.success(
    selected["Outcome"]
)

st.markdown("---")

st.subheader("🧠 Institutional Insights")

if selected["Feedback"] > 4.5:

    st.info(
        "This event achieved exceptionally strong participant satisfaction."
    )

if selected["SponsorRatio"] > df["SponsorRatio"].mean():

    st.info(
        "This event achieved above-average sponsorship support."
    )

if selected["Participants"] > df["Participants"].mean():

    st.info(
        "Participation exceeded club historical averages."
    )

st.markdown("---")

st.subheader("📂 Historical Repository")

st.dataframe(
    df[
        [
            "EventName",
            "EventType",
            "Budget",
            "Participants",
            "Feedback",
            "HealthScore"
        ]
    ],
    use_container_width=True
)