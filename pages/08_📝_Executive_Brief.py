import streamlit as st
import pandas as pd

from utils.data_manager import load_events
from utils.feature_engine import add_features
from utils.scoring_engine import health_score

st.title("📝 Executive Brief")

df = load_events()
df = add_features(df)

df["HealthScore"] = df.apply(
    health_score,
    axis=1
)

st.markdown("---")

selected_event = st.selectbox(
    "Select Event",
    df["EventName"]
)

event = df[
    df["EventName"] == selected_event
].iloc[0]

st.header("Executive Summary")

if event["HealthScore"] >= 85:
    status = "Excellent"

elif event["HealthScore"] >= 75:
    status = "Good"

else:
    status = "Needs Improvement"

st.success(
    f"""
Event: {event['EventName']}

Overall Status: {status}

Health Score: {event['HealthScore']:.1f}/100

Participants: {event['Participants']}

Budget: ₹{event['Budget']:,.0f}
"""
)

st.markdown("---")

st.header("Key Findings")

if event["Feedback"] >= 4.5:
    st.info(
        "High participant satisfaction achieved."
    )

if event["SponsorRatio"] >= 0.25:
    st.info(
        "Strong sponsorship support observed."
    )

if event["ParticipantEfficiency"] > df["ParticipantEfficiency"].mean():
    st.info(
        "Participation efficiency exceeded club average."
    )

st.markdown("---")

st.header("Major Risks")

risk_found = False

if event["SponsorRatio"] < 0.15:

    risk_found = True

    st.warning(
        "Low sponsorship dependency coverage."
    )

if event["Feedback"] < 4.0:

    risk_found = True

    st.warning(
        "Feedback below preferred threshold."
    )

if event["Participants"] < df["Participants"].mean():

    risk_found = True

    st.warning(
        "Participation below club average."
    )

if not risk_found:

    st.success(
        "No major risks identified."
    )

st.markdown("---")

st.header("Recommended Actions")

if event["Feedback"] < 4.5:

    st.write(
        "• Improve attendee engagement activities"
    )

if event["SponsorRatio"] < 0.25:

    st.write(
        "• Increase sponsor outreach efforts"
    )

if event["Participants"] < df["Participants"].mean():

    st.write(
        "• Strengthen publicity campaigns"
    )

st.write(
    "• Continue documenting lessons learnt"
)

st.write(
    "• Maintain historical event records"
)

st.markdown("---")

st.header("Expected Outcomes")

future_score = min(
    100,
    event["HealthScore"] + 5
)

st.success(
    f"""
Expected Future Health Score:
{future_score:.1f}/100

Projected Improvement:
+5 points

Recommendation Confidence:
High
"""
)