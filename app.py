
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Brahmand Treasurer Dashboard",
    page_icon="🌌",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

events = pd.read_csv("data/events.csv")
expenses = pd.read_csv("data/expenses.csv")

# =====================================================
# CALCULATIONS
# =====================================================

total_budget = events["Budget"].sum()
total_expense = events["ActualExpense"].sum()
remaining_budget = total_budget - total_expense
total_sponsorship = events["Sponsorship"].sum()

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.metric-card{
    background:#161b22;
    padding:20px;
    border-radius:18px;
    border:1px solid #2d3748;
}

.metric-title{
    color:#9ca3af;
    font-size:14px;
}

.metric-value{
    font-size:34px;
    font-weight:bold;
}

.metric-sub{
    color:#9ca3af;
    font-size:13px;
}

.block{
    background:#161b22;
    padding:20px;
    border-radius:18px;
    border:1px solid #2d3748;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.title("🚀 Brahmand Treasurer Dashboard")
st.caption("Financial Command Center")

selected_event = st.selectbox(
    "Current Event",
    events["EventName"].tolist(),
    index=len(events)-1
)

event = events[
    events["EventName"] == selected_event
].iloc[0]

# =====================================================
# KPI CARDS
# =====================================================

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-title">Total Budget</div>
    <div class="metric-value">₹{total_budget:,.0f}</div>
    <div class="metric-sub">Allocated Budget</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-title">Total Spent</div>
    <div class="metric-value">₹{total_expense:,.0f}</div>
    <div class="metric-sub">{(total_expense/total_budget)*100:.1f}% Used</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-title">Remaining Budget</div>
    <div class="metric-value">₹{remaining_budget:,.0f}</div>
    <div class="metric-sub">{(remaining_budget/total_budget)*100:.1f}% Remaining</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-title">Sponsorship</div>
    <div class="metric-value">₹{total_sponsorship:,.0f}</div>
    <div class="metric-sub">{(total_sponsorship/total_budget)*100:.1f}% Coverage</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# =====================================================
# CHARTS
# =====================================================

left,right = st.columns([2,1])

with left:

    st.markdown("### 📊 Budget vs Spending")

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=events["EventName"],
            y=events["Budget"],
            name="Allocated"
        )
    )

    fig.add_trace(
        go.Bar(
            x=events["EventName"],
            y=events["ActualExpense"],
            name="Spent"
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=420,
        barmode="group"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.markdown("### 💰 Budget Distribution")

    category_df = pd.DataFrame({
        "Category":[
            "Technical",
            "Publicity",
            "Fine Arts",
            "Logistics",
            "Hospitality"
        ],
        "Amount":[
            events["TechnicalExpense"].sum(),
            events["PublicityExpense"].sum(),
            events["FineArtsExpense"].sum(),
            events["LogisticsExpense"].sum(),
            events["HospitalityExpense"].sum()
        ]
    })

    donut = px.pie(
        category_df,
        names="Category",
        values="Amount",
        hole=0.65
    )

    donut.update_layout(
        template="plotly_dark",
        height=420
    )

    st.plotly_chart(
        donut,
        use_container_width=True
    )

# =====================================================
# SECOND ROW
# =====================================================

col1,col2,col3 = st.columns([1,1,1])

with col1:

    st.markdown("### 💳 Recent Expenses")

    recent = expenses.sort_values(
        "Date",
        ascending=False
    ).head(5)

    st.dataframe(
        recent[
            [
                "Description",
                "Category",
                "Amount",
                "SpentBy"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

with col2:

    st.markdown("### 📈 Event Overview")

    st.metric(
        "Participants",
        int(event["Participants"])
    )

    st.metric(
        "Feedback",
        f"{event['Feedback']}/5"
    )

    st.metric(
        "Sponsor Funding",
        f"₹{event['Sponsorship']:,.0f}"
    )

with col3:

    st.markdown("### 🧠 Event Health")

    feedback_score = (
        event["Feedback"]/5
    )*100

    sponsor_score = (
        event["Sponsorship"]/
        event["Budget"]
    )*100

    participation_score = min(
        event["Participants"]/6,
        100
    )

    health = round(
        (
            feedback_score +
            sponsor_score +
            participation_score
        )/3
    )

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=health,
            title={"text":"Health Score"},
            gauge={
                "axis":{"range":[0,100]}
            }
        )
    )

    gauge.update_layout(
        template="plotly_dark",
        height=350
    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

# =====================================================
# ALERTS
# =====================================================

st.markdown("### ⚠ Treasurer Alerts")

for _, row in events.iterrows():

    utilisation = (
        row["ActualExpense"] /
        row["Budget"]
    ) * 100

    if utilisation > 90:

        st.warning(
            f"{row['EventName']} has used {utilisation:.1f}% of allocated budget."
        )

# =====================================================
# RECOMMENDATIONS
# =====================================================

highest = events.loc[
    events["ActualExpense"].idxmax()
]

saving = highest["ActualExpense"] * 0.10

st.markdown("### 💡 Top Recommendation")

st.success(
    f"""
Highest Spending Event: {highest['EventName']}

Potential Savings: ₹{saving:,.0f}

Recommendation:
Reduce logistics and hospitality costs through vendor negotiation and
reuse of event materials.
"""
)
