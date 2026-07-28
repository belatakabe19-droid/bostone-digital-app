import io
from datetime import date, datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Bostone Digital - Enterprise ERP & SaaS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# Ultra-Professional Enterprise Dark Theme CSS
# ---------------------------------------------------------
st.markdown(
    """
<style>
    /* Global Page Styling */
    .stApp {
        background-color: #0B0F17;
        color: #E2E8F0;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Sidebar Customization */
    [data-testid="stSidebar"] {
        background-color: #070A10 !important;
        border-right: 1px solid #1E293B;
    }
    [data-testid="stSidebar"] * {
        color: #94A3B8 !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #F8FAFC !important;
    }
    
    /* Modern Glassmorphic Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 22px 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(12px);
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        border-color: rgba(37, 99, 235, 0.4);
        transform: translateY(-2px);
    }
    .metric-title {
        font-size: 0.75rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #F8FAFC;
        margin: 8px 0 4px 0;
        letter-spacing: -0.5px;
    }
    .metric-sub {
        font-size: 0.8rem;
        font-weight: 600;
    }
    .text-green { color: #10B981; }
    .text-red { color: #EF4444; }
    .text-blue { color: #3B82F6; }
    .text-purple { color: #8B5CF6; }
    
    /* Guide / Alert Banner */
    .guide-box {
        background: linear-gradient(90deg, rgba(14, 165, 233, 0.1) 0%, rgba(15, 23, 42, 0.6) 100%);
        border-left: 4px solid #0EA5E9;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 25px;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    .guide-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #38BDF8;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .guide-text {
        font-size: 0.85rem;
        color: #94A3B8;
        line-height: 1.5;
    }

    /* Custom Status Badges */
    .badge-active {
        background-color: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.75rem;
    }
    .badge-expired {
        background-color: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.75rem;
    }

    /* Input Field Overrides for Dark Mode */
    .stTextInput > div > div > input, .stSelectbox > div > div, .stNumberInput > div > div > input {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
        border-color: #334155 !important;
        border-radius: 8px !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Plotly Global Dark Template Setup
# ---------------------------------------------------------
def apply_chart_theme(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94A3B8", family="Inter, sans-serif"),
        margin=dict(t=30, b=30, l=20, r=20),
        legend=dict(font=dict(color="#E2E8F0")),
        xaxis=dict(gridcolor="#1E293B", zerolinecolor="#1E293B"),
        yaxis=dict(gridcolor="#1E293B", zerolinecolor="#1E293B"),
    )
    return fig

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "currency" not in st.session_state:
    st.session_state.currency = "MGA (Ariary Malgache)"

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
    "MGA (Ariary Malgache)": {"symbol": "Ar ", "rate": 1.0},
    "USD ($)": {"symbol": "$ ", "rate": 1 / 4500.0},
    "EUR (€)": {"symbol": "€ ", "rate": 0.92 / 4500.0},
}

def fmt_amt(val):
    curr_key = st.session_state.currency
    info = CURRENCY_RATES[curr_key]
    converted = val * info["rate"]
    return f"{info['symbol']}{converted:,.0f}" if info["symbol"] == "Ar " else f"{info['symbol']}{converted:,.2f}"

# ---------------------------------------------------------
# Authentication Screen
# ---------------------------------------------------------
def login_screen():
    st.markdown("<h2 style='text-align: center; color: #F8FAFC; margin-top: 50px;'>🔒 Bostone Digital — Connexion Enterprise</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Identifiant")
            password = st.text_input("Mot de passe", type="password")
            submit = st.form_submit_button("Se connecter", use_container_width=True)

            if submit:
                if username == "admin" and password == "bostone2026":
                    st.session_state.authenticated = True
                    st.success("Authentification réussie !")
                    st.rerun()
                else:
                    st.error("Identifiants incorrects (Par défaut: admin / bostone2026)")

if not st.session_state.authenticated:
    login_screen()
    st.stop()

# ---------------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------------
st.sidebar.markdown("### ⚡ BOSTONE DIGITAL")
st.sidebar.caption("Enterprise Resource Planning & SaaS")

if st.sidebar.button("🔒 Déconnexion", use_container_width=True):
    st.session_state.authenticated = False
    st.rerun()

st.sidebar.markdown("---")

st.sidebar.subheader("💱 Devise d'affichage")
st.session_state.currency = st.sidebar.selectbox(
    "Sélectionner la devise", list(CURRENCY_RATES.keys()), index=0
)

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation Principale",
    [
        "01. Tableau de bord",
        "02. Gestion des Clients",
        "03. Abonnements",
        "04. Comptabilité & Finances",
        "05. Tâches & Équipe",
        "06. Rapports & Analytics",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style="padding: 12px; background-color: #0F172A; border-radius: 10px; border: 1px solid #1E293B;">
        <p style="margin: 0; font-weight: bold; color: #F8FAFC;">👤 Administrateur</p>
        <p style="margin: 0; font-size: 0.75rem; color: #38BDF8;">Compte Super-Admin</p>
    </div>
""",
    unsafe_allow_html=True,
)

def convert_df_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Export")
    return output.getvalue()

# ---------------------------------------------------------
# View 1: Executive Dashboard with Dynamic Charts
# ---------------------------------------------------------
if menu == "01. Tableau de bord":
    st.title("📊 Tableau de Bord Exécutif")
    st.caption("Analyse décisionnelle et visualisations graphiques en temps réel.")

    st.markdown(
        """
        <div class="guide-box">
            <div class="guide-title">💡 Vue d'ensemble du Système</div>
            <div class="guide-text">
                Ce tableau de bord centralise l'analyse financière, l'état de la clientèle et la santé opérationnelle de votre entreprise.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df_clients = pd.DataFrame(st.session_state.clients)
    df_finances = pd.DataFrame(st.session_state.finances)

    total_clients = len(df_clients)
    active_subs = len(df_clients[df_clients["status"] == "Actif"]) if not df_clients.empty else 0
    total_income = df_finances[df_finances["type"] == "Revenu"]["amount"].sum() if not df_finances.empty else 0
    total_expenses = df_finances[df_finances["type"] == "Dépense"]["amount"].sum() if not df_finances.empty else 0
    net_profit = total_income - total_expenses

    # Metric Cards Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Portefeuille Clients</div>
                <div class="metric-value">{total_clients}</div>
                <div class="metric-sub text-blue">Comptes enregistrés</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Abonnements Actifs</div>
                <div class="metric-value">{active_subs}</div>
                <div class="metric-sub text-green">Actuellement en cours</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Chiffre d'Affaires</div>
                <div class="metric-value">{fmt_amt(total_income)}</div>
                <div class="metric-sub text-purple">Total des encaissements</div>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Bénéfice Net</div>
                <div class="metric-value">{fmt_amt(net_profit)}</div>
                <div class="metric-sub {'text-green' if net_profit >= 0 else 'text-red'}">Résultat courant</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Dynamic Live Visualizations
    st.subheader("📈 Graphiques & Analytics Dynamiques")
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("##### 🍩 Répartition des Revenus par Service")
        if not df_clients.empty:
            service_counts = df_clients.groupby("service")["amount"].sum().reset_index()
            fig_donut = px.pie(
                service_counts,
                values="amount",
                names="service",
                hole=0.55,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_donut.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(apply_chart_theme(fig_donut), use_container_width=True)
        else:
            st.info("Aucune donnée disponible pour construire le graphique des services.")

    with col_chart2:
        st.markdown("##### 📊 Flux de Trésorerie (Entrées vs Sorties)")
        if not df_finances.empty:
            df_finances["date"] = pd.to_datetime(df_finances["date"])
            fin_summary = df_finances.groupby(["date", "type"])["amount"].sum().reset_index()
            fig_bar = px.bar(
                fin_summary,
                x="date",
                y="amount",
                color="type",
                barmode="group",
                color_discrete_map={"Revenu": "#10B981", "Dépense": "#EF4444"}
            )
            st.plotly_chart(apply_chart_theme(fig_bar), use_container_width=True)
        else:
            st.info("Aucune transaction enregistrée pour afficher le flux de trésorerie.")

# ---------------------------------------------------------
# View 2: Clients Management
# ---------------------------------------------------------
elif menu == "02. Gestion des Clients":
    st.title("👤 Fitantanana ny Mpanjifa / Clients")
    st.caption("Registre central des clients et souscriptions de services.")

    st.markdown(
        """
        <div class="guide-box">
            <div class="guide-title">📘 Guide Client</div>
            <div class="guide-text">
                Remplissez les champs ci-dessous pour ajouter un client. La date d'échéance permet d'assurer un suivi automatisé du renouvellement.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("➕ Enregistrer un Nouveau Client", expanded=False):
        with st.form("add_client_form"):
            c1, c2 = st.columns(2)
            with c1:
                c_name = st.text_input("Nom du Client / Entreprise")
                c_phone = st.text_input("Numéro Téléphone")
                c_email = st.text_input("Adresse Email")
            with c2:
                c_address = st.text_input("Adresse / Localisation")
                c_service = st.selectbox("Service souscrit", ["ChatGPT Plus", "Netflix Premium", "Canva Pro", "YouTube Premium", "Spotify Premium", "Hébergement Web", "Sur Mesure"])
                c_amount = st.number_input("Montant mensuel (Ar)", min_value=0.0, step=5000.0)
                c_expiry = st.date_input("Date d'expiration", date.today())

            if st.form_submit_button("💾 Sauvegarder le Client", use_container_width=True):
                if c_name:
                    new_id = f"CL-{len(st.session_state.clients)+1:04d}"
                    st.session_state.clients.append({
                        "id": new_id,
                        "name": c_name,
                        "phone": c_phone,
                        "email": c_email,
                        "address": c_address,
                        "service": c_service,
                        "amount": c_amount,
                        "status": "Actif",
                        "expiry_date": str(c_expiry),
                    })
                    st.success(f"Client '{c_name}' enregistré avec succès !")
                    st.rerun()
                else:
                    st.warning("Le nom du client est obligatoire.")

    st.subheader("📋 Liste des Clients")
    if st.session_state.clients:
        df_clients = pd.DataFrame(st.session_state.clients)
        df_display = df_clients.copy()
        df_display["amount"] = df_display["amount"].apply(fmt_amt)
        st.dataframe(df_display, use_container_width=True)
    else:
        st.info("Aucun client enregistré pour l'instant.")

# ---------------------------------------------------------
# View 3: Subscriptions
# ---------------------------------------------------------
elif menu == "03. Abonnements":
    st.title("🔄 Gestion des Abonnements")
    st.caption("Contrôle dynamique des statuts d'abonnement et renouvellements.")

    if st.session_state.clients:
        df_clients = pd.DataFrame(st.session_state.clients)
        col_sub_chart, col_sub_list = st.columns([1, 1.5])

        with col_sub_chart:
            st.markdown("##### 🥧 État Global des Abonnements")
            status_counts = df_clients["status"].value_counts().reset_index()
            fig_status = px.pie(
                status_counts,
                values="count",
                names="status",
                color="status",
                color_discrete_map={"Actif": "#10B981", "Expiré": "#EF4444"},
                hole=0.4
            )
            st.plotly_chart(apply_chart_theme(fig_status), use_container_width=True)

        with col_sub_list:
            st.markdown("##### ⚡ Action Rapide sur le Statut")
            for idx, client in enumerate(st.session_state.clients):
                with st.container():
                    c1, c2, c3, c4 = st.columns([2, 2, 1.5, 1.5])
                    c1.write(f"**{client['name']}**\n{client['service']}")
                    c2.write(f"Tarif: {fmt_amt(client['amount'])}\nFin: `{client['expiry_date']}`")
                    
                    status_color = "badge-active" if client["status"] == "Actif" else "badge-expired"
                    c3.markdown(f"<span class='{status_color}'>{client['status']}</span>", unsafe_allow_html=True)

                    if c4.button("Basculer", key=f"sub_btn_{idx}"):
                        st.session_state.clients[idx]["status"] = "Expiré" if client["status"] == "Actif" else "Actif"
                        st.rerun()
                st.divider()
    else:
        st.info("Aucun abonnement en cours d'enregistrement.")

# ---------------------------------------------------------
# View 4: Finance Ledger
# ---------------------------------------------------------
elif menu == "04. Comptabilité & Finances":
    st.title("💰 Registre Financier & Comptabilité")
    st.caption("Suivi précis des entrées et sorties de fonds.")

    with st.expander("➕ Enregistrer une Transaction Financiale"):
        with st.form("add_finance_form"):
            f_date = st.date_input("Date", date.today())
            f_type = st.selectbox("Type d'opération", ["Revenu", "Dépense"])
            f_client = st.text_input("Tiers / Partenaire", "N/A")
            f_service = st.text_input("Motif", "Paiement abonnement / Frais serveur")
            f_amount = st.number_input("Montant (Ar)", min_value=0.0, step=1000.0)
            f_method = st.selectbox("Mode de Règlement", ["MVola", "Orange Money", "Airtel Money", "Espèces", "Virement"])

            if st.form_submit_button("💾 Valider l'opération", use_container_width=True):
                st.session_state.finances.append({
                    "date": str(f_date),
                    "type": f_type,
                    "client": f_client,
                    "service": f_service,
                    "amount": f_amount,
                    "method": f_method,
                })
                st.success("Transaction ajoutée au journal comptable !")
                st.rerun()

    if st.session_state.finances:
        df_finances = pd.DataFrame(st.session_state.finances)
        df_display_f = df_finances.copy()
        df_display_f["amount"] = df_display_f["amount"].apply(fmt_amt)
        st.dataframe(df_display_f, use_container_width=True)
    else:
        st.info("Le registre financier ne contient aucune donnée pour le moment.")

# ---------------------------------------------------------
# View 5: Team Tasks
# ---------------------------------------------------------
elif menu == "05. Tâches & Équipe":
    st.title("📌 Gestion des Tâches & Équipe")
    st.caption("Planification opérationnelle de l'équipe.")

    with st.expander("➕ Assigner une nouvelle tâche"):
        with st.form("add_task_form"):
            t_desc = st.text_input("Intitulé de la tâche")
            t_assignee = st.text_input("Assigné à", "Admin")
            t_priority = st.selectbox("Priorité", ["Haute", "Moyenne", "Basse"])
            t_status = st.selectbox("Statut", ["À faire", "En cours", "Terminée"])
            t_due = st.date_input("Échéance", date.today())

            if st.form_submit_button("💾 Créer la tâche", use_container_width=True) and t_desc:
                st.session_state.tasks.append({
                    "task": t_desc,
               
