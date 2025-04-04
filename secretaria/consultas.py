import streamlit as st
import pandas as pd
from datetime import datetime


### Seção 3: Monitoramento de Consultas do Dia
st.header("3. Consultas do Dia")

hoje = datetime.now().date()
consultas_hoje = st.session_state.consultas[st.session_state.consultas["Data"] == hoje]

if not consultas_hoje.empty:
    consultas_hoje = consultas_hoje.sort_values(by="Hora")
    st.write(f"Consultas marcadas para hoje ({hoje}):")
    for index, consulta in consultas_hoje.iterrows():
        # Buscar o nome do paciente pelo ID
        nome_paciente = st.session_state.pacientes[
            st.session_state.pacientes["ID Paciente"] == consulta["ID Paciente"]
        ]["Nome"].values[0]

        st.subheader(f"Hora: {consulta['Hora']}")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.write(f"Nome: {nome_paciente}")
            if st.button(
                "Finalizar Consulta", key=f"finalizar_{consulta['ID Consulta']}"
            ):
                st.session_state.consultas.at[index, "Compareceu"] = True
                st.session_state.consultas.at[index, "Cancelou"] = False
                st.success(
                    f"Consulta ID {consulta['ID Consulta']} finalizada com sucesso!"
                )

        with col2:
            st.write(f"Tipo: {consulta['Tipo']}")
            if st.button(
                "Cancelar Consulta", key=f"cancelar_{consulta['ID Consulta']}"
            ):
                st.session_state.consultas.at[index, "Cancelou"] = True
                st.success(
                    f"Consulta ID {consulta['ID Consulta']} cancelada com sucesso!"
                )

        with col3:
            st.write(f"Convênio: {consulta['Convênio']}")

        with col4:
            pagamento = st.number_input(
                "Pagamento (R$)",
                min_value=0.0,
                value=float(consulta["Pagamento"]),
                key=f"pagamento_{consulta['ID Consulta']}",
            )
            st.session_state.consultas.at[index, "Pagamento"] = pagamento
        st.write("---")
else:
    st.write("Nenhuma consulta marcada para hoje.")
