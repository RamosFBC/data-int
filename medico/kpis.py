import streamlit as st
import pandas as pd

# Title of the page
st.title("KPIs da Clínica")

# Ensure the DataFrame 'Data' column is in datetime format
if not st.session_state.consultas.empty:
    st.session_state.consultas["Data"] = pd.to_datetime(
        st.session_state.consultas["Data"]
    )
    # Extract year and month for grouping
    st.session_state.consultas["Ano"] = st.session_state.consultas["Data"].dt.year
    st.session_state.consultas["Mes"] = st.session_state.consultas["Data"].dt.month

    # Assume 'Convênio' column indicates whether it's a convênio (not 'Particular')
    # Adjust this logic based on your actual data encoding
    st.session_state.consultas["É Convênio"] = (
        st.session_state.consultas["Convênio"] != "Particular"
    )

# Function definitions for KPI calculations


def calcular_ticket_medio(df, periodo="anual"):
    """Calculate the average ticket (mean payment per consultation)."""
    if df.empty:
        return pd.Series()
    if periodo == "anual":
        return df.groupby("Ano")["Pagamento"].mean().round(2)
    elif periodo == "mensal":
        return df.groupby(["Ano", "Mes"])["Pagamento"].mean().round(2)


def calcular_ltv(df):
    """Calculate the Lifetime Value (average total payment per patient)."""
    if df.empty:
        return 0
    total_por_paciente = df.groupby("ID Paciente")["Pagamento"].sum()
    return total_por_paciente.mean().round(2)


def calcular_taxa_conversao(df, periodo="anual"):
    """Calculate the conversion rate (percentage of consultations attended)."""
    if df.empty:
        return pd.Series()
    if periodo == "anual":
        return (df.groupby("Ano")["Compareceu"].mean() * 100).round(2)
    elif periodo == "mensal":
        return (df.groupby(["Ano", "Mes"])["Compareceu"].mean() * 100).round(2)


def calcular_porcentagem_convenios(df, periodo="anual"):
    """Calculate the percentage of consultations via convênio vs particular."""
    if df.empty:
        return pd.Series()
    if periodo == "anual":
        return (df.groupby("Ano")["É Convênio"].mean() * 100).round(2)
    elif periodo == "mensal":
        return (df.groupby(["Ano", "Mes"])["É Convênio"].mean() * 100).round(2)


def calcular_no_show_rate(df, periodo="anual"):
    """Calculate the no-show rate (percentage of consultations not attended)."""
    if df.empty:
        return pd.Series()
    if periodo == "anual":
        return ((1 - df.groupby("Ano")["Compareceu"].mean()) * 100).round(2)
    elif periodo == "mensal":
        return ((1 - df.groupby(["Ano", "Mes"])["Compareceu"].mean()) * 100).round(2)


def calcular_taxa_retencao(df):
    """Calculate the retention rate (percentage of patients with more than one consultation)."""
    if df.empty:
        return 0
    consultas_por_paciente = df.groupby("ID Paciente").size()
    pacientes_retidos = (consultas_por_paciente > 1).sum()
    total_pacientes = len(consultas_por_paciente)
    return (
        (pacientes_retidos / total_pacientes * 100).round(2)
        if total_pacientes > 0
        else 0
    )


# Get the consultations DataFrame from session state
df_consultas = st.session_state.consultas

# User interface to select the period
periodo = st.selectbox("Selecione o período", ["Anual", "Mensal"])

# Check if there is data to process
if df_consultas.empty:
    st.warning("Nenhum dado de consultas disponível para calcular os KPIs.")
else:
    # Calculate KPIs based on selected period
    if periodo == "Anual":
        ticket_medio = calcular_ticket_medio(df_consultas, "anual")
        taxa_conversao = calcular_taxa_conversao(df_consultas, "anual")
        porcentagem_convenios = calcular_porcentagem_convenios(df_consultas, "anual")
        no_show_rate = calcular_no_show_rate(df_consultas, "anual")
        ltv = calcular_ltv(df_consultas)
        taxa_retencao = calcular_taxa_retencao(df_consultas)

        st.subheader("Ticket Médio Anual (R$)")
        st.write(ticket_medio.to_frame("Ticket Médio"))

        st.subheader("Taxa de Conversão Anual (%)")
        st.write(taxa_conversao.to_frame("Taxa de Conversão"))

        st.subheader("Porcentagem de Convênios Anual (%)")
        st.write(porcentagem_convenios.to_frame("Porcentagem de Convênios"))

        st.subheader("No-show Rate Anual (%)")
        st.write(no_show_rate.to_frame("No-show Rate"))

        st.subheader("LTV Médio (R$)")
        st.write(ltv)

        st.subheader("Taxa de Retenção (%)")
        st.write(taxa_retencao)

    elif periodo == "Mensal":
        ticket_medio = calcular_ticket_medio(df_consultas, "mensal")
        taxa_conversao = calcular_taxa_conversao(df_consultas, "mensal")
        porcentagem_convenios = calcular_porcentagem_convenios(df_consultas, "mensal")
        no_show_rate = calcular_no_show_rate(df_consultas, "mensal")
        ltv = calcular_ltv(df_consultas)
        taxa_retencao = calcular_taxa_retencao(df_consultas)

        st.subheader("Ticket Médio Mensal (R$)")
        st.write(ticket_medio.to_frame("Ticket Médio"))

        st.subheader("Taxa de Conversão Mensal (%)")
        st.write(taxa_conversao.to_frame("Taxa de Conversão"))

        st.subheader("Porcentagem de Convênios Mensal (%)")
        st.write(porcentagem_convenios.to_frame("Porcentagem de Convênios"))

        st.subheader("No-show Rate Mensal (%)")
        st.write(no_show_rate.to_frame("No-show Rate"))

        st.subheader("LTV Médio (R$)")
        st.write(ltv)

        st.subheader("Taxa de Retenção (%)")
        st.write(taxa_retencao)

# Optional: Debug view of the consultations DataFrame
if st.checkbox("Exibir dados de consultas (debug)"):
    st.subheader("Tabela de Consultas")
    st.write(df_consultas)
