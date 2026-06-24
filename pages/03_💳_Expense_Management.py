import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import date

st.set_page_config(layout="wide")

st.title("💳 Expense Tracker")

FILE_PATH = "data/expenses.csv"

# ====================================
# CREATE FILE IF MISSING
# ====================================

if not os.path.exists(FILE_PATH):

    pd.DataFrame(
        columns=[
            "ExpenseID",
            "EventName",
            "Category",
            "Description",
            "Amount",
            "Status",
            "Date",
            "SpentBy"
        ]
    ).to_csv(FILE_PATH, index=False)

try:
    df = pd.read_csv(FILE_PATH)

except:
    df = pd.DataFrame(
        columns=[
            "ExpenseID",
            "EventName",
            "Category",
            "Description",
            "Amount",
            "Status",
            "Date",
            "SpentBy"
        ]
    )

# ====================================
# EVENT DETAILS
# ====================================

st.header("➕ Add Expense")

col1, col2 = st.columns(2)

with col1:

    event_name = st.text_input("Event Name")

    category = st.selectbox(
        "Category",
        [
            "Fine Arts",
            "Technical - Electrical",
            "Technical - Mechanical",
            "Technical - Software",
            "Publicity",
            "Content",
            "Documentation",
            "Video Editing",
            "Graphic Design",
            "Sponsorship",
            "Hospitality",
            "Logistics",
            "Miscellaneous"
        ]
    )

    description = st.text_input("Description")

with col2:

    amount = st.number_input(
        "Amount (₹)",
        min_value=0.0
    )

    status = st.selectbox(
        "Status",
        [
            "Pending",
            "Approved",
            "Reimbursed"
        ]
    )

    spent_by = st.text_input("Spent By")

    expense_date = st.date_input(
        "Expense Date",
        value=date.today()
    )

if st.button("Add Expense"):

    expense_id = len(df) + 1

    new_row = pd.DataFrame([{
        "ExpenseID": expense_id,
        "EventName": event_name,
        "Category": category,
        "Description": description,
        "Amount": amount,
        "Status": status,
        "Date": expense_date,
        "SpentBy": spent_by
    }])

    df = pd.concat(
        [df, new_row],
        ignore_index=True
    )

    df.to_csv(FILE_PATH, index=False)

    st.success("Expense Added Successfully")

    st.rerun()

# ====================================
# EVENT FILTER
# ====================================

st.markdown("---")

events = ["All Events"]

if len(df) > 0:
    events += sorted(df["EventName"].dropna().unique())

selected_event = st.selectbox(
    "Select Event",
    events
)

if selected_event != "All Events":

    filtered_df = df[
        df["EventName"] == selected_event
    ]

else:

    filtered_df = df

# ====================================
# BUDGET INPUT
# ====================================

st.markdown("---")

budget = st.number_input(
    "Approved Budget (₹)",
    min_value=0.0,
    value=50000.0
)

spent = filtered_df["Amount"].sum()

remaining = budget - spent

utilization = 0

if budget > 0:
    utilization = (spent / budget) * 100

# ====================================
# DASHBOARD
# ====================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "💰 Budget",
        f"₹{budget:,.0f}"
    )

with c2:
    st.metric(
        "💸 Spent",
        f"₹{spent:,.0f}"
    )

with c3:
    st.metric(
        "🟢 Remaining",
        f"₹{remaining:,.0f}"
    )

with c4:
    st.metric(
        "📊 Utilization",
        f"{utilization:.1f}%"
    )

# ====================================
# TREASURER SUMMARY
# ====================================

st.markdown("---")

st.subheader("📋 Treasurer Summary")

pending = filtered_df[
    filtered_df["Status"] == "Pending"
]["Amount"].sum()

approved = filtered_df[
    filtered_df["Status"] == "Approved"
]["Amount"].sum()

reimbursed = filtered_df[
    filtered_df["Status"] == "Reimbursed"
]["Amount"].sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "⏳ Pending",
        f"₹{pending:,.0f}"
    )

with col2:
    st.metric(
        "✅ Approved",
        f"₹{approved:,.0f}"
    )

with col3:
    st.metric(
        "💵 Reimbursed",
        f"₹{reimbursed:,.0f}"
    )

# ====================================
# CATEGORY ANALYSIS
# ====================================

st.markdown("---")

st.subheader("📊 Category Spending")

if len(filtered_df) > 0:

    category_summary = (
        filtered_df
        .groupby("Category")["Amount"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        category_summary,
        x="Category",
        y="Amount",
        title="Category Wise Spending"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ====================================
# EXPENSE TABLE
# ====================================

st.markdown("---")

st.subheader("📄 Expense Records")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ====================================
# RISK ALERTS
# ====================================

st.markdown("---")

st.subheader("⚠ Budget Alerts")

if utilization >= 90:

    st.error(
        "Budget Utilization above 90%"
    )

elif utilization >= 70:

    st.warning(
        "Budget Utilization above 70%"
    )

else:

    st.success(
        "Budget Healthy"
    )
    