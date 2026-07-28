import sqlite3
from datetime import date
import pandas as pd
import plotly.express as px
import streamlit as st

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="André Bostone",
    page_icon="👑",
    layout="wide"
)

# 2. CUSTOM CSS STYLING
st.markdown("""
<style>
.stApp {
    background: #0B1220;
    color: white;
}
[data-testid="stSidebar"] {
    background: #111827;
}
div[data-testid="metric-container"] {
    background: #1E293B;
    border-radius: 15px;
    padding: 20px;
    border: 1px solid #374151;
}
.stButton>button {
    width: 100%;
    background: #2563EB;
    color: white;
    border-radius: 10px;
    height: 45px;
    border: none;
}
.stButton>button:hover {
    background: #1D4ED8;
}
input {
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# 3. DATABASE INITIALIZATION
def init_db():
    conn = sqlite3.connect("database.db", check_same_thread=False)
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        email TEXT,
        service TEXT,
        amount REAL,
        expiry TEXT
    )
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS finances(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trans_date TEXT,
        trans_type TEXT,
        description TEXT,
        amount REAL
    )
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT,
        assignee TEXT,
        priority TEXT,
        status TEXT,
        due_date TEXT
    )
    """)
    
    conn.commit()
    conn.close()

init_db()

def get_connection():
    return sqlite3.connect("database.db", check_same_thread=False)

# 4. SESSION & LOGIN GUARD
if "logged" not in st.session_state:
    st.session_state.logged = False

if not st.session_state.logged:
    st.title("👑 André Bostone")
    st.subheader("Gestion des Clients")
    st.caption("Enterprise CRM • ERP • SaaS Platform")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "bostone2026":
            st.session_state.logged = True
            st.rerun()
        else:
            st.error("Incorrect username or password.")
    st.stop()

# 5. NAVIGATION SIDEBAR
st.sidebar.title("👑 André Bostone")
menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Clients", "Finance", "Tasks"]
)

conn = get_connection()

# -----------------------------------------------------------------------------
# MENU 1: DASHBOARD
# -----------------------------------------------------------------------------
if menu == "Dashboard":
    st.title("📊 Executive Dashboard")
    st.caption("Gestion des Clients • Enterprise CRM • ERP • SaaS")
    st.divider()

    # Load Data
    df_clients = pd.read_sql("SELECT * FROM clients", conn)
    df_finances = pd.read_sql("SELECT * FROM finances", conn)
    df_tasks = pd.read_sql("SELECT * FROM tasks", conn)

    # Calculations
    client_count = len(df_clients)
    income = df_finances[df_finances["trans_type"] == "Income"]["amount"].sum() if not df_finances.empty else 0.0
    expense = df_finances[df_finances["trans_type"] == "Expense"]["amount"].sum() if not df_finances.empty else 0.0
    profit = income - expense

    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("👥 Clients", client_count)
    c2.metric("💰 Income", f"${income:,.2f}")
    c3.metric("💸 Expenses", f"${expense:,.2f}")
    c4.metric("📈 Profit", f"${profit:,.2f}")

    st.divider()

    # Graph Income vs Expense
    if not df_finances.empty:
        chart_data = df_finances.groupby("trans_type")["amount"].sum().reset_index()
        fig = px.bar(
            chart_data,
            x="trans_type",
            y="amount",
            color="trans_type",
            title="Income vs Expense",
            color_discrete_map={"Income": "#10B981", "Expense": "#EF4444"}
        )
        st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# MENU 2: CLIENTS
# -----------------------------------------------------------------------------
elif menu == "Clients":
    st.title("👥 Gestion des Clients")

    # Form Add Client
    with st.form("client_form"):
        name = st.text_input("Client Name")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        service = st.selectbox(
            "Service",
            ["ChatGPT Plus", "Netflix Premium", "Canva Pro", "Spotify Premium", "YouTube Premium"]
        )
        amount = st.number_input("Monthly Amount ($)", min_value=0.0)
        expiry = st.date_input("Expiry Date", date.today())

        save = st.form_submit_button("💾 Save Client")

        if save:
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO clients (name, phone, email, service, amount, expiry)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (name, phone, email, service, amount, str(expiry)))
            conn.commit()
            st.success("Client saved successfully.")
            st.rerun()

    st.divider()

    # Load & Search
    df_clients = pd.read_sql("SELECT * FROM clients", conn)

    # Expiry Check Warning
    if not df_clients.empty:
        today = pd.Timestamp.today().normalize()
        df_clients["expiry_dt"] = pd.to_datetime(df_clients["expiry"], errors="coerce")
        expired = df_clients[df_clients["expiry_dt"] < today]

        if not expired.empty:
            st.error(f"⚠ {len(expired)} subscription(s) expired.")

    # Search Bar
    search = st.text_input("🔍 Search Client")
    filtered_df = df_clients.copy()
    
    if search and not filtered_df.empty:
        filtered_df = filtered_df[filtered_df["name"].str.contains(search, case=False, na=False)]

    # Display Data Table (ignoring temporary helper column)
    if "expiry_dt" in filtered_df.columns:
        display_df = filtered_df.drop(columns=["expiry_dt"])
    else:
        display_df = filtered_df

    st.dataframe(display_df, use_container_width=True)

    # Export CSV
    if not display_df.empty:
        st.download_button(
            "📥 Export CSV",
            display_df.to_csv(index=False),
            "clients.csv",
            "text/csv"
        )

    # Delete Section
    if not df_clients.empty:
        delete_id = st.selectbox("Delete Client", df_clients["id"])
        if st.button("🗑 Delete"):
            cur = conn.cursor()
            cur.execute("DELETE FROM clients WHERE id=?", (int(delete_id),))
            conn.commit()
            st.success("Client deleted.")
            st.rerun()

# -----------------------------------------------------------------------------
# MENU 3: FINANCE
# -----------------------------------------------------------------------------
elif menu == "Finance":
    st.title("💰 Finance Management")

    with st.form("finance_form"):
        trans_date = st.date_input("Transaction Date", date.today())
        trans_type = st.selectbox("Type", ["Income", "Expense"])
        description = st.text_input("Description")
        amount = st.number_input("Amount ($)", min_value=0.0, step=1.0)

        save = st.form_submit_button("💾 Save Transaction")

        if save:
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO finances (trans_date, trans_type, description, amount)
            VALUES (?, ?, ?, ?)
            """, (str(trans_date), trans_type, description, amount))
            conn.commit()
            st.success("Transaction saved successfully!")
            st.rerun()

    st.divider()

    df_finances = pd.read_sql("SELECT * FROM finances ORDER BY id DESC", conn)
    st.dataframe(df_finances, use_container_width=True)

    total_income = df_finances[df_finances["trans_type"] == "Income"]["amount"].sum() if not df_finances.empty else 0.0
    total_expense = df_finances[df_finances["trans_type"] == "Expense"]["amount"].sum() if not df_finances.empty else 0.0

    c1, c2 = st.columns(2)
    c1.metric("💵 Total Income", f"${total_income:,.2f}")
    c2.metric("💸 Total Expense", f"${total_expense:,.2f}")

# -----------------------------------------------------------------------------
# MENU 4: TASKS
# -----------------------------------------------------------------------------
elif menu == "Tasks":
    st.title("📋 Task Management")

    with st.form("task_form"):
        task = st.text_input("Task")
        assignee = st.text_input("Assigned To")
        priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        status = st.selectbox("Status", ["Pending", "In Progress", "Completed"])
        due_date = st.date_input("Due Date", date.today())

        save = st.form_submit_button("💾 Save Task")

        if save:
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO tasks (task, assignee, priority, status, due_date)
            VALUES (?, ?, ?, ?, ?)
            """, (task, assignee, priority, status, str(due_date)))
            conn.commit()
            st.success("Task saved successfully!")
            st.rerun()

    st.divider()

    df_tasks = pd.read_sql("SELECT * FROM tasks ORDER BY id DESC", conn)
    st.dataframe(df_tasks, use_container_width=True)

conn.close()
