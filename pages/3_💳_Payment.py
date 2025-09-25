# pages/3_💳_Payment.py
import streamlit as st
import stripe

# Load Stripe keys from secrets
stripe.api_key = st.secrets["stripe"]["secret_key"]

st.title("💳 Make a Payment, Use bank details in the email after order confirmation from mover")

# Example fixed price (e.g., deposit for moving service)
amount = 50000  # amount in cents = 500.00 pound

#  if st.button("Pay $500"):
try:
    # Create a checkout session
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "gbp",
                "product_data": {
                    "name": "Moving Service Deposit",
                },
                "unit_amount": amount,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://localhost:8501/?payment=success",
        cancel_url="http://localhost:8501/?payment=cancel",
    )

    #st.markdown(
        #f"[Click here to complete payment]({session.url})",
        #unsafe_allow_html=True,
    #)

except Exception as e:
    st.error(f"Error creating checkout: {e}")
