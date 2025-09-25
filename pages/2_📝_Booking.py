import streamlit as st
from utils.sheets import add_lead
from datetime import datetime
st.title("📝 Book your move")
with st.form("booking_form"):
    name = st.text_input("Name*")
    email = st.text_input("Email*")
    phone = st.text_input("Phone*")
    pickup = st.text_input("Pickup address*")
    dropoff = st.text_input("Dropoff address*")
    move_date = st.date_input("Move date")
    time_window = st.selectbox("Time window", ["08:00–10:00","10:00–12:00","12:00–14:00","14:00–16:00"])
    notes = st.text_area("Notes")
    submitted = st.form_submit_button("Confirm booking", type="primary")

if submitted:
    add_lead({
        "name": name, "email": email, "phone": phone,
        "pickup": pickup, "dropoff": dropoff,
        "move_date": str(move_date), "time_window": time_window,
        "notes": notes, "status": "booked"
    })
    st.success("Booking saved to Google Sheets ✅")
    st.balloons()
