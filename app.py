import streamlit as st

st.set_page_config(page_title="SwiftMove — Moving Services", page_icon="🚚", layout="wide")

st.title("🚚 SwiftMove")
st.subheader("Stress-free house & office moves")

st.page_link("pages/1_💸_Quote_Estimator.py", label="Get an instant quote", icon="💸")
st.page_link("pages/2_📝_Booking.py", label="Book your move", icon="📝")
st.page_link("pages/3_💳_Payment.py", label="Payment", icon="💳")
st.page_link("pages/4_❓_FAQ_&_Policies.py", label="FAQ & Policies", icon="❓")
st.page_link("pages/5_📊_Admin_Dashboard.py", label="Admin dashboard", icon="📊")


query_params = st.query_params


if "payment" in query_params:
    if query_params["payment"][0] == "success":
        st.success("✅ Payment successful! Thank you.")
    elif query_params["payment"][0] == "cancel":
        st.warning("❌ Payment canceled. Please try again.")
