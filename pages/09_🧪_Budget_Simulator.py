import streamlit as st
import pandas as pd

st.title("🧪 Scenario Lab")

df = pd.read_csv("data/events.csv")

selected_event = st.selectbox(
    "Historical Event",
    df["EventName"]
)

event_data = df[
    df["EventName"] == selected_event
].iloc[0]

current_budget = event_data["Budget"]

st.metric(
    "Original Budget",
    f"₹{current_budget:,.0f}"
)

new_budget = st.number_input(
    "Available Budget After Reduction (₹)",
    min_value=1000,
    value=int(current_budget * 0.8)
)

priority = st.selectbox(
    "Primary Goal",
    [
        "Participation",
        "Technical Quality",
        "Branding",
        "Balanced"
    ]
)

cut_percent = (
    (current_budget - new_budget)
    / current_budget
) * 100

st.markdown("---")

st.metric(
    "Budget Reduction",
    f"{cut_percent:.1f}%"
)

st.markdown("---")

# ==========================
# IMPACT PREDICTION
# ==========================

if cut_percent <= 10:

    participant_loss = 5
    feedback_drop = 0.1
    risk = "Low"

elif cut_percent <= 25:

    participant_loss = 15
    feedback_drop = 0.3
    risk = "Medium"

else:

    participant_loss = 30
    feedback_drop = 0.6
    risk = "High"

st.subheader("📉 Predicted Impact")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Participation Impact",
        f"-{participant_loss}%"
    )

with c2:
    st.metric(
        "Feedback Impact",
        f"-{feedback_drop:.1f}"
    )

with c3:
    st.metric(
        "Risk Level",
        risk
    )

st.markdown("---")

# ==========================
# ALLOCATION
# ==========================

st.subheader("💰 Recommended Allocation")

if priority == "Participation":

    technical = 20
    publicity = 35
    logistics = 20
    hospitality = 15
    finearts = 10

elif priority == "Technical Quality":

    technical = 40
    publicity = 15
    logistics = 20
    hospitality = 15
    finearts = 10

elif priority == "Branding":

    technical = 20
    publicity = 40
    logistics = 15
    hospitality = 10
    finearts = 15

else:

    technical = 30
    publicity = 20
    logistics = 20
    hospitality = 15
    finearts = 15

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Technical",
        f"₹{new_budget * technical / 100:,.0f}"
    )

    st.metric(
        "Publicity",
        f"₹{new_budget * publicity / 100:,.0f}"
    )

    st.metric(
        "Fine Arts",
        f"₹{new_budget * finearts / 100:,.0f}"
    )

with col2:

    st.metric(
        "Logistics",
        f"₹{new_budget * logistics / 100:,.0f}"
    )

    st.metric(
        "Hospitality",
        f"₹{new_budget * hospitality / 100:,.0f}"
    )

st.markdown("---")

# ==========================
# HISTORICAL CONTEXT
# ==========================

st.subheader("📚 Historical Context")

st.info(
    f"""
Event: {selected_event}

Original Budget: ₹{event_data['Budget']:,.0f}

Participants: {event_data['Participants']}

Feedback: {event_data['Feedback']}/5

Actual Expense: ₹{event_data['ActualExpense']:,.0f}
"""
)

st.markdown("---")

# ==========================
# AI SUGGESTIONS
# ==========================

st.subheader("🤖 AI Suggestions")

if cut_percent > 25:

    st.error("High Risk Scenario")

    st.write("• Reduce hospitality first")
    st.write("• Reuse previous event materials")
    st.write("• Increase sponsorship outreach")
    st.write("• Seek club collaborations")
    st.write("• Avoid reducing technical requirements")

elif cut_percent > 10:

    st.warning("Moderate Risk Scenario")

    st.write("• Reduce decor and branding expenses")
    st.write("• Optimize publicity channels")
    st.write("• Protect logistics spending")
    st.write("• Focus on high-impact activities")

else:

    st.success("Low Risk Scenario")

    st.write("• Event remains financially viable")
    st.write("• No major operational compromises expected")

st.markdown("---")

# ==========================
# HISTORICAL ASSESSMENT
# ==========================

st.subheader("📊 Historical Assessment")

if cut_percent > 25:

    st.error(
        "Historical data suggests this reduction may significantly affect participation and event quality."
    )

elif cut_percent > 10:

    st.warning(
        "Moderate reduction. Prioritize technical execution and logistics."
    )

else:

    st.success(
        "Budget remains within historical operating range."
    )

st.markdown("---")

# ==========================
# SCENARIO SCORE
# ==========================

scenario_score = max(
    0,
    100 - cut_percent
)

st.subheader("🎯 Scenario Viability")

st.progress(int(scenario_score))

st.metric(
    "Scenario Score",
    f"{scenario_score:.0f}/100"
)