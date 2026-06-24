import streamlit as st
import pandas as pd
import os

from streamlit_calendar import calendar

st.title("📅 Club Operations Calendar")

FILE_PATH = "data/calendar_events.csv"

# ==========================
# CREATE FILE IF MISSING
# ==========================

if not os.path.exists(FILE_PATH):

    pd.DataFrame(
        columns=[
            "EventName",
            "Date",
            "Priority",
            "Status",
            "Lead"
        ]
    ).to_csv(
        FILE_PATH,
        index=False
    )

# ==========================
# LOAD DATA
# ==========================

df = pd.read_csv(FILE_PATH)

# ==========================
# ADD EVENT
# ==========================

st.subheader("➕ Add Event")
st.markdown("""
### 🎨 Calendar Legend

🟢 Completed &nbsp;&nbsp;&nbsp;
🔵 In Progress &nbsp;&nbsp;&nbsp;
🟠 Upcoming &nbsp;&nbsp;&nbsp;
🔴 High Priority &nbsp;&nbsp;&nbsp;
⚫ Cancelled
""")
with st.form("event_form"):

    event_name = st.text_input(
        "Event Name"
    )

    event_date = st.date_input(
        "Event Date"
    )

    priority = st.selectbox(
        "Priority",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

    status = st.selectbox(
        "Status",
        [
            "Upcoming",
            "In Progress",
            "Completed",
            "Cancelled"
        ]
    )

    lead = st.text_input(
        "Event Lead"
    )

    submit = st.form_submit_button(
        "Add Event"
    )

    if submit:

        new_row = pd.DataFrame([{
            "EventName": event_name,
            "Date": str(event_date),
            "Priority": priority,
            "Status": status,
            "Lead": lead
        }])

        df = pd.concat(
            [df, new_row],
            ignore_index=True
        )

        df.to_csv(
            FILE_PATH,
            index=False
        )

        st.success(
            "Event Added Successfully"
        )

        st.rerun()

# ==========================
# CALENDAR
# ==========================

st.markdown("---")

st.subheader("📆 Annual Event Calendar")

events = []

for _, row in df.iterrows():

    status = row["Status"]
    priority = row["Priority"]

    if status == "Completed":

        color = "green"

    elif status == "In Progress":

        color = "blue"

    elif status == "Cancelled":

        color = "gray"

    elif priority == "High":

        color = "red"

    else:

        color = "orange"

    events.append(
        {
            "title": row["EventName"],
            "start": row["Date"],
            "backgroundColor": color,
            "borderColor": color
        }
    )

calendar_options = {
    "initialView": "dayGridMonth",
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek"
    }
}

calendar(
    events=events,
    options=calendar_options
)

# ==========================
# EVENT STATUS MANAGER
# ==========================

st.markdown("---")

st.subheader("✅ Update Event Status")

if len(df) > 0:

    selected_event = st.selectbox(
        "Select Event",
        df["EventName"]
    )

    new_status = st.selectbox(
        "New Status",
        [
            "Upcoming",
            "In Progress",
            "Completed",
            "Cancelled"
        ]
    )

    if st.button(
        "Update Status"
    ):

        df.loc[
            df["EventName"]
            ==
            selected_event,
            "Status"
        ] = new_status

        df.to_csv(
            FILE_PATH,
            index=False
        )

        st.success(
            "Status Updated"
        )

        st.rerun()

# ==========================
# EVENT TABLE
# ==========================

st.markdown("---")

st.subheader("📋 Event Registry")

st.dataframe(
    df,
    use_container_width=True
)

# ==========================
# SUMMARY
# ==========================

st.markdown("---")

st.subheader("📊 Planning Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Total Events",
        len(df)
    )

with c2:

    st.metric(
        "Completed",
        len(
            df[
                df["Status"]
                ==
                "Completed"
            ]
        )
    )

with c3:

    st.metric(
        "Upcoming",
        len(
            df[
                df["Status"]
                ==
                "Upcoming"
            ]
        )
    )

with c4:

    st.metric(
        "In Progress",
        len(
            df[
                df["Status"]
                ==
                "In Progress"
            ]
        )
    )