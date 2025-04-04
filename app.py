import streamlit as st
import pandas as pd
from datetime import datetime

# Inicialização dos DataFrames no session_state para persistência durante a sessão
if "pacientes" not in st.session_state:
    st.session_state.pacientes = pd.DataFrame(
        columns=["ID Paciente", "Nome", "Telefone", "Email", "Como Conheceu"]
    )

if "consultas" not in st.session_state:
    st.session_state.consultas = pd.DataFrame(
        columns=[
            "ID Consulta",
            "ID Paciente",
            "Data",
            "Hora",
            "Pagamento",
            "Compareceu",
            "Primeira Consulta",
            "Tipo",
            "Convênio",
            "Cancelou",
        ]
    )


if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "Secretaria", "Médico", "Admin"]


def login():

    st.header("Log in")
    role = st.selectbox("Choose your role", ROLES)

    if st.button("Log in"):
        st.session_state.role = role
        st.rerun()


def logout():
    st.session_state.role = None
    st.rerun()


role = st.session_state.role

logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
settings = st.Page("settings.py", title="Settings", icon=":material/settings:")


# Define pages
cadastro_pacientes = st.Page(
    "secretaria/cadastro_pacientes.py",
    title="Cadastro de Pacientes",
    icon="📝",
)


marcar_consulta = st.Page(
    "secretaria/marcar_consulta.py",
    title="Marcar Consulta",
    icon="📋",
    default=(role == "Admin"),
)

consultas = st.Page(
    "secretaria/consultas.py",
    title="Consultas do Dia",
    icon="📅",
    default=(role == "Secretaria"),
)

kpis = st.Page(
    "medico/kpis.py",
    title="KPIs",
    icon="📊",
    default=(role == "Médico"),
)

# Create a list of pages for navigation
account_pages = [logout_page, settings]
secretary_pages = [cadastro_pacientes, marcar_consulta, consultas]
doctor_pages = [kpis]

# Título do aplicativo
st.title("Gestão de Consultas Médicas")

page_dict = {}
if st.session_state.role in ["Secretaria", "Médico", "Admin"]:
    page_dict["Secretaria"] = secretary_pages
if st.session_state.role in ["Médico", "Admin"]:
    page_dict["Médico"] = doctor_pages


if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login)])


# Run the selected page
pg.run()

# Optional: Debug tables
if st.checkbox("Exibir tabelas de dados (debug)"):
    st.subheader("Tabela de Pacientes")
    st.write(st.session_state.pacientes)
    st.subheader("Tabela de Consultas")
    st.write(st.session_state.consultas)
