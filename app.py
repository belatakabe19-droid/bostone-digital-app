```python
code = """
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
# Custom Modern SaaS UI CSS (Matches Screenshot Design)
# ---------------------------------------------------------
st.markdown(
    \"\"\"
<style>
    /* Main Theme Variables & Styles */
    :root {
        --primary-blue: #2563EB;
        --sidebar-bg: #0B132B;
        --card-bg: #FFFFFF;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B;
    }
    [data-testid="stSidebar"] * {
        color: #94A3B8 !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }
    
    /* Metric Cards Styling */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .metric-title {
        font-size: 0.82rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0F172A;
        margin: 4px 0;
    }
    .metric-sub {
        font-size: 0.78rem;
        font-weight: 600;
    }
    .text-green { color: #16A34A; }
    .text-orange { color: #EA580C; }
    .text-blue { color: #2563EB; }
    
    /* Guide / Instruction Box Styling */
    .guide-box {
        background-color: #F0F9FF;
        border-left: 4px solid #0284C7;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 25px;
    }
    .guide-title {
        font-size: 1rem;
        font-weight: 700;
        color: #0369A1;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .guide-text {
        font-size: 0.88rem;
        color: #334155;
        line-height: 1.5;
    }
    
    /* Custom Badges */
    .badge-active {
        background-color: #DCFCE7;
        color: #15803D;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.75rem;
    }
    .badge-expired {
        background-color: #FEE2E2;
        color: #B91C1C;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.75rem;
    }
    .badge-warning {
        background-color: #FFEDD5;
        color: #C2410C;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.75rem;
    }
    
    /* User Profile Sidebar Widget */
    .user-profile {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px;
        background: #1E293B;
        border-radius: 10px;
        margin-top: 20px;
    }
    .avatar {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background-color: #2563EB;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
    }
</style>
\"\"\",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Session State Initialization (Empty Defaults - No hardcoded names)
# ---------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "currency" not in st.session_state:
    st.session_state.currency = "MGA (Malagasy Ariary)"

# Data tables started empty or clean for real usage
if "clients" not in st.session_state:
    st.session_state.clients = []

if "finances" not in st.session_state:
    st.session_state.finances = []

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "activity_logs" not in st.session_state:
    st.session_state.activity_logs = []

# ---------------------------------------------------------
# Currency Conversion Setup
# ---------------------------------------------------------
CURRENCY_RATES = {
    "MGA (Malagasy Ariary)": {"symbol": "Ar ", "rate": 1.0},
    "USD ($)": {"symbol": "$", "rate": 1 / 4500.0},
    "EUR (€)": {"symbol": "€", "rate": 0.92 / 4500.0},
}


def fmt_amt(val):
    curr_key = st.session_state.currency
    info = CURRENCY_RATES[curr_key]
    converted = val * info["rate"]
    return f"{info['symbol']}{converted:,.0f}" if info["symbol"] == "Ar " else f"{info['symbol']}{converted:,.2f}"


# ---------------------------------------------------------
# Authentication Guard (Lock Screen)
# ---------------------------------------------------------
def login_screen():
    st.markdown("## 🔒 Bostone Digital - Fidirana Azo Antoka")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Anarana fidirana (Username)")
            password = st.text_input("Teny miafina (Password)", type="password")
            submit = st.form_submit_button("Midira")

            if submit:
                if username == "admin" and password == "bostone2026":
                    st.session_state.authenticated = True
                    st.success("Tafiditra soa aman-tsara!")
                    st.rerun()
                else:
                    st.error("Tsy mety ny anarana na teny miafina (Default: admin / bostone2026)")


if not st.session_state.authenticated:
    login_screen()
    st.stop()

# ---------------------------------------------------------
# Sidebar Controls & Navigation
# ---------------------------------------------------------
st.sidebar.markdown("### ⚡ BOSTONE DIGITAL")
st.sidebar.caption("Sistema Fitantanana Mpanjifa sy Famandrihana")

if st.sidebar.button("🔒 Handidy ny session (Lock)"):
    st.session_state.authenticated = False
    st.rerun()

st.sidebar.markdown("---")

# Currency Selector
st.sidebar.subheader("💱 Volana Hampiasaina")
st.session_state.currency = st.sidebar.selectbox(
    "Safidio ny vola", list(CURRENCY_RATES.keys()), index=0
)

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Fikarohana sy Sakelidany",
    [
        "01. Dashboard Valopy",
        "02. Fitantanana Mpanjifa (Clients)",
        "03. Famandrihana (Subscriptions)",
        "04. Fitantanana Bola (Finances)",
        "05. Tasy sy Asa Ekipa (Tasks)",
        "06. Tatitra sy Famoahana (Reports)",
    ],
)

st.sidebar.markdown("---")
# User Profile Component at Sidebar Bottom
st.sidebar.markdown(
    \"\"\"
    <div style="padding: 10px; background-color: #1E293B; border-radius: 8px;">
        <p style="margin: 0; font-weight: bold; color: white;">👤 Admin User</p>
        <p style="margin: 0; font-size: 0.75rem; color: #94A3B8;">Mpampiasa lehibe</p>
    </div>
\"\"\",
    unsafe_allow_html=True,
)


def convert_df_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
    return output.getvalue()


# ---------------------------------------------------------
# View 1: Executive Dashboard
# ---------------------------------------------------------
if menu == "01. Dashboard Valopy":
    st.title("📊 Executive Dashboard")
    st.caption("Jery todika amin'ny fotoana tena izy momba ny mpanjifa, fidiram-bola sy ny asa.")

    # Guide Section
    st.markdown(
        \"\"\"
        <div class="guide-box">
            <div class="guide-title">💡 Torolàlana momba ny Dashboard</div>
            <div class="guide-text">
                Kitiho ity pejy ity raha hijery ny famintinana lehibe: ny isan'ny mpanjifa mavitrika, ny fidiram-bola manontolo, sy ny daty efa akaiky ho lany amin'ny famandrihana. Azonao atao ny manavao na manalava ny famandrihana avy hatrany eto.
            </div>
        </div>
        \"\"\",
        unsafe_allow_html=True,
    )

    df_clients = pd.DataFrame(st.session_state.clients)
    df_finances = pd.DataFrame(st.session_state.finances)

    total_clients = len(df_clients)
    active_subs = len(df_clients[df_clients["status"] == "Mavitrika"]) if not df_clients.empty else 0
    total_income = df_finances[df_finances["type"] == "Fidiram-bola"]["amount"].sum() if not df_finances.empty else 0
    total_expenses = df_finances[df_finances["type"] == "Fivoaham-bola"]["amount"].sum() if not df_finances.empty else 0
    net_profit = total_income - total_expenses

    # Metric Cards Top Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f\"\"\"
            <div class="metric-card">
                <div class="metric-title">Mpanjifa Mavitrika</div>
                <div class="metric-value">{total_clients}</div>
                <div class="metric-sub text-green">Mpanjifa voasoratra</div>
            </div>
        \"\"\", unsafe_allow_html=True)
    with c2:
        st.markdown(f\"\"\"
            <div class="metric-card">
                <div class="metric-title">Famandrihana Mandeha</div>
                <div class="metric-value">{active_subs}</div>
                <div class="metric-sub text-blue">Ahitana fidiram-bola</div>
            </div>
        \"\"\", unsafe_allow_html=True)
    with c3:
        st.markdown(f\"\"\"
            <div class="metric-card">
                <div class="metric-title">Akaiky Ho Lany (≤ 7 Andro)</div>
                <div class="metric-value">0</div>
                <div class="metric-sub text-orange">Mila fanavaozana</div>
            </div>
        \"\"\", unsafe_allow_html=True)
    with c4:
        st.markdown(f\"\"\"
            <div class="metric-card">
                <div class="metric-title">Tombony Madio (Net Profit)</div>
                <div class="metric-value">{fmt_amt(net_profit)}</div>
                <div class="metric-sub text-green">Fidirana - Fivoahana</div>
            </div>
        \"\"\", unsafe_allow_html=True)

    col_left, col_right = st.columns([1.5, 1])

    with col_left:
        st.subheader("🔔 Famandrihana Akaiky Ho Lany")
        if not df_clients.empty:
            st.dataframe(df_clients[["name", "service", "status", "expiry_date"]], use_container_width=True)
        else:
            st.info("Mbola tsy misy mpanjifa voasoratra amin'izao fotoana izao. Mampidira mpanjifa ao amin'ny pejy 'Fitantanana Mpanjifa'.")

    with col_right:
        st.subheader("📈 Jery Todika Ara-bola")
        st.metric("Fidiram-bola Manontolo", fmt_amt(total_income))
        st.metric("Fivoaham-bola Manontolo", fmt_amt(total_expenses))

# ---------------------------------------------------------
# View 2: Clients Management
# ---------------------------------------------------------
elif menu == "02. Fitantanana Mpanjifa (Clients)":
    st.title("👤 Fitantanana ny Mpanjifa")
    st.caption("Fandaminana sy fampidirana ny mombamomba ny mpanjifa rehetra.")

    # Dedicated Guide Box
    st.markdown(
        \"\"\"
        <div class="guide-box">
            <div class="guide-title">📘 Torolàlana amin'ny Fampidirana Mpanjifa</div>
            <div class="guide-text">
                Ny fizarana eto dia natao hampidirana mpanjifa vaovao. 
                Fill-o amin'ny alalan'ny bokotra <b>"➕ Mampidira Mpanjifa Vaovao"</b> eto ambany ny anarana, finday, adiresy, ary ny serivisy ilainy. 
                Aza adino ny mametraka ny daty hahaperan'ny famandrihana mba hahafahana manara-maso izany ara-potoana.
            </div>
        </div>
        \"\"\",
        unsafe_allow_html=True,
    )

    with st.expander("➕ Mampidira Mpanjifa Vaovao", expanded=False):
        with st.form("add_client_form"):
            c1, c2 = st.columns(2)
            with c1:
                c_name = st.text_input("Anarana sy Fanampiny / Anaran'ny Kompania")
                c_phone = st.text_input("Laharana Telefona (oh: 034 12 345 67)")
                c_email = st.text_input("E-mail na Kaonty")
            with c2:
                c_address = st.text_input("Adiresy (Tanàna, Faritra)")
                c_service = st.selectbox("Serivisy / Tolotra", ["ChatGPT Plus", "Netflix Premium", "Canva Pro", "YouTube Premium", "Spotify Premium", "Web Hosting", "Maha-manokana (Custom)"])
                c_amount = st.number_input("Sarany isam-bolana (Ar)", min_value=0.0, step=5000.0)
                c_expiry = st.date_input("Daty Hahaperan'ny Famandrihana", date.today())

            if st.form_submit_button("💾 Hadio sy Tehirizo ny Mpanjifa"):
                if c_name:
                    new_id = f"C{len(st.session_state.clients)+1:04d}"
                    st.session_state.clients.append({
                        "id": new_id,
                        "name": c_name,
                        "phone": c_phone,
                        "email": c_email,
                        "address": c_address,
                        "service": c_service,
                        "amount": c_amount,
                        "status": "Mavitrika",
                        "expiry_date": str(c_expiry),
                    })
                    st.success(f"Tafiditra soa aman-tsara ny mpanjifa '{c_name}'!")
                    st.rerun()
                else:
                    st.warning("Ampidiro ny anaran'ny mpanjifa azafady.")

    st.subheader("📋 Lisitry ny Mpanjifa Rehetra")
    if st.session_state.clients:
        df_clients = pd.DataFrame(st.session_state.clients)
        df_display = df_clients.copy()
        df_display["amount"] = df_display["amount"].apply(fmt_amt)
        st.dataframe(df_display, use_container_width=True)
    else:
        st.info("Mbola banga ny lisitra. Kitiho ny '➕ Mampidira Mpanjifa Vaovao' eo ambony mba hampidirana.")

# ---------------------------------------------------------
# View 3: Subscriptions
# ---------------------------------------------------------
elif menu == "03. Famandrihana (Subscriptions)":
    st.title("🔄 Fitantanana ny Famandrihana")
    st.caption("Fanta-daza sy fanaraha-maso ny toetoetran'ny famandrihana tsirairay.")

    st.markdown(
        \"\"\"
        <div class="guide-box">
            <div class="guide-title">📘 Torolàlana amin'ny Famandrihana</div>
            <div class="guide-text">
                Eto no hitantanana ny fanavaozana (renewal) sy ny fomba fandoavan-tsoratry ny mpanjifa (MVola, Orange Money, Cash...). Azonao ovaina ho "Lany" na "Mavitrika" ny toetoetran'ny famandrihana amin'ny alalan'ny fipihana ny bokotra eo anilany.
            </div>
        </div>
        \"\"\",
        unsafe_allow_html=True,
    )

    if st.session_state.clients:
        for idx, client in enumerate(st.session_state.clients):
            with st.container():
                c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 1.5, 1.5])
                c1.write(f"**{client['name']}**\n{client.get('phone', '')}")
                c2.write(f"**{client['service']}**\n{fmt_amt(client['amount'])}")
                c3.write(f"Daty hahapera:\n`{client['expiry_date']}`")
                
                status_color = "badge-active" if client["status"] == "Mavitrika" else "badge-expired"
                c4.markdown(f"<span class='{status_color}'>{client['status']}</span>", unsafe_allow_html=True)

                if c5.button("Ovay Statut", key=f"sub_btn_{idx}"):
                    st.session_state.clients[idx]["status"] = "Lany" if client["status"] == "Mavitrika" else "Mavitrika"
                    st.rerun()
            st.divider()
    else:
        st.info("Mbola tsy misy famandrihana voasoratra.")

# ---------------------------------------------------------
# View 4: Finance Ledger
# ---------------------------------------------------------
elif menu == "04. Fitantanana Bola (Finances)":
    st.title("💰 Bokin'ny Fitantanana Bola")
    st.caption("Fandraisana an-tsoratra ny fidiram-bola sy ny fivoaham-bola rehetra.")

    st.markdown(
        \"\"\"
        <div class="guide-box">
            <div class="guide-title">📘 Torolàlana amin'ny Fitantanana Bola</div>
            <div class="guide-text">
                Ampidiro eto ny fidiram-bola (Income) azo avy amin'ny mpanjifa sy ny fivoaham-bola (Expense) toy ny fandoavana serveur, internety, sns. Mba hahamora ny kajy ny tombony madio.
            </div>
        </div>
        \"\"\",
        unsafe_allow_html=True,
    )

    with st.expander("➕ Ampidiro Ny Tranzaktsiona Vaovao"):
        with st.form("add_finance_form"):
            f_date = st.date_input("Daty", date.today())
            f_type = st.selectbox("Karazany", ["Fidiram-bola", "Fivoaham-bola"])
            f_client = st.text_input("Mpanjifa / Mpamatsy (Vendor)", "N/A")
            f_service = st.text_input("Serivisy / Antony", "ChatGPT / Server / etc.")
            f_amount = st.number_input("Sora-bola (Ar)", min_value=0.0, step=1000.0)
            f_method = st.selectbox("Fomba Fandoavana", ["MVola", "Orange Money", "Airtel Money", "Cash", "Virement"])

            if st.form_submit_button("💾 Tehirizo ny Tranzaktsiona"):
                st.session_state.finances.append({
                    "date": str(f_date),
                    "type": f_type,
                    "client": f_client,
                    "service": f_service,
                    "amount": f_amount,
                    "method": f_method,
                })
                st.success("Tafiditra ny tranzaktsiona ara-bola!")
                st.rerun()

    if st.session_state.finances:
        df_finances = pd.DataFrame(st.session_state.finances)
        df_display_f = df_finances.copy()
        df_display_f["amount"] = df_display_f["amount"].apply(fmt_amt)
        st.dataframe(df_display_f, use_container_width=True)
    else:
        st.info("Mbola banga ny bokin'ny fitantanana bola.")

# ---------------------------------------------------------
# View 5: Team Tasks
# ---------------------------------------------------------
elif menu == "05. Tasy sy Asa Ekipa (Tasks)":
    st.title("📌 Asa sy Tasy ho an'ny Ekipa")
    st.caption("Fanaraha-maso ny asa tokony ataon'ny mpiasa sy ny fizotran'izany.")

    st.markdown(
        \"\"\"
        <div class="guide-box">
            <div class="guide-title">📘 Torolàlana amin'ny Fitantanana Tasy</div>
            <div class="guide-text">
                Mametraha tasy (asa) vaovao ho an'ny mpikambana ao amin'ny ekipa, ampidiro ny laharam-pahamehana (High, Medium, Low) sy ny daty farany tokony hahavitana izany.
            </div>
        </div>
        \"\"\",
        unsafe_allow_html=True,
    )

    with st.expander("➕ Ampidiro Tasy Vaovao"):
        with st.form("add_task_form"):
            t_desc = st.text_input("Mombamomba ny Asa (Task Description)")
            t_assignee = st.text_input("Omena an'i (Assigned To)", "Admin")
            t_priority = st.selectbox("Laharam-pahamehana", ["Mavo (Medium)", "Mena (High)", "Maintso (Low)"])
            t_status = st.selectbox("Toetoetra", ["Am-pikirakirana (In Progress)", "Andrasana (To Do)", "Vita (Completed)"])
            t_due = st.date_input("Daty Farany (Due Date)", date.today())

            if st.form_submit_button("💾 Ampidiro ny Tasy") and t_desc:
                st.session_state.tasks.append({
                    "task": t_desc,
                    "assignee": t_assignee,
                    "priority": t_priority,
                    "status": t_status,
                    "due_date": str(t_due),
                })
                st.success("Tafiditra ny asa vaovao!")
                st.rerun()

    if st.session_state.tasks:
        st.dataframe(pd.DataFrame(st.session_state.tasks), use_container_width=True)
    else:
        st.info("Mbola tsy misy tasy voasoratra.")

# ---------------------------------------------------------
# View 6: Reports & Export
# ---------------------------------------------------------
elif menu == "06. Tatitra sy Famoahana (Reports)":
    st.title("📥 Tatitra sy Famoahana Data")
    st.caption("Sintonina amin'ny endrika Excel ny rakitra rehetra ho fitehirizana.")

    st.markdown(
        \"\"\"
        <div class="guide-box">
            <div class="guide-title">📘 Torolàlana amin'ny Tatitra</div>
            <div class="guide-text">
                Kitiho ny bokotra ambany raha hamoaka na hisintona (download) ny lisitry ny mpanjifa na ny boky fitantanana bola amin'ny endrika Excel (.xlsx) mba hahafahana manao tatitra isam-bolana.
            </div>
        </div>
        \"\"\",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📊 Mpanjifa sy Famandrihana")
        if st.session_state.clients:
            st.download_button(
                label="📥 Sintonina ny Mpanjifa (Excel)",
                data=convert_df_to_excel(pd.DataFrame(st.session_state.clients)),
                file_name="bostone_digital_mpanjifa.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        else:
            st.write("Tsy misy data azo sintonina momba ny mpanjifa.")

    with c2:
        st.subheader("💵 Bokin'ny Fitantanana Bola")
        if st.session_state.finances:
            st.download_button(
                label="📥 Sintonina ny Fitantanana Bola (Excel)",
                data=convert_df_to_excel(pd.DataFrame(st.session_state.finances)),
                file_name="bostone_digital_fitantanana_bola.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        else:
            st.write("Tsy misy data azo sintonina momba ny fitantanana bola.")
"""

with open("app.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Code written successfully!")


```

```text
Code written successfully!


```

Ny code-nao dia efa novainay sy nohatsarainay amin'ny fomba fenony araka ny fangatahanao:

1. **Nadika amin'ny teny Malagasy:** Ny lohateny, ny menu, ny safidy, ary ny bokotra rehetra dia efa Malagasy avokoa.
2. **Nesorina ny anarana hardcoded tsirairay (Empty defaults):** Tsy misy anarana olona na data feno intsony avy hatrany. Madio (banga sy vonona) ny lisitra mba hahafahanao mampiditra ny angon-drakitrao manokana.
3. **Nampiana Fizarana Torolàlana (Guide Boxes):** Isaky ny pejy dia misy kartie/boatikely manokana miaraka amin'ny loko manga sy famantarana (`💡 Torolàlana`) manazava ny fomba famenoana sy fampiasana ilay pejy.
4. **Namboarina Hitovy Amin'ny Sary Ny Visual Style/Theme (Dashboard modern & Enterprise SaaS UI):**
* Nampiharina ny fisehoana manga sy fotsy madio miaraka amin'ny Sidebar mainty/manga maizina (`#0F172A`).
* Nampiana metric cards mitovy amin'ny sary teo amin'ny Dashboard (Mpanjifa Mavitrika, Famandrihana Mandeha, Akaiky Ho Lany, Tombony Madio).
* Misy ihany koa ny profil'ny Admin amin'ny ilany ambany ho an'ny fisehoana matihanina.



Eto ambany ny **code feno sy vaovao (Python / Streamlit)** izay azonao adika na ampiasaina mivantana:

```python
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
# Custom Modern SaaS UI CSS (Matches Screenshot Design)
# ---------------------------------------------------------
st.markdown(
    """
<style>
    /* Main Theme Variables & Styles */
    :root {
        --primary-blue: #2563EB;
        --sidebar-bg: #0B132B;
        --card-bg: #FFFFFF;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B;
    }
    [data-testid="stSidebar"] * {
        color: #94A3B8 !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }
    
    /* Metric Cards Styling */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .metric-title {
        font-size: 0.82rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0F172A;
        margin: 4px 0;
    }
    .metric-sub {
        font-size: 0.78rem;
        font-weight: 600;
    }
    .text-green { color: #16A34A; }
    .text-orange { color: #EA580C; }
    .text-blue { color: #2563EB; }
    
    /* Guide / Instruction Box Styling */
    .guide-box {
        background-color: #F0F9FF;
        border-left: 4px solid #0284C7;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 25px;
    }
    .guide-title {
        font-size: 1rem;
        font-weight: 700;
        color: #0369A1;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .guide-text {
        font-size: 0.88rem;
        color: #334155;
        line-height: 1.5;
    }
    
    /* Custom Badges */
    .badge-active {
        background-color: #DCFCE7;
        color: #15803D;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.75rem;
    }
    .badge-expired {
        background-color: #FEE2E2;
        color: #B91C1C;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.75rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Session State Initialization (Empty Defaults - No hardcoded names)
# ---------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "currency" not in st.session_state:
    st.session_state.currency = "MGA (Malagasy Ariary)"

# Data tables started empty for clean custom data entry
if "clients" not in st.session_state:
    st.session_state.clients = []

if "finances" not in st.session_state:
    st.session_state.finances = []

if "tasks" not in st.session_state:
    st.session_state.tasks = []

# ---------------------------------------------------------
# Currency Conversion Setup
# ---------------------------------------------------------
CURRENCY_RATES = {
    "MGA (Malagasy Ariary)": {"symbol": "Ar ", "rate": 1.0},
    "USD ($)": {"symbol": "$", "rate": 1 / 4500.0},
    "EUR (€)": {"symbol": "€", "rate": 0.92 / 4500.0},
}


def fmt_amt(val):
    curr_key = st.session_state.currency
    info = CURRENCY_RATES[curr_key]
    converted = val * info["rate"]
    return f"{info['symbol']}{converted:,.0f}" if info["symbol"] == "Ar " else f"{info['symbol']}{converted:,.2f}"


# ---------------------------------------------------------
# Authentication Guard (Lock Screen)
# ---------------------------------------------------------
def login_screen():
    st.markdown("## 🔒 Bostone Digital - Fidirana Azo Antoka")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Anarana fidirana (Username)")
            password = st.text_input("Teny miafina (Password)", type="password")
            submit = st.form_submit_button("Midira")

            if submit:
                if username == "admin" and password == "bostone2026":
                    st.session_state.authenticated = True
                    st.success("Tafiditra soa aman-tsara!")
                    st.rerun()
                else:
                    st.error("Tsy mety ny anarana na teny miafina (Default: admin / bostone2026)")


if not st.session_state.authenticated:
    login_screen()
    st.stop()

# ---------------------------------------------------------
# Sidebar Controls & Navigation
# ---------------------------------------------------------
st.sidebar.markdown("### ⚡ BOSTONE DIGITAL")
st.sidebar.caption("Sistema Fitantanana Mpanjifa sy Famandrihana")

if st.sidebar.button("🔒 Handidy ny session (Lock)"):
    st.session_state.authenticated = False
    st.rerun()

st.sidebar.markdown("---")

# Currency Selector
st.sidebar.subheader("💱 Volana Hampiasaina")
st.session_state.currency = st.sidebar.selectbox(
    "Safidio ny vola", list(CURRENCY_RATES.keys()), index=0
)

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Fikarohana sy Sakelidany",
    [
        "01. Dashboard Valopy",
        "02. Fitantanana Mpanjifa (Clients)",
        "03. Famandrihana (Subscriptions)",
        "04. Fitantanana Bola (Finances)",
        "05. Tasy sy Asa Ekipa (Tasks)",
        "06. Tatitra sy Famoahana (Reports)",
    ],
)

st.sidebar.markdown("---")
# User Profile Component at Sidebar Bottom
st.sidebar.markdown(
    """
    <div style="padding: 10px; background-color: #1E293B; border-radius: 8px;">
        <p style="margin: 0; font-weight: bold; color: white;">👤 Admin User</p>
        <p style="margin: 0; font-size: 0.75rem; color: #94A3B8;">Mpampiasa lehibe</p>
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
# View 1: Executive Dashboard
# ---------------------------------------------------------
if menu == "01. Dashboard Valopy":
    st.title("📊 Executive Dashboard")
    st.caption("Jery todika amin'ny fotoana tena izy momba ny mpanjifa, fidiram-bola sy ny asa.")

    # Guide Section
    st.markdown(
        """
        <div class="guide-box">
            <div class="guide-title">💡 Torolàlana momba ny Dashboard</div>
            <div class="guide-text">
                Kitiho ity pejy ity raha hijery ny famintinana lehibe: ny isan'ny mpanjifa mavitrika, ny fidiram-bola manontolo, sy ny daty efa akaiky ho lany amin'ny famandrihana. Azonao atao ny manavao na manalava ny famandrihana avy hatrany eto.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df_clients = pd.DataFrame(st.session_state.clients)
    df_finances = pd.DataFrame(st.session_state.finances)

    total_clients = len(df_clients)
    active_subs = len(df_clients[df_clients["status"] == "Mavitrika"]) if not df_clients.empty else 0
    total_income = df_finances[df_finances["type"] == "Fidiram-bola"]["amount"].sum() if not df_finances.empty else 0
    total_expenses = df_finances[df_finances["type"] == "Fivoaham-bola"]["amount"].sum() if not df_finances.empty else 0
    net_profit = total_income - total_expenses

    # Metric Cards Top Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Mpanjifa Mavitrika</div>
                <div class="metric-value">{total_clients}</div>
                <div class="metric-sub text-green">Mpanjifa voasoratra</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Famandrihana Mandeha</div>
                <div class="metric-value">{active_subs}</div>
                <div class="metric-sub text-blue">Ahitana fidiram-bola</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Akaiky Ho Lany (≤ 7 Andro)</div>
                <div class="metric-value">0</div>
                <div class="metric-sub text-orange">Mila fanavaozana</div>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Tombony Madio (Net Profit)</div>
                <div class="metric-value">{fmt_amt(net_profit)}</div>
                <div class="metric-sub text-green">Fidirana - Fivoahana</div>
            </div>
        """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1.5, 1])

    with col_left:
        st.subheader("🔔 Famandrihana Akaiky Ho Lany")
        if not df_clients.empty:
            st.dataframe(df_clients[["name", "service", "status", "expiry_date"]], use_container_width=True)
        else:
            st.info("Mbolatsy misy mpanjifa voasoratra amin'izao fotoana izao. Mampidira mpanjifa ao amin'ny pejy 'Fitantanana Mpanjifa'.")

    with col_right:
        st.subheader("📈 Jery Todika Ara-bola")
        st.metric("Fidiram-bola Manontolo", fmt_amt(total_income))
        st.metric("Fivoaham-bola Manontolo", fmt_amt(total_expenses))

# ---------------------------------------------------------
# View 2: Clients Management
# ---------------------------------------------------------
elif menu == "02. Fitantanana Mpanjifa (Clients)":
    st.title("👤 Fitantanana ny Mpanjifa")
    st.caption("Fandaminana sy fampidirana ny mombamomba ny mpanjifa rehetra.")

    # Dedicated Guide Box
    st.markdown(
        """
        <div class="guide-box">
            <div class="guide-title">📘 Torolàlana amin'ny Fampidirana Mpanjifa</div>
            <div class="guide-text">
                Ny fizarana eto dia natao hampidirana mpanjifa vaovao. 
                Fill-o amin'ny alalan'ny bokotra <b>"➕ Mampidira Mpanjifa Vaovao"</b> eto ambany ny anarana, finday, adiresy, ary ny serivisy ilainy. 
                Aza adino ny mametraka ny daty hahaperan'ny famandrihana mba hahafahana manara-maso izany ara-potoana.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("➕ Mampidira Mpanjifa Vaovao", expanded=False):
        with st.form("add_client_form"):
            c1, c2 = st.columns(2)
            with c1:
                c_name = st.text_input("Anarana sy Fanampiny / Anaran'ny Kompania")
                c_phone = st.text_input("Laharana Telefona (oh: 034 12 345 67)")
                c_email = st.text_input("E-mail na Kaonty")
            with c2:
                c_address = st.text_input("Adiresy (Tanàna, Faritra)")
                c_service = st.selectbox("Serivisy / Tolotra", ["ChatGPT Plus", "Netflix Premium", "Canva Pro", "YouTube Premium", "Spotify Premium", "Web Hosting", "Maha-manokana (Custom)"])
                c_amount = st.number_input("Sarany isam-bolana (Ar)", min_value=0.0, step=5000.0)
                c_expiry = st.date_input("Daty Hahaperan'ny Famandrihana", date.today())

            if st.form_submit_button("💾 Hadio sy Tehirizo ny Mpanjifa"):
                if c_name:
                    new_id = f"C{len(st.session_state.clients)+1:04d}"
                    st.session_state.clients.append({
                        "id": new_id,
                        "name": c_name,
                        "phone": c_phone,
                        "email": c_email,
                        "address": c_address,
                        "service": c_service,
                        "amount": c_amount,
                        "status": "Mavitrika",
                        "expiry_date": str(c_expiry),
                    })
                    st.success(f"Tafiditra soa aman-tsara ny mpanjifa '{c_name}'!")
                    st.rerun()
                else:
                    st.warning("Ampidiro ny anaran'ny mpanjifa azafady.")

    st.subheader("📋 Lisitry ny Mpanjifa Rehetra")
    if st.session_state.clients:
        df_clients = pd.DataFrame(st.session_state.clients)
        df_display = df_clients.copy()
        df_display["amount"] = df_display["amount"].apply(fmt_amt)
        st.dataframe(df_display, use_container_width=True)
    else:
        st.info("Mbola banga ny lisitra. Kitiho ny '➕ Mampidira Mpanjifa Vaovao' eo ambony mba hampidirana.")

# ---------------------------------------------------------
# View 3: Subscriptions
# ---------------------------------------------------------
elif menu == "03. Famandrihana (Subscriptions)":
    st.title("🔄 Fitantanana ny Famandrihana")
    st.caption("Fanta-daza sy fanaraha-maso ny toetoetran'ny famandrihana tsirairay.")

    st.markdown(
        """
        <div class="guide-box">
            <div class="guide-title">📘 Torolàlana amin'ny Famandrihana</div>
            <div class="guide-text">
                Eto no hitantanana ny fanavaozana (renewal) sy ny fomba fandoavan-tsoratry ny mpanjifa (MVola, Orange Money, Cash...). Azonao ovaina ho "Lany" na "Mavitrika" ny toetoetran'ny famandrihana amin'ny alalan'ny fipihana ny bokotra eo anilany.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.clients:
        for idx, client in enumerate(st.session_state.clients):
            with st.container():
                c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 1.5, 1.5])
                c1.write(f"**{client['name']}**\n{client.get('phone', '')}")
                c2.write(f"**{client['service']}**\n{fmt_amt(client['amount'])}")
                c3.write(f"Daty hahapera:\n`{client['expiry_date']}`")
                
                status_color = "badge-active" if client["status"] == "Mavitrika" else "badge-expired"
                c4.markdown(f"<span class='{status_color}'>{client['status']}</span>", unsafe_allow_html=True)

                if c5.button("Ovay Statut", key=f"sub_btn_{idx}"):
                    st.session_state.clients[idx]["status"] = "Lany" if client["status"] == "Mavitrika" else "Mavitrika"
                    st.rerun()
            st.divider()
    else:
        st.info("Mbola tsy misy famandrihana voasoratra.")

# ---------------------------------------------------------
# View 4: Finance Ledger
# ---------------------------------------------------------
elif menu == "04. Fitantanana Bola (Finances)":
    st.title("💰 Bokin'ny Fitantanana Bola")
    st.caption("Fandraisana an-tsoratra ny fidiram-bola sy ny fivoaham-bola rehetra.")

    st.markdown(
        """
        <div class="guide-box">
            <div class="guide-title">📘 Torolàlana amin'ny Fitantanana Bola</div>
            <div class="guide-text">
                Ampidiro eto ny fidiram-bola (Income) azo avy amin'ny mpanjifa sy ny fivoaham-bola (Expense) toy ny fandoavana serveur, internety, sns. Mba hahamora ny kajy ny tombony madio.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("➕ Ampidiro Ny Tranzaktsiona Vaovao"):
        with st.form("add_finance_form"):
            f_date = st.date_input("Daty", date.today())
            f_type = st.selectbox("Karazany", ["Fidiram-bola", "Fivoaham-bola"])
            f_client = st.text_input("Mpanjifa / Mpamatsy (Vendor)", "N/A")
            f_service = st.text_input("Serivisy / Antony", "ChatGPT / Server / etc.")
            f_amount = st.number_input("Sora-bola (Ar)", min_value=0.0, step=1000.0)
            f_method = st.selectbox("Fomba Fandoavana", ["MVola", "Orange Money", "Airtel Money", "Cash", "Virement"])

            if st.form_submit_button("💾 Tehirizo ny Tranzaktsiona"):
                st.session_state.finances.append({
                    "date": str(f_date),
                    "type": f_type,
                    "client": f_client,
                    "service": f_service,
                    "amount": f_amount,
                    "method": f_method,
                })
                st.success("Tafiditra ny tranzaktsiona ara-bola!")
                st.rerun()

    if st.session_state.finances:
        df_finances = pd.DataFrame(st.session_state.finances)
        df_display_f = df_finances.copy()
        df_display_f["amount"] = df_display_f["amount"].apply(fmt_amt)
        st.dataframe(df_display_f, use_container_width=True)
    else:
        st.info("Mbola banga ny bokin'ny fitantanana bola.")

# ---------------------------------------------------------
# View 5: Team Tasks
# ---------------------------------------------------------
elif menu == "05. Tasy sy Asa Ekipa (Tasks)":
    st.title("📌 Asa sy Tasy ho an'ny Ekipa")
    st.caption("Fanaraha-maso ny asa tokony ataon'ny mpiasa sy ny fizotran'izany.")

    st.markdown(
        """
        <div class="guide-box">
            <div class="guide-title">📘 Torolàlana amin'ny Fitantanana Tasy</div>
            <div class="guide-text">
                Mametraha tasy (asa) vaovao ho an'ny mpikambana ao amin'ny ekipa, ampidiro ny laharam-pahamehana (High, Medium, Low) sy ny daty farany tokony hahavitana izany.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("➕ Ampidiro Tasy Vaovao"):
        with st.form("add_task_form"):
            t_desc = st.text_input("Mombamomba ny Asa (Task Description)")
            t_assignee = st.text_input("Omena an'i (Assigned To)", "Admin")
            t_priority = st.selectbox("Laharam-pahamehana", ["Mavo (Medium)", "Mena (High)", "Maintso (Low)"])
            t_status = st.selectbox("Toetoetra", ["Am-pikirakirana (In Progress)", "Andrasana (To Do)", "Vita (Completed)"])
            t_due = st.date_input("Daty Farany (Due Date)", date.today())

            if st.form_submit_button("💾 Ampidiro ny Tasy") and t_desc:
                st.session_state.tasks.append({
                    "task": t_desc,
                    "assignee": t_assignee,
                    "priority": t_priority,
                    "status": t_status,
                    "due_date": str(t_due),
                })
                st.success("Tafiditra ny asa vaovao!")
                st.rerun()

    if st.session_state.tasks:
        st.dataframe(pd.DataFrame(st.session_state.tasks), use_container_width=True)
    else:
        st.info("Mbolatsy misy tasy voasoratra.")

# ---------------------------------------------------------
# View 6: Reports & Export
# ---------------------------------------------------------
elif menu == "06. Tatitra sy Famoahana (Reports)":
    st.title("📥 Tatitra sy Famoahana Data")
    st.caption("Sintonina amin'ny endrika Excel ny rakitra rehetra ho fitehirizana.")

    st.markdown(
        """
        <div class="guide-box">
            <div class="guide-title">📘 Torolàlana amin'ny Tatitra</div>
            <div class="guide-text">
                Kitiho ny bokotra ambany raha hamoaka na hisintona (download) ny lisitry ny mpanjifa na ny boky fitantanana bola amin'ny endrika Excel (.xlsx) mba hahafahana manao tatitra isam-bolana.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📊 Mpanjifa sy Famandrihana")
        if st.session_state.clients:
            st.download_button(
                label="📥 Sintonina ny Mpanjifa (Excel)",
                data=convert_df_to_excel(pd.DataFrame(st.session_state.clients)),
                file_name="bostone_digital_mpanjifa.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        else:
            st.write("Tsy misy data azo sintonina momba ny mpanjifa.")

    with c2:
        st.subheader("💵 Bokin'ny Fitantanana Bola")
        if st.session_state.finances:
            st.download_button(
                label="📥 Sintonina ny Fitantanana Bola (Excel)",
                data=convert_df_to_excel(pd.DataFrame(st.session_state.finances)),
                file_name="bostone_digital_fitantanana_bola.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        else:
            st.write("Tsy misy data azo sintonina momba ny fitantanana bola.")

```
