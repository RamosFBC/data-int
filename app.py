import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state for data persistence
if "pacientes" not in st.session_state:
    st.session_state.pacientes = pd.DataFrame(columns=["Nome", "CPF", "Telefone"])
if "consultas" not in st.session_state:
    st.session_state.consultas = pd.DataFrame(
        columns=["Paciente", "Data", "Horário", "Médico"]
    )

# Título do aplicativo
st.title("Gestão de Consultas Médicas")

# Define pages
cadastro = st.Page(
    "secretaria/cadastro.py",
    title="Cadastro de Pacientes e Consultas",
    icon="📝",
)

consultas = st.Page(
    "secretaria/consultas.py",
    title="Consultas do Dia",
    icon="📅",
)

# Create a list of pages for navigation
pages = [cadastro, consultas]

# Set up navigation
pg = st.navigation(pages)

# Run the selected page
pg.run()

# Optional: Debug tables
if st.checkbox("Exibir tabelas de dados (debug)"):
    st.subheader("Tabela de Pacientes")
    st.write(st.session_state.pacientes)
    st.subheader("Tabela de Consultas")
    st.write(st.session_state.consultas)
