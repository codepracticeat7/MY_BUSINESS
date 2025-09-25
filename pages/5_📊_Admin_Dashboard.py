import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth

from utils.pricing import pretty
from utils.sheets import fetch_leads, update_status, send_email,show_inventory,fetch_inventory

st.title("📊 Admin Dashboard")

# --- Authentication ---
credentials = {
    "usernames": {
        st.secrets["auth"]["admin_email"]: {
            "email": st.secrets["auth"]["admin_email"],
            "name": "Admin",
            "password": st.secrets["auth"]["admin_pw"],
        }
    }
}

authenticator = stauth.Authenticate(
    credentials,
    st.secrets["auth"]["cookie_name"],
    st.secrets["auth"]["signature_key"],
    cookie_expiry_days=1
)

# --- Login ---
authenticator.login()  # ✅ no arguments needed in v0.4.2

# --- Check authentication status ---
if st.session_state.get("authentication_status"):
    st.success(f"✅ Welcome {st.session_state['name']}")

    # Fetch leads
    leads = fetch_leads()
    df = pd.DataFrame(leads)
    inventory_data=fetch_inventory()
    df2 = pd.DataFrame(inventory_data)

    if not df.empty:
        # Clean est_price column safely
        if "est_price" in df.columns:
            df["est_price"] = (
                pd.to_numeric(df["est_price"], errors="coerce")
                .fillna(0)
                .astype(int)
                .apply(pretty)
            )

        st.subheader("📋 All Leads")
        st.dataframe(df, use_container_width=True)

        # Download CSV
        st.download_button(
            "⬇️ Download leads CSV",
            df.to_csv(index=False),
            "leads.csv",
            mime="text/csv"
        )

        # Detailed view
        st.subheader("🔍 Lead Details")
        lead_names = df["name"].tolist()
        selected_lead = st.selectbox("Select a customer", lead_names)
        if st.button("📦 Load Inventory"):
            show_inventory(selected_lead,df2)


        if selected_lead:
            lead_row = df[df["name"] == selected_lead].iloc[0]
            st.subheader(repr(lead_row.index.tolist()))

            st.markdown(f"### 👤 {lead_row['name']}")
            if st.button("Notes"):
                st.write(f"📝 Notes: {lead_row['notes']}")
            st.markdown("#### 📊 Quote Summary")
            st.write(f"{lead_row['email']}, 📞 {lead_row['phone ']}, Total Volume:** {lead_row['volume_m3']} cu ft,  Move date: {lead_row['move_date']},  Estimated Price: ** {lead_row['est_price']}")
            st.write(f"**")
            if st.button("SHOW_FULL_LEAD_DETAILS"):
                st.dataframe(lead_row, use_container_width=True)
            # --- Status update ---
            st.markdown("#### 🚦 Update Status")
            current_status = lead_row.get("status", "quoted")
            status_options = ["quoted", "booked", "paid", "completed"]
            new_status = st.selectbox(
                "Change status",
                status_options,
                index=status_options.index(current_status)
                if current_status in status_options else 0
            )

            if st.button("💾 Save Status"):
                if update_status(selected_lead, new_status):
                    st.success(f"✅ Status updated to {new_status}")
                else:
                    st.error("❌ Failed to update status")

    else:
        st.warning("⚠️ No leads found yet.")

    # --- Logout ---
    authenticator.logout()

elif st.session_state.get("authentication_status") is False:
    st.error("❌ Invalid username or password")
else:
    st.info("🔑 Please log in to view admin dashboard")
