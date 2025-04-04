import streamlit as st
import pandas as pd
from datetime import datetime


### Seção 2: Cadastro de Consulta
st.header("Cadastro de Consulta")

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
