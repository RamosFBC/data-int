import streamlit as st
import pandas as pd
from datetime import datetime


### Seção 1: Cadastro de Pacientes
st.header("1. Cadastro de Pacientes")

with st.form("cadastro_paciente"):
    nome_paciente = st.text_input("Nome do Paciente")
    telefone_paciente = st.text_input("Telefone")
    email_paciente = st.text_input("Email")
    como_conheceu = st.selectbox(
        "Como conheceu o médico",
        ["Rede Social", "Website", "Google", "Indicação", "Outros"],
    )
    submit_paciente = st.form_submit_button("Cadastrar Paciente")

if submit_paciente:
    # Gerar ID único para o paciente
    id_paciente = len(st.session_state.pacientes) + 1
    novo_paciente = pd.DataFrame(
        {
            "ID Paciente": [id_paciente],
            "Nome": [nome_paciente],
            "Telefone": [telefone_paciente],
            "Email": [email_paciente],
            "Como Conheceu": [como_conheceu],
        }
    )
    st.session_state.pacientes = pd.concat(
        [st.session_state.pacientes, novo_paciente], ignore_index=True
    )
    st.success(f"Paciente {nome_paciente} cadastrado com sucesso! ID: {id_paciente}")
