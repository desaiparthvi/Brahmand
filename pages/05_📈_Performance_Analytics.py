import streamlit as st
import pandas as pd

from utils.data_manager import load_events
from utils.feature_engine import add_features
from utils.scoring_engine import health_score

st.title("📈 ROI Analytics")

df = load_events()
df = add_features(df)

df["HealthScore"] = df.apply(
    health_score,
    axis=1
)

event = st.selectbox(
    "Select Event",
    df["EventName"]
)

selected = df[
    df["EventName"] == event
].iloc[0]

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Participants",
        int(selected["Participants"])
    )

with col2:
    st.metric(
        "Feedback",
        round(selected["Feedback"],1)
    )

with col3:
    st.metric(
        "Health Score",
        round(selected["HealthScore"],1)
    )

st.markdown("---")

st.subheader("📊 Historical Comparison")

avg_participants = df["Participants"].mean()
avg_feedback = df["Feedback"].mean()

participant_diff = (
    selected["Participants"]
    - avg_participants
)

feedback_diff = (
    selected["Feedback"]
    - avg_feedback
)

st.metric(
    "Participation vs Club Average",
    f"{participant_diff:+.0f}"
)

st.metric(
    "Feedback vs Club Average",
    f"{feedback_diff:+.2f}"
)

st.markdown("---")

st.subheader("💪 Strengths")

if selected["Participants"] > avg_participants:
    st.success(
        "Participation exceeded club average."
    )

if selected["Feedback"] > avg_feedback:
    st.success(
        "Feedback exceeded club average."
    )

if selected["SponsorRatio"] > df["SponsorRatio"].mean():
    st.success(
        "Strong sponsorship support."
    )

st.markdown("---")

st.subheader("⚠ Improvement Areas")

if selected["Participants"] < avg_participants:
    st.warning(
        "Participation below club average."
    )

if selected["Feedback"] < avg_feedback:
    st.warning(
        "Feedback below club average."
    )

if selected["SponsorRatio"] < df["SponsorRatio"].mean():
    st.warning(
        "Increase sponsorship outreach."
    )

st.markdown("---")

st.subheader("🤖 Generated Insights")

if selected["Participants"] > avg_participants:

    st.info(
        "This event performed above average in attendance and can be used as a benchmark for future planning."
    )

else:

    st.info(
        "Participation was below historical averages. Increased publicity and collaborations may improve future turnout."
    )

if selected["Feedback"] > 4.5:

    st.info(
        "High attendee satisfaction suggests strong event execution and planning."
    )