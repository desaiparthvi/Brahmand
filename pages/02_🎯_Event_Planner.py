import streamlit as st
import pandas as pd

st.title("🧠 Recommendation Engine")

df = pd.read_csv("data/events.csv")

event_type = st.selectbox(
    "Event Type",
    [
        "Workshop",
        "Non-Tech Event/Collab",
        "Festival",
        "Guest Lecture",
        "Observation Event",
        "Competition"
    ]
)

participants = st.number_input(
    "Target Participants",
    min_value=50,
    value=200
)

budget = st.number_input(
    "Event Budget (₹)",
    min_value=1000,
    value=50000
)

goal = st.selectbox(
    "Primary Goal",
    [
        "Max Participation",
        "Max Feedback",
        "Max Sponsorship"
    ]
)

st.markdown("---")

if goal == "Max Participation":

    technical = int(budget * 0.25)
    publicity = int(budget * 0.30)
    logistics = int(budget * 0.20)
    hospitality = int(budget * 0.15)
    reserve = int(budget * 0.10)

    reason = "Participation-focused events perform best with stronger publicity and outreach."

    similar = df.sort_values(
        "Participants",
        ascending=False
    ).head(2)

elif goal == "Max Feedback":

    technical = int(budget * 0.35)
    publicity = int(budget * 0.15)
    logistics = int(budget * 0.25)
    hospitality = int(budget * 0.15)
    reserve = int(budget * 0.10)

    reason = "Higher feedback is strongly linked to technical quality and logistics."

    similar = df.sort_values(
        "Feedback",
        ascending=False
    ).head(2)

else:

    technical = int(budget * 0.20)
    publicity = int(budget * 0.20)
    logistics = int(budget * 0.15)
    hospitality = int(budget * 0.10)
    reserve = int(budget * 0.05)
    sponsorship = int(budget * 0.30)

    reason = "More budget is allocated to sponsorship outreach and partnerships."

    similar = df.sort_values(
        "Sponsorship",
        ascending=False
    ).head(2)

st.subheader("💡 Recommended Budget Allocation")

col1, col2 = st.columns(2)

with col1:
    st.metric("Technical", f"₹{technical:,}")
    st.metric("Publicity", f"₹{publicity:,}")
    st.metric("Logistics", f"₹{logistics:,}")

with col2:
    st.metric("Hospitality", f"₹{hospitality:,}")
    st.metric("Reserve", f"₹{reserve:,}")

    if goal == "Max Sponsorship":
        st.metric(
            "Sponsor Outreach",
            f"₹{sponsorship:,}"
        )

st.markdown("---")

st.subheader("📌 Why This Recommendation?")
st.info(reason)

st.markdown("---")

st.subheader("📊 Similar Historical Events")

st.dataframe(
    similar[
        [
            "EventName",
            "Budget",
            "Participants",
            "Feedback",
            "Sponsorship"
        ]
    ],
    use_container_width=True
)

st.markdown("---")

st.subheader("🤖 AI Recommendation")

if event_type == "Workshop":

    similar_event = "AstroZen"
    recommended_budget = participants * 80

elif event_type == "Non-Tech Event/Collab":

    similar_event = "Lunar Canvas"
    recommended_budget = participants * 95

elif event_type == "Festival":

    similar_event = "AstroFest 2026"
    recommended_budget = participants * 140

elif event_type == "Guest Lecture":

    similar_event = "Cosmic Talks"
    recommended_budget = participants * 100

elif event_type == "Observation Event":

    similar_event = "Stargazing Night"
    recommended_budget = participants * 90

else:

    similar_event = "Lunar Canvas"
    recommended_budget = participants * 85

recommended_sponsor = int(
    recommended_budget * 0.25
)

st.success(
    f"""
Recommended Budget: ₹{recommended_budget:,}

Recommended Sponsor Target: ₹{recommended_sponsor:,}

Most Similar Historical Event: {similar_event}

Expected Cost Per Participant: ₹{recommended_budget/participants:.0f}
"""
)