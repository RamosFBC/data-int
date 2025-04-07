import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# Initialize DataFrames in session_state for persistence during the session
if "patients" not in st.session_state:
    data = requests.get(
        "https://feliperamos.app.n8n.cloud/webhook-test/21afb425-402d-4fa8-8b19-cd2b92d42fb2"
    ).json()
    print(data)
    if data:
        st.session_state.patients = pd.DataFrame(data)
    # Populate the state with retrieved data
    else:
        st.session_state.patients = pd.DataFrame(
            columns=[
                "row_number",
                "Patient ID",
                "Name",
                "Phone",
                "Email",
                "Referral Source",
            ]
        )

if "appointments" not in st.session_state:
    st.session_state.appointments = pd.DataFrame(
        columns=[
            "Appointment ID",
            "Patient ID",
            "Date",
            "Time",
            "Payment Status",
            "Attended",
            "First Appointment",
            "Insurance",
            "Canceled",
        ]
    )


if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "Secretary", "Doctor", "Admin"]


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
patient_registration = st.Page(
    "secretary/patient_registration.py",
    title="Cadastro de Pacientes",
    icon="📝",
)


appointment_registration = st.Page(
    "secretary/appointment_registration.py",
    title="Marcar Consulta",
    icon="📋",
    default=(role == "Admin"),
)

appointments = st.Page(
    "secretary/appointments.py",
    title="Consultas do Dia",
    icon="📅",
    default=(role == "Secretary"),
)

kpis = st.Page(
    "medico/kpis.py",
    title="KPIs",
    icon="📊",
    default=(role == "Doctor"),
)

# Create a list of pages for navigation
account_pages = [logout_page, settings]
secretary_pages = [patient_registration, appointment_registration, appointments]
doctor_pages = [kpis]

# Título do aplicativo
st.title("Gestão de Consultas Médicas")

page_dict = {}
if st.session_state.role in ["Secretary", "Doctor", "Admin"]:
    page_dict["Cadastro"] = secretary_pages
if st.session_state.role in ["Doctor", "Admin"]:
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
    st.write(st.session_state.patients)
    st.subheader("Tabela de Consultas")
    st.write(st.session_state.appointments)
