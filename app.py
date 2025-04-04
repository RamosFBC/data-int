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

# Título do aplicativo
st.title("Gestão de Consultas Médicas")

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
)

consultas = st.Page(
    "secretaria/consultas.py",
    title="Consultas do Dia",
    icon="📅",
)

# Create a list of pages for navigation
pages = [cadastro_pacientes, marcar_consulta, consultas]

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
