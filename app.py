import streamlit as st
import pandas as pd
from datetime import datetime, date
import io

# ---------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Bostone Digital - Client & Subscription Manager",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional SaaS Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .status-active {
        color: #166534;
        background-color: #DCFCE7;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .status-expired {
        color: #991B1B;
        background-color: #FEE2E2;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Data Store Initialization (Session State)
# ---------------------------------------------------------
if 'clients' not in st.session_state:
    st.session_state.clients = [
        {"id": 1, "name": "Acme Corp", "contact": "john@acme.com", "service": "Web Hosting & SEO", "amount": 250.0, "status": "Active", "expiry_date": "2026-08-15"},
        {"id": 2, "name": "Apex Marketing", "contact": "sarah@apex.com", "service": "Social Media Mgmt", "amount": 500.0, "status": "Active", "expiry_date": "2026-08-01"},
        {"id": 3, "name": "Global Tech", "contact": "admin@globaltech.com", "service": "Custom Software", "amount": 1200.0, "status": "Expired", "expiry_date": "2026-06-30"}
    ]

if 'finances' not in st.session_state:
    st.session_state.finances = [
        {"date": "2026-07-01", "type": "Income", "category": "Subscription", "client": "Acme Corp", "amount": 250.0},
        {"date": "2026-07-01", "type": "Income", "category": "Subscription", "client": "Apex Marketing", "amount": 500.0},
        {"date": "2026-07-05", "type": "Expense", "category": "Server Cost", "client": "N/A", "amount": 120.0}
    ]

if 'tasks' not in st.session_state:
    st.session_state.tasks = [
        {"task": "Renew SSL Certificate", "assignee": "Tech Team", "priority": "High", "status": "In Progress"},
        {"task": "Send Monthly Invoice to Apex", "assignee": "Finance", "priority": "Medium", "status": "Done"},
        {"task": "Client Onboarding Call - Acme", "assignee": "Account Mgr", "priority": "Low", "status": "To Do"}
    ]

# ---------------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------------
st.sidebar.image("https://via.placeholder.com/150x50.png?text=Bostone+Digital", use_container_width=True)
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Client Registry", "Subscriptions", "Finance Ledger", "Team Tasks", "Reports & Export"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Bostone Digital Management v1.0")

# ---------------------------------------------------------
# Helper Functions for Export
# ---------------------------------------------------------
def convert_df_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    return output.getvalue()

# ---------------------------------------------------------
# View 1: Dashboard
# ---------------------------------------------------------
if menu == "Dashboard":
    st.markdown("<div class='main-header'>Bostone Digital Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Real-time overview of subscriptions, revenue, and tasks</div>", unsafe_allow_html=True)

    df_clients = pd.DataFrame(st.session_state.clients)
    df_finances = pd.DataFrame(st.session_state.finances)
    
    total_clients = len(df_clients)
    active_subs = len(df_clients[df_clients['status'] == 'Active'])
    total_revenue = df_finances[df_finances['type'] == 'Income']['amount'].sum()
    total_expenses = df_finances[df_finances['type'] == 'Expense']['amount'].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Clients", total_clients)
    col2.metric("Active Subscriptions", active_subs)
    col3.metric("Total Income", f"${total_revenue:,.2f}")
    col4.metric("Net Profit", f"${(total_revenue - total_expenses):,.2f}")

    st.markdown("---")
    st.subheader("Client Overview")
    st.dataframe(df_clients[['name', 'service', 'amount', 'status', 'expiry_date']], use_container_width=True)

# ---------------------------------------------------------
# View 2: Client Registry
# ---------------------------------------------------------
elif menu == "Client Registry":
    st.markdown("<div class='main-header'>Client Registry</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Manage client records and add new accounts</div>", unsafe_allow_html=True)

    with st.expander("➕ Add New Client"):
        with st.form("add_client_form"):
            c_name = st.text_input("Client / Company Name")
            c_contact = st.text_input("Contact Email")
            c_service = st.text_input("Service Provided")
            c_amount = st.number_input("Monthly Fee ($)", min_value=0.0, step=10.0)
            c_expiry = st.date_input("Subscription Renewal Date", date.today())
            
            submitted = st.form_submit_button("Save Client")
            if submitted and c_name:
                new_id = len(st.session_state.clients) + 1
                st.session_state.clients.append({
                    "id": new_id,
                    "name": c_name,
                    "contact": c_contact,
                    "service": c_service,
                    "amount": c_amount,
                    "status": "Active",
                    "expiry_date": str(c_expiry)
                })
                st.success(f"Client '{c_name}' added successfully!")
                st.rerun()

    df_clients = pd.DataFrame(st.session_state.clients)
    st.dataframe(df_clients, use_container_width=True)

# ---------------------------------------------------------
# View 3: Subscriptions
# ---------------------------------------------------------
elif menu == "Subscriptions":
    st.markdown("<div class='main-header'>Subscription Tracker</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Monitor renewal dates and active/expired status</div>", unsafe_allow_html=True)

    df_clients = pd.DataFrame(st.session_state.clients)
    for idx, row in df_clients.iterrows():
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 1.5, 1])
        col1.write(f"**{row['name']}**")
        col2.write(row['service'])
        col3.write(f"Expires: {row['expiry_date']}")
        
        status_class = "status-active" if row['status'] == "Active" else "status-expired"
        col4.markdown(f"<span class='{status_class}'>{row['status']}</span>", unsafe_allow_html=True)
        
        if col5.button("Toggle Status", key=f"btn_{idx}"):
            st.session_state.clients[idx]['status'] = "Expired" if row['status'] == "Active" else "Active"
            st.rerun()

# ---------------------------------------------------------
# View 4: Finance Ledger
# ---------------------------------------------------------
elif menu == "Finance Ledger":
    st.markdown("<div class='main-header'>Finance Ledger</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Log business revenue and recurring operational costs</div>", unsafe_allow_html=True)

    with st.expander("➕ Add Transaction"):
        with st.form("add_finance_form"):
            f_date = st.date_input("Date", date.today())
            f_type = st.selectbox("Type", ["Income", "Expense"])
            f_category = st.text_input("Category (e.g. Hosting, Subscription, Tools)")
            f_client = st.text_input("Client/Vendor Name", "N/A")
            f_amount = st.number_input("Amount ($)", min_value=0.0, step=5.0)
            
            submitted = st.form_submit_button("Record Transaction")
            if submitted:
                st.session_state.finances.append({
                    "date": str(f_date),
                    "type": f_type,
                    "category": f_category,
                    "client": f_client,
                    "amount": f_amount
                })
                st.success("Transaction recorded!")
                st.rerun()

    df_finances = pd.DataFrame(st.session_state.finances)
    st.dataframe(df_finances, use_container_width=True)

# ---------------------------------------------------------
# View 5: Team Tasks
# ---------------------------------------------------------
elif menu == "Team Tasks":
    st.markdown("<div class='main-header'>Team Task Board</div>", unsafe_allow_header=True)
    st.markdown("<div class='sub-header'>Track internal team deliverables</div>", unsafe_allow_html=True)

    with st.expander("➕ Add New Task"):
        with st.form("add_task_form"):
            t_name = st.text_input("Task Title")
            t_assignee = st.text_input("Assignee")
            t_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
            t_status = st.selectbox("Status", ["To Do", "In Progress", "Done"])
            
            submitted = st.form_submit_button("Create Task")
            if submitted and t_name:
                st.session_state.tasks.append({
                    "task": t_name,
                    "assignee": t_assignee,
                    "priority": t_priority,
                    "status": t_status
                })
                st.success("Task created!")
                st.rerun()

    df_tasks = pd.DataFrame(st.session_state.tasks)
    st.dataframe(df_tasks, use_container_width=True)

# ---------------------------------------------------------
# View 6: Reports & Export
# ---------------------------------------------------------
elif menu == "Reports & Export":
    st.markdown("<div class='main-header'>Reports & Monthly Export</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Download data logs for bookkeeping and reporting</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Client & Subscription Data")
        df_clients = pd.DataFrame(st.session_state.clients)
        excel_data_clients = convert_df_to_excel(df_clients)
        st.download_button(
            label="📥 Download Clients (Excel)",
            data=excel_data_clients,
            file_name="bostone_digital_clients.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    with col2:
        st.subheader("Financial Ledger Data")
        df_finances = pd.DataFrame(st.session_state.finances)
        excel_data_finances = convert_df_to_excel(df_finances)
        st.download_button(
            label="📥 Download Financials (Excel)",
            data=excel_data_finances,
            file_name="bostone_digital_finances.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
