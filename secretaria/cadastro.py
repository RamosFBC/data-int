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

### Seção 2: Cadastro de Consulta
st.header("2. Cadastro de Consulta")

# Verificar se há pacientes cadastrados
if not st.session_state.pacientes.empty:
    # Criar uma lista de pacientes para seleção
    pacientes_list = st.session_state.pacientes["Nome"].tolist()
    paciente_selecionado = st.selectbox("Selecione o Paciente", pacientes_list)

    with st.form("cadastro_consulta"):
        data = st.date_input("Data da Consulta")
        hora = st.time_input("Hora da Consulta")

        tipo = st.selectbox("Tipo de Consulta", ["Convênio", "Particular"])
        convenio = st.selectbox(
            "Convênio", ["Unimed", "Bradesco Saúde", "Amil", "Particular", "Outro"]
        )
        submit_consulta = st.form_submit_button("Marcar Consulta")

    if submit_consulta:
        # Encontrar o ID do paciente selecionado
        id_paciente = st.session_state.pacientes[
            st.session_state.pacientes["Nome"] == paciente_selecionado
        ]["ID Paciente"].values[0]

        # Gerar ID único para a consulta
        id_consulta = len(st.session_state.consultas) + 1

        # Verificar se é a primeira consulta
        if st.session_state.consultas.empty:
            primeira_consulta = True
        else:
            primeira_consulta = (
                st.session_state.consultas[
                    st.session_state.consultas["ID Paciente"] == id_paciente
                ].shape[0]
                == 0
            )

        # Criar nova entrada na tabela de Consultas com ID do paciente
        nova_consulta = pd.DataFrame(
            {
                "ID Consulta": [id_consulta],
                "ID Paciente": [id_paciente],
                "Data": [data],
                "Hora": [hora],
                "Pagamento": [0.0],
                "Compareceu": [False],
                "Primeira Consulta": [primeira_consulta],
                "Tipo": [tipo],
                "Convênio": [convenio],
                "Cancelou": [False],
            }
        )
        st.session_state.consultas = pd.concat(
            [st.session_state.consultas, nova_consulta], ignore_index=True
        )
        st.success(f"Consulta marcada com sucesso! ID da consulta: {id_consulta}")
else:
    st.warning("Nenhum paciente cadastrado. Cadastre um paciente primeiro.")
