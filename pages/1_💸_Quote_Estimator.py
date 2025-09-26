import streamlit as st
import pandas as pd
from utils.sheets import add_lead,add_inventory  # <-- your Google Sheets helper

# --- Load Moving Items ---
@st.cache_data
def load_items():
    df = pd.read_csv("moving_items.csv")  # Ensure file is in your project root
    # Standardize column name for easier access
    df = df.rename(columns={"Volume (ftÂ³)": "Volume"})
    return df

items_df = load_items()

st.title("💸 Approximate Quote Estimator and submit a Quote For Moving ")

# --- Customer details ---
st.subheader("👤 Customer Information")
with st.form("quote_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    move_date = st.date_input("Preferred Moving Date")
    distance_in_miles=st.number_input("enter distance in miles")
    Additional_Notes = st.text_area("Additional Notes")

    st.subheader("📦 Select Items for Move")
    categories = items_df["Item"].unique()
    st.write(f"""Hello, Thank you for using our service, please go to the Booking page to confirm your booking.
             It is important to select items and submit using the button at the end of this page.""")
    st.write(f"Hello these are categories, {categories}!")

    selected_items = []
    total_volume = 0

    for cat in categories:
        st.markdown(f"#### {cat}")
        cat_items = items_df[items_df["Item"] == cat]

        for _, row in cat_items.iterrows():
            qty = st.number_input(
                f"{row['Item']} ({row['Volume']} cu ft each)",
                min_value=0, max_value=20, step=1, key=row['Item']
            )
            if qty > 0:
                selected_items.append((row["Item"], qty, row["Volume"]))
                total_volume += qty * row["Volume"]

    # --- Pricing logic ---
    price_short_distance= 1
    price_medium_distance= 1.5
    price_per_cuft = 2  # Example rate: £2 per cubic foot for long travel move
    if distance_in_miles <80:
        total_price = total_volume * price_short_distance
    elif distance_in_miles<150:
        total_price = total_volume * price_medium_distance
    else:
        total_price = total_volume * price_per_cuft
    if st.form_submit_button("Quote Estimate"):
        st.markdown("### 📊 Quote Summary")
        for item, qty, vol in selected_items:
            st.write(f"- {qty} × {item} = {qty * vol} cu ft")

        st.info(f"**Total Volume:** {total_volume} cu ft")
        st.info(f"**Estimated Price:** £{total_price:,.2f}")

    submitted = st.form_submit_button("Submit")

    if submitted:
        if not name or not email or not phone or not move_date:
            st.error("⚠️ Please fill in your name,phone number,move date and email.")
        elif not selected_items:
            st.error("⚠️ Please select at least one item.")
        else:
            # Save lead to Google Sheets
            add_inventory({
                "name": name,
                "email": email,
                "phone": phone,
                "move_date": str(move_date),
                "Additional_Notes":str(Additional_Notes),
                "items": ", ".join([f"{qty}x {item}" for item, qty, _ in selected_items]),
                "total_volume": total_volume,
                "est_price":total_price
            })
            # Show summary
            st.success("✅ Quote saved and sent to admin dashboard!")

            st.markdown("### 📊 Quote Summary")
            for item, qty, vol in selected_items:
                st.write(f"- {qty} × {item} = {qty * vol} cu ft")

            st.info(f"**Total Volume:** {total_volume} cu ft")
            st.info(f"**Estimated Price:** £{total_price:,.2f}")