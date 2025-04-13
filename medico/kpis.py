import streamlit as st
import pandas as pd

# Title of the page
st.title("KPIs da Clínica")

# Ensure the DataFrame 'Date' column is in datetime format
if not st.session_state.appointments.empty:
    st.session_state.appointments["Date"] = pd.to_datetime(
        st.session_state.appointments["Date"]
    )
    # Extract year and month for grouping
    st.session_state.appointments["Year"] = st.session_state.appointments[
        "Date"
    ].dt.year
    st.session_state.appointments["Month"] = st.session_state.appointments[
        "Date"
    ].dt.month

    # Assume 'Insurance' column indicates whether it's insurance (not 'Private')
    st.session_state.appointments["Is Insurance"] = (
        st.session_state.appointments["Insurance"] != "Private"
    )

    # Ensure payments status is a float for calculations
    st.session_state.appointments["Payment Status"] = st.session_state.appointments[
        "Payment Status"
    ].astype(float)

# Function definitions for KPI calculations


def calculate_average_ticket(df, period="annual"):
    """Calculate the average ticket (mean payment per appointment)."""
    if df.empty:
        return pd.Series()
    if period == "annual":
        return df.groupby("Year")["Payment Status"].mean().round(2)
    elif period == "monthly":
        return df.groupby(["Year", "Month"])["Payment Status"].mean().round(2)


def calculate_ltv(df):
    """Calculate the Lifetime Value (average total payment per patient)."""
    if df.empty:
        return 0
    total_per_patient = df.groupby("Patient ID")["Payment Status"].sum()
    return total_per_patient.mean().round(2)


def calculate_conversion_rate(df, period="annual"):
    """Calculate the conversion rate (percentage of appointments attended)."""
    if df.empty:
        return pd.Series()
    if period == "annual":
        return (df.groupby("Year")["Attended"].mean() * 100).round(2)
    elif period == "monthly":
        return (df.groupby(["Year", "Month"])["Attended"].mean() * 100).round(2)


def calculate_insurance_percentage(df, period="annual"):
    """Calculate the percentage of appointments via insurance vs private."""
    if df.empty:
        return pd.Series()
    if period == "annual":
        return (df.groupby("Year")["Is Insurance"].mean() * 100).round(2)
    elif period == "monthly":
        return (df.groupby(["Year", "Month"])["Is Insurance"].mean() * 100).round(2)


def calculate_no_show_rate(df, period="annual"):
    """Calculate the no-show rate (percentage of appointments not attended)."""
    if df.empty:
        return pd.Series()
    if period == "annual":
        return ((1 - df.groupby("Year")["Attended"].mean()) * 100).round(2)
    elif period == "monthly":
        return ((1 - df.groupby(["Year", "Month"])["Attended"].mean()) * 100).round(2)


def calculate_retention_rate(df):
    """Calculate the retention rate (percentage of patients with more than one appointment)."""
    if df.empty:
        return 0
    appointments_per_patient = df.groupby("Patient ID").size()
    retained_patients = (appointments_per_patient > 1).sum()
    total_patients = len(appointments_per_patient)
    return (
        (retained_patients / total_patients * 100).round(2) if total_patients > 0 else 0
    )


# Get the appointments DataFrame from session state
df_appointments = st.session_state.appointments

# User interface to select the period
period = st.selectbox("Selecione o período", ["Anual", "Mensal"])

# Check if there is data to process
if df_appointments.empty:
    st.warning("Nenhum dado de consulta disponível para calcular os KPIs.")
else:
    # Calculate KPIs based on selected period
    if period == "Anual":
        average_ticket = calculate_average_ticket(df_appointments, "annual")
        conversion_rate = calculate_conversion_rate(df_appointments, "annual")
        insurance_percentage = calculate_insurance_percentage(df_appointments, "annual")
        no_show_rate = calculate_no_show_rate(df_appointments, "annual")
        ltv = calculate_ltv(df_appointments)
        retention_rate = calculate_retention_rate(df_appointments)

        st.subheader("Ticket Médio Anual (R$)")
        st.write(average_ticket.to_frame("Ticket Médio"))

        st.subheader("Taxa de Conversão Anual (%)")
        st.write(conversion_rate.to_frame("Taxa de Conversão"))

        st.subheader("Percentual de Convênios Anual (%)")
        st.write(insurance_percentage.to_frame("Percentual de Convênios"))

        st.subheader("Taxa de Faltas Anual (%)")
        st.write(no_show_rate.to_frame("Taxa de Faltas"))

        st.subheader("LTV Médio (R$)")
        st.write(ltv)

        st.subheader("Taxa de Retenção (%)")
        st.write(retention_rate)

    elif period == "Mensal":
        average_ticket = calculate_average_ticket(df_appointments, "monthly")
        conversion_rate = calculate_conversion_rate(df_appointments, "monthly")
        insurance_percentage = calculate_insurance_percentage(
            df_appointments, "monthly"
        )
        no_show_rate = calculate_no_show_rate(df_appointments, "monthly")
        ltv = calculate_ltv(df_appointments)
        retention_rate = calculate_retention_rate(df_appointments)

        st.subheader("Ticket Médio Mensal (R$)")
        st.write(average_ticket.to_frame("Ticket Médio"))

        st.subheader("Taxa de Conversão Mensal (%)")
        st.write(conversion_rate.to_frame("Taxa de Conversão"))

        st.subheader("Percentual de Convênios Mensal (%)")
        st.write(insurance_percentage.to_frame("Percentual de Convênios"))

        st.subheader("Taxa de Faltas Mensal (%)")
        st.write(no_show_rate.to_frame("Taxa de Faltas"))

        st.subheader("LTV Médio (R$)")
        st.write(ltv)

        st.subheader("Taxa de Retenção (%)")
        st.write(retention_rate)

# Optional: Debug view of the appointments DataFrame
if st.checkbox("Mostrar dados das consultas (debug)"):
    st.subheader("Tabela de Consultas")
    st.write(df_appointments)
