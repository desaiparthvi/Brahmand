import streamlit as st
from utils.data_manager import load_events
from utils.feature_engine import add_features
from utils.scoring_engine import health_score

df = load_events()
df = add_features(df)

df["HealthScore"] = df.apply(
    health_score,
    axis=1
)

st.title("📊 Event Intelligence")

event_name = st.text_input("Event Name")

budget = st.number_input("Budget", min_value=0)

participants = st.number_input("Participants", min_value=1)

feedback = st.slider("Feedback Score", 1.0, 5.0, 4.0)

if participants > 0:
    cpp = budget / participants

    st.metric(
        "Cost Per Participant",
        f"₹{cpp:.2f}"
    )

health_score = (
    (feedback/5)*50 +
    min(participants/500,1)*50
)

st.metric(
    "Event Health Score",
    f"{health_score:.1f}/100"
)
st.header("🏆 Event Health Rankings")

df = df.sort_values(
    "HealthScore",
    ascending=False
)

st.dataframe(
df[
        [
            "EventName",
            "HealthScore",
            "Participants",
            "Feedback",
            "SponsorRatio"
        ]
    ],
    use_container_width=True
)
ranking_df = df.sort_values(
    "HealthScore",
    ascending=False
)
st.metric(
    "Best Event",
    ranking_df.iloc[0]["EventName"]
)

st.metric(
    "Average Health Score",
    round(df["HealthScore"].mean(),1)
)
st.bar_chart(
    ranking_df.set_index("EventName")["HealthScore"]
)