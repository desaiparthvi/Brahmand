import streamlit as st
import pandas as pd

from utils.data_manager import load_events
from utils.feature_engine import add_features

st.title("🤝 Sponsorship Intelligence")

df = load_events()
df = add_features(df)

st.subheader("📊 Sponsorship Analytics")

total_sponsorship = df["Sponsorship"].sum()

avg_sponsorship = df["Sponsorship"].mean()

best_event = df.loc[
    df["Sponsorship"].idxmax()
]

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Total Sponsorship",
        f"₹{total_sponsorship:,.0f}"
    )

with c2:
    st.metric(
        "Average Sponsorship",
        f"₹{avg_sponsorship:,.0f}"
    )

with c3:
    st.metric(
        "Best Sponsored Event",
        best_event["EventName"]
    )

st.markdown("---")

st.subheader("📈 Sponsorship Performance")

sponsor_df = df[
    [
        "EventName",
        "Sponsorship"
    ]
].set_index(
    "EventName"
)

st.bar_chart(
    sponsor_df
)

st.markdown("---")

st.subheader("⚠ Sponsorship Risk Analysis")

avg_ratio = df["SponsorRatio"].mean()

high_risk_events = df[
    df["SponsorRatio"] < avg_ratio
]

for event in high_risk_events["EventName"]:

    st.warning(
        f"{event} has below-average sponsor coverage."
    )

st.markdown("---")

st.subheader("🎯 Recommended Sponsor Targets")

for _, row in df.iterrows():

    target = int(
        row["Budget"] * 0.30
    )

    st.info(
        f"""
{row['EventName']}

Current Sponsorship:
₹{row['Sponsorship']:,.0f}

Recommended Target:
₹{target:,.0f}
"""
    )

st.markdown("---")

st.subheader("🤖 Sponsorship Insights")

best_ratio = df.loc[
    df["SponsorRatio"].idxmax()
]

st.success(
    f"""
Highest Sponsor Efficiency:

{best_ratio['EventName']}

Coverage:
{best_ratio['SponsorRatio']:.1%}
"""
)

st.info(
    """
Events with stronger sponsorship support
reduce dependence on approved club funding
and create greater flexibility for event execution.
"""
)