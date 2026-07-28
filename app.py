import io
from datetime import date, datetime
import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Bostone Digital - Enterprise SaaS",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# Dark Professional Custom CSS
# ---------------------------------------------------------
st.markdown(
    """
<style>
    /* Dark Theme Sidebar Customization */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
    }
    [data-testid="stSidebar"] * {
        color: #E2E8F0 !important;
    }
    
    /* Main Canvas Headers */
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 0.1rem;
        letter-spacing: -0.5px;
    }
    .sub-header {
        font-size: 1rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    
    /* Professional Badges */
    .status-active {
        color: #15803D;
        background-color: #DCFCE7;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    .status-expired {
        color: #B91C1C;
        background-color: #FEE2E2;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    
    /* Copyright Watermark Badge */
    .watermark-badge {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        margin-top: 20px;
    }
    .watermark-title {
        color: #D97706 !important;
        font-weight: bold;
        font-size: 0.85rem;
        margin-bottom: 2px;
    }
    .watermark-sub {
        color: #94A3B8 !important;
        font-size: 0.7rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "currency" not in st.session_state:
    st.session_state.currency = "USD"

if "clients" not in st.session_state:
    st.session_state.clients = [
        {
            "id": 1,
            "name": "Acme Corp",
            "contact": "john@acme.com",
            "service": "Web Hosting & SEO",
            "amount": 250.0,
            "status": "Active",
            "expiry_date": "2026-08-15",
        },
        {
            "id": 2,
            "name": "Apex Marketing",
            "contact": "sarah@apex.com",
            "service": "Social Media Mgmt",
            "amount": 500.0,
            "status": "Active",
            "expiry_date": "2026-08-01",
        },
        {
            "id": 3,
            "name": "Global Tech",
            "contact": "admin@globaltech.com",
            "service": "Custom Software",
            "amount": 1200.0,
            "status": "Expired",
            "expiry_date": "2026-06-30",
        },
    ]

if "finances" not in st.session_state:
    st.session_state.finances = [
        {
            "date": "2026-07-01",
            "type": "Income",
            "category": "Subscription",
            "client": "Acme Corp",
            "amount": 250.0,
        },
        {
            "date": "2026-07-01",
            "type": "Income",
            "category": "Subscription",
            "client": "Apex Marketing",
            "amount": 500.0,
        },
        {
            "date": "2026-07-05",
            "type": "Expense",
            "category": "Server Cost",
            "client": "N/A",
            "amount": 120.0,
        },
    ]

if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {
            "task": "Renew SSL Certificate",
            "assignee": "Tech Team",
            "priority": "High",
            "status": "In Progress",
        },
        {
            "task": "Send Monthly Invoice to Apex",
            "assignee": "Finance",
            "priority": "Medium",
            "status": "Done",
        },
        {
            "task": "Client Onboarding Call - Acme",
            "assignee": "Account Mgr",
            "priority": "Low",
            "status": "To Do",
        },
    ]

# ---------------------------------------------------------
# Currency Conversion Setup
# ---------------------------------------------------------
CURRENCY_RATES = {
    "USD ($)": {"symbol": "$", "rate": 1.0},
    "MGA (Malagasy Ariary)": {"symbol": "Ar ", "rate": 4500.0},
    "EUR (€)": {"symbol": "€", "rate": 0.92},
    "GBP (£)": {"symbol": "£", "rate": 0.78},
    "CAD (CA$)": {"symbol": "CA$", "rate": 1.36},
}


def fmt_amt(val_usd):
    curr_key = st.session_state.currency
    info = CURRENCY_RATES[curr_key]
    converted = val_usd * info["rate"]
    return f"{info['symbol']}{converted:,.2f}"


# ---------------------------------------------------------
# Authentication Guard (Lock Screen)
# ---------------------------------------------------------
def login_screen():
    st.markdown("## 🔒 Bostone Digital - Secure Login")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Log In")

            if submit:
                if username == "admin" and password == "bostone2026":
                    st.session_state.authenticated = True
                    st.success("Authenticated successfully!")
                    st.rerun()
                else:
                    st.error("Invalid credentials (Default: admin / bostone2026)")


if not st.session_state.authenticated:
    login_screen()
    st.stop()

# ---------------------------------------------------------
# Sidebar Controls & Lock System
# ---------------------------------------------------------
st.sidebar.markdown("### 👑 BOSTONE DIGITAL")
st.sidebar.caption("Client & Subscription Manager")

if st.sidebar.button("🔒 Lock Session"):
    st.session_state.authenticated = False
    st.rerun()

st.sidebar.markdown("---")

# Currency Selector
st.sidebar.subheader("💱 Currency Switcher")
st.session_state.currency = st.sidebar.selectbox(
    "Display Currency", list(CURRENCY_RATES.keys()), index=0
)

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Client Registry",
        "Subscriptions",
        "Finance Ledger",
        "Team Tasks",
        "Reports & Export",
    ],
)

# Copyright Watermark Footer
st.sidebar.markdown(
    """
    <div class="watermark-badge">
        <div class="watermark-title">BOSTONE DIGITAL</div>
        <div class="watermark-sub">Adapt. Survive. Conquer.</div>
        <div class="watermark-sub">© 2026 All Rights Reserved</div>
    </div>
""",
    unsafe_allow_html=True,
)


def convert_df_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
    return output.getvalue()


# ---------------------------------------------------------
# View 1: Dashboard
# ---------------------------------------------------------
if menu == "Dashboard":
    st.markdown(
        "<div class='main-header'>Bostone Digital Dashboard</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='sub-header'>Real-time overview of subscriptions, revenue, and tasks</div>",
        unsafe_allow_html=True,
    )

    df_clients = pd.DataFrame(st.session_state.clients)
    df_finances = pd.DataFrame(st.session_state.finances)

    total_clients = len(df_clients)
    active_subs = len(df_clients[df_clients["status"] == "Active"])
    total_revenue = df_finances[df_finances["type"] == "Income"][
        "amount"
    ].sum()
    total_expenses = df_finances[df_finances["type"] == "Expense"][
        "amount"
    ].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Clients", total_clients)
    col2.metric("Active Subscriptions", active_subs)
    col3.metric("Total Income", fmt_amt(total_revenue))
    col4.metric("Net Profit", fmt_amt(total_revenue - total_expenses))

    st.markdown("---")
    st.subheader("Client Overview")

    display_df = df_clients.copy()
    display_df["amount"] = display_df["amount"].apply(fmt_amt)
    st.dataframe(
        display_df[["name", "service", "amount", "status", "expiry_date"]],
        use_container_width=True,
    )

# ---------------------------------------------------------
# View 2: Client Registry
# ---------------------------------------------------------
elif menu == "Client Registry":
    st.markdown(
        "<div class='main-header'>Client Registry</div>", unsafe_allow_html=True
    )
    st.markdown(
        "<div class='sub-header'>Manage client records and add new accounts</div>",
        unsafe_allow_html=True,
    )

    with st.expander("➕ Add New Client"):
        with st.form("add_client_form"):
            c_name = st.text_input("Client / Company Name")
            c_contact = st.text_input("Contact Email")
            c_service = st.text_input("Service Provided")
            c_amount = st.number_input(
                "Monthly Fee (USD Base)", min_value=0.0, step=10.0
            )
            c_expiry = st.date_input(
                "Subscription Renewal Date", date.today()
            )

            if st.form_submit_button("Save Client") and c_name:
                new_id = len(st.session_state.clients) + 1
                st.session_state.clients.append({
                    "id": new_id,
                    "name": c_name,
                    "contact": c_contact,
                    "service": c_service,
                    "amount": c_amount,
                    "status": "Active",
                    "expiry_date": str(c_expiry),
                })
                st.success(f"Client '{c_name}' added successfully!")
                st.rerun()

    df_clients = pd.DataFrame(st.session_state.clients)
    df_clients["amount"] = df_clients["amount"].apply(fmt_amt)
    st.dataframe(df_clients, use_container_width=True)

# ---------------------------------------------------------
# View 3: Subscriptions
# ---------------------------------------------------------
elif menu == "Subscriptions":
    st.markdown(
        "<div class='main-header'>Subscription Tracker</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='sub-header'>Monitor renewal dates and active/expired status</div>",
        unsafe_allow_html=True,
    )

    for idx, client in enumerate(st.session_state.clients):
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 1.5, 1])
        col1.write(f"**{client['name']}**")
        col2.write(f"{client['service']} ({fmt_amt(client['amount'])})")
        col3.write(f"Expires: {client['expiry_date']}")

        status_class = (
            "status-active"
            if client["status"] == "Active"
            else "status-expired"
        )
        col4.markdown(
            f"<span class='{status_class}'>{client['status']}</span>",
            unsafe_allow_html=True,
        )

        if col5.button("Toggle Status", key=f"btn_{client['id']}"):
            st.session_state.clients[idx]["status"] = (
                "Expired" if client["status"] == "Active" else "Active"
            )
            st.rerun()

# ---------------------------------------------------------
# View 4: Finance Ledger
# ---------------------------------------------------------
elif menu == "Finance Ledger":
    st.markdown(
        "<div class='main-header'>Finance Ledger</div>", unsafe_allow_html=True
    )
    st.markdown(
        "<div class='sub-header'>Log business revenue and recurring operational costs</div>",
        unsafe_allow_html=True,
    )

    with st.expander("➕ Add Transaction"):
        with st.form("add_finance_form"):
            f_date = st.date_input("Date", date.today())
            f_type = st.selectbox("Type", ["Income", "Expense"])
            f_category = st.text_input("Category")
            f_client = st.text_input("Client/Vendor Name", "N/A")
            f_amount = st.number_input(
                "Amount (USD Base)", min_value=0.0, step=5.0
            )

            if st.form_submit_button("Record Transaction"):
                st.session_state.finances.append({
                    "date": str(f_date),
                    "type": f_type,
                    "category": f_category,
                    "client": f_client,
                    "amount": f_amount,
                })
                st.success("Transaction recorded!")
                st.rerun()

    df_finances = pd.DataFrame(st.session_state.finances)
    df_finances["amount"] = df_finances["amount"].apply(fmt_amt)
    st.dataframe(df_finances, use_container_width=True)

# ---------------------------------------------------------
# View 5: Team Tasks
# ---------------------------------------------------------
elif menu == "Team Tasks":
    st.markdown(
        "<div class='main-header'>Team Task Board</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='sub-header'>Track internal team deliverables</div>",
        unsafe_allow_html=True,
    )

    with st.expander("➕ Add New Task"):
        with st.form("add_task_form"):
            t_name = st.text_input("Task Title")
            t_assignee = st.text_input("Assignee")
            t_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
            t_status = st.selectbox("Status", ["To Do", "In Progress", "Done"])

            if st.form_submit_button("Create Task") and t_name:
                st.session_state.tasks.append({
                    "task": t_name,
                    "assignee": t_assignee,
                    "priority": t_priority,
                    "status": t_status,
                })
                st.success("Task created!")
                st.rerun()

    df_tasks = pd.DataFrame(st.session_state.tasks)
    st.dataframe(df_tasks, use_container_width=True)

# ---------------------------------------------------------
# View 6: Reports & Export
# ---------------------------------------------------------
elif menu == "Reports & Export":
    st.markdown(
        "<div class='main-header'>Reports & Monthly Export</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='sub-header'>Download data logs for bookkeeping and reporting</div>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Client & Subscription Data")
        st.download_button(
            label="📥 Download Clients (Excel)",
            data=convert_df_to_excel(pd.DataFrame(st.session_state.clients)),
            file_name="bostone_digital_clients.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    with col2:
        st.subheader("Financial Ledger Data")
        st.download_button(
            label="📥 Download Financials (Excel)",
            data=convert_df_to_excel(pd.DataFrame(st.session_state.finances)),
            file_name="bostone_digital_finances.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
