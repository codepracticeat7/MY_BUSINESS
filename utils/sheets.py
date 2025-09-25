import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- Auth scopes ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# --- Google Sheets client ---
@st.cache_resource
def get_client():
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        st.secrets["google"], scope
    )
    return gspread.authorize(creds)

def get_sheet(sheet_name="Leads"):
    """Return a worksheet by name."""
    client = get_client()
    # Get sheet name from secrets, e.g. st.secrets["google"]["sheet_name"]
    sh = client.open(st.secrets["google"]["sheet_name"])
    return sh.worksheet(sheet_name)

# --- Leads ---
def fetch_leads():
    ws = get_sheet("Leads")
    return ws.get_all_records()

def add_lead(data: dict):
    """
    Append a new lead with timestamp.
    data should be a dict with keys matching your sheet headers.
    """
    ws = get_sheet("Leads")
    row = [datetime.now().strftime('%d/%m/%Y %H:%M:%S')] + [data.get(k, "") for k in data.keys()]
    ws.append_row(row, value_input_option="USER_ENTERED")

def update_status(lead_name: str, new_status: str) -> bool:
    """
    Update the 'status' column for a lead with given name.
    Returns True if updated, False if not found.
    """
    ws = get_sheet("Leads")
    records = ws.get_all_records()
    for i, row in enumerate(records, start=2):  # row 1 = header
        if row.get("name") == lead_name:
            # Find index of "status" column
            col_index = list(row.keys()).index("status") + 1
            ws.update_cell(i, col_index, new_status)
            return True
    return False

# --- Inventory ---
def add_inventory(data: dict):
    """
    Append inventory items linked to a lead.
    items should be list of tuples: (item, qty, volume)
    """
    ws = get_sheet("Inventory")
    row = [datetime.now().strftime('%d/%m/%Y %H:%M:%S')] + [data.get(k, "") for k in data.keys()]
    ws.append_row(row, value_input_option="USER_ENTERED")
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

def send_email(to_email, subject, body):
    sender = st.secrets["email"]["sender"]
    password = st.secrets["email"]["password"]
    smtp_server = st.secrets["email"]["smtp_server"]
    smtp_port = st.secrets["email"]["smtp_port"]

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Email failed: {e}")
        return False

def fetch_inventory():
    ws = get_sheet("Inventory")
    return ws.get_all_records()

def show_inventory(selected_lead,df2):
    st.session_state["show_inventory"] = True
    inventory_row = df2[df2["Name"] == selected_lead]
    if inventory_row.shape[0]!=0:
        if st.session_state["show_inventory"]:
            st.subheader("Inventory Table")
            st.dataframe(inventory_row)
        if st.button("❌ Exit Inventory"):
            st.session_state["show_inventory"] = False
    else:
        st.write(f"No inventory for {selected_lead}")

