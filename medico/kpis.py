import streamlit as st
import pandas as pd

# Title of the page
st.title("Clinic KPIs")

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
period = st.selectbox("Select the period", ["Annual", "Monthly"])

# Check if there is data to process
if df_appointments.empty:
    st.warning("No appointment data available to calculate KPIs.")
else:
    # Calculate KPIs based on selected period
    if period == "Annual":
        average_ticket = calculate_average_ticket(df_appointments, "annual")
        conversion_rate = calculate_conversion_rate(df_appointments, "annual")
        insurance_percentage = calculate_insurance_percentage(df_appointments, "annual")
        no_show_rate = calculate_no_show_rate(df_appointments, "annual")
        ltv = calculate_ltv(df_appointments)
        retention_rate = calculate_retention_rate(df_appointments)

        st.subheader("Annual Average Ticket (R$)")
        st.write(average_ticket.to_frame("Average Ticket"))

        st.subheader("Annual Conversion Rate (%)")
        st.write(conversion_rate.to_frame("Conversion Rate"))

        st.subheader("Annual Insurance Percentage (%)")
        st.write(insurance_percentage.to_frame("Insurance Percentage"))

        st.subheader("Annual No-show Rate (%)")
        st.write(no_show_rate.to_frame("No-show Rate"))

        st.subheader("Average LTV (R$)")
        st.write(ltv)

        st.subheader("Retention Rate (%)")
        st.write(retention_rate)

    elif period == "Monthly":
        average_ticket = calculate_average_ticket(df_appointments, "monthly")
        conversion_rate = calculate_conversion_rate(df_appointments, "monthly")
        insurance_percentage = calculate_insurance_percentage(
            df_appointments, "monthly"
        )
        no_show_rate = calculate_no_show_rate(df_appointments, "monthly")
        ltv = calculate_ltv(df_appointments)
        retention_rate = calculate_retention_rate(df_appointments)

        st.subheader("Monthly Average Ticket (R$)")
        st.write(average_ticket.to_frame("Average Ticket"))

        st.subheader("Monthly Conversion Rate (%)")
        st.write(conversion_rate.to_frame("Conversion Rate"))

        st.subheader("Monthly Insurance Percentage (%)")
        st.write(insurance_percentage.to_frame("Insurance Percentage"))

        st.subheader("Monthly No-show Rate (%)")
        st.write(no_show_rate.to_frame("No-show Rate"))

        st.subheader("Average LTV (R$)")
        st.write(ltv)

        st.subheader("Retention Rate (%)")
        st.write(retention_rate)

# Optional: Debug view of the appointments DataFrame
if st.checkbox("Show appointment data (debug)"):
    st.subheader("Appointments Table")
    st.write(df_appointments)
